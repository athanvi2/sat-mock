"""Score projection and skill analytics.

IMPORTANT: The College Board does not publish its scoring model. Everything here is an ESTIMATE built from a simple,
transparent item-response model (Rasch with a guessing floor). Treat it as a training signal. The strongest anchor it can
have is a real score: an official SAT/PSAT or a Bluebook practice test entered as a prior score (see `prior_from_scores`).

Model
  P(correct) = c + (1 - c) * sigmoid(theta - b)     c = 0.25 for multiple choice, 0 for student-produced response
  b = -1.1 / 0 / +1.1 for easy / medium / hard items (difficulty labels are author judgments, not measured)
  Section score = 500 + 105 * theta, clipped to 200-800, reported as an 80% range.

What goes into an estimate, and why (each rule is a guard against a specific way the number could mislead):
  1. First attempts only. A second try after a hint, or anything after an answer was revealed, is never scored.
  2. Blanks in a submitted TIMED module count as wrong, as on the real test. Otherwise skipping hard questions would
     raise the estimate. Blanks in untimed practice are questions not reached and are left out (db.response_rows).
  3. Recency: weight halves every 60 days, so improvement shows up and old habits fade.
  4. Context weights: untimed practice x0.7 (no time pressure inflates accuracy), skill- or domain-focused practice
     x0.6 (a student drilling one topic is warmed up on it). Paper homework entered afterwards x0.5 (no clock, notes and
     help may be at hand, and answers are typed in after the fact), on top of the x0.6 for being on one skill.
  5. Domain balance: if one content domain makes up more of the evidence than it does of the real test, its answers
     are scaled down to its official share. Drilling linear equations cannot stand in for a whole Math score.
  5b. Per-skill cap: at most 12 answers' worth of evidence per skill. Questions on one skill are strongly correlated
     (same idea, same traps), so the 200th linear-equation question says little the 12th did not.
  6. Coverage: domains with little or no evidence add uncertainty (their ability could differ from the rest by about
     half a standard deviation), so the range widens instead of pretending to know.
  7. Prior: with no earlier score, theta ~ Normal(0, 1.2) (a wide, population-level guess). With an earlier official or
     Bluebook score, the prior is centred on that score with its measurement error (about 30 points per section) plus
     drift for the time since the test (about 25 points per 6 months), so an old PSAT matters less than last month's SAT.
"""
import math

B = {0: -1.1, 1: 0.0, 2: 1.1}
GRID = [i * 0.05 for i in range(-80, 81)]  # theta from -4 to 4
PRIOR_SD = 1.2
SLOPE = 105.0
HALF_LIFE_DAYS = 60.0
W_UNTIMED, W_FOCUSED, W_HOMEWORK = 0.7, 0.6, 0.5
DOMAIN_SD = 0.5          # how far one domain's ability can sit from the section's, in theta units
DOMAIN_FULL_N = 4.0      # effective answers in a domain before it counts as covered
SKILL_CAP = 12.0         # most evidence one skill can contribute to a section estimate
PRIOR_SEM = 0.3          # measurement error of an official section score (~30 points), in theta units
PRIOR_DRIFT_6MO = 0.25   # added uncertainty per 6 months since that score
Z80 = 1.2816


def _sig(x):
    return 1.0 / (1.0 + math.exp(-x))


def p_correct(theta, d, is_mc):
    c = 0.25 if is_mc else 0.0
    return c + (1 - c) * _sig(theta - B[d])


def posterior(resps, prior_mean=0.0, prior_sd=PRIOR_SD):
    """resps: list of (d, is_mc, correct, weight). Returns (mean, sd, grid weights) of theta."""
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


def to_theta(score):
    return (score - 500.0) / SLOPE


def r10(x):
    return int(round(x / 10.0) * 10)


# ------------------------------------------------------------------ evidence weighting
def row_weight(r, now_ts):
    """Recency x context weight for one response row (see module docstring, rules 3-4)."""
    age = max(0.0, (now_ts - r['ts']) / 86400.0)
    w = 0.5 ** (age / HALF_LIFE_DAYS)
    if r.get('mode') == 'practice' and not r.get('timed', 1): w *= W_UNTIMED
    if r.get('mode') == 'homework': w *= W_HOMEWORK
    if r.get('focus'): w *= W_FOCUSED
    return w


def balanced(rows, now_ts, domain_share):
    """Weighted evidence with over-represented domains scaled to their official share (rule 5).
    Returns (resps, effective answers per domain)."""
    ws = [row_weight(r, now_ts) for r in rows]
    per_skill = {}
    for r, w in zip(rows, ws): per_skill[r.get('skill')] = per_skill.get(r.get('skill'), 0.0) + w
    ws = [w * min(1.0, SKILL_CAP / per_skill[r.get('skill')]) for r, w in zip(rows, ws)]
    tot = sum(ws)
    by_dom = {}
    for r, w in zip(rows, ws): by_dom[r['domain']] = by_dom.get(r['domain'], 0.0) + w
    scale = {}
    for dom, w in by_dom.items():
        obs = w / tot if tot else 0.0
        tgt = domain_share.get(dom, 0.0)
        scale[dom] = min(1.0, tgt / obs) if obs > 0 else 1.0
    resps, eff = [], {}
    for r, w in zip(rows, ws):
        w2 = w * scale[r['domain']]
        resps.append((r['d'], bool(r['is_mc']), bool(r['correct']), w2))
        eff[r['domain']] = eff.get(r['domain'], 0.0) + w2
    return resps, eff


def coverage_var(eff, domain_share):
    """Extra theta variance for domains the evidence does not cover (rule 6). Also returns covered share (0-1)."""
    extra, covered = 0.0, 0.0
    for dom, share in domain_share.items():
        c = min(1.0, eff.get(dom, 0.0) / DOMAIN_FULL_N)
        extra += (share ** 2) * (1 - c) * DOMAIN_SD ** 2
        covered += share * c
    return extra, covered


def prior_from_scores(scores, section, now_ts):
    """(mean, sd) prior on theta from earlier real scores, or None. Uses the most informative single score (smallest sd)
    rather than averaging, because older scores describe a student who has since studied."""
    best = None
    for s in scores:
        val = s.get(section)
        if not val: continue
        months = max(0.0, (now_ts - s['taken_ts']) / (86400 * 30.4))
        extra = 0.1 if s['test'].startswith('PSAT') else 0.0  # PSAT is a shorter test on the same scale
        sd = math.sqrt(PRIOR_SEM ** 2 + (PRIOR_DRIFT_6MO * months / 6.0) ** 2 + extra ** 2)
        sd = min(sd, PRIOR_SD)
        if best is None or sd < best[1]:
            best = (to_theta(val), sd, s)
    return best


# ------------------------------------------------------------------ estimates
def section_estimate(rows, now_ts, domain_share, prior=None):
    """80% range for one section from response rows (dicts from db.response_rows).
    prior: (mean, sd, score_row) from prior_from_scores, or None.
    Returns dict(lo, mid, hi, n, n_eff, theta, sd, sd_score, coverage, has_data, prior_used)."""
    resps, eff = balanced(rows, now_ts, domain_share)
    pm, psd = (prior[0], prior[1]) if prior else (0.0, PRIOR_SD)
    mean, sd, wts = posterior(resps, pm, psd)
    lo = hi = None
    acc = 0.0
    for t, w in zip(GRID, wts):
        acc += w
        if lo is None and acc >= 0.10: lo = t
        if hi is None and acc >= 0.90: hi = t
    extra, covered = coverage_var(eff, domain_share)
    if prior:  # a real score already describes the whole section, so missing domains add less
        extra *= 0.35
    k = math.sqrt(1 + extra / max(sd * sd, 1e-9))
    lo, hi = mean - (mean - lo) * k, mean + (hi - mean) * k
    sd_tot = math.sqrt(sd * sd + extra)
    n_eff = sum(w for _, _, _, w in resps)
    return dict(lo=r10(to_score(lo)), mid=r10(to_score(mean)), hi=r10(to_score(hi)), n=len(rows), n_eff=n_eff, theta=mean,
                sd=sd_tot, sd_score=sd_tot * SLOPE, coverage=covered, has_data=bool(prior) or n_eff >= 8,
                prior_used=prior[2] if prior else None)


def total_estimate(rw, math_):
    """Section errors are independent given the data, so their variances add."""
    mid = rw['mid'] + math_['mid']
    sd = math.sqrt(rw['sd_score'] ** 2 + math_['sd_score'] ** 2)
    lo = max(400, r10(mid - Z80 * sd)); hi = min(1600, r10(mid + Z80 * sd))
    return dict(lo=lo, mid=min(1600, max(400, mid)), hi=hi, n=rw['n'] + math_['n'], sd_score=sd,
                has_data=rw['has_data'] and math_['has_data'])


def confidence_label(est, scale=1200):
    """Plain-language confidence from the actual width of the 80% range, not a raw answer count.
    scale: 1200 for a total (400-1600), 600 for a section (200-800)."""
    rel = (est['hi'] - est['lo']) / float(scale)
    if rel > 0.40: return 'very rough'
    if rel > 0.25: return 'rough'
    if rel > 0.15: return 'fairly reliable'
    return 'reliable'


# ------------------------------------------------------------------ per-skill
def mastery(theta, n):
    """Absolute level on a skill: chance of getting a MEDIUM question right without guessing."""
    if n < 5: return 'not enough data'
    p = _sig(theta - B[1])
    if p >= 0.80 and n >= 8: return 'mastered'
    if p >= 0.62: return 'solid'
    if p >= 0.40: return 'developing'
    return 'needs work'


def skill_table(rows_by_skill, section_theta, now_ts):
    """Per-skill stats, strength (skill theta minus section theta), absolute mastery, and trend."""
    out = []
    for skill, rows in rows_by_skill.items():
        rows = sorted(rows, key=lambda r: r['ts'])
        n = len(rows)
        acc = sum(1 for r in rows if r['correct']) / float(n)
        resps = [(r['d'], bool(r['is_mc']), bool(r['correct']), row_weight(r, now_ts)) for r in rows]
        mean, sd, _ = posterior(resps, prior_mean=section_theta, prior_sd=0.9)
        trend, delta, acc_early, acc_late = 'new', 0.0, None, None
        if n >= 10:
            cut = max(5, int(n * 0.6))
            early, late = rows[:cut], rows[cut:]
            if len(late) >= 5 and len(early) >= 5:
                m1, s1, _ = posterior([(r['d'], bool(r['is_mc']), bool(r['correct']), 1.0) for r in early], section_theta, 0.9)
                m2, s2, _ = posterior([(r['d'], bool(r['is_mc']), bool(r['correct']), 1.0) for r in late], section_theta, 0.9)
                delta = m2 - m1
                acc_early = sum(1 for r in early if r['correct']) / float(len(early))
                acc_late = sum(1 for r in late if r['correct']) / float(len(late))
                # a change only counts when it is bigger than the noise in the two halves
                noise = math.sqrt(s1 * s1 + s2 * s2)
                trend = 'improving' if delta >= max(0.35, noise) else ('slipping' if delta <= -max(0.35, noise) else 'steady')
            else:
                trend = 'steady'
        elif n >= 5:
            trend = 'steady'
        times = [r['time_ms'] for r in rows if r['time_ms'] and not r.get('omitted')]
        out.append(dict(skill=skill, n=n, acc=acc, theta=mean, sd=sd, strength=mean - section_theta, trend=trend, delta=delta,
                        acc_early=acc_early, acc_late=acc_late, mastery=mastery(mean, n), p_medium=_sig(mean - B[1]),
                        hints=sum(1 for r in rows if r.get('hint_used')),
                        avg_sec=(sum(times) / len(times) / 1000.0) if times else None))
    return out


def target_mix(theta, target=0.7, spread=0.15):
    """Easy/medium/hard weights that keep expected accuracy near `target` (the zone where practice is hard enough to
    teach but not so hard it discourages). Used for 'auto' difficulty and recommended practice."""
    w = {}
    for d in (0, 1, 2):
        p = _sig(theta - B[d])
        w[d] = math.exp(-((p - target) / spread) ** 2) + 0.05
    s = sum(w.values())
    return {d: v / s for d, v in w.items()}
