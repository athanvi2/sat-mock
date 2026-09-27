"""How many distinct questions each skill can produce at each difficulty (counted by uid, plus the figure when there is one, over many seeds)."""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bank import pool
from bank.skills import SKILLS

print('%-26s %-5s %6s %6s %6s' % ('skill', 'sect', 'easy', 'med', 'hard'))
for k, s in SKILLS.items():
    row = []
    for d in range(3):
        seen = set()
        for seed in range(1, 1500):
            try:
                q = pool.make(k, d, seed, False)
                seen.add(q['uid'] + repr(q.get('figure', '')))  # uids ignore choice order; a different plot is a different question
            except Exception:
                pass
        row.append(len(seen))
    print('%-26s %-5s %6d %6d %6d' % (k, s['section'], row[0], row[1], row[2]))
