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
        t['date'] = day.strftime('%b %d') if day.year == this_year else day.strftime("%b '%y")
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
        out.append(dict(start=datetime.date.fromtimestamp(a + 86400).strftime('%b %d'), n=len(rr),
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
            s += '<rect x="%d" y="%d" width="%d" height="14" class="hl"/>' % (x(est['lo']), y - 7, max(4, x(est['hi']) - x(est['lo'])))
            s += '<line x1="%d" x2="%d" y1="%d" y2="%d" class="mid"/>' % (x(est['mid']), x(est['mid']), y - 12, y + 12)
        else:
            s += '<text x="%d" y="%d" class="tk">not enough evidence yet</text>' % (x((mn + mx) / 2.0), y - 10)
        if goal_v: s += '<path d="M%d %d l-5 -9 h10 z" class="goal"/>' % (x(goal_v), y - 12)
        return s
    body = row(28, 'Total', total, 400, 1600, goal)
    body += row(88, 'Reading & Writing', rw, 200, 800)
    body += row(148, 'Math', mt, 200, 800)
    return '<svg viewBox="0 0 %d 180" class="ruler" role="img" aria-label="Estimated score ranges">%s</svg>' % (w, body)


def svg_timeline(tl, goal=None, w=640, h=210):
    est = [t for t in tl if not t['reported']]
    if len(tl) < 2 or not est:
        return ''
    xs = lambda i: 46 + i * (w - 70) / float(len(tl) - 1)
    lo_v = min(min(t['lo'] for t in tl), goal or 9999) - 40
    hi_v = max(max(t['hi'] for t in tl), goal or 0) + 40
    ys = lambda v: 16 + (hi_v - v) / float(hi_v - lo_v) * (h - 56)
    idx = [(i, t) for i, t in enumerate(tl) if not t['reported']]
    s = ''
    if len(idx) >= 2:
        band = ' '.join('%.1f,%.1f' % (xs(i), ys(t['hi'])) for i, t in idx) + ' ' + ' '.join('%.1f,%.1f' % (xs(i), ys(t['lo'])) for i, t in reversed(idx))
        s += '<polygon points="%s" class="band"/><polyline points="%s" class="tline"/>' % (band, ' '.join('%.1f,%.1f' % (xs(i), ys(t['mid'])) for i, t in idx))
    for i, t in enumerate(tl):
        if t['reported']:
            s += '<path d="M%.1f %.1f l6 6 l-6 6 l-6 -6 z" class="goal"><title>%s %s: %d (Reading and Writing %d, Math %d)</title></path>' % (
                xs(i), ys(t['mid']) - 6, t['date'], t['kind'], t['mid'], t['rw'], t['math'])
        else:
            s += '<circle cx="%.1f" cy="%.1f" r="3.5" class="dot"><title>%s: %d (range %d-%d)</title></circle>' % (xs(i), ys(t['mid']), t['date'], t['mid'], t['lo'], t['hi'])
        if len(tl) <= 10 or i % 2 == 0: s += '<text x="%.1f" y="%d" class="tk">%s</text>' % (xs(i), h - 8, t['date'])
    if goal: s += '<line x1="40" x2="%d" y1="%.1f" y2="%.1f" class="goalline"/><text x="%d" y="%.1f" class="tkr">goal %d</text>' % (w - 10, ys(goal), ys(goal), w - 10, ys(goal) - 4, goal)
    for v in range(int(lo_v // 100 * 100 + 100), int(hi_v), 100):
        s += '<text x="0" y="%.1f" class="tkl">%d</text>' % (ys(v) + 3, v)
    return '<svg viewBox="0 0 %d %d" class="tl" role="img" aria-label="Estimated total score over time">%s</svg>' % (w, h, s)


def svg_weekly(wk, w=640, h=150):
    """Questions per week as bars, first-try accuracy as dots on the same weeks."""
    if not any(x['n'] for x in wk): return ''
    top = max(10, max(x['n'] for x in wk))
    bw = (w - 60) / float(len(wk))
    ys = lambda v: 12 + (1 - v / float(top)) * (h - 46)
    ya = lambda a: 12 + (1 - a) * (h - 46)
    s = ''
    for i, x in enumerate(wk):
        x0 = 44 + i * bw
        if x['n']:
            s += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="wbar"><title>Week of %s: %d questions, %d minutes</title></rect>' % (
                x0 + bw * 0.18, ys(x['n']), bw * 0.64, ys(0) - ys(x['n']), x['start'], x['n'], x['minutes'])
        if x['acc'] is not None:
            s += '<circle cx="%.1f" cy="%.1f" r="3.5" class="wacc"><title>%d%% correct on first try</title></circle>' % (x0 + bw / 2, ya(x['acc']), round(x['acc'] * 100))
        if i % 2 == len(wk) % 2 or len(wk) <= 6: s += '<text x="%.1f" y="%d" class="tk">%s</text>' % (x0 + bw / 2, h - 16, x['start'])
    s += '<text x="0" y="%.1f" class="tkl">%d</text><text x="0" y="%.1f" class="tkl">0</text>' % (ys(top) + 4, top, ys(0))
    s += '<text x="%d" y="%.1f" class="tkr">100%%</text><text x="%d" y="%.1f" class="tkr">0%%</text>' % (w, ya(1) + 4, w, ya(0))
    s += '<text x="%d" y="%d" class="tk">bars: questions per week (left scale) &#183; dots: share right on the first try (right scale)</text>' % (w / 2, h - 2)
    return '<svg viewBox="0 0 %d %d" class="tl" role="img" aria-label="Weekly practice volume and accuracy">%s</svg>' % (w, h, s)
