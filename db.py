"""SQLite storage. One file (sat_mock.db) next to the app. No ORM; small helper functions."""
import json
import os
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
CREATE INDEX IF NOT EXISTS ix_items_module ON items(module_id);
CREATE INDEX IF NOT EXISTS ix_modules_session ON modules(session_id);
CREATE INDEX IF NOT EXISTS ix_sessions_student ON sessions(student_id);
"""


def conn():
    c = sqlite3.connect(PATH)
    c.row_factory = sqlite3.Row
    return c


def init():
    c = conn()
    c.executescript(SCHEMA)
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
    """Every graded response for a student, flattened for analytics."""
    sql = '''SELECT r.item_id, r.correct, r.is_mc, r.time_ms, r.ts, i.section, i.domain, i.skill, i.d, s.id AS session_id, s.mode,
                    s.created AS session_created
             FROM responses r JOIN items i ON i.id=r.item_id JOIN modules m ON m.id=i.module_id JOIN sessions s ON s.id=m.session_id
             WHERE s.student_id=? AND r.answer IS NOT NULL AND r.answer!=''
             ORDER BY r.ts'''
    rows = [dict(r) for r in q(sql, (student_id,))]
    if upto_ts:
        rows = [r for r in rows if r['session_created'] <= upto_ts]
    return rows
