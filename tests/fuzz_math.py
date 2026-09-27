import sys, random, traceback
sys.path.insert(0, '.')
from bank.math_gen import GEN
bad = 0
for k, g in GEN.items():
    for d in range(3):
        for spr in (False, True):
            for seed in range(1500):
                r = random.Random(seed * 7 + d)
                try:
                    q = g(r, d, spr)
                    assert q.get('q') and q.get('expl') and q.get('type') in ('mc', 'spr', 'scatter'), 'missing fields'
                    if q['type'] == 'mc': assert len(q['choices']) == 4 and q['answer'] in 'ABCD'
                except Exception as e:
                    bad += 1
                    if bad <= 12: print(k, d, spr, seed, repr(e)[:150])
print('failures:', bad)
