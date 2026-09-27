"""Local mock Digital SAT. Run:  python app.py   then open http://127.0.0.1:5000"""
import datetime
import hashlib
import json
import os
import random
import re
import time
from fractions import Fraction

from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for

import analytics
import db
import scoring as S
from bank import pool
from bank.skills import DOMAINS, REFERENCE_HTML, SECTION_NAME, SKILLS

app = Flask(__name__)
app.secret_key = os.environ.get('SAT_SECRET', 'local-only-not-a-secret')
DESMOS_KEY = os.environ.get('DESMOS_API_KEY', 'dcb31709b452b1cf9dc26972add0fda6')  # demo key; get your own free key at desmos.com/api
db.init()


# ------------------------------------------------------------------ helpers
def me():
    sid = session.get('sid')
    if not sid: return None
    return db.q('SELECT * FROM students WHERE id=?', (sid,), one=True)


def need_student():
    s = me()
    if not s: abort(redirect(url_for('login')))
    return s


def hpin(p): return hashlib.sha256(('sat-mock:' + p).encode('utf-8')).hexdigest() if p else None


def own_session(sid, student):
    s = db.q('SELECT * FROM sessions WHERE id=?', (sid,), one=True)
    if not s or s['student_id'] != student['id']: abort(404)
    return s


def own_module(mid, student):
    m = db.q('SELECT * FROM modules WHERE id=?', (mid,), one=True)
    if not m: abort(404)
    own_session(m['session_id'], student)
    return m


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
    o = ['<svg viewBox="0 0 %d %d" width="100%%" style="max-width:420px;font-family:sans-serif">' % (W, H)]
    x = f['xmin']
    while x <= f['xmax']:
        o.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" stroke="#DDE2E8"/><text x="%.1f" y="%d" font-size="10" text-anchor="middle">%s</text>' % (sx(x), sx(x), T, T + ph, sx(x), H - B + 14, x))
        x += f['xstep']
    y = f['ymin']
    while y <= f['ymax']:
        o.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#DDE2E8"/><text x="%d" y="%.1f" font-size="10" text-anchor="end">%s</text>' % (L, L + pw, sy(y), sy(y), L - 6, sy(y) + 3, y))
        y += f['ystep']
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#18212E" stroke-width="1.5"/>' % (L, T, pw, ph))
    if f.get('line'):
        (a, b), (c, d) = f['line']
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1F4FA3" stroke-width="2"/>' % (sx(a), sy(b), sx(c), sy(d)))
    for px, py in f['points']:
        o.append('<circle cx="%.1f" cy="%.1f" r="3.6" fill="#18212E"/>' % (sx(px), sy(py)))
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


# ------------------------------------------------------------------ schedule helper (Sundays; 5th Sunday = mock)
def sunday_info(day):
    n = (day.day - 1) // 7 + 1
    return n, n == 5


def next_sunday(today=None):
    today = today or datetime.date.today()
    d = today + datetime.timedelta(days=(6 - today.weekday()) % 7)
    return d


def upcoming_mocks(count=3, today=None):
    d = next_sunday(today)
    out = []
    while len(out) < count:
        if sunday_info(d)[1]: out.append(d)
        d += datetime.timedelta(days=7)
    return out


# ------------------------------------------------------------------ session / module creation
def create_session(student, mode, kind, label, plan, feedback, timed):
    sid = db.x('INSERT INTO sessions(student_id, mode, kind, label, plan_json, feedback, timed, created) VALUES (?,?,?,?,?,?,?,?)',
               (student['id'], mode, kind, label, json.dumps(plan), int(feedback), int(timed), time.time()))
    return sid


def create_module(sess, seq, section, module_no, variant):
    plan = json.loads(sess['plan_json'])
    sp = plan['sizes'][section]
    avoid = db.seen_uids(sess['student_id'])
    used = set(r['uid'] for r in db.q('SELECT i.uid FROM items i JOIN modules m ON m.id=i.module_id WHERE m.session_id=?', (sess['id'],)))
    qs = pool.build_module(section, sp['n'], variant, random.Random(), avoid | used, focus=plan.get('focus'), diff=plan.get('diff'))
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
    return None


# ------------------------------------------------------------------ login
@app.route('/login', methods=['GET', 'POST'])
def login():
    err = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        s = db.q('SELECT * FROM students WHERE name=?', (name,), one=True)
        if not s: err = 'No student with that name.'
        elif s['pin_hash'] and s['pin_hash'] != hpin(request.form.get('pin', '')): err = 'That PIN does not match.'
        else:
            session['sid'] = s['id']
            return redirect(url_for('home'))
    return render_template('login.html', students=db.q('SELECT name, pin_hash FROM students ORDER BY name'), err=err)


@app.route('/students/new', methods=['POST'])
def new_student():
    name = request.form.get('name', '').strip()
    if not name: return redirect(url_for('login'))
    try:
        sid = db.x('INSERT INTO students(name, pin_hash, goal_total, parent_name, created) VALUES (?,?,?,?,?)',
                   (name, hpin(request.form.get('pin', '').strip()), int(request.form.get('goal') or 1200), request.form.get('parent', '').strip(), time.time()))
    except Exception:
        return render_template('login.html', students=db.q('SELECT name, pin_hash FROM students ORDER BY name'), err='A student with that name already exists.')
    session['sid'] = sid
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('sid', None)
    return redirect(url_for('login'))


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
    if not s: return redirect(url_for('login'))
    ns = next_sunday()
    n, is_mock = sunday_info(ns)
    recent = db.q('SELECT * FROM sessions WHERE student_id=? ORDER BY created DESC LIMIT 6', (s['id'],))
    rows = db.response_rows(s['id'])
    rw, mt, tot = analytics.student_estimates(rows)
    return render_template('home.html', s=s, next_sun=ns, is_mock=is_mock, nth=n, mocks=upcoming_mocks(),
                           recent=recent, tot=tot, rw=rw, mt=mt, nrows=len(rows), conf=S.confidence_label(len(rows)),
                           plan=pool.mock_plan(55))


# ------------------------------------------------------------------ practice setup
@app.route('/practice', methods=['GET', 'POST'])
def practice():
    s = need_student()
    if request.method == 'POST':
        f = request.form
        sec = f.get('section', 'math')
        what = f.get('what', 'm1')
        length = f.get('length', 'session')
        timed = f.get('timed', '1') == '1'
        feedback = f.get('feedback', '1') == '1'
        if length == 'module': sz = pool.session_plan(pool.OFFICIAL[sec]['minutes'], sec)
        elif length == 'custom':
            n = max(3, min(int(f.get('custom_n') or 10), pool.OFFICIAL[sec]['n']))
            sec_per_q = pool.OFFICIAL[sec]['minutes'] * 60.0 / pool.OFFICIAL[sec]['n']
            sz = dict(n=n, limit=int(n * sec_per_q))
        else: sz = pool.session_plan(30, sec)
        plan = dict(order=[sec], sizes={sec: sz}, adaptive=False, f=sz['limit'] / float(pool.OFFICIAL[sec]['minutes'] * 60))
        variant, kind = 'm1', ''
        if what in ('m1', 'easy', 'hard'):
            variant = what
            kind = '%s %s' % (SECTION_NAME[sec], pool.VARIANT_LABEL[what])
        elif what == 'full':
            plan['adaptive'] = True
            plan['sizes'][sec] = pool.session_plan(pool.OFFICIAL[sec]['minutes'], sec)
            kind = '%s, both modules' % SECTION_NAME[sec]
        elif what.startswith('domain:'):
            dom = what.split(':', 1)[1]
            plan['focus'] = ['domain', dom]
            kind = '%s: %s' % (SECTION_NAME[sec], dom)
            if f.get('difficulty', 'mixed') != 'mixed': plan['diff'] = int(f['difficulty'])
        elif what.startswith('skill:'):
            key = what.split(':', 1)[1]
            plan['focus'] = ['skill', key]
            kind = 'Skill: %s' % SKILLS[key]['name']
            if f.get('difficulty', 'mixed') != 'mixed': plan['diff'] = int(f['difficulty'])
            variant = 'm1'
        if what.startswith(('domain:', 'skill:')):
            plan['focus'] = tuple(plan['focus'])
        plan['variant'] = variant
        sid = create_session(s, 'practice', kind, kind, plan, feedback, timed)
        sess = db.q('SELECT * FROM sessions WHERE id=?', (sid,), one=True)
        create_module(sess, 0, sec, 2 if variant in ('easy', 'hard') else 1, variant)
        return redirect(url_for('run', sid=sid))
    by_sec = {sec: [(k, v['name']) for k, v in SKILLS.items() if v['section'] == sec] for sec in ('rw', 'math')}
    return render_template('practice_setup.html', s=s, by_sec=by_sec, domains=DOMAINS, p30={sec: pool.session_plan(30, sec) for sec in ('rw', 'math')},
                           pfull={sec: pool.OFFICIAL[sec] for sec in ('rw', 'math')}, pre=request.args)


# ------------------------------------------------------------------ exam setup
@app.route('/exam', methods=['GET', 'POST'])
def exam():
    s = need_student()
    if request.method == 'POST':
        kind = request.form.get('kind', 'mock')
        if kind == 'full':
            plan = pool.full_plan(); label = 'Full-length mock SAT'
        else:
            minutes = max(30, min(120, int(request.form.get('minutes') or 55)))
            plan = pool.mock_plan(minutes); label = 'Mock SAT (%d-minute version)' % minutes
        full = dict(order=['rw', 'math'], sizes={'rw': plan['rw'], 'math': plan['math']}, adaptive=True, f=plan['f'], total_min=plan['total_min'])
        sid = create_session(s, 'exam', label, label, full, False, True)
        sess = db.q('SELECT * FROM sessions WHERE id=?', (sid,), one=True)
        create_module(sess, 0, 'rw', 1, 'm1')
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
        entry = dict(id=it['id'], idx=it['idx'], q=public(qd), answer=r['answer'] if r else '', flagged=bool(r and r['flagged']),
                     struck=json.loads(r['struck']) if r and r['struck'] else [], checked=bool(r and r['checked']), time_ms=r['time_ms'] if r else 0)
        if entry['checked']:
            entry['fb'] = dict(correct=bool(r['correct']), key=qd.get('answer'), expl=qd.get('expl'))
        payload.append(entry)
    plan = json.loads(sess['plan_json'])
    if sess['mode'] == 'exam' or plan.get('adaptive'):
        label = '%s: Module %d' % (SECTION_NAME[m['section']], m['module_no'])
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
    if prev and prev['checked']:  # practice answers are locked once checked
        return jsonify(ok=True, locked=True)
    tms = (prev['time_ms'] if prev else 0) + max(0, min(int(j.get('time_ms') or 0), 900000))
    db.x('''INSERT INTO responses(item_id, answer, correct, is_mc, time_ms, flagged, struck, ts) VALUES (?,?,?,?,?,?,?,?)
            ON CONFLICT(item_id) DO UPDATE SET answer=excluded.answer, correct=excluded.correct, time_ms=excluded.time_ms,
            flagged=excluded.flagged, struck=excluded.struck, ts=excluded.ts''',
         (it['id'], ans, grade(qd, ans), 1 if qd['type'] == 'mc' else 0, tms, 1 if j.get('flagged') else 0, json.dumps(j.get('struck') or []), time.time()))
    return jsonify(ok=True)


@app.route('/api/check', methods=['POST'])
def api_check():
    s = need_student()
    j = request.get_json(force=True)
    it, m, sess = _item_ctx(int(j['item_id']), s)
    if not sess['feedback'] or m['finished']: abort(403)
    qd = json.loads(it['qjson'])
    ans = (j.get('answer') or '').strip()
    prev = db.q('SELECT * FROM responses WHERE item_id=?', (it['id'],), one=True)
    tms = (prev['time_ms'] if prev else 0) + max(0, min(int(j.get('time_ms') or 0), 900000))
    ok = grade(qd, ans)
    db.x('''INSERT INTO responses(item_id, answer, correct, is_mc, time_ms, flagged, struck, checked, ts) VALUES (?,?,?,?,?,?,?,1,?)
            ON CONFLICT(item_id) DO UPDATE SET answer=excluded.answer, correct=excluded.correct, time_ms=excluded.time_ms, checked=1, ts=excluded.ts''',
         (it['id'], ans, ok, 1 if qd['type'] == 'mc' else 0, tms, 0, '[]', time.time()))
    return jsonify(ok=True, correct=bool(ok), key=qd.get('answer'), expl=qd.get('expl'))


@app.route('/api/finish', methods=['POST'])
def api_finish():
    s = need_student()
    j = request.get_json(force=True)
    m = own_module(int(j['module_id']), s)
    finish_module(m)
    return jsonify(ok=True, next=url_for('run', sid=m['session_id']))


# ------------------------------------------------------------------ results and review
def session_rows(sid):
    return [dict(r) for r in db.q('''SELECT i.*, r.answer, r.correct, r.time_ms, r.flagged, m.module_no, m.variant, m.section AS msec, m.seq
                                    FROM items i JOIN modules m ON m.id=i.module_id LEFT JOIN responses r ON r.item_id=i.id
                                    WHERE m.session_id=? ORDER BY m.seq, i.idx''', (sid,))]


def weakest_skill(student_id, rows):
    """Skill in this session with the biggest shortfall against what the student's overall level predicts."""
    allrows = db.response_rows(student_id)
    est = {sec: analytics._est(allrows, sec, time.time()) for sec in ('rw', 'math')}
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
    s = need_student()
    sess = own_session(sid, s)
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
    rw, mt, tot = analytics.student_estimates(all_rows)
    sr = [x for x in all_rows if x['session_id'] == sid]
    srw, smt = analytics._est(sr, 'rw', time.time()), analytics._est(sr, 'math', time.time())
    wk = weakest_skill(s['id'], rows)
    return render_template('results.html', s=s, sess=sess, per_mod=per_mod, dom=sorted(dom.items()), sk=sk, tot=tot, rw=rw, mt=mt,
                           srw=srw, smt=smt, weak=wk, total_q=len(rows), right=sum(1 for r in rows if r['correct']),
                           ruler=analytics.svg_ruler(rw, mt, tot, s['goal_total']), nrows=len(all_rows), conf=S.confidence_label(len(all_rows)))


@app.route('/review/<int:sid>')
def review(sid):
    s = need_student()
    sess = own_session(sid, s)
    rows = session_rows(sid)
    items = []
    for r in rows:
        qd = json.loads(r['qjson'])
        items.append(dict(r=r, q=qd, skill=SKILLS[r['skill']], mine=r['answer'] or '', ok=bool(r['correct'])))
    return render_template('review.html', s=s, sess=sess, items=items, only=request.args.get('only'))


# ------------------------------------------------------------------ dashboard
@app.route('/dashboard')
def dashboard_view():
    s = need_student()
    d = analytics.dashboard(s['id'])
    view = request.args.get('view', 'student')
    return render_template('dashboard.html', s=s, d=d, view=view, ruler=analytics.svg_ruler(d['rw'], d['math'], d['total'], d['goal']),
                           tline=analytics.svg_timeline(d['timeline'], d['goal']))


# ------------------------------------------------------------------ homework and lecture sheets
def hw_count(skill):
    return int(max(10, min(15, round(1800 / (1.5 * SKILLS[skill]['avg_sec'])))))


@app.route('/homework')
def homework():
    s = need_student()
    skill = request.args.get('skill')
    if skill not in SKILLS:
        abort(404)
    n = int(request.args.get('n') or hw_count(skill))
    rows = [r for r in db.response_rows(s['id']) if r['skill'] == skill]
    acc = (sum(1 for r in rows if r['correct']) / float(len(rows))) if rows else None
    mix = (.35, .45, .20) if (acc is None or acc < .55) else (.15, .40, .45)
    c = pool.apportion(n, {0: mix[0], 1: mix[1], 2: mix[2]})
    ds = [0] * c[0] + [1] * c[1] + [2] * c[2]
    seed_base = int(request.args.get('seed') or random.randrange(1, 10 ** 6))
    rng = random.Random(seed_base)
    avoid, qs = set(), []
    for d in ds:
        qd = pool.make_safe(skill, d, rng.randrange(1, 10 ** 9), False, avoid)
        avoid.add(qd['uid']); qs.append(qd)
    return render_template('homework.html', s=s, skill=SKILLS[skill], qs=qs, n=n, today=datetime.date.today(), acc=acc, seed=seed_base,
                           key=request.args.get('key') == '1', mins=30)


@app.route('/lecture/<skill>')
def lecture(skill):
    s = need_student()
    if skill not in SKILLS: abort(404)
    rng = random.Random(int(request.args.get('seed') or 7))
    ex = [pool.make_safe(skill, d, rng.randrange(1, 10 ** 9), False, set()) for d in (0, 1, 2)]
    return render_template('lecture.html', s=s, skill=SKILLS[skill], ex=ex, reference=REFERENCE_HTML)


@app.route('/skills')
def skills_index():
    s = need_student()
    return render_template('skills.html', s=s, skills=SKILLS, domains=DOMAINS)


@app.route('/api/calc-ping')
def calc_ping():
    return jsonify(ok=True)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 5000)), debug=False)
