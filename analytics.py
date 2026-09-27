"""Dashboard numbers, plain-language summaries, and small SVG charts (server-side so they also print)."""
import time
import datetime

import db
import scoring as S
from bank.skills import SKILLS, DOMAINS, SECTION_NAME

SEC_TARGET_SEC = {'rw': 32 * 60 / 27.0, 'math': 35 * 60 / 22.0}


def _est(rows, sec, now_ts):
    return S.section_estimate(S.weighted([r for r in rows if r['section'] == sec], now_ts))


def student_estimates(rows, now_ts=None):
    now_ts = now_ts or time.time()
    rw, mt = _est(rows, 'rw', now_ts), _est(rows, 'math', now_ts)
    return rw, mt, S.total_estimate(rw, mt)


def timeline(student_id):
    rows = db.response_rows(student_id)
    sess = db.q('SELECT id, created, kind, mode FROM sessions WHERE student_id=? AND finished IS NOT NULL ORDER BY created', (student_id,))
    out = []
    for s in sess:
        up = [r for r in rows if r['session_created'] <= s['created']]
        if not up: continue
        rw, mt, tot = student_estimates(up, s['created'])
        out.append(dict(session_id=s['id'], ts=s['created'], date=datetime.date.fromtimestamp(s['created']).strftime('%b %d'), kind=s['kind'],
                        mode=s['mode'], rw=rw['mid'], math=mt['mid'], lo=tot['lo'], mid=tot['mid'], hi=tot['hi'], n=tot['n']))
    if len(set(t['date'] for t in out)) < len(out):
        for i, t in enumerate(out):
            t['date'] = '%d. %s' % (i + 1, t['date'])
    return out


def dashboard(student_id):
    now = time.time()
    st = db.q('SELECT * FROM students WHERE id=?', (student_id,), one=True)
    rows = db.response_rows(student_id)
    rw, mt, tot = student_estimates(rows, now)
    data = dict(student=dict(st), n=len(rows), rw=rw, math=mt, total=tot, conf=S.confidence_label(len(rows)))
    data['goal'] = st['goal_total'] or 1200
    data['gap'] = data['goal'] - tot['mid']
    data['timeline'] = timeline(student_id)
    # skills
    skills = []
    for sec, est in (('rw', rw), ('math', mt)):
        by = {}
        for r in rows:
            if r['section'] == sec: by.setdefault(r['skill'], []).append(r)
        for t in S.skill_table(by, est['theta'], now):
            meta = SKILLS[t['skill']]
            t.update(name=meta['name'], section=sec, domain=meta['domain'])
            tgt = SEC_TARGET_SEC[sec]
            t['pace'] = None if t['avg_sec'] is None else t['avg_sec'] / tgt
            skills.append(t)
    seen = set(s['skill'] for s in skills)
    data['untried'] = [SKILLS[k]['name'] for k in SKILLS if k not in seen]
    ranked = sorted([s for s in skills if s['n'] >= 4], key=lambda s: s['strength'])
    data['weakest'] = ranked[:3]
    data['strongest'] = [s for s in reversed(ranked[-3:]) if s['strength'] > -0.05] if len(ranked) >= 4 else []
    data['skills'] = sorted(skills, key=lambda s: (s['section'], s['strength']))
    data['improving'] = [s for s in skills if s['trend'] == 'improving']
    data['slipping'] = [s for s in skills if s['trend'] == 'slipping']
    # domains
    dom = []
    for sec in ('rw', 'math'):
        for d in DOMAINS[sec]:
            rr = [r for r in rows if r['section'] == sec and r['domain'] == d]
            if rr: dom.append(dict(section=sec, domain=d, n=len(rr), acc=sum(1 for r in rr if r['correct']) / float(len(rr))))
    data['domains'] = dom
    # habits
    wk = now - 7 * 86400
    data['q_week'] = len([r for r in rows if r['ts'] >= wk])
    weeks = set(int((now - r['session_created']) // (7 * 86400)) for r in rows)
    streak = 0
    while streak in weeks: streak += 1
    data['streak'] = streak
    data['sessions'] = db.q('SELECT COUNT(*) c FROM sessions WHERE student_id=? AND finished IS NOT NULL', (student_id,), one=True)['c']
    pace = {}
    for sec in ('rw', 'math'):
        ts = [r['time_ms'] for r in rows if r['section'] == sec and r['time_ms']]
        if len(ts) >= 10: pace[sec] = sum(ts) / len(ts) / 1000.0 / SEC_TARGET_SEC[sec]
    data['pace'] = pace
    data['summary'] = summary_text(data)
    return data


def _name(s): return s['name']


def summary_text(d):
    """Plain-language paragraph for parents and students. Never claims more certainty than the data supports."""
    nm = d['student']['name'].split(' ')[0]
    if d['n'] < 20:
        return ('%s has answered %d practice questions so far. That is too few for a dependable score estimate, so the range below is deliberately wide. '
                'It will tighten as more sessions are completed.' % (nm, d['n']))
    t = d['total']
    parts = ['Based on %d answered questions, %s\'s current estimate is %d to %d out of 1600 (most likely about %d). The estimate is %s.' % (
        d['n'], nm, t['lo'], t['hi'], t['mid'], d['conf'])]
    gap = d['gap']
    if gap > 20: parts.append('The goal is %d, so roughly %d points remain.' % (d['goal'], gap))
    elif gap < -20: parts.append('That is already above the goal of %d.' % d['goal'])
    else: parts.append('That is right around the goal of %d.' % d['goal'])
    if d['strongest']: parts.append('Strongest areas: %s.' % ', '.join(_name(s) for s in d['strongest'][:2]))
    if d['weakest']: parts.append('Most room to grow: %s. Homework will focus there.' % ', '.join(_name(s) for s in d['weakest'][:2]))
    if d['improving']: parts.append('Improving: %s.' % ', '.join(_name(s) for s in d['improving'][:2]))
    if d['slipping']: parts.append('Worth a refresher: %s.' % ', '.join(_name(s) for s in d['slipping'][:2]))
    sl = [s for s, v in d['pace'].items() if v > 1.25]
    if sl: parts.append('Pacing: %s questions are taking noticeably longer than the real test allows.' % ' and '.join(SECTION_NAME[s] for s in sl))
    return ' '.join(parts)


# ------------------------------------------------------------------ SVG
def svg_ruler(rw, mt, total, goal=None, w=640):
    """Score ranges drawn as highlighter strokes on a ruler. Two rulers: total (400-1600) and each section (200-800)."""
    def row(y, label, lo, mid, hi, mn, mx, goal_v=None):
        x = lambda v: 150 + (v - mn) / float(mx - mn) * (w - 190)
        s = '<text x="0" y="%d" class="rl">%s</text>' % (y + 4, label)
        s += '<line x1="%d" x2="%d" y1="%d" y2="%d" class="rule"/>' % (x(mn), x(mx), y, y)
        step = 200 if mx - mn > 800 else 100
        v = mn
        while v <= mx:
            s += '<line x1="%d" x2="%d" y1="%d" y2="%d" class="tick"/><text x="%d" y="%d" class="tk">%d</text>' % (x(v), x(v), y - 5, y + 5, x(v), y + 20, v)
            v += step
        s += '<rect x="%d" y="%d" width="%d" height="14" class="hl"/>' % (x(lo), y - 7, max(4, x(hi) - x(lo)))
        s += '<line x1="%d" x2="%d" y1="%d" y2="%d" class="mid"/>' % (x(mid), x(mid), y - 12, y + 12)
        if goal_v: s += '<path d="M%d %d l-5 -9 h10 z" class="goal"/>' % (x(goal_v), y - 12)
        return s
    body = row(28, 'Total', total['lo'], total['mid'], total['hi'], 400, 1600, goal)
    body += row(88, 'Reading & Writing', rw['lo'], rw['mid'], rw['hi'], 200, 800)
    body += row(148, 'Math', mt['lo'], mt['mid'], mt['hi'], 200, 800)
    return '<svg viewBox="0 0 %d 180" class="ruler" role="img" aria-label="Estimated score ranges">%s</svg>' % (w, body)


def svg_timeline(tl, goal=None, w=640, h=210):
    if len(tl) < 2:
        return ''
    xs = lambda i: 46 + i * (w - 70) / float(len(tl) - 1)
    lo_v = min(min(t['lo'] for t in tl), goal or 9999) - 40
    hi_v = max(max(t['hi'] for t in tl), goal or 0) + 40
    ys = lambda v: 16 + (hi_v - v) / float(hi_v - lo_v) * (h - 56)
    band = ' '.join('%.1f,%.1f' % (xs(i), ys(t['hi'])) for i, t in enumerate(tl)) + ' ' + ' '.join('%.1f,%.1f' % (xs(i), ys(t['lo'])) for i, t in reversed(list(enumerate(tl))))
    line = ' '.join('%.1f,%.1f' % (xs(i), ys(t['mid'])) for i, t in enumerate(tl))
    s = '<polygon points="%s" class="band"/><polyline points="%s" class="tline"/>' % (band, line)
    for i, t in enumerate(tl):
        s += '<circle cx="%.1f" cy="%.1f" r="3.5" class="dot"><title>%s: %d (range %d-%d)</title></circle>' % (xs(i), ys(t['mid']), t['date'], t['mid'], t['lo'], t['hi'])
        if len(tl) <= 10 or i % 2 == 0: s += '<text x="%.1f" y="%d" class="tk">%s</text>' % (xs(i), h - 8, t['date'])
    if goal: s += '<line x1="40" x2="%d" y1="%.1f" y2="%.1f" class="goalline"/><text x="%d" y="%.1f" class="tkr">goal %d</text>' % (w - 10, ys(goal), ys(goal), w - 10, ys(goal) - 4, goal)
    for v in range(int(lo_v // 100 * 100 + 100), int(hi_v), 100):
        s += '<text x="0" y="%.1f" class="tkl">%d</text>' % (ys(v) + 3, v)
    return '<svg viewBox="0 0 %d %d" class="tl" role="img" aria-label="Projected total score by session">%s</svg>' % (w, h, s)
