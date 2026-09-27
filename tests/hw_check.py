"""Checks the Desktop homework folders (hwsync.py) against a temporary folder. Run:  python tests/hw_check.py
Needs Chrome for PDF output; skips (exit 0) if none is installed. Never touches the real Desktop or database."""
import datetime, glob, json, os, shutil, sys, tempfile, time
TMP = tempfile.mkdtemp(prefix='hwcheck-')
os.environ['SAT_DB'] = os.path.join(TMP, 'hw.db')
os.environ['HW_ROOT'] = os.path.join(TMP, 'Desktop')
os.makedirs(os.environ['HW_ROOT'])
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app as A, auth, db, hwsync, pdfout

if not pdfout.available():
    print('SKIPPED: no Chrome for PDF export'); sys.exit(0)
fails = []


def check(cond, msg):
    print(('ok    ' if cond else 'FAIL  ') + msg)
    if not cond: fails.append(msg)


def top(d): return sorted(f for f in os.listdir(d) if f.endswith('.pdf'))
def hist(d): return sorted(os.listdir(os.path.join(d, 'History')))


today = datetime.date(2026, 9, 28)  # Monday; lessons Sun Oct 4, 11, 18...; homework Wed Oct 7, 14, 21...
sid = db.x('INSERT INTO students(name, pin_hash, goal_total, created, onboard) VALUES (?,?,?,?,?)', ('Sam Rivera', auth.hash_pin('1234'), 1300, time.time(), 'prior'))
db.x('INSERT INTO prior_scores(student_id, test, rw, math, taken, created) VALUES (?,?,?,?,?,?)', (sid, 'SAT', 520, 540, '2026-06-06', time.time()))
none = db.x('INSERT INTO students(name, pin_hash, goal_total, created, onboard) VALUES (?,?,?,?,?)', ('New Kid', auth.hash_pin('1234'), 1200, time.time(), 'new'))

# a student with no starting point has no homework and gets no folder
r = hwsync.sync_student(A.app, none, today)
check(r['ok'] and not os.path.exists(os.path.join(os.environ['HW_ROOT'], 'New_Kid_HW')), 'no folder before the calendar has homework')

# first sync: this week's sheet, plus a time-stamped History entry with the sheet and its answer key
r = hwsync.sync_student(A.app, sid, today)
d = os.path.join(os.environ['HW_ROOT'], 'Sam_Rivera_HW')
check(os.path.isdir(d) and r['ok'], 'folder created on the Desktop root: %s' % os.path.basename(d))
check(len(top(d)) == 1 and top(d)[0].startswith('Homework - due Wed Oct 7 - '), 'one current sheet, due Wed Oct 7: %s' % top(d))
h = hist(d)
check(len(h) == 1 and ' at ' in h[0] and len(os.listdir(os.path.join(d, 'History', h[0]))) == 2, 'History has a time-stamped folder with sheet and key')
with open(os.path.join(d, top(d)[0]), 'rb') as fh: check(fh.read(4) == b'%PDF', 'the sheet is a real PDF')
first = top(d)[0]

# unchanged plan: nothing regenerated
r = hwsync.sync_student(A.app, sid, today)
check(top(d) == [first] and len(hist(d)) == 1 and r['message'] == 'Up to date.', 'unchanged plan makes no new sheet')

# the plan changes: a "no session" Sunday moves the lesson, so this week's homework changes
db.x('INSERT INTO events(student_id, day, kind, title, note, created) VALUES (?,?,?,?,?,?)', (sid, '2026-10-04', 'skip', 'Trip', '', time.time()))
time.sleep(1)
r = hwsync.sync_student(A.app, sid, today)
check(first not in top(d) and len(top(d)) == 1 and 'due Wed Oct 14' in top(d)[0], 'plan change replaces the sheet (now due Oct 14): %s' % top(d))
check(len(hist(d)) == 2 and any('Oct 7' in x for x in hist(d)), 'the replaced sheet stays in History')
check('Removed' in r['message'], 'the status says what was removed')

# time passes: after the due date, next week's homework takes over
r = hwsync.sync_student(A.app, sid, datetime.date(2026, 10, 15))
check(len(top(d)) == 1 and 'due Wed Oct 21' in top(d)[0], 'after the due date the next week\'s sheet appears: %s' % top(d))

# a missing or half-written current sheet (app stopped mid-write, or deleted by hand) is simply made again
cur = top(d)[0]
os.remove(os.path.join(d, cur))
r = hwsync.sync_student(A.app, sid, datetime.date(2026, 10, 15))
check(top(d) == [cur], 'a deleted current sheet is recreated on the next update')

# renaming the student carries the folder over
db.x("UPDATE students SET name='Samuel Rivera' WHERE id=?", (sid,))
r = hwsync.sync_student(A.app, sid, datetime.date(2026, 10, 15))
nd = os.path.join(os.environ['HW_ROOT'], 'Samuel_Rivera_HW')
check(os.path.isdir(nd) and not os.path.exists(d) and len(hist(nd)) >= 3, 'rename moves the folder with its History')
m = json.load(open(os.path.join(nd, '.manifest.json')))
check(m['student'] == 'Samuel Rivera' and len(m['current']) == 1, 'manifest records the current sheet')
check(hwsync.safe('Ana-María O\'Neil / 2') == 'Ana-María_ONeil_2', 'names become safe folder names')

keep = os.environ.get('KEEP_HW')
if keep: shutil.copytree(nd, keep, dirs_exist_ok=True)
# a second copy of the app cannot claim the folders while the first holds the lock; the lock frees when it exits
import subprocess
check(hwsync._claim(), 'this process claims the homework folders')
other = subprocess.run([sys.executable, '-c', 'import os,sys; sys.path.insert(0, %r); import hwsync; print(hwsync._claim())' % os.path.dirname(os.path.dirname(os.path.abspath(__file__)))],
                       env=dict(os.environ), capture_output=True, text=True)
check(other.stdout.strip() == 'False', 'a second running copy is refused (%s)' % (other.stdout.strip() or other.stderr.strip()[-200:]))
hwsync._owner.close(); hwsync._owner = None
other = subprocess.run([sys.executable, '-c', 'import os,sys; sys.path.insert(0, %r); import hwsync; print(hwsync._claim())' % os.path.dirname(os.path.dirname(os.path.abspath(__file__)))],
                       env=dict(os.environ), capture_output=True, text=True)
check(other.stdout.strip() == 'True', 'after the first copy lets go, a restart claims them again')

shutil.rmtree(TMP, ignore_errors=True)
print('\n%s' % ('ALL HOMEWORK FOLDER CHECKS PASSED' if not fails else '%d FAILED' % len(fails)))
sys.exit(1 if fails else 0)
