"""SQLite storage. One file (sat_mock.db) next to the app. No ORM; small helper functions."""
import json
import os
import shutil
import sqlite3
import time

PATH = os.environ.get('SAT_DB', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sat_mock.db'))

SCHEMA = """
CREATE TABLE IF NOT EXISTS students(
  id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, pin_hash TEXT, goal_total INTEGER DEFAULT 1200,
  parent_name TEXT, created REAL);
CREATE TABLE IF NOT EXISTS sessions(
  id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, mode TEXT NOT NULL, kind TEXT NOT NULL, label TEXT,
  plan_json TEXT, feedback INTEGER DEFAULT 0, timed INTEGER DEFAULT 1, created REAL, finished REAL);
CREATE TABLE IF NOT EXISTS modules(
  id INTEGER PRIMARY KEY, session_id INTEGER NOT NULL, seq INTEGER NOT NULL, section TEXT NOT NULL, module_no INTEGER,
  variant TEXT, n INTEGER, limit_sec INTEGER, warn_sec INTEGER, started REAL, finished REAL);
CREATE TABLE IF NOT EXISTS items(
  id INTEGER PRIMARY KEY, module_id INTEGER NOT NULL, idx INTEGER NOT NULL, section TEXT, domain TEXT, skill TEXT, d INTEGER,
  uid TEXT, qjson TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS responses(
  item_id INTEGER PRIMARY KEY, answer TEXT, correct INTEGER, is_mc INTEGER, time_ms INTEGER DEFAULT 0, flagged INTEGER DEFAULT 0,
  struck TEXT, checked INTEGER DEFAULT 0, ts REAL);
CREATE TABLE IF NOT EXISTS prior_scores(
  id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, test TEXT NOT NULL, rw INTEGER NOT NULL, math INTEGER NOT NULL,
  taken TEXT NOT NULL, created REAL);
CREATE TABLE IF NOT EXISTS settings(k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS creds(
  id TEXT PRIMARY KEY, x TEXT NOT NULL, y TEXT NOT NULL, sign_count INTEGER DEFAULT 0, label TEXT, created REAL);
CREATE INDEX IF NOT EXISTS ix_items_module ON items(module_id);
CREATE INDEX IF NOT EXISTS ix_modules_session ON modules(session_id);
CREATE INDEX IF NOT EXISTS ix_sessions_student ON sessions(student_id);
CREATE INDEX IF NOT EXISTS ix_prior_student ON prior_scores(student_id);
"""

# Columns added after the first release. init() adds any that an older database file is missing.
#   students.onboard: 'new' until the student takes the diagnostic or enters an earlier PSAT/SAT score.
#   sessions.assist: 'end' (answers after the set), 'hint' (hint after a wrong first try, then answer), 'answer' (answer after first try).
#   sessions.purpose: 'diagnostic' for the first-visit mock, '' otherwise. sessions.focus: 'skill'/'domain' for targeted practice.
#   responses.correct always holds the FIRST attempt, which is what scoring uses; a second try after a hint goes in retry_*.
MIGRATIONS = [
    ('students', 'grade', 'TEXT'), ('students', 'test_date', 'TEXT'), ('students', 'onboard', "TEXT DEFAULT 'new'"),
    ('students', 'last_seen', 'REAL'),
    ('sessions', 'assist', "TEXT DEFAULT 'end'"), ('sessions', 'purpose', "TEXT DEFAULT ''"), ('sessions', 'focus', "TEXT DEFAULT ''"),
    ('responses', 'attempts', 'INTEGER DEFAULT 0'), ('responses', 'hint_used', 'INTEGER DEFAULT 0'),
    ('responses', 'retry_answer', 'TEXT'), ('responses', 'retry_correct', 'INTEGER'),
]


def conn():
    c = sqlite3.connect(PATH)
    c.row_factory = sqlite3.Row
    return c


def init():
    c = conn()
    c.executescript(SCHEMA)
    for table, col, decl in MIGRATIONS:
        have = set(r['name'] for r in c.execute('PRAGMA table_info(%s)' % table))
        if col not in have:
            c.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table, col, decl))
    # sessions made before 'assist' existed: feedback on meant the answer was shown after each check
    c.execute("UPDATE sessions SET assist='answer' WHERE feedback=1 AND (assist IS NULL OR assist='end') AND mode='practice'")
    c.commit()
    c.close()


def q(sql, args=(), one=False):
    c = conn()
    cur = c.execute(sql, args)
    rows = cur.fetchall()
    c.close()
    if one:
        return rows[0] if rows else None
    return rows


def x(sql, args=()):
    c = conn()
    cur = c.execute(sql, args)
    c.commit()
    lid = cur.lastrowid
    c.close()
    return lid


def setting(k, default=None):
    r = q('SELECT v FROM settings WHERE k=?', (k,), one=True)
    return r['v'] if r else default


def set_setting(k, v):
    x('INSERT INTO settings(k, v) VALUES (?,?) ON CONFLICT(k) DO UPDATE SET v=excluded.v', (k, v))


def backup(tag):
    """Copy the database file into backups/ (next to it) before anything destructive. Returns the backup path."""
    folder = os.path.join(os.path.dirname(os.path.abspath(PATH)), 'backups')
    if not os.path.isdir(folder):
        os.makedirs(folder)
    dest = os.path.join(folder, 'sat_mock-%s-%s.db' % (time.strftime('%Y-%m-%d-%H%M%S'), tag))
    src = conn()
    dst = sqlite3.connect(dest)
    src.backup(dst)  # consistent copy even while the app is running
    dst.close(); src.close()
    return dest


def delete_student(student_id):
    """Remove a student and every session, module, item, response, and prior score that belongs to them."""
    c = conn()
    sess = '(SELECT id FROM sessions WHERE student_id=?)'
    mods = '(SELECT id FROM modules WHERE session_id IN %s)' % sess
    c.execute('DELETE FROM responses WHERE item_id IN (SELECT id FROM items WHERE module_id IN %s)' % mods, (student_id,))
    c.execute('DELETE FROM items WHERE module_id IN %s' % mods, (student_id,))
    c.execute('DELETE FROM modules WHERE session_id IN %s' % sess, (student_id,))
    c.execute('DELETE FROM sessions WHERE student_id=?', (student_id,))
    c.execute('DELETE FROM prior_scores WHERE student_id=?', (student_id,))
    c.execute('DELETE FROM students WHERE id=?', (student_id,))
    c.commit()
    c.close()


def add_items(module_id, questions):
    c = conn()
    for i, qu in enumerate(questions):
        c.execute('INSERT INTO items(module_id, idx, section, domain, skill, d, uid, qjson) VALUES (?,?,?,?,?,?,?,?)',
                  (module_id, i, qu['section'], qu['domain'], qu['skill'], qu['d'], qu['uid'], json.dumps(qu)))
    c.commit()
    c.close()


def seen_uids(student_id, days=45):
    """uids this student has already answered recently, so new sessions prefer fresh items."""
    since = time.time() - days * 86400
    rows = q('''SELECT DISTINCT i.uid FROM items i JOIN modules m ON m.id=i.module_id JOIN sessions s ON s.id=m.session_id
                WHERE s.student_id=? AND s.created>=?''', (student_id, since))
    return set(r['uid'] for r in rows)


def response_rows(student_id, upto_ts=None):
    """Every scorable response for a student, flattened for analytics.

    A blank counts as a wrong answer when it was left in a TIMED module that has been submitted, because that is how
    the real test treats it (skipping hard questions must not raise the estimate). Blanks in untimed practice are
    questions the student simply did not get to, so they are left out. `correct` is always the first attempt."""
    sql = '''SELECT r.item_id, r.answer, r.correct, r.is_mc, r.time_ms, r.ts, r.hint_used, r.attempts,
                    i.section, i.domain, i.skill, i.d, s.id AS session_id, s.mode, s.timed, s.purpose, s.focus, s.assist,
                    s.created AS session_created, m.limit_sec, m.finished AS module_finished
             FROM responses r JOIN items i ON i.id=r.item_id JOIN modules m ON m.id=i.module_id JOIN sessions s ON s.id=m.session_id
             WHERE s.student_id=? AND ((r.answer IS NOT NULL AND r.answer!='') OR (m.limit_sec>0 AND m.finished IS NOT NULL))
             ORDER BY r.ts'''
    rows = [dict(r) for r in q(sql, (student_id,))]
    for r in rows:
        r['omitted'] = 0 if r['answer'] else 1
        if r['omitted']: r['correct'] = 0
    if upto_ts:
        rows = [r for r in rows if r['session_created'] <= upto_ts]
    return rows


def prior_scores(student_id):
    return [dict(r) for r in q('SELECT * FROM prior_scores WHERE student_id=? ORDER BY taken', (student_id,))]
