"""Dashboard numbers, plain-language summaries, and small SVG charts (server-side so they also print)."""
import datetime
import time

import db
import scoring as S
from bank.skills import SKILLS, DOMAINS, SECTION_NAME

SEC_TARGET_SEC = {'rw': 32 * 60 / 27.0, 'math': 35 * 60 / 22.0}
SECTIONS = ('rw', 'math')


def _date_ts(s):
    return time.mktime(datetime.datetime.strptime(s, '%Y-%m-%d').timetuple())


def priors(student_id):
    """Earlier real scores (official SAT/PSAT or Bluebook practice tests), each with a timestamp for its test date."""
    out = []
    for p in db.prior_scores(student_id):
        p['taken_ts'] = _date_ts(p['taken'])
        out.append(p)
    return out


def _est(rows, sec, now_ts, prior_rows=None):
    pr = [p for p in (prior_rows or []) if p['taken_ts'] <= now_ts]
    return S.section_estimate([r for r in rows if r['section'] == sec], now_ts, DOMAINS[sec], S.prior_from_scores(pr, sec, now_ts))


def student_estimates(rows, now_ts=None, prior_rows=None):
    now_ts = now_ts or time.time()
    rw, mt = _est(rows, 'rw', now_ts, prior_rows), _est(rows, 'math', now_ts, prior_rows)
    return rw, mt, S.total_estimate(rw, mt)


def timeline(student_id, rows=None, prior_rows=None):
    """Estimate after each finished session, plus each reported real score as its own point."""
    rows = db.response_rows(student_id) if rows is None else rows
    prior_rows = priors(student_id) if prior_rows is None else prior_rows
    sess = db.q('SELECT id, created, finished, kind, mode, purpose FROM sessions WHERE student_id=? AND finished IS NOT NULL ORDER BY created', (student_id,))
    out = []
    for s in sess:
        up = [r for r in rows if r['session_created'] <= s['created']]
        if not up: continue
        rw, mt, tot = student_estimates(up, s['finished'], prior_rows)
        if not tot['has_data']: continue
        out.append(dict(session_id=s['id'], ts=s['finished'], kind=s['kind'], mode=s['mode'], purpose=s['purpose'], reported=False,
                        rw=rw['mid'], math=mt['mid'], lo=tot['lo'], mid=tot['mid'], hi=tot['hi'], n=tot['n']))
    for p in prior_rows:
        tot = p['rw'] + p['math']
        out.append(dict(session_id=None, ts=p['taken_ts'], kind=p['test'], mode='reported', purpose='', reported=True,
                        rw=p['rw'], math=p['math'], lo=tot, mid=tot, hi=tot, n=0))
    out.sort(key=lambda t: t['ts'])
    this_year = datetime.date.today().year
    for t in out:
        day = datetime.date.fromtimestamp(t['ts'])
        t['date'] = '%s %d' % (day.strftime('%b'), day.day) if day.year == this_year else day.strftime("%b '%y")
    if len(set(t['date'] for t in out)) < len(out):
        for i, t in enumerate(out):
            t['date'] = '%d. %s' % (i + 1, t['date'])
    return out


def weekly(rows, now, weeks=10):
    """Questions answered, first-try accuracy, and minutes per week, oldest first (for the activity chart)."""
    out = []
    for k in range(weeks - 1, -1, -1):
        a, b = now - (k + 1) * 7 * 86400, now - k * 7 * 86400
        rr = [r for r in rows if a <= r['ts'] < b and not r['omitted']]
        wd = datetime.date.fromtimestamp(a + 86400)
        out.append(dict(start='%s %d' % (wd.strftime('%b'), wd.day), n=len(rr),
                        acc=(sum(1 for r in rr if r['correct']) / float(len(rr))) if rr else None,
                        minutes=sum(r['time_ms'] or 0 for r in rr) / 60000.0))
    return out


def recommendations(skills, est, k=3):
    """Skills where practice should move the score most: official weight of the skill x chance of missing a medium
    question at the current level. Untried skills use the section level. Slipping skills get a nudge."""
    by_key = dict((s['skill'], s) for s in skills)
    cands = []
    for sec in SECTIONS:
        for dom, share in DOMAINS[sec].items():
            keys = [key for key, v in SKILLS.items() if v['section'] == sec and v['domain'] == dom]
            for key in keys:
                s = by_key.get(key)
                p = s['p_medium'] if s and s['n'] >= 3 else S._sig(est[sec]['theta'] - S.B[1])
                gain = share / len(keys) * (1 - p) * (1.25 if s and s['trend'] == 'slipping' else 1.0)
                why = ('not tried yet' if not s else 'only %d answered so far' % s['n'] if s['n'] < 3 else
                       'slipping lately' if s['trend'] == 'slipping' else '%d%% correct' % round(s['acc'] * 100))
                cands.append(dict(skill=key, name=SKILLS[key]['name'], section=sec, gain=gain, why=why))
    cands.sort(key=lambda c: -c['gain'])
    picked = []
    for sec in SECTIONS:  # at least one per section, then the best of the rest
        top = [c for c in cands if c['section'] == sec][:1]
        picked += top
    for c in cands:
        if len(picked) >= k: break
        if c not in picked: picked.append(c)
    return picked[:k]


def dashboard(student_id):
    now = time.time()
    st = db.q('SELECT * FROM students WHERE id=?', (student_id,), one=True)
    rows = db.response_rows(student_id)
    pr = priors(student_id)
    rw, mt, tot = student_estimates(rows, now, pr)
    answered = [r for r in rows if not r['omitted']]
    data = dict(student=dict(st), n=len(rows), n_answered=len(answered), rw=rw, math=mt, total=tot,
                conf=S.confidence_label(tot), priors=pr)
    data['goal'] = st['goal_total'] or 1200
    data['gap'] = data['goal'] - tot['mid']
    data['timeline'] = timeline(student_id, rows, pr)
    data['weekly'] = weekly(rows, now)
    # skills
    skills = []
    for sec, est in (('rw', rw), ('math', mt)):
        by = {}
        for r in rows:
            if r['section'] == sec: by.setdefault(r['skill'], []).append(r)
        for t in S.skill_table(by, est['theta'], now):
            meta = SKILLS[t['skill']]
            t.update(name=meta['name'], section=sec, domain=meta['domain'])
            t['pace'] = None if t['avg_sec'] is None else t['avg_sec'] / SEC_TARGET_SEC[sec]
            skills.append(t)
    seen = set(s['skill'] for s in skills)
    data['untried'] = [SKILLS[k]['name'] for k in SKILLS if k not in seen]
    ranked = sorted([s for s in skills if s['n'] >= 4], key=lambda s: s['strength'])
    data['weakest'] = ranked[:3]
    data['strongest'] = [s for s in reversed(ranked[-3:]) if s['strength'] > -0.05] if len(ranked) >= 4 else []
    data['skills'] = sorted(skills, key=lambda s: (s['section'], s['strength']))
    data['improving'] = [s for s in skills if s['trend'] == 'improving']
    data['slipping'] = [s for s in skills if s['trend'] == 'slipping']
    data['recommend'] = recommendations(skills, {'rw': rw, 'math': mt})
    counts = {}
    for s in skills: counts[s['mastery']] = counts.get(s['mastery'], 0) + 1
    data['mastery_counts'] = counts
    # domains
    dom = []
    for sec in SECTIONS:
        for d in DOMAINS[sec]:
            rr = [r for r in rows if r['section'] == sec and r['domain'] == d]
            if rr: dom.append(dict(section=sec, domain=d, n=len(rr), acc=sum(1 for r in rr if r['correct']) / float(len(rr))))
    data['domains'] = dom
    # habits
    wk = now - 7 * 86400
    data['q_week'] = len([r for r in answered if r['ts'] >= wk])
    weeks = set(int((now - r['ts']) // (7 * 86400)) for r in answered)
    streak = 0
    while streak in weeks: streak += 1
    data['streak'] = streak
    data['sessions'] = db.q('SELECT COUNT(*) c FROM sessions WHERE student_id=? AND finished IS NOT NULL', (student_id,), one=True)['c']
    data['omitted'] = len(rows) - len(answered)
    data['hint_rate'] = (sum(1 for r in answered if r['hint_used']) / float(len(answered))) if answered else 0.0
    pace = {}
    for sec in SECTIONS:
        ts = [r['time_ms'] for r in answered if r['section'] == sec and r['time_ms'] and r['timed']]
        if len(ts) >= 10: pace[sec] = sum(ts) / len(ts) / 1000.0 / SEC_TARGET_SEC[sec]
    data['pace'] = pace
    data['timing'] = timing(rows)
    data['summary'] = summary_text(data)
    return data


def _name(s): return s['name']


def summary_text(d):
    """Plain-language paragraph for parents and students. Never claims more certainty than the data supports."""
    nm = d['student']['name'].split(' ')[0]
    t = d['total']
    if not t['has_data']:
        missing = [SECTION_NAME[s] for s, e in (('rw', d['rw']), ('math', d['math'])) if not e['has_data']]
        return ('%s has answered %d questions so far. There is not yet enough evidence in %s for a dependable estimate; '
                'the 1-hour diagnostic, or an earlier official score, fixes that.' % (nm, d['n_answered'], ' or '.join(missing)))
    parts = []
    basis = 'Based on %d answered questions' % d['n_answered']
    if t['n'] == 0 or d['n_answered'] < 20:
        pu = d['rw']['prior_used'] or d['math']['prior_used']
        if pu: basis = 'Based mostly on the %s score from %s' % (pu['test'], pu['taken'])
    parts.append('%s, %s\'s current estimate is %d to %d out of 1600 (most likely about %d). The estimate is %s.' % (
        basis, nm, t['lo'], t['hi'], t['mid'], d['conf']))
    low_cov = [SECTION_NAME[s] for s, e in (('rw', d['rw']), ('math', d['math'])) if e['coverage'] < 0.75 and not e['prior_used']]
    if low_cov: parts.append('Some %s topics have little evidence yet, which keeps the range wide.' % ' and '.join(low_cov))
    gap = d['gap']
    if gap > 20: parts.append('The goal is %d, so roughly %d points remain.' % (d['goal'], gap))
    elif gap < -20: parts.append('That is already above the goal of %d.' % d['goal'])
    else: parts.append('That is right around the goal of %d.' % d['goal'])
    if d['strongest']: parts.append('Strongest areas: %s.' % ', '.join(_name(s) for s in d['strongest'][:2]))
    if d['weakest']: parts.append('Most room to grow: %s.' % ', '.join(_name(s) for s in d['weakest'][:2]))
    if d['improving']: parts.append('Improving: %s.' % ', '.join(_name(s) for s in d['improving'][:2]))
    if d['slipping']: parts.append('Worth a refresher: %s.' % ', '.join(_name(s) for s in d['slipping'][:2]))
    sl = [s for s, v in d['pace'].items() if v > 1.25]
    if sl: parts.append('Pacing: %s questions are taking noticeably longer than the real test allows.' % ' and '.join(SECTION_NAME[s] for s in sl))
    return ' '.join(parts)


def roster_row(student):
    """One line of the instructor's student list."""
    rows = db.response_rows(student['id'])
    pr = priors(student['id'])
    rw, mt, tot = student_estimates(rows, None, pr)
    last = db.q('SELECT MAX(COALESCE(finished, created)) t FROM sessions WHERE student_id=?', (student['id'],), one=True)['t']
    wk = time.time() - 7 * 86400
    return dict(s=student, total=tot, conf=S.confidence_label(tot), n=len([r for r in rows if not r['omitted']]),
                q_week=len([r for r in rows if r['ts'] >= wk and not r['omitted']]), last=last or student['last_seen'],
                sessions=db.q('SELECT COUNT(*) c FROM sessions WHERE student_id=?', (student['id'],), one=True)['c'])


# ------------------------------------------------------------------ SVG
# Charts are drawn server-side as plain SVG (they print, and need no JS library). Colors come from CSS roles in app.css
# (--c-s1, --hl, --c-goal ...), which have validated light and dark steps. Marks with data-tip get a hover/keyboard
# tooltip from static/charts.js; hit targets are larger than the marks.
def _esc(t):
    return str(t).replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


def svg_ruler(rw, mt, total, goal=None, w=640):
    """Score ranges drawn as highlighter strokes on a ruler. Two rulers: total (400-1600) and each section (200-800).
    A section (or the total) without enough evidence is drawn as an empty ruler with a note instead of a guess."""
    def row(y, label, est, mn, mx, goal_v=None):
        x = lambda v: 150 + (v - mn) / float(mx - mn) * (w - 190)
        s = '<text x="0" y="%d" class="rl">%s</text>' % (y + 4, label)
        s += '<line x1="%d" x2="%d" y1="%d" y2="%d" class="rule"/>' % (x(mn), x(mx), y, y)
        step = 200 if mx - mn > 800 else 100
        v = mn
        while v <= mx:
            s += '<line x1="%d" x2="%d" y1="%d" y2="%d" class="tick"/><text x="%d" y="%d" class="tk">%d</text>' % (x(v), x(v), y - 5, y + 5, x(v), y + 20, v)
            v += step
        if est['has_data']:
            tip = '%s: likely %d to %d, best guess %d' % (label.replace('&amp;', 'and'), est['lo'], est['hi'], est['mid'])
            s += '<g data-tip="%s" tabindex="0"><rect x="%d" y="%d" width="%d" height="26" class="hit"/>' % (_esc(tip), x(est['lo']) - 4, y - 13, max(12, x(est['hi']) - x(est['lo']) + 8))
            s += '<rect x="%d" y="%d" width="%d" height="14" rx="2" class="hl"/>' % (x(est['lo']), y - 7, max(4, x(est['hi']) - x(est['lo'])))
            s += '<line x1="%d" x2="%d" y1="%d" y2="%d" class="mid"/></g>' % (x(est['mid']), x(est['mid']), y - 12, y + 12)
        else:
            s += '<text x="%d" y="%d" class="tk">not enough evidence yet</text>' % (x((mn + mx) / 2.0), y - 10)
        if goal_v: s += '<g data-tip="Goal: %d" tabindex="0"><path d="M%d %d l-6 -10 h12 z" class="goal"/></g>' % (goal_v, x(goal_v), y - 12)
        return s
    body = row(28, 'Total', total, 400, 1600, goal)
    body += row(88, 'Reading &amp; Writing', rw, 200, 800)
    body += row(148, 'Math', mt, 200, 800)
    return '<svg viewBox="0 0 %d 180" class="ruler" role="img" aria-label="Estimated score ranges: total %s">%s</svg>' % (
        w, '%d to %d' % (total['lo'], total['hi']) if total['has_data'] else 'not enough evidence yet', body)


def svg_timeline(tl, goal=None, w=640, h=220):
    """Estimated total after each session (line + 80% band) with official/Bluebook scores as diamonds and the goal as a
    dashed line. One y-axis (total score). Legend is drawn in HTML by the template."""
    est = [t for t in tl if not t['reported']]
    if len(tl) < 2 or not est:
        return ''
    L, R, T, B = 46, 34, 14, 34
    xs = lambda i: L + i * (w - L - R) / float(len(tl) - 1)
    lo_v = min(min(t['lo'] for t in tl), goal or 9999) - 40
    hi_v = max(max(t['hi'] for t in tl), goal or 0) + 40
    lo_v, hi_v = max(400, lo_v // 100 * 100), min(1600, -(-hi_v // 100) * 100)
    ys = lambda v: T + (hi_v - v) / float(hi_v - lo_v) * (h - T - B)
    s = ''
    for v in range(int(lo_v), int(hi_v) + 1, 100):
        s += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="grid"/><text x="0" y="%.1f" class="tkl">%d</text>' % (L, w - R, ys(v), ys(v), ys(v) + 4, v)
    idx = [(i, t) for i, t in enumerate(tl) if not t['reported']]
    if len(idx) >= 2:
        band = ' '.join('%.1f,%.1f' % (xs(i), ys(t['hi'])) for i, t in idx) + ' ' + ' '.join('%.1f,%.1f' % (xs(i), ys(t['lo'])) for i, t in reversed(idx))
        s += '<polygon points="%s" class="band"/><polyline points="%s" class="tline"/>' % (band, ' '.join('%.1f,%.1f' % (xs(i), ys(t['mid'])) for i, t in idx))
    if goal:
        s += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="goalline"/>' % (L, w - R, ys(goal), ys(goal))
    for i, t in enumerate(tl):
        x, y = xs(i), ys(t['mid'])
        if t['reported']:
            tip = '%s, %s: %d (Reading and Writing %d, Math %d)' % (t['kind'], t['date'], t['mid'], t['rw'], t['math'])
            s += '<g data-tip="%s" tabindex="0"><circle cx="%.1f" cy="%.1f" r="12" class="hit"/><path d="M%.1f %.1f l7 7 l-7 7 l-7 -7 z" class="rep mark"/></g>' % (_esc(tip), x, y, x, y - 7)
        else:
            tip = '%s after %s: about %d (likely %d to %d)' % (t['date'], t['kind'], t['mid'], t['lo'], t['hi'])
            s += '<g data-tip="%s" tabindex="0"><circle cx="%.1f" cy="%.1f" r="12" class="hit"/><circle cx="%.1f" cy="%.1f" r="4.5" class="dot mark"/></g>' % (_esc(tip), x, y, x, y)
        if len(tl) <= 10 or i % 2 == 0: s += '<text x="%.1f" y="%d" class="tk">%s</text>' % (x, h - 10, t['date'])
    return '<svg viewBox="0 0 %d %d" class="tl" role="img" aria-label="Estimated total score over time">%s</svg>' % (w, h, s)


def _bar(x, y0, width, height, r=4):
    """A bar with rounded data-end (top) and a square end on the baseline."""
    if height <= 0: return ''
    r = min(r, height, width / 2.0)
    return ('M%.1f %.1f V%.1f Q%.1f %.1f %.1f %.1f H%.1f Q%.1f %.1f %.1f %.1f V%.1f Z' %
            (x, y0, y0 - height + r, x, y0 - height, x + r, y0 - height, x + width - r, x + width, y0 - height, x + width, y0 - height + r, y0))


def svg_week_volume(wk, w=320, h=170):
    """Questions answered per week: one series, so no legend; the heading names it."""
    if not any(x['n'] for x in wk): return ''
    L, R, T, B = 30, 6, 10, 28
    top = max(10, max(x['n'] for x in wk)); top = int(-(-top // 10) * 10)
    bw = (w - L - R) / float(len(wk))
    ys = lambda v: T + (1 - v / float(top)) * (h - T - B)
    s = ''
    for v in (0, top // 2, top):
        s += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="%s"/><text x="0" y="%.1f" class="tkl">%d</text>' % (L, w - R, ys(v), ys(v), 'axis' if v == 0 else 'grid', ys(v) + 4, v)
    for i, x in enumerate(wk):
        x0 = L + i * bw
        tip = 'Week of %s: %d question%s, %d minutes' % (x['start'], x['n'], '' if x['n'] == 1 else 's', round(x['minutes']))
        s += '<g data-tip="%s" tabindex="0"><rect x="%.1f" y="%d" width="%.1f" height="%.1f" class="hit"/>' % (_esc(tip), x0, T, bw, h - T - B)
        if x['n']: s += '<path d="%s" class="wbar mark"/>' % _bar(x0 + 1, ys(0), bw - 2, ys(0) - ys(x['n']))
        s += '</g>'
        if i % 3 == (len(wk) - 1) % 3: s += '<text x="%.1f" y="%d" class="tk">%s</text>' % (x0 + bw / 2, h - 8, x['start'])
    return '<svg viewBox="0 0 %d %d" class="tl" role="img" aria-label="Questions answered per week">%s</svg>' % (w, h, s)


def svg_week_accuracy(wk, w=320, h=170):
    """Share right on the first try per week, 0-100% on its own axis (a separate chart, never a second axis)."""
    pts = [(i, x) for i, x in enumerate(wk) if x['acc'] is not None]
    if not pts: return ''
    L, R, T, B = 36, 24, 10, 28
    step = (w - L - R) / float(max(1, len(wk) - 1))
    xs = lambda i: L + i * step
    ys = lambda a: T + (1 - a) * (h - T - B)
    s = ''
    for a in (0, .5, 1):
        s += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="%s"/><text x="0" y="%.1f" class="tkl">%d%%</text>' % (L, w - R, ys(a), ys(a), 'axis' if a == 0 else 'grid', ys(a) + 4, a * 100)
    runs, cur = [], []
    for i, x in enumerate(wk):  # the line breaks across weeks with no practice rather than inventing a value
        if x['acc'] is None:
            if cur: runs.append(cur); cur = []
        else: cur.append((i, x['acc']))
    if cur: runs.append(cur)
    for run in runs:
        if len(run) > 1: s += '<polyline points="%s" class="aline"/>' % ' '.join('%.1f,%.1f' % (xs(i), ys(a)) for i, a in run)
    for i, x in pts:
        tip = 'Week of %s: %d%% right on the first try (%d questions)' % (x['start'], round(x['acc'] * 100), x['n'])
        s += '<g data-tip="%s" tabindex="0"><circle cx="%.1f" cy="%.1f" r="12" class="hit"/><circle cx="%.1f" cy="%.1f" r="4.5" class="adot mark"/></g>' % (_esc(tip), xs(i), ys(x['acc']), xs(i), ys(x['acc']))
    for i, x in enumerate(wk):
        if i % 3 == (len(wk) - 1) % 3: s += '<text x="%.1f" y="%d" class="tk">%s</text>' % (xs(i), h - 8, x['start'])
    return '<svg viewBox="0 0 %d %d" class="tl" role="img" aria-label="Share of questions right on the first try, per week">%s</svg>' % (w, h, s)


# ------------------------------------------------------------------ timing
FAST_FRAC = 0.35   # an answer in under 35% of the real test's average time per question is treated as a quick one
SLOW_FRAC = 2.0    # more than twice the average is a long one
MIN_TIMING_N = 20  # answers per section before timing is described at all


def _median(xs):
    xs = sorted(xs)
    n = len(xs)
    return None if not n else (xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2.0)


def timing(rows):
    """How the student spends time, per section, from in-app sets where no answer was shown until the end (so the clock
    measures thinking, not reading explanations). Returns {section: dict(n, target, median, by_d, findings)}.
    Each finding is (kind, headline, detail); kind 'watch' is worth acting on, 'good' is reassurance. Only patterns with
    at least five answers behind them are called out."""
    out = {}
    for sec in SECTIONS:
        target = SEC_TARGET_SEC[sec]
        rr = [r for r in rows if r['section'] == sec and not r['omitted'] and r['time_ms'] and r.get('mode') != 'homework'
              and r.get('assist', 'end') in ('end', None, '')]
        blanks = [r for r in rows if r['section'] == sec and r['omitted'] and r.get('limit_sec')]
        timed_n = len([r for r in rows if r['section'] == sec and r.get('limit_sec')])
        secs = [min(r['time_ms'], 600000) / 1000.0 for r in rr]
        info = dict(n=len(rr), target=target, median=_median(secs), by_d=[], findings=[])
        for d, name in enumerate(('Easy', 'Medium', 'Hard')):
            x = [(t, r['correct']) for t, r in zip(secs, rr) if r['d'] == d]
            info['by_d'].append(dict(d=d, name=name, n=len(x), median=_median([t for t, _ in x]),
                                     acc=(sum(c for _, c in x) / float(len(x))) if x else None))
        out[sec] = info
        if len(rr) < MIN_TIMING_N:
            continue
        acc_all = sum(r['correct'] for r in rr) / float(len(rr))
        f = info['findings']
        hard, easy = info['by_d'][2], info['by_d'][0]
        if hard['n'] >= 5 and hard['median'] < 0.6 * target and hard['acc'] < 0.45:
            f.append(('watch', 'Rushing hard questions',
                      'Hard questions get a median of %d seconds, well under the real test&rsquo;s average of %d, and %d%% of them are right. '
                      'Slowing down on these is likely worth points.' % (hard['median'], target, round(hard['acc'] * 100))))
        fast = [(t, r['correct']) for t, r in zip(secs, rr) if t < FAST_FRAC * target]
        if len(fast) >= 5 and not f:  # when hard questions are already flagged as rushed, this would say the same thing again
            fa = sum(c for _, c in fast) / float(len(fast))
            if fa < 0.4:
                f.append(('watch', 'Quick answers are often guesses',
                          '%d answers came in under %d seconds, and only %d%% of those were right. Reading the whole question before answering should help.'
                          % (len(fast), round(FAST_FRAC * target), round(fa * 100))))
        if easy['n'] >= 5 and easy['median'] > 1.3 * target:
            f.append(('watch', 'Spending long on easy questions',
                      'Easy questions take a median of %d seconds, more than the real test&rsquo;s average of %d per question, which leaves less time for harder ones.'
                      % (easy['median'], target)))
        slow = [(t, r['correct']) for t, r in zip(secs, rr) if t > SLOW_FRAC * target]
        if len(slow) >= 5:
            sa = sum(c for _, c in slow) / float(len(slow))
            if sa < acc_all - 0.15:
                f.append(('watch', 'Extra time is not paying off',
                          'Questions that took more than %d seconds were right %d%% of the time, against %d%% overall. Past that point, mark it, make a guess, and come back if time allows.'
                          % (round(SLOW_FRAC * target), round(sa * 100), round(acc_all * 100))))
        if len(blanks) >= 3 and timed_n and len(blanks) / float(timed_n) >= 0.05:
            f.append(('watch', 'Running out of time',
                      '%d questions were left blank in timed sets (%d%%). Blanks count as wrong, so a guess on every question before time runs out is free points.'
                      % (len(blanks), round(100.0 * len(blanks) / timed_n))))
        if not f:
            f.append(('good', 'Pacing looks healthy',
                      'A median of %d seconds per question against the real test&rsquo;s average of %d, with no sign of rushing or getting stuck.' % (info['median'], target)))
    return out


def svg_timing(info, w=320, h=180):
    """Median seconds per question at each difficulty, with the real test's average time per question as a dashed
    reference line (named, with its value, in the caption under the chart). One series, one axis; the heading names the section."""
    bars = [b for b in info['by_d'] if b['n']]
    if info['n'] < MIN_TIMING_N or not bars: return ''
    L, R, T, B = 34, 8, 14, 28
    top = max([b['median'] for b in bars] + [info['target']]) * 1.15
    step = 30 if top <= 180 else 60
    top = int(-(-top // step) * step)
    ys = lambda v: T + (1 - v / float(top)) * (h - T - B)
    s = ''
    for v in range(0, top + 1, step):
        s += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="%s"/><text x="0" y="%.1f" class="tkl">%ds</text>' % (L, w - R, ys(v), ys(v), 'axis' if v == 0 else 'grid', ys(v) + 4, v)
    bw = (w - L - R) / 3.0
    for b in info['by_d']:
        x0 = L + b['d'] * bw
        if b['n']:
            tip = '%s: median %d seconds over %d answers, %d%% right' % (b['name'], round(b['median']), b['n'], round(b['acc'] * 100))
            s += '<g data-tip="%s" tabindex="0"><rect x="%.1f" y="%d" width="%.1f" height="%.1f" class="hit"/>' % (_esc(tip), x0, T, bw, h - T - B)
            s += '<path d="%s" class="wbar mark"/></g>' % _bar(x0 + bw * 0.22, ys(0), bw * 0.56, ys(0) - ys(b['median']))
        s += '<text x="%.1f" y="%d" class="tk">%s</text>' % (x0 + bw / 2, h - 8, b['name'])
    y = ys(info['target'])
    s += '<g data-tip="Real test average: %d seconds per question" tabindex="0"><line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="hit" stroke-width="10" stroke="transparent"/>' % (round(info['target']), L, w - R, y, y)
    s += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="goalline"/></g>' % (L, w - R, y, y)
    return '<svg viewBox="0 0 %d %d" class="tl" role="img" aria-label="Median seconds per question by difficulty">%s</svg>' % (w, h, s)
