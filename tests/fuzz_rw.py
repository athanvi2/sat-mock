import sys, random
sys.path.insert(0, '.')
from bank.rw_gen import GEN
from bank.skills import SKILLS
missing = [k for k, s in SKILLS.items() if s['section'] == 'rw' and k not in GEN]
print('missing RW gens:', missing)
bad = 0
for k, g in GEN.items():
    uids = set()
    for d in range(3):
        for seed in range(300):
            r = random.Random(seed * 13 + d)
            try:
                q = g(r, d, False)
                assert q['q'] and q['expl'] and len(q['choices']) == 4 and q['answer'] in 'ABCD' and len(set(q['choices'])) == 4
                uids.add(q['uid'])
            except Exception as e:
                bad += 1
                if bad < 15: print(k, d, seed, repr(e)[:160])
    print('%-24s unique items seen: %d' % (k, len(uids)))
print('failures:', bad)
