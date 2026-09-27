"""Score projection and skill analytics.

IMPORTANT: The College Board does not publish its scoring model. Everything here is an ESTIMATE built from a simple,
transparent item-response model (Rasch with a guessing floor). Treat it as a training signal, and calibrate it against the
student's first official practice test (Bluebook) when available.

Model
  P(correct) = c + (1 - c) * sigmoid(theta - b)     c = 0.25 for multiple choice, 0 for student-produced response
  b = -1.1 / 0 / +1.1 for easy / medium / hard items
  theta gets a Normal(0, 1.2) prior, so with little data the range is wide and it narrows as answers accumulate.
  Recent answers count more (half-life 60 days) so improvement shows up.
  Section score = 500 + 105 * theta, clipped to 200-800, shown as an 80% range.
"""
import math

B = {0: -1.1, 1: 0.0, 2: 1.1}
GRID = [i * 0.05 for i in range(-80, 81)]  # theta from -4 to 4
PRIOR_SD = 1.2
SLOPE = 105.0
HALF_LIFE_DAYS = 60.0


def _sig(x):
    return 1.0 / (1.0 + math.exp(-x))


def p_correct(theta, d, is_mc):
    c = 0.25 if is_mc else 0.0
    return c + (1 - c) * _sig(theta - B[d])


def posterior(resps, prior_mean=0.0, prior_sd=PRIOR_SD):
    """resps: list of (d, is_mc, correct, weight). Returns (mean, sd) of theta on a grid."""
    logp = []
    for t in GRID:
        lp = -0.5 * ((t - prior_mean) / prior_sd) ** 2
        for d, is_mc, ok, w in resps:
            p = p_correct(t, d, is_mc)
            p = min(max(p, 1e-6), 1 - 1e-6)
            lp += w * (math.log(p) if ok else math.log(1 - p))
        logp.append(lp)
    m = max(logp)
    ws = [math.exp(x - m) for x in logp]
    z = sum(ws)
    mean = sum(t * w for t, w in zip(GRID, ws)) / z
    var = sum(((t - mean) ** 2) * w for t, w in zip(GRID, ws)) / z
    return mean, math.sqrt(var), [w / z for w in ws]


def to_score(theta):
    return max(200.0, min(800.0, 500.0 + SLOPE * theta))


def r10(x):
    return int(round(x / 10.0) * 10)


def section_estimate(resps):
    """80% range for one section. Returns dict(lo, mid, hi, n, theta, sd)."""
    n = len(resps)
    mean, sd, wts = posterior(resps)
    acc, lo, hi = 0.0, None, None
    for t, w in zip(GRID, wts):
        acc += w
        if lo is None and acc >= 0.10: lo = t
        if hi is None and acc >= 0.90: hi = t
    return dict(lo=r10(to_score(lo)), mid=r10(to_score(mean)), hi=r10(to_score(hi)), n=n, theta=mean, sd=sd,
                sd_score=sd * SLOPE)


def total_estimate(rw, math_):
    mid = rw['mid'] + math_['mid']
    sd = math.sqrt(rw['sd_score'] ** 2 + math_['sd_score'] ** 2)
    lo = max(400, r10(mid - 1.28 * sd)); hi = min(1600, r10(mid + 1.28 * sd))
    return dict(lo=lo, mid=min(1600, max(400, mid)), hi=hi, n=rw['n'] + math_['n'])


def confidence_label(n):
    if n < 20: return 'very rough'
    if n < 60: return 'rough'
    if n < 150: return 'fairly reliable'
    return 'reliable'


def weighted(rows, now_ts):
    """rows: dicts with d, is_mc, correct, ts. Adds recency weights."""
    out = []
    for r in rows:
        age = max(0.0, (now_ts - r['ts']) / 86400.0)
        out.append((r['d'], r['is_mc'], bool(r['correct']), 0.5 ** (age / HALF_LIFE_DAYS)))
    return out


def skill_table(rows_by_skill, section_theta, now_ts):
    """Per-skill stats, strength index (skill theta minus section theta), and trend."""
    out = []
    for skill, rows in rows_by_skill.items():
        rows = sorted(rows, key=lambda r: r['ts'])
        n = len(rows)
        acc = sum(1 for r in rows if r['correct']) / float(n)
        mean, sd, _ = posterior(weighted(rows, now_ts), prior_mean=section_theta, prior_sd=0.9)
        trend, delta, acc_early, acc_late = 'new', 0.0, None, None
        if n >= 10:
            cut = max(5, int(n * 0.6))
            early, late = rows[:cut], rows[cut:]
            if len(late) >= 5 and len(early) >= 5:
                m1, _, _ = posterior([(r['d'], r['is_mc'], bool(r['correct']), 1.0) for r in early])
                m2, _, _ = posterior([(r['d'], r['is_mc'], bool(r['correct']), 1.0) for r in late])
                delta = m2 - m1
                acc_early = sum(1 for r in early if r['correct']) / float(len(early))
                acc_late = sum(1 for r in late if r['correct']) / float(len(late))
                trend = 'improving' if delta >= 0.35 else ('slipping' if delta <= -0.35 else 'steady')
            else:
                trend = 'steady'
        elif n >= 5:
            trend = 'steady'
        times = [r['time_ms'] for r in rows if r['time_ms']]
        out.append(dict(skill=skill, n=n, acc=acc, theta=mean, sd=sd, strength=mean - section_theta, trend=trend, delta=delta, acc_early=acc_early, acc_late=acc_late,
                        avg_sec=(sum(times) / len(times) / 1000.0) if times else None))
    return out
