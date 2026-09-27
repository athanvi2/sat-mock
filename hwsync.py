"""Keeps a homework folder per student on the tutor's Desktop in step with the calendar.

    ~/Desktop/Sam_Rivera_HW/
        Homework - due Wed Oct 7 - Boundaries (punctuation).pdf      <- this week's sheet(s) only
        History/
            2026-09-27 at 14.32 - due Wed Oct 7 - Boundaries (punctuation)/
                Homework - due Wed Oct 7 - Boundaries (punctuation).pdf
                Answer key - due Wed Oct 7 - Boundaries (punctuation).pdf
        .manifest.json                                                <- what is current, and for which calendar item

"This week's" homework is the next homework item on the student's calendar (planner.plan), plus any refresher due on or
before it. When the plan changes (a different skill, a different due date) or that due date passes, the old sheet is
removed from the top of the folder and a new one is made; every sheet ever made stays in History with a time stamp.
Nothing is regenerated while the plan is unchanged, so the same calendar item never produces a second sheet.

Runs in a background thread (sync_soon) so pages never wait on PDF rendering. HW_ROOT sets the parent folder; by default
it is ~/Desktop, but only when the app is using its real database (tests and scratch runs set SAT_DB and never touch the
Desktop unless they also set HW_ROOT).
"""
import datetime
import hashlib
import json
import os
import re
import shutil
import threading
import time
import traceback

try:
    import fcntl  # macOS/Linux: one running copy of the app manages the folders
except ImportError:  # Windows
    fcntl = None

import db
import pdfout
import planner
from bank.skills import SKILLS

_lock = threading.Lock()
_pending = set()
_status = {}  # student_id -> dict(ok, when, message, files)
KINDS = ('homework', 'refresher')


def root():
    r = os.environ.get('HW_ROOT')
    if r: return os.path.expanduser(r)
    if os.environ.get('SAT_DB'): return None  # a test or scratch database: never write to the real Desktop
    return os.path.join(os.path.expanduser('~'), 'Desktop')


def enabled():
    return bool(root()) and pdfout.available()


def safe(name):
    """A folder/file-name-safe version of a student's name: letters, digits, spaces -> underscores."""
    s = re.sub(r'[^\w\- ]+', '', name, flags=re.UNICODE).strip()
    return re.sub(r'\s+', '_', s) or 'Student'


def folder(student):
    return os.path.join(root(), '%s_HW' % safe(student['name']))


def _nice(d):
    return '%s %s %d' % (d.strftime('%a'), d.strftime('%b'), d.day)


def current_items(pl, today):
    """The homework the student should be working on now: the next homework item, plus refreshers due by then."""
    fut = [i for i in pl['items'] if i['status'] == 'planned' and i['kind'] in KINDS and i['day'] >= today and i.get('skill')]
    hw = [i for i in fut if i['kind'] == 'homework']
    if not hw:
        return fut[:1]
    due = hw[0]['day']
    return [i for i in fut if i['day'] <= due and (i['kind'] == 'refresher' or i is hw[0])]


def _key(it):
    return '%s|%s|%s' % (it['day'].isoformat(), it['kind'], it['skill'])


def _seed(student_id, it):
    return int(hashlib.sha256(('%d|%s' % (student_id, _key(it))).encode('utf-8')).hexdigest()[:8], 16)


def _title(it):
    name = SKILLS[it['skill']]['name']
    what = 'Homework' if it['kind'] == 'homework' else 'Refresher'
    return '%s - due %s - %s' % (what, _nice(it['day']), name)


def _render(app, student, it, key):
    """HTML for one sheet (student copy, or tutor copy with the answer key), rendered outside a web request."""
    import flask
    with app.test_request_context('/homework'):
        hw = app.extensions['build_homework'](student, it['skill'], _seed(student['id'], it))
        due = '%s, %s %d' % (it['day'].strftime('%A'), it['day'].strftime('%B'), it['day'].day)
        return flask.render_template('homework.html', s=None, st=student, skill=SKILLS[it['skill']], seed=0, mins=30, key=key, due=due, **hw)


def _manifest_path(d):
    return os.path.join(d, '.manifest.json')


def _load(d):
    try:
        with open(_manifest_path(d)) as fh: return json.load(fh)
    except (OSError, ValueError):
        return {'current': {}}


def _save(d, m):
    tmp = _manifest_path(d) + '.tmp'
    with open(tmp, 'w') as fh: json.dump(m, fh, indent=1)
    os.replace(tmp, _manifest_path(d))


def _move_renamed_folder(student, d):
    """If the student was renamed, carry the old folder over instead of starting a new one."""
    prev = db.setting('hwdir:%d' % student['id'])
    if prev and prev != d and os.path.isdir(prev) and not os.path.exists(d):
        shutil.move(prev, d)
    if os.path.isdir(d): db.set_setting('hwdir:%d' % student['id'], d)


def sync_student(app, student_id, today=None):
    """Bring one student's folder in line with their calendar. Returns a status dict."""
    if not enabled():
        return dict(ok=False, message='PDF export or the homework folder is not available here.', files=[])
    student = db.q('SELECT * FROM students WHERE id=?', (student_id,), one=True)
    if not student: return dict(ok=False, message='No such student.', files=[])
    today = today or datetime.date.today()
    pl = planner.plan(student_id, today)
    # the calendar pencils in lessons after a planned diagnostic, but homework starts only once there is a real starting
    # point: the diagnostic finished, or an official/Bluebook score entered
    started = student['onboard'] in ('diagnostic', 'prior') or bool(db.prior_scores(student_id))
    want = current_items(pl, today) if started else []
    d = folder(student)
    _move_renamed_folder(student, d)
    if not want and not os.path.isdir(d):
        st = dict(ok=True, when=time.time(), message='No homework on the calendar yet (it starts after the diagnostic).', files=[], folder=d)
        _status[student_id] = st
        return st
    os.makedirs(os.path.join(d, 'History'), exist_ok=True)
    db.set_setting('hwdir:%d' % student['id'], d)
    m = _load(d)
    cur = m.get('current', {})
    want_keys = dict((_key(it), it) for it in want)
    made, removed = [], []
    for k, fname in list(cur.items()):  # sheets no longer on the plan: remove from the top level (History keeps them)
        if k not in want_keys:
            p = os.path.join(d, fname)
            if os.path.exists(p): os.remove(p)
            removed.append(fname); del cur[k]
    stamp = datetime.datetime.now().strftime('%Y-%m-%d at %H.%M')
    for k, it in want_keys.items():
        fname = _title(it) + '.pdf'
        if k in cur and os.path.exists(os.path.join(d, cur[k])):
            continue  # unchanged plan: keep the sheet the student already has
        sheet = pdfout.html_to_pdf(_render(app, student, it, False))
        keypdf = pdfout.html_to_pdf(_render(app, student, it, True))
        hist = os.path.join(d, 'History', '%s - %s' % (stamp, _title(it)))
        os.makedirs(hist, exist_ok=True)
        with open(os.path.join(hist, fname), 'wb') as fh: fh.write(sheet)
        with open(os.path.join(hist, fname.replace('Homework - ', 'Answer key - ', 1).replace('Refresher - ', 'Answer key - Refresher - ', 1)), 'wb') as fh: fh.write(keypdf)
        with open(os.path.join(d, fname), 'wb') as fh: fh.write(sheet)
        cur[k] = fname
        made.append(fname)
    m['current'] = cur
    m['updated'] = time.time()
    m['student'] = student['name']
    _save(d, m)
    msg = ('Made %s.' % ', '.join(made) if made else 'Up to date.') + (' Removed %s (kept in History).' % ', '.join(removed) if removed else '')
    st = dict(ok=True, when=time.time(), message=msg, files=sorted(cur.values()), folder=d)
    _status[student_id] = st
    return st


def status(student_id):
    return _status.get(student_id)


def sync_soon(app, student_id=None):
    """Queue a background sync for one student (or everyone). Returns immediately."""
    if not enabled() or not _claim(): return
    with _lock:
        if student_id is None:
            _pending.update(r['id'] for r in db.q('SELECT id FROM students'))
        else:
            _pending.add(student_id)
    threading.Thread(target=_drain, args=(app,), daemon=True).start()


_worker = threading.Lock()


def _drain(app):
    if not _worker.acquire(blocking=False): return  # one worker at a time; it picks up everything queued
    try:
        while True:
            with _lock:
                if not _pending: return
                sid = _pending.pop()
            try:
                sync_student(app, sid)
            except Exception:  # a failed sheet must never take the app down; the error shows on the instructor page
                _status[sid] = dict(ok=False, when=time.time(), message='Homework folder update failed: ' + traceback.format_exc(limit=1).strip().splitlines()[-1], files=[])
    finally:
        _worker.release()
        with _lock:
            again = bool(_pending)
        if again: _drain(app)


_owner = None


def _claim():
    """Only one running copy of the app may manage the homework folders (two would write the same files). The claim is
    an OS file lock, released automatically when that copy exits or crashes, so a restart never finds a stale lock."""
    global _owner
    if _owner is not None or fcntl is None: return True
    fh = open(os.path.join(os.path.dirname(os.path.abspath(db.PATH)), '.hwsync.lock'), 'w')
    try:
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        fh.close()
        return False
    _owner = fh
    return True


def start_hourly(app, check_every=300, period=3600):
    """Sync everyone at startup (catching up on anything that changed while the app was off), then once an hour of
    wall-clock time has passed or the date has changed. Checking every 5 minutes against the real clock means a Mac
    waking from sleep catches up within minutes rather than waiting out an hour of awake time."""
    if not enabled(): return False
    if not _claim():
        print('  Homework folders: another copy of the app is already updating them.')
        return False

    def loop():
        last, day = 0.0, None
        while True:
            now = time.time()
            if now - last >= period or datetime.date.today() != day:
                sync_soon(app)
                last, day = now, datetime.date.today()
            time.sleep(check_every)
    threading.Thread(target=loop, daemon=True).start()
    return True
