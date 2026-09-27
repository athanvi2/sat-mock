"""Mock Digital SAT for in-person tutoring. Run:  python app.py

Students open it on their own devices over the tutor's Wi-Fi (the address is shown on the instructor page).
The instructor view only opens on the tutor's own Mac (http://localhost:5050) behind Touch ID or a 6-digit PIN."""
import datetime
import json
import os
import random
import re
import socket
import subprocess
import sys
import time
from fractions import Fraction

from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for

import analytics
import auth
import db
import hwsync
import pdfout
import planner
import scoring as S
from bank import pool
from bank.skills import DOMAINS, REFERENCE_HTML, SECTION_NAME, SKILLS

app = Flask(__name__)
db.init()
app.secret_key = auth.secret_key()
app.config.update(SESSION_COOKIE_SAMESITE='Lax', SESSION_COOKIE_HTTPONLY=True)
DESMOS_KEY = os.environ.get('DESMOS_API_KEY', 'dcb31709b452b1cf9dc26972add0fda6')  # demo key; get your own free key at desmos.com/api
PORT = int(os.environ.get('PORT', 80))  # set for real in __main__: 80 (no ":port" in the address) if free, else 5050


def pick_port():
    """80 gives students a clean address. macOS 10.14+ lets any user listen on it; if it is taken (or not allowed),
    fall back to 5050 (5000 is used by macOS AirPlay Receiver). PORT in the environment always wins."""
    if os.environ.get('PORT'):
        return int(os.environ['PORT'])
    for p in (80, 5050):
        t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            t.bind(('0.0.0.0', p)); return p
        except OSError:
            continue
        finally:
            t.close()
    return 5050


def base_url(host):
    return 'http://%s%s' % (host, '' if PORT == 80 else ':%d' % PORT)
INST_IDLE_SEC = 2 * 3600
ASSIST = {'end': 'Answers at the end', 'hint': 'Hint after a wrong first try, then the answer', 'answer': 'Answer after the first try'}
PRIOR_TESTS = {  # test name -> (min, max) section score
    'SAT': (200, 800), 'Bluebook practice test': (200, 800), 'PSAT/NMSQT or PSAT 10': (160, 760), 'PSAT 8/9': (120, 720)}
DIAGNOSTIC_MIN = 60


# ------------------------------------------------------------------ who is asking
def local_request():
    return request.remote_addr in ('127.0.0.1', '::1')


def is_instructor():
    t = session.get('inst_at')
    if not t or not local_request() or time.time() - t > INST_IDLE_SEC:
        return False
    session['inst_at'] = time.time()
    return True


def need_instructor():
    if not local_request(): abort(404)  # instructor pages do not exist as far as other devices can tell
    if not auth.instructor_pin_set(): abort(redirect(url_for('instructor_setup')))
    if not is_instructor(): abort(redirect(url_for('instructor_login', next=request.path)))


def me():
    sid = session.get('sid')
    if not sid: return None
    return db.q('SELECT * FROM students WHERE id=?', (sid,), one=True)


def need_student():
    s = me()
    if not s: abort(redirect(url_for('login')))
    return s


def student_for_session(sid):
    """The session row and its student: the signed-in student's own session, or any session for the instructor."""
    sess = db.q('SELECT * FROM sessions WHERE id=?', (sid,), one=True)
    if not sess: abort(404)
    if is_instructor():
        return sess, db.q('SELECT * FROM students WHERE id=?', (sess['student_id'],), one=True)
    s = need_student()
    if sess['student_id'] != s['id']: abort(404)
    return sess, s


def own_session(sid, student):
    s = db.q('SELECT * FROM sessions WHERE id=?', (sid,), one=True)
    if not s or s['student_id'] != student['id']: abort(404)
    return s


def own_module(mid, student):
    m = db.q('SELECT * FROM modules WHERE id=?', (mid,), one=True)
    if not m: abort(404)
    own_session(m['session_id'], student)
    return m


@app.before_request
def housekeeping():
    # Touch ID only works on http://localhost (not 127.0.0.1), and cookies differ between the two, so keep the tutor on one.
    if request.path.startswith('/instructor') and request.host.split(':')[0] == '127.0.0.1':
        return redirect(request.url.replace('127.0.0.1', 'localhost', 1))
    sid = session.get('sid')
    if sid and request.endpoint not in (None, 'static'):
        db.x('UPDATE students SET last_seen=? WHERE id=?', (time.time(), sid))


@app.context_processor
def viewer():
    return dict(inst=is_instructor() if request.endpoint != 'static' else False, ASSIST=ASSIST)


# ------------------------------------------------------------------ grading and small helpers
def parse_num(txt):
    t = (txt or '').strip().replace(' ', '').replace(',', '')
    if not t: return None
    try:
        if '/' in t:
            a, b = t.split('/', 1)
            return float(Fraction(int(a), int(b))) if re.match(r'^-?\d+$', a) and re.match(r'^-?\d+$', b) and int(b) != 0 else None
        return float(t)
    except (ValueError, ZeroDivisionError):
        return None


def grade(qd, ans):
    if ans is None or str(ans).strip() == '': return 0
    if qd['type'] == 'mc':
        return 1 if str(ans).strip().upper() == qd['answer'] else 0
    v = parse_num(ans)
    if v is None: return 0
    return 1 if abs(v - qd['value']) <= max(qd.get('tol', 1e-9), 1e-9) else 0


def hint_for(qd):
    """A nudge that points at the method without giving the answer: the question's own hint when its generator wrote
    one, otherwise the skill's first 'how to' step and its most common trap."""
    if qd.get('hint'): return qd['hint']
    sk = SKILLS[qd['skill']]
    h = 'Key step: %s' % sk['how'][0]
    if sk['traps']: h += ' Watch out for: %s.' % sk['traps'][0].rstrip('.')
    return h


def public(qd):
    keep = ('type', 'passage', 'q', 'choices', 'figure', 'skill_name', 'domain', 'section')
    return {k: qd[k] for k in keep if k in qd}


def fmt_time(sec):
    sec = int(sec)
    return '%d:%02d' % (sec // 60, sec % 60)


def svg_scatter(f):
    if not f or f.get('type') != 'scatter': return ''
    W, H, L, B, T, Rr = 380, 270, 42, 34, 12, 14
    pw, ph = W - L - Rr, H - B - T
    sx = lambda x: L + (x - f['xmin']) / float(f['xmax'] - f['xmin']) * pw
    sy = lambda y: T + ph - (y - f['ymin']) / float(f['ymax'] - f['ymin']) * ph
    o = ['<svg class="fig" viewBox="0 0 %d %d" width="100%%" style="max-width:420px" role="img" aria-label="Scatterplot with line of best fit">' % (W, H)]
    x = f['xmin']
    while x <= f['xmax']:
        o.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" class="fig-grid"/><text x="%.1f" y="%d" font-size="10" text-anchor="middle">%s</text>' % (sx(x), sx(x), T, T + ph, sx(x), H - B + 14, x))
        x += f['xstep']
    y = f['ymin']
    while y <= f['ymax']:
        o.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="fig-grid"/><text x="%d" y="%.1f" font-size="10" text-anchor="end">%s</text>' % (L, L + pw, sy(y), sy(y), L - 6, sy(y) + 3, y))
        y += f['ystep']
    o.append('<rect x="%d" y="%d" width="%d" height="%d" class="fig-frame"/>' % (L, T, pw, ph))
    if f.get('line'):
        (a, b), (c, d) = f['line']
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="fig-line"/>' % (sx(a), sy(b), sx(c), sy(d)))
    for px, py in f['points']:
        o.append('<circle cx="%.1f" cy="%.1f" r="3.6" class="fig-dot"/>' % (sx(px), sy(py)))
    o.append('<text x="%d" y="%d" font-size="11" text-anchor="middle">%s</text>' % (L + pw // 2, H - 4, f.get('xlabel', 'x')))
    o.append('<text x="11" y="%d" font-size="11" text-anchor="middle" transform="rotate(-90 11 %d)">%s</text></svg>' % (T + ph // 2, T + ph // 2, f.get('ylabel', 'y')))
    return ''.join(o)


app.jinja_env.filters['fig'] = svg_scatter
app.jinja_env.filters['mmss'] = fmt_time
app.jinja_env.globals.update(SECTION_NAME=SECTION_NAME, SKILLS=SKILLS, DOMAINS=DOMAINS, VARIANT_LABEL=pool.VARIANT_LABEL)


@app.template_filter('pct')
def pct(v): return '%d%%' % round(v * 100)


@app.template_filter('dt')
def dt(ts): return datetime.datetime.fromtimestamp(ts).strftime('%a %b %d, %I:%M %p').replace(' 0', ' ')


@app.template_filter('ds')
def ds(d, fmt):
    """strftime with %-d (day without a leading zero) that also works on Windows."""
    return d.strftime(fmt.replace('%-d', str(d.day)))


@app.template_filter('signed')
def signed(n):
    """+30 / \u221240 / 0 with a real minus sign."""
    n = int(n)
    return ('+%d' % n) if n > 0 else ('\u2212%d' % -n) if n < 0 else '0'


@app.template_filter('ago')
def ago(ts):
    if not ts: return 'never'
    d = time.time() - ts
    if d < 3600: return 'just now'
    if d < 86400: return '%d hours ago' % (d // 3600)
    if d < 2 * 86400: return 'yesterday'
    return '%d days ago' % (d // 86400)


def valid_pin(p, n):
    return bool(re.match(r'^\d{%d}$' % n, p or ''))


def lan_addresses():
    """How students reach this Mac: its Bonjour name and its Wi-Fi IP address."""
    out = []
    try:  # macOS's Bonjour name; socket.gethostname() can carry the router's domain (e.g. name.attlocal.net)
        host = subprocess.check_output(['scutil', '--get', 'LocalHostName'], stderr=subprocess.DEVNULL).decode().strip()
    except (OSError, subprocess.CalledProcessError):
        host = socket.gethostname().split('.')[0]
    if host:
        out.append(base_url(host.lower() + '.local'))
    try:
        u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        u.connect(('192.0.2.1', 9))  # no packet is sent; this just asks which interface would be used
        out.append(base_url(u.getsockname()[0]))
        u.close()
    except OSError:
        pass
    return out


# ------------------------------------------------------------------ schedule helper (Sundays; 5th Sunday = mock)
def sunday_info(day):
    n = (day.day - 1) // 7 + 1
    return n, n == 5


def next_sunday(today=None):
    today = today or datetime.date.today()
    return today + datetime.timedelta(days=(6 - today.weekday()) % 7)


def upcoming_mocks(count=3, today=None):
    d = next_sunday(today)
    out = []
    while len(out) < count:
        if sunday_info(d)[1]: out.append(d)
        d += datetime.timedelta(days=7)
    return out


# ------------------------------------------------------------------ session / module creation
def create_session(student, mode, kind, label, plan, assist, timed, purpose='', focus=''):
    return db.x('INSERT INTO sessions(student_id, mode, kind, label, plan_json, feedback, timed, created, assist, purpose, focus) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                (student['id'], mode, kind, label, json.dumps(plan), 0 if assist == 'end' else 1, int(timed), time.time(), assist, purpose, focus))


def create_module(sess, seq, section, module_no, variant):
    plan = json.loads(sess['plan_json'])
    sp = plan['sizes'][section]
    avoid = db.seen_uids(sess['student_id'])
    used = set(r['uid'] for r in db.q('SELECT i.uid FROM items i JOIN modules m ON m.id=i.module_id WHERE m.session_id=?', (sess['id'],)))
    mix = dict((int(k), v) for k, v in plan['mix'].items()) if plan.get('mix') else None
    focus = tuple(plan['focus']) if plan.get('focus') else None
    qs = pool.build_module(section, sp['n'], variant, random.Random(), avoid, focus=focus, diff=plan.get('diff'), mix=mix, hard=used)
    limit = sp['limit'] if sess['timed'] else 0
    warn = max(60, int(300 * plan.get('f', 1.0))) if limit else 0
    mid = db.x('INSERT INTO modules(session_id, seq, section, module_no, variant, n, limit_sec, warn_sec) VALUES (?,?,?,?,?,?,?,?)',
               (sess['id'], seq, section, module_no, variant, len(qs), limit, warn))
    db.add_items(mid, qs)
    return mid


def module_score_ratio(mid):
    """Difficulty-weighted share correct in a module (used to route module 2)."""
    rows = db.q('SELECT i.d, r.correct FROM items i LEFT JOIN responses r ON r.item_id=i.id WHERE i.module_id=?', (mid,))
    w = {0: 1.0, 1: 1.5, 2: 2.0}
    tot = sum(w[r['d']] for r in rows) or 1.0
    got = sum(w[r['d']] for r in rows if r['correct'])
    return got / tot


ROUTE_THRESHOLD = 0.60


def finish_module(m):
    if m['finished']: return
    now = time.time()
    c = db.conn()
    for it in c.execute('SELECT id, qjson FROM items WHERE module_id=?', (m['id'],)).fetchall():
        qd = json.loads(it['qjson'])
        c.execute('INSERT OR IGNORE INTO responses(item_id, answer, correct, is_mc, ts) VALUES (?,?,?,?,?)',
                  (it['id'], '', 0, 1 if qd['type'] == 'mc' else 0, now))
    c.execute('UPDATE modules SET finished=? WHERE id=?', (now, m['id']))
    c.commit(); c.close()


def advance(sess):
    """Create the next module if the plan calls for one; otherwise close the session. Returns module id or None."""
    plan = json.loads(sess['plan_json'])
    mods = db.q('SELECT * FROM modules WHERE session_id=? ORDER BY seq', (sess['id'],))
    last = mods[-1]
    if not last['finished']: return last['id']
    if plan.get('adaptive'):
        if last['module_no'] == 1:
            variant = 'hard' if module_score_ratio(last['id']) >= ROUTE_THRESHOLD else 'easy'
            return create_module(sess, last['seq'] + 1, last['section'], 2, variant)
        order = plan['order']
        i = order.index(last['section'])
        if i + 1 < len(order):
            return create_module(sess, last['seq'] + 1, order[i + 1], 1, 'm1')
    db.x('UPDATE sessions SET finished=? WHERE id=?', (time.time(), sess['id']))
    if sess['purpose'] == 'diagnostic':
        db.x("UPDATE students SET onboard='diagnostic' WHERE id=?", (sess['student_id'],))
    hwsync.sync_soon(app, sess['student_id'])  # new results can change the plan, and so this week's homework
    return None


def exam_plan(minutes):
    plan = pool.full_plan() if minutes is None else pool.mock_plan(minutes)
    return dict(order=['rw', 'math'], sizes={'rw': plan['rw'], 'math': plan['math']}, adaptive=True, f=plan['f'], total_min=plan['total_min'])


def start_diagnostic(student):
    plan = exam_plan(DIAGNOSTIC_MIN)
    label = '1-hour diagnostic'
    sid = create_session(student, 'exam', label, label, plan, 'end', True, purpose='diagnostic')
    create_module(db.q('SELECT * FROM sessions WHERE id=?', (sid,), one=True), 0, 'rw', 1, 'm1')
    return sid


# ------------------------------------------------------------------ welcome, sign in, join
def students_list():
    return db.q('SELECT id, name FROM students ORDER BY name COLLATE NOCASE')


@app.route('/login', methods=['GET', 'POST'])
def login():
    err = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        key = 'student:' + name.lower()
        wait = auth.locked_for(key)
        s = db.q('SELECT * FROM students WHERE name=?', (name,), one=True)
        if wait: err = 'Too many wrong PINs. Try again in %d minutes.' % (wait // 60 + 1)
        elif not s: err = 'Pick your name from the list.'
        elif not auth.check_pin(s['pin_hash'], request.form.get('pin', '')):
            auth.note_fail(key); err = 'That PIN does not match.'
        else:
            auth.note_ok(key)
            session['sid'] = s['id']
            return redirect(url_for('home'))
    return render_template('login.html', students=students_list(), err=err, pre=request.form.get('name', ''))


@app.route('/join', methods=['GET', 'POST'])
def join():
    err, f = None, request.form
    if request.method == 'POST':
        name = ' '.join(f.get('name', '').split())
        pin = f.get('pin', '')
        if not name or len(name) > 40: err = 'Please enter your name (up to 40 characters).'
        elif not valid_pin(pin, 4): err = 'Your PIN needs to be exactly 4 digits.'
        elif pin != f.get('pin2', ''): err = 'The two PINs do not match.'
        elif db.q('SELECT 1 FROM students WHERE name=? COLLATE NOCASE', (name,), one=True):
            err = 'Someone already uses that name. Add your last initial, like "%s R."' % name.split(' ')[0]
        else:
            goal = max(400, min(1600, int(round(int(f.get('goal') or 1200) / 10.0) * 10)))
            sid = db.x('INSERT INTO students(name, pin_hash, goal_total, parent_name, created, grade, test_date, onboard) VALUES (?,?,?,?,?,?,?,?)',
                       (name, auth.hash_pin(pin), goal, '', time.time(), f.get('grade', ''), f.get('test_date', '') or None, 'new'))
            session['sid'] = sid
            return redirect(url_for('start'))
    return render_template('join.html', err=err, f=f)


@app.route('/logout')
def logout():
    session.pop('sid', None)
    return redirect(url_for('login'))


@app.route('/start', methods=['GET', 'POST'])
def start():
    """First visit: take the 1-hour diagnostic, or enter an earlier PSAT/SAT score instead."""
    s = need_student()
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == 'diagnostic':
            return redirect(url_for('run', sid=start_diagnostic(s)))
        if choice == 'later':
            db.x("UPDATE students SET onboard='skipped' WHERE id=? AND onboard='new'", (s['id'],))
            return redirect(url_for('home'))
    return render_template('start.html', s=s, plan=exam_plan(DIAGNOSTIC_MIN))


@app.route('/scores', methods=['GET', 'POST'])
def scores():
    """Earlier official or Bluebook scores. They anchor the estimate (see scoring.prior_from_scores)."""
    s = need_student()
    err, f = None, request.form
    if request.method == 'POST':
        test = f.get('test')
        try:
            rw, mt = int(f.get('rw') or 0), int(f.get('math') or 0)
            taken = datetime.datetime.strptime(f.get('taken', ''), '%Y-%m-%d').date()
        except ValueError:
            rw = mt = 0; taken = None
        if test not in PRIOR_TESTS: err = 'Pick which test this was.'
        elif not taken: err = 'Enter the date of the test.'
        elif taken > datetime.date.today(): err = 'The test date cannot be in the future.'
        elif not all(PRIOR_TESTS[test][0] <= v <= PRIOR_TESTS[test][1] and v % 10 == 0 for v in (rw, mt)):
            err = '%s section scores run from %d to %d in steps of 10.' % ((test,) + PRIOR_TESTS[test])
        else:
            db.x('INSERT INTO prior_scores(student_id, test, rw, math, taken, created) VALUES (?,?,?,?,?,?)',
                 (s['id'], test, rw, mt, taken.isoformat(), time.time()))
            db.x("UPDATE students SET onboard='prior' WHERE id=? AND onboard IN ('new', 'skipped')", (s['id'],))
            hwsync.sync_soon(app, s['id'])
            return redirect(url_for('home') if f.get('from') == 'start' else url_for('scores'))
    return render_template('scores.html', s=s, err=err, f=f, tests=PRIOR_TESTS, rows=db.prior_scores(s['id']),
                           today=datetime.date.today().isoformat(), src=request.values.get('from', ''))


@app.route('/scores/<int:pid>/delete', methods=['POST'])
def delete_score(pid):
    p = db.q('SELECT * FROM prior_scores WHERE id=?', (pid,), one=True)
    if not p: abort(404)
    if not is_instructor():
        s = need_student()
        if p['student_id'] != s['id']: abort(404)
    db.x('DELETE FROM prior_scores WHERE id=?', (pid,))
    hwsync.sync_soon(app, p['student_id'])
    return redirect(request.referrer or url_for('scores'))


@app.route('/goal', methods=['POST'])
def set_goal():
    s = need_student()
    g = int(request.form.get('goal') or 1200)
    db.x('UPDATE students SET goal_total=? WHERE id=?', (max(400, min(1600, g)), s['id']))
    return redirect(request.referrer or url_for('dashboard_view'))


# ------------------------------------------------------------------ home
@app.route('/')
def home():
    s = me()
    if not s:
        return redirect(url_for('instructor_home') if is_instructor() else url_for('login'))
    ns = next_sunday()
    n, is_mock = sunday_info(ns)
    recent = db.q('SELECT * FROM sessions WHERE student_id=? ORDER BY created DESC LIMIT 6', (s['id'],))
    rows = db.response_rows(s['id'])
    pr = analytics.priors(s['id'])
    rw, mt, tot = analytics.student_estimates(rows, None, pr)
    skills = []
    for sec, est in (('rw', rw), ('math', mt)):
        by = {}
        for r in rows:
            if r['section'] == sec: by.setdefault(r['skill'], []).append(r)
        skills += [dict(t, section=sec) for t in S.skill_table(by, est['theta'], time.time())]
    diag = db.q("SELECT * FROM sessions WHERE student_id=? AND purpose='diagnostic' ORDER BY created DESC LIMIT 1", (s['id'],), one=True)
    return render_template('home.html', s=s, next_sun=ns, is_mock=is_mock, nth=n, mocks=upcoming_mocks(),
                           recent=recent, tot=tot, rw=rw, mt=mt, conf=S.confidence_label(tot), diag=diag,
                           rec=analytics.recommendations(skills, {'rw': rw, 'math': mt}), plan=pool.mock_plan(55))


# ------------------------------------------------------------------ practice setup
def level_mix(student, section, skill=None):
    """Difficulty mix matched to the student's current level (on the skill if there is enough evidence)."""
    rows = db.response_rows(student['id'])
    est = analytics._est(rows, section, time.time(), analytics.priors(student['id']))
    theta = est['theta']
    if skill:
        sr = [r for r in rows if r['skill'] == skill]
        if len(sr) >= 5:
            theta = S.skill_table({skill: sr}, est['theta'], time.time())[0]['theta']
    return S.target_mix(theta)


@app.route('/practice', methods=['GET', 'POST'])
def practice():
    s = need_student()
    if request.method == 'POST':
        f = request.form
        sec = f.get('section', 'math')
        if sec not in ('rw', 'math'): abort(400)
        what = f.get('what', 'm1')
        length = f.get('length', 'session')
        timed = f.get('timed', '1') == '1'
        assist = f.get('assist', 'hint')
        if assist not in ASSIST: assist = 'hint'
        if length == 'module': sz = pool.session_plan(pool.OFFICIAL[sec]['minutes'], sec)
        elif length == 'custom':
            n = max(3, min(int(f.get('custom_n') or 10), pool.OFFICIAL[sec]['n']))
            sec_per_q = pool.OFFICIAL[sec]['minutes'] * 60.0 / pool.OFFICIAL[sec]['n']
            sz = dict(n=n, limit=int(n * sec_per_q))
        else: sz = pool.session_plan(30, sec)
        plan = dict(order=[sec], sizes={sec: sz}, adaptive=False, f=sz['limit'] / float(pool.OFFICIAL[sec]['minutes'] * 60))
        variant, kind, focus = 'm1', '', ''
        diff = f.get('difficulty', 'auto')
        if what in ('m1', 'easy', 'hard'):
            variant = what
            kind = '%s %s' % (SECTION_NAME[sec], pool.VARIANT_LABEL[what])
        elif what == 'full':
            plan['adaptive'] = True
            plan['sizes'][sec] = pool.session_plan(pool.OFFICIAL[sec]['minutes'], sec)
            kind = '%s, both modules' % SECTION_NAME[sec]
        elif what == 'rec':
            recs = [r['skill'] for r in home_recs(s, sec)]
            plan['focus'] = ['skills', recs]
            kind = '%s: recommended skills' % SECTION_NAME[sec]
            focus = 'skills'
        elif what.startswith('domain:'):
            dom = what.split(':', 1)[1]
            if dom not in DOMAINS[sec]: abort(400)
            plan['focus'] = ['domain', dom]
            kind = '%s: %s' % (SECTION_NAME[sec], dom)
            focus = 'domain'
        elif what.startswith('skill:'):
            key = what.split(':', 1)[1]
            if key not in SKILLS: abort(400)
            plan['focus'] = ['skill', key]
            kind = 'Skill: %s' % SKILLS[key]['name']
            focus = 'skill'
        if focus:
            if diff in ('0', '1', '2'): plan['diff'] = int(diff)
            elif diff == 'auto':
                plan['mix'] = level_mix(s, sec, plan['focus'][1] if focus == 'skill' else None)
        plan['variant'] = variant
        sid = create_session(s, 'practice', kind, kind, plan, assist, timed, focus=focus)
        sess = db.q('SELECT * FROM sessions WHERE id=?', (sid,), one=True)
        create_module(sess, 0, sec, 2 if variant in ('easy', 'hard') else 1, variant)
        return redirect(url_for('run', sid=sid))
    by_sec = {sec: [(k, v['name']) for k, v in SKILLS.items() if v['section'] == sec] for sec in ('rw', 'math')}
    return render_template('practice_setup.html', s=s, by_sec=by_sec, domains=DOMAINS, p30={sec: pool.session_plan(30, sec) for sec in ('rw', 'math')},
                           pfull={sec: pool.OFFICIAL[sec] for sec in ('rw', 'math')}, pre=request.args,
                           recs={sec: home_recs(s, sec) for sec in ('rw', 'math')})


def home_recs(student, section, k=3):
    d = analytics.dashboard(student['id'])
    ranked = [r for r in analytics.recommendations(d['skills'], {'rw': d['rw'], 'math': d['math']}, k=30) if r['section'] == section]
    return ranked[:k]


# ------------------------------------------------------------------ exam setup
@app.route('/exam', methods=['GET', 'POST'])
def exam():
    s = need_student()
    if request.method == 'POST':
        kind = request.form.get('kind', 'mock')
        if kind == 'full':
            plan = exam_plan(None); label = 'Full-length mock SAT'
        else:
            minutes = max(30, min(120, int(request.form.get('minutes') or 55)))
            plan = exam_plan(minutes); label = 'Mock SAT (%d-minute version)' % minutes
        sid = create_session(s, 'exam', label, label, plan, 'end', True)
        create_module(db.q('SELECT * FROM sessions WHERE id=?', (sid,), one=True), 0, 'rw', 1, 'm1')
        return redirect(url_for('run', sid=sid))
    return render_template('exam_setup.html', s=s, mock=pool.mock_plan(55), full=pool.full_plan(), o=pool.OFFICIAL)


# ------------------------------------------------------------------ run flow
@app.route('/run/<int:sid>')
def run(sid):
    s = need_student()
    sess = own_session(sid, s)
    mods = db.q('SELECT * FROM modules WHERE session_id=? ORDER BY seq', (sid,))
    last = mods[-1]
    if not last['finished']:
        return redirect(url_for('module_page' if last['started'] else 'module_intro', mid=last['id']))
    nxt = advance(sess)
    if nxt: return redirect(url_for('module_intro', mid=nxt))
    return redirect(url_for('results', sid=sid))


@app.route('/module/<int:mid>/intro', methods=['GET', 'POST'])
def module_intro(mid):
    s = need_student()
    m = own_module(mid, s)
    sess = db.q('SELECT * FROM sessions WHERE id=?', (m['session_id'],), one=True)
    if m['finished']: return redirect(url_for('run', sid=sess['id']))
    if request.method == 'POST' or m['started']:
        if not m['started']: db.x('UPDATE modules SET started=? WHERE id=?', (time.time(), mid))
        return redirect(url_for('module_page', mid=mid))
    plan = json.loads(sess['plan_json'])
    prev = db.q('SELECT * FROM modules WHERE session_id=? AND seq<? ORDER BY seq DESC LIMIT 1', (sess['id'], m['seq']), one=True)
    return render_template('intro.html', s=s, m=m, sess=sess, plan=plan, prev=prev, new_section=bool(prev and prev['section'] != m['section']))


def feedback_payload(qd, r):
    """What the runner shows once an item is revealed: first-try verdict, the retry verdict if there was one, key, explanation."""
    fb = dict(correct=bool(r['correct']), key=qd.get('answer'), expl=qd.get('expl'), first=r['answer'])
    if r['attempts'] and r['attempts'] >= 2:
        fb['retry'] = r['retry_answer']; fb['retry_correct'] = bool(r['retry_correct'])
    return fb


@app.route('/module/<int:mid>')
def module_page(mid):
    s = need_student()
    m = own_module(mid, s)
    sess = db.q('SELECT * FROM sessions WHERE id=?', (m['session_id'],), one=True)
    if m['finished']: return redirect(url_for('run', sid=sess['id']))
    if not m['started']: return redirect(url_for('module_intro', mid=mid))
    remaining = None
    if m['limit_sec']:
        remaining = m['limit_sec'] - (time.time() - m['started'])
        if remaining <= 0:
            finish_module(m)
            return redirect(url_for('run', sid=sess['id']))
    items = db.q('SELECT * FROM items WHERE module_id=? ORDER BY idx', (mid,))
    resp = {r['item_id']: r for r in db.q('SELECT * FROM responses WHERE item_id IN (SELECT id FROM items WHERE module_id=?)', (mid,))}
    payload = []
    for it in items:
        qd = json.loads(it['qjson'])
        r = resp.get(it['id'])
        attempts = (r['attempts'] or 0) if r else 0
        shown = (r['retry_answer'] or '') if attempts >= 1 and r and not r['checked'] else (r['answer'] if r else '')
        entry = dict(id=it['id'], idx=it['idx'], q=public(qd), answer=shown or '', flagged=bool(r and r['flagged']),
                     struck=json.loads(r['struck']) if r and r['struck'] else [], checked=bool(r and r['checked']),
                     time_ms=r['time_ms'] if r else 0, attempts=attempts)
        if entry['checked']:
            entry['fb'] = feedback_payload(qd, r)
        elif attempts == 1:
            entry['hint'] = hint_for(qd); entry['first'] = r['answer']
        payload.append(entry)
    plan = json.loads(sess['plan_json'])
    if sess['mode'] == 'exam' or plan.get('adaptive'):
        label = '%s: Module %d' % (SECTION_NAME[m['section']], m['module_no'])
        if sess['purpose'] == 'diagnostic': label = 'Diagnostic. ' + label
    else:
        label = sess['kind']
    return render_template('runner.html', s=s, m=m, sess=sess, label=label, remaining=remaining, desmos_key=DESMOS_KEY,
                           reference=REFERENCE_HTML, payload=json.dumps(payload))


def _item_ctx(item_id, student):
    it = db.q('SELECT * FROM items WHERE id=?', (item_id,), one=True)
    if not it: abort(404)
    m = own_module(it['module_id'], student)
    sess = db.q('SELECT * FROM sessions WHERE id=?', (m['session_id'],), one=True)
    return it, m, sess


@app.route('/api/save', methods=['POST'])
def api_save():
    s = need_student()
    j = request.get_json(force=True)
    it, m, sess = _item_ctx(int(j['item_id']), s)
    if m['finished'] or not m['started']: return jsonify(ok=False, reason='closed'), 409
    if m['limit_sec'] and time.time() - m['started'] > m['limit_sec'] + 15: return jsonify(ok=False, reason='time'), 409
    qd = json.loads(it['qjson'])
    ans = (j.get('answer') or '').strip()
    prev = db.q('SELECT * FROM responses WHERE item_id=?', (it['id'],), one=True)
    tms = (prev['time_ms'] if prev else 0) + max(0, min(int(j.get('time_ms') or 0), 900000))
    flag, struck = 1 if j.get('flagged') else 0, json.dumps(j.get('struck') or [])
    if prev and prev['checked']:  # answer is locked once revealed; flags and cross-outs still save
        db.x('UPDATE responses SET flagged=?, struck=?, time_ms=? WHERE item_id=?', (flag, struck, tms, it['id']))
        return jsonify(ok=True, locked=True)
    if prev and prev['attempts']:  # waiting for the second try after a hint: the first answer (which is scored) stays put
        db.x('UPDATE responses SET retry_answer=?, flagged=?, struck=?, time_ms=? WHERE item_id=?', (ans, flag, struck, tms, it['id']))
        return jsonify(ok=True)
    db.x('''INSERT INTO responses(item_id, answer, correct, is_mc, time_ms, flagged, struck, ts) VALUES (?,?,?,?,?,?,?,?)
            ON CONFLICT(item_id) DO UPDATE SET answer=excluded.answer, correct=excluded.correct, time_ms=excluded.time_ms,
            flagged=excluded.flagged, struck=excluded.struck, ts=excluded.ts''',
         (it['id'], ans, grade(qd, ans), 1 if qd['type'] == 'mc' else 0, tms, flag, struck, time.time()))
    return jsonify(ok=True)


@app.route('/api/check', methods=['POST'])
def api_check():
    """Assist levels. 'answer': reveal after the first try. 'hint': a wrong first try gets a hint and one more try, then
    the reveal. The first try is what gets scored either way; the second try is kept only for the tutor's view."""
    s = need_student()
    j = request.get_json(force=True)
    it, m, sess = _item_ctx(int(j['item_id']), s)
    if sess['assist'] not in ('hint', 'answer') or m['finished']: abort(403)
    qd = json.loads(it['qjson'])
    ans = (j.get('answer') or '').strip()
    if not ans: return jsonify(ok=False, reason='empty'), 400
    prev = db.q('SELECT * FROM responses WHERE item_id=?', (it['id'],), one=True)
    if prev and prev['checked']:
        return jsonify(ok=True, reveal=feedback_payload(qd, prev))
    tms = (prev['time_ms'] if prev else 0) + max(0, min(int(j.get('time_ms') or 0), 900000))
    mc = 1 if qd['type'] == 'mc' else 0
    if not prev or not prev['attempts']:
        ok = grade(qd, ans)
        reveal = 1 if (ok or sess['assist'] == 'answer') else 0
        db.x('''INSERT INTO responses(item_id, answer, correct, is_mc, time_ms, flagged, struck, checked, attempts, hint_used, ts)
                VALUES (?,?,?,?,?,?,?,?,1,?,?)
                ON CONFLICT(item_id) DO UPDATE SET answer=excluded.answer, correct=excluded.correct, time_ms=excluded.time_ms,
                checked=excluded.checked, attempts=1, hint_used=excluded.hint_used, ts=excluded.ts''',
             (it['id'], ans, ok, mc, tms, prev['flagged'] if prev else 0, prev['struck'] if prev else '[]', reveal, 0 if reveal else 1, time.time()))
    else:
        db.x('UPDATE responses SET retry_answer=?, retry_correct=?, attempts=2, checked=1, time_ms=? WHERE item_id=?',
             (ans, grade(qd, ans), tms, it['id']))
    r = db.q('SELECT * FROM responses WHERE item_id=?', (it['id'],), one=True)
    if r['checked']:
        return jsonify(ok=True, reveal=feedback_payload(qd, r))
    return jsonify(ok=True, hint=hint_for(qd), first=r['answer'])


@app.route('/api/finish', methods=['POST'])
def api_finish():
    s = need_student()
    j = request.get_json(force=True)
    m = own_module(int(j['module_id']), s)
    finish_module(m)
    return jsonify(ok=True, next=url_for('run', sid=m['session_id']))


# ------------------------------------------------------------------ results and review
def session_rows(sid):
    return [dict(r) for r in db.q('''SELECT i.*, r.answer, r.correct, r.time_ms, r.flagged, r.hint_used, r.attempts, r.retry_answer, r.retry_correct,
                                           m.module_no, m.variant, m.section AS msec, m.seq
                                    FROM items i JOIN modules m ON m.id=i.module_id LEFT JOIN responses r ON r.item_id=i.id
                                    WHERE m.session_id=? ORDER BY m.seq, i.idx''', (sid,))]


def weakest_skill(student_id, rows):
    """Skill in this session with the biggest shortfall against what the student's overall level predicts."""
    allrows = db.response_rows(student_id)
    pr = analytics.priors(student_id)
    est = {sec: analytics._est(allrows, sec, time.time(), pr) for sec in ('rw', 'math')}
    agg = {}
    for r in rows:
        if r['answer'] in (None, ''): continue
        th = est[r['section']]['theta']
        p = S.p_correct(th, r['d'], json.loads(r['qjson'])['type'] == 'mc')
        a = agg.setdefault(r['skill'], dict(n=0, miss=0, gap=0.0))
        a['n'] += 1; a['miss'] += 0 if r['correct'] else 1; a['gap'] += (1 if r['correct'] else 0) - p
    if not agg: return None
    cands = [(v['gap'] / v['n'] - 0.02 * v['miss'], k) for k, v in agg.items() if v['miss'] > 0] or [(0, k) for k in agg]
    return min(cands)[1]


@app.route('/results/<int:sid>')
def results(sid):
    sess, s = student_for_session(sid)
    rows = session_rows(sid)
    mods = db.q('SELECT * FROM modules WHERE session_id=? ORDER BY seq', (sid,))
    per_mod = []
    for m in mods:
        rr = [r for r in rows if r['module_id'] == m['id']]
        ans = [r for r in rr if r['answer']]
        per_mod.append(dict(m=m, n=len(rr), answered=len(ans), right=sum(1 for r in ans if r['correct']),
                            time=(m['finished'] - m['started']) if m['finished'] and m['started'] else 0))
    dom = {}
    for r in rows:
        d = dom.setdefault((r['section'], r['domain']), dict(n=0, right=0, blank=0))
        d['n'] += 1
        if r['answer']: d['right'] += 1 if r['correct'] else 0
        else: d['blank'] += 1
    sk = {}
    for r in rows:
        k = sk.setdefault(r['skill'], dict(n=0, right=0))
        if r['answer']:
            k['n'] += 1; k['right'] += 1 if r['correct'] else 0
    all_rows = db.response_rows(s['id'])
    pr = analytics.priors(s['id'])
    rw, mt, tot = analytics.student_estimates(all_rows, None, pr)
    sr = [x for x in all_rows if x['session_id'] == sid]
    srw, smt = analytics._est(sr, 'rw', time.time()), analytics._est(sr, 'math', time.time())
    wk = weakest_skill(s['id'], rows)
    assists = dict(hints=sum(1 for r in rows if r['hint_used']), fixed=sum(1 for r in rows if r['hint_used'] and r['retry_correct']))
    return render_template('results.html', s=me(), st=s, sess=sess, per_mod=per_mod, dom=sorted(dom.items()), sk=sk, tot=tot, rw=rw, mt=mt,
                           srw=srw, smt=smt, weak=wk, total_q=len(rows), right=sum(1 for r in rows if r['correct']), assists=assists,
                           ruler=analytics.svg_ruler(rw, mt, tot, s['goal_total']), nrows=len(all_rows), conf=S.confidence_label(tot))


@app.route('/review/<int:sid>')
def review(sid):
    sess, s = student_for_session(sid)
    if not sess['finished'] and not is_instructor(): return redirect(url_for('run', sid=sid))
    rows = session_rows(sid)
    items = []
    for r in rows:
        qd = json.loads(r['qjson'])
        items.append(dict(r=r, q=qd, skill=SKILLS[r['skill']], mine=r['answer'] or '', ok=bool(r['correct'])))
    return render_template('review.html', s=me(), st=s, sess=sess, items=items, only=request.args.get('only'))


# ------------------------------------------------------------------ dashboard
def dashboard_page(student, view):
    d = analytics.dashboard(student['id'])
    return render_template('dashboard.html', s=me(), d=d, view=view, ruler=analytics.svg_ruler(d['rw'], d['math'], d['total'], d['goal']),
                           tline=analytics.svg_timeline(d['timeline'], d['goal']), wvol=analytics.svg_week_volume(d['weekly']), wacc=analytics.svg_week_accuracy(d['weekly']))


@app.route('/dashboard')
def dashboard_view():
    return dashboard_page(need_student(), 'student')


# ------------------------------------------------------------------ calendar
def calendar_page(student, view):
    today = datetime.date.today()
    try:
        y, m = [int(v) for v in request.args.get('m', '').split('-')]
        datetime.date(y, m, 1)
    except ValueError:
        y, m = today.year, today.month
    pl = planner.plan(student['id'], today)
    first = datetime.date(y, m, 1)
    shown = [first]
    if not request.args.get('m') and today.day > 20:  # late in the month the plan lives mostly in the next one: show both
        shown.append((first + datetime.timedelta(days=32)).replace(day=1))
    months = [dict(month=mo, weeks=planner.month_grid(mo.year, mo.month, pl['items'], today)) for mo in shown]
    prev_m = (first - datetime.timedelta(days=1)).replace(day=1)
    next_m = (shown[-1] + datetime.timedelta(days=32)).replace(day=1)
    upcoming = [i for i in pl['items'] if i['day'] >= today and i['status'] in ('planned', 'event')][:14]
    recent = [i for i in pl['items'] if i['day'] < today and i['status'] in ('done', 'open', 'missed')][-6:]
    return render_template('calendar.html', s=me(), st=student, view=view, pl=pl, months=months, prev_m=prev_m, next_m=next_m, today=today, upcoming=upcoming, recent=recent, rules=planner.RULES,
                           msg=request.args.get('msg'), err=request.args.get('err'))


@app.route('/plan')
def my_plan():
    return calendar_page(need_student(), 'student')


@app.route('/instructor/students/<int:stid>/plan')
def instructor_plan(stid):
    need_instructor()
    return calendar_page(_student_or_404(stid), 'tutor')


@app.route('/instructor/students/<int:stid>/events', methods=['POST'])
def instructor_add_event(stid):
    need_instructor()
    _student_or_404(stid)
    f = request.form
    try:
        day = datetime.datetime.strptime(f.get('day', ''), '%Y-%m-%d').date()
    except ValueError:
        return redirect(url_for('instructor_plan', stid=stid, err='Pick a date.'))
    kind = f.get('kind') if f.get('kind') in ('custom', 'skip') else 'custom'
    title = ' '.join(f.get('title', '').split())[:80] or ('No session' if kind == 'skip' else 'Note')
    db.x('INSERT INTO events(student_id, day, kind, title, note, created) VALUES (?,?,?,?,?,?)',
         (stid, day.isoformat(), kind, title, f.get('note', '').strip()[:400], time.time()))
    hwsync.sync_soon(app, stid)
    return redirect(url_for('instructor_plan', stid=stid, m=day.strftime('%Y-%m'), msg='Added to the calendar.'))


@app.route('/instructor/events/<int:eid>/delete', methods=['POST'])
def instructor_delete_event(eid):
    need_instructor()
    e = db.q('SELECT * FROM events WHERE id=?', (eid,), one=True)
    if not e: abort(404)
    db.x('DELETE FROM events WHERE id=?', (eid,))
    hwsync.sync_soon(app, e['student_id'])
    return redirect(url_for('instructor_plan', stid=e['student_id'], m=e['day'][:7], msg='Removed from the calendar.'))


# ------------------------------------------------------------------ homework and lecture sheets
def hw_count(skill):
    return int(max(10, min(15, round(1800 / (1.5 * SKILLS[skill]['avg_sec'])))))


@app.route('/homework')
def homework():
    """Printable homework. Students get the sheet; only the instructor can print the answer key.
    The difficulty mix is matched to the student's level on this skill."""
    inst = is_instructor()
    if inst and request.args.get('student'):
        s = db.q('SELECT * FROM students WHERE id=?', (int(request.args['student']),), one=True)
        if not s: abort(404)
    elif inst and not me():
        s = None
    else:
        s = need_student()
    skill = request.args.get('skill')
    if skill not in SKILLS: abort(404)
    seed_base = int(request.args.get('seed') or random.randrange(1, 10 ** 6))
    hw = build_homework(s, skill, seed_base, request.args.get('n'))
    return render_template('homework.html', s=me(), st=s, skill=SKILLS[skill], seed=seed_base, mins=30,
                           key=inst and request.args.get('key') == '1', **hw)


def build_homework(student, skill, seed, n=None):
    """Questions for one homework sheet: 10-15 problems (about 30 minutes), difficulty matched to the student's level on
    the skill, no repeats within the sheet, avoiding what the student saw recently. Same seed -> same sheet."""
    n = max(5, min(25, int(n or hw_count(skill))))
    mix = level_mix(student, SKILLS[skill]['section'], skill) if student else {0: .3, 1: .45, 2: .25}
    c = pool.apportion(n, mix)
    ds = [0] * c[0] + [1] * c[1] + [2] * c[2]
    rng = random.Random(seed)
    avoid = db.seen_uids(student['id']) if student else set()
    hard, qs = set(), []
    for d in ds:
        qd = pool.make_safe(skill, d, rng.randrange(1, 10 ** 9), False, avoid, hard)
        hard.add(qd['uid']); qs.append(qd)
    qs.sort(key=lambda q: q['d'])
    return dict(qs=qs, n=n, level=mix)


app.extensions['build_homework'] = build_homework  # hwsync renders sheets in the background with the same builder


def browsing():
    """Lecture sheets and the skills list are open to a signed-in student or the instructor."""
    s = me()
    if not s and not is_instructor(): abort(redirect(url_for('login')))
    return s


@app.route('/lecture/<skill>')
def lecture(skill):
    s = browsing()
    if skill not in SKILLS: abort(404)
    rng = random.Random(int(request.args.get('seed') or 7))
    ex = [pool.make_safe(skill, d, rng.randrange(1, 10 ** 9), False, set()) for d in (0, 1, 2)]
    for q in ex: q['hint'] = hint_for(q)
    return render_template('lecture.html', s=s, skill=SKILLS[skill], ex=ex, reference=REFERENCE_HTML)


@app.route('/skills')
def skills_index():
    return render_template('skills.html', s=browsing(), skills=SKILLS, domains=DOMAINS)


@app.route('/api/calc-ping')
def calc_ping():
    return jsonify(ok=True)


# ------------------------------------------------------------------ instructor: lock
@app.route('/instructor/setup', methods=['GET', 'POST'])
def instructor_setup():
    if not local_request(): abort(404)
    if auth.instructor_pin_set(): return redirect(url_for('instructor_login'))
    err = None
    if request.method == 'POST':
        p = request.form.get('pin', '')
        if not valid_pin(p, 6): err = 'The PIN must be exactly 6 digits.'
        elif p != request.form.get('pin2'): err = 'The two PINs do not match.'
        elif len(set(p)) == 1 or p in '0123456789' or p in '9876543210': err = 'Pick something less guessable than %s.' % p
        else:
            auth.set_instructor_pin(p)
            session['inst_at'] = time.time()
            return redirect(url_for('instructor_settings', first=1))
    return render_template('instructor/setup.html', err=err)


@app.route('/instructor/login', methods=['GET', 'POST'])
def instructor_login():
    if not local_request(): abort(404)
    if not auth.instructor_pin_set(): return redirect(url_for('instructor_setup'))
    nxt = request.values.get('next') or url_for('instructor_home')
    if not nxt.startswith('/'): nxt = url_for('instructor_home')
    err = None
    if request.method == 'POST':
        wait = auth.locked_for('instructor')
        if wait: err = 'Too many wrong PINs. Try again in %d minutes, or use Touch ID.' % (wait // 60 + 1)
        elif auth.check_instructor_pin(request.form.get('pin', '')):
            auth.note_ok('instructor'); session['inst_at'] = time.time()
            return redirect(nxt)
        else:
            auth.note_fail('instructor'); err = 'That PIN is not right.'
    return render_template('instructor/login.html', err=err, nxt=nxt, touch=bool(db.q('SELECT 1 FROM creds LIMIT 1')))


@app.route('/instructor/logout')
def instructor_logout():
    session.pop('inst_at', None)
    return redirect(url_for('login'))


def _origin():
    return request.host_url.rstrip('/')


@app.route('/instructor/webauthn/<step>', methods=['POST'])
def webauthn(step):
    if not local_request(): abort(404)
    try:
        if step == 'auth-begin':
            session['wa_chal'] = auth.challenge()
            return jsonify(auth.auth_options(session['wa_chal']))
        if step == 'auth-finish':
            auth.finish_auth(request.get_json(force=True), session.pop('wa_chal', ''), _origin())
            auth.note_ok('instructor'); session['inst_at'] = time.time()
            return jsonify(ok=True)
        need_instructor()  # enrolling a new fingerprint needs an unlocked instructor session
        if step == 'register-begin':
            session['wa_chal'] = auth.challenge()
            return jsonify(auth.registration_options(session['wa_chal']))
        if step == 'register-finish':
            auth.finish_registration(request.get_json(force=True), session.pop('wa_chal', ''), _origin(), 'Touch ID on this Mac')
            return jsonify(ok=True)
    except (ValueError, KeyError, IndexError, TypeError) as e:
        return jsonify(ok=False, error=str(e)), 400
    abort(404)


# ------------------------------------------------------------------ instructor: students
@app.route('/instructor')
def instructor_home():
    need_instructor()
    roster = [analytics.roster_row(st) for st in db.q('SELECT * FROM students ORDER BY name COLLATE NOCASE')]
    return render_template('instructor/home.html', roster=roster, lan=lan_addresses(), err=request.args.get('err'), msg=request.args.get('msg'))


@app.route('/instructor/students/new', methods=['POST'])
def instructor_new_student():
    need_instructor()
    f = request.form
    name = ' '.join(f.get('name', '').split())
    pin = f.get('pin', '')
    if not name or len(name) > 40: return redirect(url_for('instructor_home', err='Enter a name (up to 40 characters).'))
    if not valid_pin(pin, 4): return redirect(url_for('instructor_home', err='The student PIN must be 4 digits.'))
    if db.q('SELECT 1 FROM students WHERE name=? COLLATE NOCASE', (name,), one=True):
        return redirect(url_for('instructor_home', err='A student named %s already exists.' % name))
    db.x('INSERT INTO students(name, pin_hash, goal_total, parent_name, created, grade, test_date, onboard) VALUES (?,?,?,?,?,?,?,?)',
         (name, auth.hash_pin(pin), int(f.get('goal') or 1200), f.get('parent', '').strip(), time.time(), f.get('grade', ''), None, 'new'))
    return redirect(url_for('instructor_home', msg='Added %s. They sign in with the PIN you set.' % name))


def _student_or_404(stid):
    st = db.q('SELECT * FROM students WHERE id=?', (stid,), one=True)
    if not st: abort(404)
    return st


@app.route('/instructor/students/<int:stid>')
def instructor_student(stid):
    need_instructor()
    st = _student_or_404(stid)
    if request.args.get('view') == 'parent':
        return redirect(url_for('parent_report', stid=stid))
    sessions = db.q('SELECT * FROM sessions WHERE student_id=? ORDER BY created DESC', (stid,))
    d = analytics.dashboard(stid)
    return render_template('instructor/student.html', st=st, d=d, sessions=sessions, tests=PRIOR_TESTS, view='tutor', hw=hw_info(st),
                           ruler=analytics.svg_ruler(d['rw'], d['math'], d['total'], d['goal']),
                           tline=analytics.svg_timeline(d['timeline'], d['goal']), wvol=analytics.svg_week_volume(d['weekly']), wacc=analytics.svg_week_accuracy(d['weekly']),
                           msg=request.args.get('msg'), err=request.args.get('err'))


def hw_info(st):
    """What the instructor page shows about the student's Desktop homework folder."""
    if not hwsync.root(): return None
    d = hwsync.folder(st)
    files = sorted(f for f in os.listdir(d) if f.endswith('.pdf')) if os.path.isdir(d) else []
    return dict(folder=d, exists=os.path.isdir(d), files=files, status=hwsync.status(st['id']), enabled=hwsync.enabled())


@app.route('/instructor/students/<int:stid>/edit', methods=['POST'])
def instructor_edit_student(stid):
    need_instructor()
    st = _student_or_404(stid)
    f = request.form
    name = ' '.join(f.get('name', '').split()) or st['name']
    clash = db.q('SELECT id FROM students WHERE name=? COLLATE NOCASE AND id!=?', (name, stid), one=True)
    if clash: return redirect(url_for('instructor_student', stid=stid, err='Another student is already called %s.' % name))
    goal = max(400, min(1600, int(f.get('goal') or st['goal_total'] or 1200)))
    db.x('UPDATE students SET name=?, goal_total=?, grade=?, test_date=?, parent_name=? WHERE id=?',
         (name, goal, f.get('grade', ''), f.get('test_date') or None, f.get('parent', '').strip(), stid))
    pin = f.get('pin', '')
    if pin:
        if not valid_pin(pin, 4): return redirect(url_for('instructor_student', stid=stid, err='A new PIN must be 4 digits.'))
        db.x('UPDATE students SET pin_hash=? WHERE id=?', (auth.hash_pin(pin), stid))
    hwsync.sync_soon(app, stid)
    return redirect(url_for('instructor_student', stid=stid, msg='Saved.'))


@app.route('/instructor/students/<int:stid>/delete', methods=['POST'])
def instructor_delete_student(stid):
    need_instructor()
    st = _student_or_404(stid)
    if request.form.get('confirm', '').strip().lower() != st['name'].lower():
        return redirect(url_for('instructor_student', stid=stid, err='To delete, type the name exactly as shown: %s' % st['name']))
    path = db.backup('before-deleting-%d' % stid)
    db.delete_student(stid)
    if session.get('sid') == stid: session.pop('sid', None)
    return redirect(url_for('instructor_home', msg='Deleted %s. A backup was saved to %s.' % (st['name'], os.path.basename(path))))


@app.route('/instructor/students/<int:stid>/scores', methods=['POST'])
def instructor_add_score(stid):
    need_instructor()
    _student_or_404(stid)
    f = request.form
    test = f.get('test')
    try:
        rw, mt = int(f.get('rw')), int(f.get('math'))
        taken = datetime.datetime.strptime(f.get('taken', ''), '%Y-%m-%d').date()
    except (TypeError, ValueError):
        return redirect(url_for('instructor_student', stid=stid, err='Enter both section scores and the test date.'))
    if test not in PRIOR_TESTS or taken > datetime.date.today() or not all(
            PRIOR_TESTS[test][0] <= v <= PRIOR_TESTS[test][1] and v % 10 == 0 for v in (rw, mt)):
        return redirect(url_for('instructor_student', stid=stid, err='Those scores are not valid for that test.'))
    db.x('INSERT INTO prior_scores(student_id, test, rw, math, taken, created) VALUES (?,?,?,?,?,?)', (stid, test, rw, mt, taken.isoformat(), time.time()))
    db.x("UPDATE students SET onboard='prior' WHERE id=? AND onboard IN ('new', 'skipped')", (stid,))
    hwsync.sync_soon(app, stid)
    return redirect(url_for('instructor_student', stid=stid, msg='Score added.'))


# ------------------------------------------------------------------ parent guide (public: it describes the program, not a student)
@app.route('/guide')
def guide():
    return render_template('guide.html', pdf=False, rules=planner.RULES, can_pdf=pdfout.available())


@app.route('/guide.pdf')
def guide_pdf():
    try:
        data = pdfout.html_to_pdf(render_template('guide.html', pdf=True, rules=planner.RULES, can_pdf=False))
    except (RuntimeError, OSError, subprocess.SubprocessError):
        return redirect(url_for('guide'))
    return app.response_class(data, mimetype='application/pdf', headers={'Content-Disposition': 'attachment; filename="SAT prep - guide for families.pdf"'})


# ------------------------------------------------------------------ parent report
def report_data(st):
    today = datetime.date.today()
    d = analytics.dashboard(st['id'])
    pl = planner.plan(st['id'], today)
    rows = db.response_rows(st['id'])
    since = time.time() - 30 * 86400
    recent = [r for r in rows if r['ts'] >= since and not r['omitted']]
    month = dict(sessions=db.q('SELECT COUNT(*) c FROM sessions WHERE student_id=? AND finished>=?', (st['id'], since), one=True)['c'],
                 questions=len(recent), minutes=int(round(sum(r['time_ms'] or 0 for r in recent) / 60000.0)),
                 acc=(sum(1 for r in recent if r['correct']) / float(len(recent))) if recent else None)
    # change is measured from the first estimate made in this app, not from an older official score on a different test
    est = [t for t in d['timeline'] if not t['reported']]
    start = est[0] if est else None
    change = (d['total']['mid'] - start['mid']) if (start and d['total']['has_data'] and len(est) >= 2) else None
    upcoming = [i for i in pl['items'] if today <= i['day'] <= today + datetime.timedelta(days=28) and i['status'] in ('planned', 'event')]
    return dict(d=d, pl=pl, month=month, start=start, change=change, upcoming=upcoming, today=today,
                ruler=analytics.svg_ruler(d['rw'], d['math'], d['total'], d['goal']), tline=analytics.svg_timeline(d['timeline'], d['goal']))


@app.route('/instructor/students/<int:stid>/report')
def parent_report(stid):
    need_instructor()
    st = _student_or_404(stid)
    ctx = report_data(st)
    pdf = request.args.get('format') == 'pdf'
    html = render_template('report.html', st=st, pdf=pdf, rules=planner.RULES, can_pdf=pdfout.available(), msg=request.args.get('msg'), **ctx)
    if not pdf: return html
    try:
        data = pdfout.html_to_pdf(html)
    except (RuntimeError, OSError, subprocess.SubprocessError) as e:
        return redirect(url_for('parent_report', stid=stid, msg='Could not make the PDF here (%s). Use Print, then Save as PDF.' % e))
    fname = 'Progress report - %s - %s.pdf' % (st['name'], ctx['today'].isoformat())
    return app.response_class(data, mimetype='application/pdf', headers={'Content-Disposition': 'attachment; filename="%s"' % fname.replace('"', '')})


@app.route('/instructor/students/<int:stid>/report/note', methods=['POST'])
def save_report_note(stid):
    need_instructor()
    _student_or_404(stid)
    db.x('UPDATE students SET report_note=? WHERE id=?', (request.form.get('note', '').strip()[:2000], stid))
    return redirect(url_for('parent_report', stid=stid, msg='Note saved.'))


@app.route('/instructor/students/<int:stid>/homework-folder', methods=['POST'])
def instructor_hw_folder(stid):
    need_instructor()
    st = _student_or_404(stid)
    if request.form.get('act') == 'open':
        d = hwsync.folder(st) if hwsync.root() else None
        if d and os.path.isdir(d) and sys.platform == 'darwin':
            subprocess.Popen(['open', d])
        return redirect(url_for('instructor_student', stid=stid))
    try:
        res = hwsync.sync_student(app, stid)
    except Exception as e:  # show the problem instead of a server error
        res = dict(ok=False, message='Update failed: %s' % e)
    return redirect(url_for('instructor_student', stid=stid, **{'msg' if res['ok'] else 'err': 'Homework folder: ' + res['message']}))


# ------------------------------------------------------------------ instructor: settings
@app.route('/instructor/settings', methods=['GET', 'POST'])
def instructor_settings():
    need_instructor()
    msg = err = None
    if request.method == 'POST':
        act = request.form.get('act')
        if act == 'pin':
            new = request.form.get('pin', '')
            if not auth.check_instructor_pin(request.form.get('old', '')): err = 'The current PIN is not right.'
            elif not valid_pin(new, 6) or new != request.form.get('pin2'): err = 'The new PIN must be 6 digits, typed the same twice.'
            else: auth.set_instructor_pin(new); msg = 'PIN changed.'
        elif act == 'forget':
            db.x('DELETE FROM creds WHERE id=?', (request.form.get('id', ''),)); msg = 'Touch ID removed.'
        elif act == 'backup':
            msg = 'Backup saved: %s' % os.path.basename(db.backup('manual'))
    return render_template('instructor/settings.html', creds=db.q('SELECT * FROM creds ORDER BY created'), lan=lan_addresses(),
                           msg=msg, err=err, first=request.args.get('first'), db_path=db.PATH)


if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    PORT = pick_port()
    hwsync.start_hourly(app)
    print('\n  Instructor (this Mac):  %s/instructor' % base_url('localhost'))
    for a in lan_addresses(): print('  Students on the Wi-Fi:  %s' % a)
    print('')
    app.run(host=host, port=PORT, debug=False, threaded=True)
