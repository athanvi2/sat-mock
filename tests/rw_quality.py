"""Test-wiseness check for authored Reading & Writing items. Run:  python tests/rw_quality.py

A student should not be able to score well by picking the longest (or shortest) choice. For each skill this reports how
often the correct choice is the longest and the shortest; with four choices chance is 25%. Fails if the correct answer
is the longest or the shortest more than 40% of the time in any skill (or at either extreme less than 30%), or if any item has duplicate choices.
Pass -v to list the items where the correct choice is much longer than every wrong one."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bank.rw_gen import RECS

LIMIT = 0.40
MIN_EXTREME = 0.30  # chance is 0.50
verbose = '-v' in sys.argv


def plain(t):
    return re.sub(r'&[a-z]+;', 'x', re.sub(r'<[^>]+>', '', t))


bad = []
for skill, recs in sorted(RECS.items()):
    longest = shortest = 0
    for i, x in enumerate(recs):
        lens = [len(plain(x['ans'][0]))] + [len(plain(w[0])) for w in x['wrongs']]
        texts = [x['ans'][0]] + [w[0] for w in x['wrongs']]
        if len(set(texts)) < 4: bad.append('%s #%d has duplicate choices' % (skill, i))
        if lens[0] == max(lens): longest += 1
        if lens[0] == min(lens): shortest += 1
        if verbose and lens[0] > 1.25 * max(lens[1:]):
            print('  %s #%d (d=%d): correct %d chars vs longest wrong %d' % (skill, i, x['d'], lens[0], max(lens[1:])))
    n = float(len(recs))
    flag = longest / n > LIMIT or shortest / n > LIMIT
    print('%-24s %3d items   correct is longest %3d%%   shortest %3d%%%s' % (skill, len(recs), 100 * longest / n, 100 * shortest / n, '   <-- a length giveaway' if flag else ''))
    if longest / n > LIMIT: bad.append('%s: correct answer is the longest choice %d%% of the time' % (skill, 100 * longest / n))
    if shortest / n > LIMIT: bad.append('%s: correct answer is the shortest choice %d%% of the time' % (skill, 100 * shortest / n))
    if (longest + shortest) / n < MIN_EXTREME:  # never at either extreme: "rule out the longest and shortest" becomes a strategy
        bad.append('%s: correct answer is almost never the longest or shortest (%d%%)' % (skill, 100 * (longest + shortest) / n))

print('\n' + ('OK' if not bad else 'FAIL\n' + '\n'.join(bad)))
sys.exit(1 if bad else 0)
