"""Checks that the score estimate behaves defensibly. Run:  python tests/score_check.py

Simulated students with a known true ability answer an adaptive diagnostic drawn from the same item model, so this checks
the estimator's internal honesty (is the 80% range right about 80% of the time? is it biased?) and its edge cases. It
cannot check that the model matches the real SAT; that is what entering a real Bluebook/official score is for."""
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scoring as S
from bank.skills import DOMAINS

NOW = time.time()
MIX = {'m1': (.30, .40, .30), 'easy': (.55, .35, .10), 'hard': (.10, .35, .55)}


def draw(rng, theta, sec, n, variant, mode='exam', timed=1, focus='', domain=None, d=None, spr_frac=.25):
    rows = []
    doms = list(DOMAINS[sec].items())
    for _ in range(n):
        dom = domain or rng.choices([k for k, _ in doms], [w for _, w in doms])[0]
        dd = d if d is not None else rng.choices([0, 1, 2], MIX[variant])[0]
        mc = sec == 'rw' or rng.random() > spr_frac
        ok = rng.random() < S.p_correct(theta, dd, mc)
        skill = 'drilled' if focus else '%s-%d' % (dom, rng.randrange(4))
        rows.append(dict(d=dd, is_mc=mc, correct=ok, ts=NOW, mode=mode, timed=timed, focus=focus, domain=dom, skill=skill, time_ms=60000))
    return rows


def adaptive(rng, theta, sec, n):
    m1 = draw(rng, theta, sec, n, 'm1')
    w = {0: 1.0, 1: 1.5, 2: 2.0}
    ratio = sum(w[r['d']] for r in m1 if r['correct']) / sum(w[r['d']] for r in m1)
    return m1 + draw(rng, theta, sec, n, 'hard' if ratio >= .6 else 'easy')


def est(rows, sec, prior=None):
    return S.section_estimate(rows, NOW, DOMAINS[sec], prior)


fails = []


def check(cond, msg):
    print(('ok    ' if cond else 'FAIL  ') + msg)
    if not cond: fails.append(msg)


rng = random.Random(11)
for label, n_mod in (('1-hour diagnostic', 11), ('full-length test', 27)):
    hits = errs = tot = 0
    widths = []
    for _ in range(300):
        th = rng.uniform(-2.0, 2.2)
        e = est(adaptive(rng, th, 'rw', n_mod), 'rw')
        true = S.to_score(th)
        hits += e['lo'] <= true <= e['hi']
        errs += e['mid'] - true; tot += abs(e['mid'] - true)
        widths.append(e['hi'] - e['lo'])
    cov = hits / 300.0
    print('%s: 80%% range contains the true section score %.0f%% of the time, mean error %+.0f, mean |error| %.0f, median width %d'
          % (label, cov * 100, errs / 300.0, tot / 300.0, sorted(widths)[150]))
    check(0.72 <= cov <= 0.93, '%s: coverage close to 80%%' % label)
    check(abs(errs / 300.0) < 25, '%s: no large systematic bias' % label)

# drilling one easy skill must not produce a confident high Math score
drill = draw(rng, 0.0, 'math', 200, 'm1', mode='practice', timed=0, focus='skill', domain='Algebra', d=0)
for r in drill: r['correct'] = True
e = est(drill, 'math')
print('drilling 200 easy Algebra questions, all correct: %d to %d (mid %d), coverage %.2f' % (e['lo'], e['hi'], e['mid'], e['coverage']))
check(e['hi'] - e['lo'] >= 150, 'one-topic drilling leaves a wide range')
check(e['mid'] <= 620, 'one-topic drilling cannot claim a high score (%d)' % e['mid'])
check(e['coverage'] < 0.5, 'coverage reflects the untested domains')

# perfect and chance-level full tests
perfect = adaptive(rng, 5.0, 'math', 22)
for r in perfect: r['correct'] = True
check(est(perfect, 'math')['mid'] >= 740, 'a perfect full-length Math section estimates 740 or more (%d)' % est(perfect, 'math')['mid'])
guess = [dict(r, correct=rng.random() < (.25 if r['is_mc'] else 0)) for r in adaptive(rng, -4, 'math', 22)]
check(est(guess, 'math')['mid'] <= 380, 'random guessing estimates 380 or less (%d)' % est(guess, 'math')['mid'])

# no data
e0 = est([], 'rw')
check(not e0['has_data'] and e0['hi'] - e0['lo'] >= 250, 'no answers: flagged as no data, range very wide')

# prior scores
recent = dict(test='SAT', rw=650, math=620, taken_ts=NOW - 30 * 86400)
old = dict(test='PSAT/NMSQT', rw=650, math=620, taken_ts=NOW - 24 * 30.4 * 86400)
pr, po = S.prior_from_scores([recent], 'rw', NOW), S.prior_from_scores([old], 'rw', NOW)
er, eo = est([], 'rw', pr), est([], 'rw', po)
print('prior only: SAT last month %d to %d; PSAT two years ago %d to %d' % (er['lo'], er['hi'], eo['lo'], eo['hi']))
check(abs(er['mid'] - 650) <= 10 and er['hi'] - er['lo'] <= 110, 'recent SAT anchors the estimate tightly')
check(eo['hi'] - eo['lo'] > er['hi'] - er['lo'], 'an older PSAT anchors it more loosely')
avg = sum(est(adaptive(rng, S.to_theta(500), 'rw', 27), 'rw', po)['mid'] for _ in range(30)) / 30.0
check(avg < 560, 'full tests at the 500 level pull an old 650 PSAT prior down (average %d)' % avg)

# recency: a big improvement 4 months ago vs. now
def mixed_history():
    old_rows = [dict(r, ts=NOW - 150 * 86400) for r in adaptive(rng, -1.0, 'rw', 27)]
    return est(old_rows + adaptive(rng, 1.0, 'rw', 27), 'rw')['mid']
avg = sum(mixed_history() for _ in range(30)) / 30.0
check(avg > S.to_score(0.4), 'a 395-level test 5 months ago counts far less than a 605-level test today (average %d)' % avg)

# total
t = S.total_estimate(est(adaptive(rng, 0.5, 'rw', 27), 'rw'), est(adaptive(rng, 0.5, 'math', 22), 'math'))
check(t['lo'] <= t['mid'] <= t['hi'] and 400 <= t['lo'] and t['hi'] <= 1600, 'total range is ordered and on the 400-1600 scale')
check(not S.total_estimate(e0, est(perfect, 'math'))['has_data'], 'total is not shown when one section has no data')

print('\n%s' % ('ALL SCORE CHECKS PASSED' if not fails else '%d FAILED' % len(fails)))
sys.exit(1 if fails else 0)
