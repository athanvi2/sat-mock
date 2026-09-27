"""Question factory. A question is fully determined by (skill, difficulty, seed, spr) so any question can be rebuilt,
but the app also stores the built question JSON with each session so old sessions never change."""
import hashlib
import random

from bank.skills import SKILLS, DOMAINS
from bank import math_gen, rw_gen

GEN = {}
GEN.update(rw_gen.GEN)
GEN.update(math_gen.GEN)

DOMAIN_ORDER = {
    'rw': ['Craft and Structure', 'Information and Ideas', 'Standard English Conventions', 'Expression of Ideas'],
    'math': ['Algebra', 'Advanced Math', 'Problem-Solving and Data Analysis', 'Geometry and Trigonometry'],
}
# share of easy / medium / hard in each kind of module (module 1 is broad, module 2 targets the student)
MIX = {'m1': (.30, .40, .30), 'easy': (.55, .35, .10), 'hard': (.10, .35, .55)}
VARIANT_LABEL = {'m1': 'Module 1', 'easy': 'Module 2 (easier)', 'hard': 'Module 2 (harder)'}
# official pacing (seconds per question) from the test specification
OFFICIAL = {'rw': dict(n=27, minutes=32), 'math': dict(n=22, minutes=35)}
OFFICIAL_TOTAL_MIN = 134.0


def apportion(total, weights):
    """Largest-remainder split of `total` by weights (dict name->weight)."""
    s = float(sum(weights.values()))
    raw = {k: total * v / s for k, v in weights.items()}
    out = {k: int(v) for k, v in raw.items()}
    left = total - sum(out.values())
    for k in sorted(raw, key=lambda k: raw[k] - out[k], reverse=True)[:left]:
        out[k] += 1
    return out


def make(skill, d, seed, spr=False):
    r = random.Random(seed)
    q = GEN[skill](r, d, spr)
    s = SKILLS[skill]
    q.update(skill=skill, d=d, seed=seed, section=s['section'], domain=s['domain'], skill_name=s['name'])
    q.setdefault('passage', '')
    if 'uid' not in q:
        # order-independent: the same question with its choices shuffled is the same question
        key = q['q'] + '|' + ('|'.join(sorted(q['choices'])) if q.get('choices') else str(q.get('answer')))
        q['uid'] = 'm:' + hashlib.md5(key.encode('utf-8')).hexdigest()[:12]
    return q


RETIRED = set()  # uids the tutor took out of use (db.retired, loaded by app.py); never given again


def make_safe(skill, d, seed, spr, avoid, hard=None):
    """Build a question whose uid is not in `avoid` (soft: given recently) and never in `hard` (already in this set).
    `avoid` may be a set, or a dict {uid: when last given} (db.seen_uids). Order of preference:
      1. a fresh question at the requested difficulty;
      2. a fresh question at the nearest other difficulty (thin hand-written skills run dry at one level long before all
         three; its level is scored as it is, while a repeat overstates what the student knows);
      3. a recently given question at the requested difficulty, the one given LONGEST ago;
      4. anything at another difficulty that does not repeat inside this set."""
    hard = hard or set()
    when = avoid.get if isinstance(avoid, dict) else (lambda u: 0)
    seen, last = {}, None
    for d2 in sorted([0, 1, 2], key=lambda x: (abs(x - d), x)):
        for k in range(60 if d2 == d else 30):
            try:
                q = make(skill, d2, seed + k * (7919 if d2 == d else 104729), spr)
            except Exception:
                continue
            last = last or q
            if q['uid'] in hard or q['uid'] in RETIRED:
                continue
            if q['uid'] not in avoid:
                return q
            if d2 == d:
                seen.setdefault(q['uid'], q)
    if seen:
        return min(seen.values(), key=lambda q: when(q['uid']) or 0)
    for d2 in sorted(set([0, 1, 2]) - set([d]), key=lambda x: abs(x - d)):
        for k in range(20):
            try:
                q = make(skill, d2, seed + k * 104729, spr)
            except Exception:
                continue
            if q['uid'] not in hard and q['uid'] not in RETIRED:
                return q
    if last is None:
        raise RuntimeError('could not build a question for %s' % skill)
    return last


def build_module(section, n, variant='m1', rng=None, avoid=None, focus=None, diff=None, spr_frac=.25, mix=None, hard=None):
    """Return a list of n built questions ordered like the real test (by domain, easy to hard within a domain).
    focus: None, ('domain', name), ('skill', key) or ('skills', [keys]). diff: None (use variant mix) or 0/1/2 to force
    one level. mix: optional {0: w, 1: w, 2: w} difficulty weights (overrides the variant mix, e.g. matched to level).
    avoid: uids to prefer not to reuse (recent history). hard: uids that must not repeat (this session)."""
    rng = rng or random.Random()
    avoid = avoid if isinstance(avoid, dict) else set(avoid or [])
    hard = set(hard or [])
    if focus and focus[0] == 'skill':
        slots = [focus[1]] * n
    elif focus and focus[0] == 'skills':
        keys = list(focus[1])
        slots = [keys[i % len(keys)] for i in range(n)]
    elif focus and focus[0] == 'domain':
        pool = [k for k, s in SKILLS.items() if s['section'] == section and s['domain'] == focus[1]]
        slots = [pool[i % len(pool)] for i in range(n)]
        rng.shuffle(pool)
    else:
        slots = []
        for dom, cnt in apportion(n, DOMAINS[section]).items():
            pool = [k for k, s in SKILLS.items() if s['section'] == section and s['domain'] == dom]
            rng.shuffle(pool)
            slots += [pool[i % len(pool)] for i in range(cnt)]
    if diff is None:
        m = mix or {0: MIX[variant][0], 1: MIX[variant][1], 2: MIX[variant][2]}
        c = apportion(n, {0: m[0], 1: m[1], 2: m[2]})
        dl = [0] * c[0] + [1] * c[1] + [2] * c[2]
    else:
        dl = [diff] * n
    rng.shuffle(dl)
    spr_n = int(round(n * spr_frac)) if section == 'math' else 0
    spr_flags = [True] * spr_n + [False] * (n - spr_n)
    rng.shuffle(spr_flags)
    out = []
    for sk, d, sp in zip(slots, dl, spr_flags):
        q = make_safe(sk, d, rng.randrange(1, 10 ** 9), sp, avoid, hard)
        hard.add(q['uid'])
        out.append(q)
    order = DOMAIN_ORDER[section]
    out.sort(key=lambda q: (order.index(q['domain']), q['d']))
    return out


def mock_plan(minutes=55.0):
    """Compress the official 98-question, 134-minute test to fit `minutes` while keeping the per-question pace,
    the two-module structure, and the domain weights. Returns per-section module size and time limit."""
    f = float(minutes) / OFFICIAL_TOTAL_MIN
    plan = {}
    for sec, o in OFFICIAL.items():
        n = max(6, int(round(o['n'] * f)))
        sec_per_q = o['minutes'] * 60.0 / o['n']
        plan[sec] = dict(n=n, limit=int(round(n * sec_per_q)))
    plan['f'] = f
    plan['total_min'] = round(2 * (plan['rw']['limit'] + plan['math']['limit']) / 60.0, 1)
    return plan


def full_plan():
    plan = {sec: dict(n=o['n'], limit=o['minutes'] * 60) for sec, o in OFFICIAL.items()}
    plan['f'] = 1.0
    plan['total_min'] = OFFICIAL_TOTAL_MIN
    return plan


def session_plan(minutes_for_session, section):
    """Practice length that fits a time slot at official pace (e.g. 30 minutes)."""
    o = OFFICIAL[section]
    sec_per_q = o['minutes'] * 60.0 / o['n']
    n = max(5, int(round(minutes_for_session * 60 / sec_per_q)))
    return dict(n=min(n, o['n']), limit=int(round(min(n, o['n']) * sec_per_q)))
