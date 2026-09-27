"""Checks that the calendar follows the rules it tells parents it follows (planner.RULES). Run:  python tests/plan_check.py
Uses /tmp/plan_check.db, never the real student database."""
import datetime, json, os, sys, time
os.environ['SAT_DB'] = '/tmp/plan_check.db'
if os.path.exists('/tmp/plan_check.db'): os.remove('/tmp/plan_check.db')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db, planner, auth
from bank.skills import SKILLS

db.init()
fails = []


def check(cond, msg):
    print(('ok    ' if cond else 'FAIL  ') + msg)
    if not cond: fails.append(msg)


def student(name, **kw):
    sid = db.x('INSERT INTO students(name, pin_hash, goal_total, created, onboard, test_date) VALUES (?,?,?,?,?,?)',
               (name, auth.hash_pin('1234'), 1300, time.time(), kw.get('onboard', 'new'), kw.get('test_date')))
    return sid


def future(pl, today, kinds=None):
    return [i for i in pl['items'] if i['day'] >= today and i['status'] == 'planned' and (kinds is None or i['kind'] in kinds)]


today = datetime.date(2026, 9, 28)  # a Monday; the next Sundays are Oct 4, 11, 18, 25 and Nov 1 (Nov 29 is a 5th Sunday)

# 1. no starting point: the diagnostic comes first
a = student('New Student')
pl = planner.plan(a, today)
first = future(pl, today)[0]
check(first['kind'] == 'diagnostic' and first['day'] == datetime.date(2026, 10, 4), 'with no starting point, the next Sunday is the diagnostic')

# 2. with a starting point: lessons with reasons, homework on the Wednesday after, section balance, 5th-Sunday mock
b = student('Scored Student', onboard='prior')
db.x('INSERT INTO prior_scores(student_id, test, rw, math, taken, created) VALUES (?,?,?,?,?,?)', (b, 'SAT', 520, 540, '2026-06-06', time.time()))
pl = planner.plan(b, today)
lessons = future(pl, today, ('lesson',))
check(len(lessons) >= 5, 'a starting point produces a run of lessons (%d)' % len(lessons))
check(all('Priority #' in l['why'] for l in lessons), 'every lesson states its priority and why')
hw = dict((i['day'], i) for i in future(pl, today, ('homework',)))
check(all((l['day'] + datetime.timedelta(days=3)) in hw for l in lessons if l['day'] + datetime.timedelta(days=3) <= pl['end']), 'homework lands on the Wednesday after each lesson')
secs = [SKILLS[l['skill']]['section'] for l in lessons]
check(all(not (secs[i] == secs[i + 1] == secs[i + 2]) for i in range(len(secs) - 2)), 'never three lessons in a row on one section %s' % secs)
later = datetime.date(2026, 10, 5)  # its 8-week window reaches the 5th Sunday of November (Nov 29)
mocks = [i['day'] for i in future(planner.plan(b, later), later, ('mock',))]
check(datetime.date(2026, 11, 29) in mocks, 'the 5th Sunday of November is a practice test')
check(all(((d.day - 1) // 7 + 1) == 5 for d in mocks), 'practice tests land only on 5th Sundays')
check(len(set(l['skill'] for l in lessons[:3])) == 3, 'the first three lessons are three different skills (the plan moves on)')

# 3. a test date: full-length test 8-14 days out, light review in the final week, nothing new after
c = student('Test Soon', onboard='prior', test_date=(today + datetime.timedelta(days=20)).isoformat())
db.x('INSERT INTO prior_scores(student_id, test, rw, math, taken, created) VALUES (?,?,?,?,?,?)', (c, 'PSAT 8/9', 480, 470, '2026-03-01', time.time()))
pl = planner.plan(c, today)
tday = today + datetime.timedelta(days=20)
full = future(pl, today, ('fullmock',)); rev = future(pl, today, ('review',)); sat = future(pl, today, ('sat',))
check(len(full) == 1 and 8 <= (tday - full[0]['day']).days <= 14, 'one full-length test 8-14 days before the SAT')
check(len(rev) == 1 and 0 < (tday - rev[0]['day']).days <= 7, 'light review in the final week')
check(sat and sat[0]['day'] == tday, 'the SAT itself is on the calendar')
check(not [l for l in future(pl, today, ('lesson',)) if (tday - l['day']).days <= 14], 'no new lessons in the last two weeks')
check(pl['end'] == tday, 'the plan runs to the test date')
check([i['kind'] for i in pl['items'] if i['day'] == tday] == ['sat'], 'test day holds only the SAT (it falls on a Sunday here)')

# 4. a "no session" Sunday: no lesson that day, and the lesson sequence moves forward
before = [(l['day'], l['title']) for l in future(planner.plan(b, today), today, ('lesson',))]
db.x('INSERT INTO events(student_id, day, kind, title, note, created) VALUES (?,?,?,?,?,?)', (b, '2026-10-11', 'skip', 'Trip', '', time.time()))
after = [(l['day'], l['title']) for l in future(planner.plan(b, today), today, ('lesson',))]
check(not [x for x in after if x[0] == datetime.date(2026, 10, 11)], 'no lesson on a skipped Sunday')
check(after[1][1] == before[1][1] and after[1][0] == datetime.date(2026, 10, 18), 'the skipped lesson moves to the next Sunday')

# 5. what changed: compare with an earlier day's saved plan
db.x('DELETE FROM plan_snapshots WHERE student_id=?', (b,))
old = [dict(day='2026-10-04', kind='lesson', title='Something Else Entirely')]
db.x('INSERT INTO plan_snapshots(student_id, day, plan_json) VALUES (?,?,?)', (b, '2026-09-20', json.dumps(old)))
pl = planner.plan(b, today)
ch = pl['changes']
check(ch and ch['since'] == datetime.date(2026, 9, 20) and ch['items'] and ch['items'][0]['before'] == 'Something Else Entirely',
      'a changed lesson is reported with before and after')
check(ch['items'][0]['why'].startswith('Priority #'), 'the change carries the new reason')

# 6. past sessions show up as done
sid = db.x('INSERT INTO sessions(student_id, mode, kind, label, plan_json, created, finished, assist, purpose) VALUES (?,?,?,?,?,?,?,?,?)',
           (b, 'practice', 'x', 'Math Module 1', '{}', time.mktime(datetime.date(2026, 9, 20).timetuple()) + 3600,
            time.mktime(datetime.date(2026, 9, 20).timetuple()) + 5400, 'end', ''))
pl = planner.plan(b, today)
check([i for i in pl['items'] if i.get('session_id') == sid and i['status'] == 'done'], 'finished sessions appear as done on their day')
grid = planner.month_grid(2026, 10, pl['items'], today)
check(all(len(w) == 7 for w in grid) and grid[0][0]['day'].weekday() == 6, 'month grid is whole weeks starting on Sunday')

print('\n%s' % ('ALL PLAN CHECKS PASSED' if not fails else '%d FAILED' % len(fails)))
sys.exit(1 if fails else 0)
