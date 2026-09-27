"""End-to-end check of the Flask app through its test client. Run:  python tests/smoke.py
Uses /tmp/smoke.db, never the real student database."""
import datetime, glob, os, sys, json, re, random, time
os.environ['SAT_DB'] = '/tmp/smoke.db'
for f in ['/tmp/smoke.db'] + glob.glob('/tmp/backups/sat_mock-*'):
    os.remove(f)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app as A, db, auth

c = A.app.test_client()            # a student's browser on this Mac
ci = A.app.test_client()           # the instructor's browser on this Mac
REMOTE = {'REMOTE_ADDR': '192.168.1.23'}  # a student's own device on the Wi-Fi


def ok(r, what):
    assert r.status_code in (200, 302), (what, r.status_code, r.data[:800])
    assert b'Traceback' not in r.data, what
    return r


def sid_from(r):
    return int(r.headers['Location'].rstrip('/').split('/')[-1])


# ------------------------------------------------------------------ welcome and joining
r = ok(c.get('/', follow_redirects=True), 'root'); assert b'I&rsquo;m new here' in r.data
r = ok(c.post('/join', data=dict(name='Test Student', pin='12', pin2='12')), 'short pin'); assert b'exactly 4 digits' in r.data
r = ok(c.post('/join', data=dict(name='Test Student', pin='1234', pin2='1243')), 'mismatch'); assert b'do not match' in r.data
r = ok(c.post('/join', data=dict(name='Test Student', pin='1234', pin2='1234', grade='11', goal='1300')), 'join')
assert r.headers['Location'].endswith('/start')
r = ok(c.get('/start'), 'start'); assert b'1-hour diagnostic' in r.data
assert db.q("SELECT onboard FROM students WHERE name='Test Student'", one=True)['onboard'] == 'new'
c2 = A.app.test_client()
r = ok(c2.post('/join', data=dict(name='test student', pin='5555', pin2='5555')), 'dup'); assert b'already uses that name' in r.data
for path in ['/', '/practice', '/exam', '/dashboard', '/skills', '/scores']:
    ok(c.get(path), path)


def payload(html):
    m = re.search(r'items: (\[.*?\]), remaining:', html, re.S)
    return json.loads(m.group(1))


def wrong(qd):
    return ('A' if qd['answer'] != 'A' else 'B') if qd['type'] == 'mc' else '999'


def play(mid, acc, rng, assist='end', blank=False):
    """Answer every item in module `mid`, right with probability acc (key read from the server DB)."""
    items = payload(ok(c.get('/module/%d' % mid), 'module page').data.decode())
    for it in items:
        qd = json.loads(db.q('SELECT qjson FROM items WHERE id=?', (it['id'],), one=True)['qjson'])
        if blank: continue
        ans = qd['answer'] if rng.random() < acc else wrong(qd)
        j = c.post('/api/save', json=dict(item_id=it['id'], answer=ans, time_ms=60000, flagged=rng.random() < .1, struck=[])).get_json()
        assert j['ok'], j
        if assist != 'end':
            j = c.post('/api/check', json=dict(item_id=it['id'], answer=ans, time_ms=1000)).get_json()
            assert j['ok'] and ('reveal' in j or 'hint' in j), j
            if 'hint' in j:
                assert assist == 'hint' and ans != qd['answer']
                c.post('/api/save', json=dict(item_id=it['id'], answer=qd['answer'], time_ms=5000, flagged=False, struck=[ans]))
                j = c.post('/api/check', json=dict(item_id=it['id'], answer=qd['answer'], time_ms=1000)).get_json()
                assert j['reveal']['retry_correct'] and not j['reveal']['correct'], j
    j = c.post('/api/finish', json=dict(module_id=mid)).get_json()
    assert j['ok']


def drive(sid, acc, rng, assist='end', blank=False):
    for _ in range(12):
        r = c.get('/run/%d' % sid, follow_redirects=False)
        loc = r.headers.get('Location', '')
        if '/results/' in loc: return loc
        if '/intro' in loc:
            mid = int(re.search(r'/module/(\d+)/intro', loc).group(1))
            ok(c.get(loc), 'intro'); ok(c.post(loc), 'start'); play(mid, acc, rng, assist, blank)
        elif '/module/' in loc:
            play(int(re.search(r'/module/(\d+)', loc).group(1)), acc, rng, assist, blank)
        else: raise AssertionError(loc)
    raise AssertionError('loop')


rng = random.Random(4)
me = db.q("SELECT * FROM students WHERE name='Test Student'", one=True)

# ------------------------------------------------------------------ diagnostic
r = ok(c.post('/start', data=dict(choice='diagnostic')), 'diagnostic'); dsid = sid_from(r)
sess = db.q('SELECT * FROM sessions WHERE id=?', (dsid,), one=True)
assert sess['purpose'] == 'diagnostic' and sess['assist'] == 'end' and sess['mode'] == 'exam'
ok(c.get(drive(dsid, 0.6, rng)), 'diagnostic results')
mods = db.q('SELECT section, n, limit_sec FROM modules WHERE session_id=? ORDER BY seq', (dsid,))
assert len(mods) == 4 and 55 * 60 <= sum(m['limit_sec'] for m in mods) <= 62 * 60, [tuple(m) for m in mods]
assert db.q('SELECT onboard FROM students WHERE id=?', (me['id'],), one=True)['onboard'] == 'diagnostic'
print('diagnostic ok:', sum(m['n'] for m in mods), 'questions,', round(sum(m['limit_sec'] for m in mods) / 60.0, 1), 'minutes')

# ------------------------------------------------------------------ earlier scores
r = ok(c.post('/scores', data=dict(test='PSAT 8/9', taken='2026-03-01', rw='750', math='700')), 'bad psat'); assert b'120 to 720' in r.data
r = ok(c.post('/scores', data=dict(test='SAT', taken='2099-01-01', rw='600', math='600')), 'future'); assert b'future' in r.data
ok(c.post('/scores', data=dict(test='PSAT/NMSQT or PSAT 10', taken='2026-03-01', rw='560', math='540')), 'good psat')
assert len(db.prior_scores(me['id'])) == 1

# ------------------------------------------------------------------ practice with each assist level
for form in [dict(section='math', what='m1', length='session', timed='1', assist='answer'),
             dict(section='rw', what='rec', length='custom', custom_n='6', difficulty='auto', timed='1', assist='hint'),
             dict(section='math', what='full', length='session', timed='1', assist='hint'),
             dict(section='rw', what='domain:Standard English Conventions', length='custom', custom_n='8', difficulty='auto', timed='0', assist='end'),
             dict(section='math', what='skill:systems_2lin', length='custom', custom_n='6', difficulty='2', timed='1', assist='answer'),
             dict(section='math', what='hard', length='module', timed='1', assist='end')]:
    sid = sid_from(ok(c.post('/practice', data=form), 'practice ' + str(form)))
    loc = drive(sid, 0.5, rng, form['assist'])
    for path in [loc, '/review/%d' % sid, '/review/%d?only=missed' % sid]:
        r = ok(c.get(path), path); assert b'jinja' not in r.data.lower(), path
    uids = [x['uid'] for x in db.q('SELECT i.uid FROM items i JOIN modules m ON m.id=i.module_id WHERE m.session_id=?', (sid,))]
    assert len(uids) == len(set(uids)), 'a question repeated inside one session'
    print('practice ok', form['what'], form['assist'], sid)

# first tries are what count: every hinted item must still be scored wrong
hinted = db.q('SELECT correct, retry_correct FROM responses WHERE hint_used=1')
assert hinted and all(h['correct'] == 0 and h['retry_correct'] == 1 for h in hinted)

# blanks: count as wrong in a submitted timed set, ignored in untimed practice
before = len(db.response_rows(me['id']))
sid = sid_from(ok(c.post('/practice', data=dict(section='rw', what='m1', length='custom', custom_n='5', timed='1', assist='end')), 'blank timed'))
drive(sid, 0, rng, blank=True)
sid2 = sid_from(ok(c.post('/practice', data=dict(section='rw', what='m1', length='custom', custom_n='5', timed='0', assist='end')), 'blank untimed'))
drive(sid2, 0, rng, blank=True)
rows = db.response_rows(me['id'])
assert len(rows) == before + 5 and all(r['correct'] == 0 and r['omitted'] for r in rows if r['session_id'] == sid)

# ------------------------------------------------------------------ adaptive routing (both directions must hold)
for acc, want in ((0.97, 'hard'), (0.05, 'easy')):
    sid = sid_from(ok(c.post('/exam', data=dict(kind='mock', minutes='55')), 'exam'))
    ok(c.get(drive(sid, acc, rng)), 'exam results')
    mods = db.q('SELECT section, module_no, variant, n, limit_sec FROM modules WHERE session_id=? ORDER BY seq', (sid,))
    print('exam acc', acc, [(m['section'], m['module_no'], m['variant'], m['n'], m['limit_sec']) for m in mods])
    assert [m['variant'] for m in mods if m['module_no'] == 2] == [want, want]

r = ok(c.get('/dashboard'), 'dash'); html = r.data.decode()
assert 'Where the score is likely' in html and 'Score over time' in html and 'Questions answered per week' in html and 'Right on the first try' in html and 'data-tip=' in html and 'Up next' in html

# ------------------------------------------------------------------ lecture and homework: students never see keys
r = ok(c.get('/lecture/circles'), 'lec'); assert b'Show answer' in r.data and b'Instructor view' not in r.data
r = ok(c.get('/homework?skill=circles&key=1'), 'hw'); assert b'Answer key for the tutor' not in r.data
for k in A.SKILLS:
    ok(c.get('/homework?skill=%s' % k), k); ok(c.get('/lecture/%s' % k), k)

# ------------------------------------------------------------------ another student cannot see this one's work
other = A.app.test_client()
ok(other.post('/join', data=dict(name='Other Kid', pin='4321', pin2='4321')), 'join 2')
assert other.get('/results/%d' % dsid).status_code == 404 and other.get('/review/%d' % dsid).status_code == 404
r = ok(A.app.test_client().post('/login', data=dict(name='Test Student', pin='0000')), 'bad pin'); assert b'does not match' in r.data
r = A.app.test_client().post('/login', data=dict(name='Test Student', pin='1234')); assert r.status_code == 302

# ------------------------------------------------------------------ student address: no port when serving on 80
A.PORT = 80; assert all(':' not in u.split('//')[1] for u in A.lan_addresses())
A.PORT = 5050; assert all(u.endswith(':5050') for u in A.lan_addresses())
A.PORT = 80

# ------------------------------------------------------------------ instructor lock
rx = A.app.test_client()
assert rx.get('/instructor', environ_overrides=REMOTE).status_code == 404, 'instructor must not exist for other devices'
assert rx.get('/instructor/login', environ_overrides=REMOTE).status_code == 404
assert rx.post('/instructor/webauthn/auth-begin', environ_overrides=REMOTE).status_code == 404
assert ci.get('/instructor').headers['Location'].endswith('/instructor/setup')
r = ok(ci.post('/instructor/setup', data=dict(pin='111111', pin2='111111')), 'weak pin'); assert b'less guessable' in r.data
ok(ci.post('/instructor/setup', data=dict(pin='482913', pin2='482913')), 'set pin')
ci.get('/instructor/logout')
assert '/instructor/login' in ci.get('/instructor').headers['Location']
for _ in range(auth.MAX_FAILS):
    ci.post('/instructor/login', data=dict(pin='000000'))
r = ok(ci.post('/instructor/login', data=dict(pin='482913')), 'locked out'); assert b'Too many wrong PINs' in r.data
auth._fails.clear()
assert ci.post('/instructor/login', data=dict(pin='482913', next='/instructor')).status_code == 302
j = ci.post('/instructor/webauthn/auth-begin').get_json(); assert j['rpId'] == 'localhost' and j['userVerification'] == 'required'
j = ci.post('/instructor/webauthn/register-begin').get_json(); assert j['pubKeyCredParams'][0]['alg'] == -7
assert A.app.test_client().post('/instructor/webauthn/register-begin').status_code == 302, 'enrolling needs an unlocked session'

# ------------------------------------------------------------------ instructor pages and student CRUD
r = ok(ci.get('/instructor'), 'roster'); assert b'Test Student' in r.data and b'Other Kid' in r.data and b'.local' in r.data
ok(ci.post('/instructor/students/new', data=dict(name='Added By Tutor', pin='2468', goal='1350')), 'add')
added = db.q("SELECT * FROM students WHERE name='Added By Tutor'", one=True); assert added and added['goal_total'] == 1350
for path in ['/instructor/students/%d' % me['id'], '/instructor/students/%d?view=parent' % me['id'], '/instructor/settings',
             '/results/%d' % dsid, '/review/%d' % dsid, '/skills', '/lecture/circles']:
    ok(ci.get(path), path)
r = ci.get('/lecture/circles'); assert b'Instructor view' in r.data
r = ok(ci.get('/homework?skill=circles&student=%d&key=1' % me['id']), 'hw key'); assert b'Answer key for the tutor' in r.data and b'Test Student' in r.data
# calendar, parent report, guide
r = ok(c.get('/plan'), 'my plan'); assert b'Coming up' in r.data and b'How this plan is built' in r.data and b'class="chip' in r.data
assert b'Add to the calendar' not in r.data, 'students cannot edit the calendar'
r = ok(ci.get('/instructor/students/%d/plan' % me['id']), 'tutor plan'); assert b'Add to the calendar' in r.data
nxt = datetime.date.today() + datetime.timedelta(days=(6 - datetime.date.today().weekday()) % 7 or 7)
ok(ci.post('/instructor/students/%d/events' % me['id'], data=dict(day=nxt.isoformat(), kind='skip', title='Holiday')), 'add event')
ev = db.q('SELECT * FROM events WHERE student_id=?', (me['id'],), one=True); assert ev and ev['kind'] == 'skip'
assert b'Holiday' in ci.get('/instructor/students/%d/plan?m=%s' % (me['id'], nxt.strftime('%Y-%m'))).data
ok(ci.post('/instructor/events/%d/delete' % ev['id']), 'delete event'); assert not db.q('SELECT 1 FROM events WHERE id=?', (ev['id'],), one=True)
assert A.app.test_client().post('/instructor/students/%d/events' % me['id'], data=dict(day=nxt.isoformat()), environ_overrides=REMOTE).status_code == 404
ok(ci.post('/instructor/students/%d/report/note' % me['id'], data=dict(note='Great focus this month.')), 'note')
r = ok(ci.get('/instructor/students/%d/report' % me['id']), 'report'); assert b'Great focus this month.' in r.data and b'The next four weeks' in r.data
assert rx.get('/instructor/students/%d/report' % me['id'], environ_overrides=REMOTE).status_code == 404
assert c.get('/instructor/students/%d/report' % me['id']).status_code in (302, 404), 'students cannot open parent reports'
r = ok(A.app.test_client().get('/guide'), 'guide'); assert b'How SAT prep works here' in r.data and b'It updates itself.' in r.data
if __import__('pdfout').available():
    r = ci.get('/instructor/students/%d/report?format=pdf' % me['id']); assert r.status_code == 200 and r.data[:4] == b'%PDF', r.status_code
    r = A.app.test_client().get('/guide.pdf'); assert r.status_code == 200 and r.data[:4] == b'%PDF'
    print('pdf export ok')
assert b'class="themebtn' in c.get('/').data and b'theme.js' in c.get('/').data
ok(ci.post('/instructor/students/%d/edit' % added['id'], data=dict(name='Added By Tutor', goal='1400', grade='10', pin='1357')), 'edit')
assert auth.check_pin(db.q('SELECT pin_hash FROM students WHERE id=?', (added['id'],), one=True)['pin_hash'], '1357')
ok(ci.post('/instructor/students/%d/scores' % added['id'], data=dict(test='SAT', taken='2026-05-02', rw='610', math='590')), 'score')
ok(ci.post('/instructor/students/%d/delete' % me['id'], data=dict(confirm='wrong name')), 'bad confirm')
assert db.q('SELECT 1 FROM students WHERE id=?', (me['id'],), one=True), 'deleted without the right confirmation'
ok(ci.post('/instructor/students/%d/delete' % me['id'], data=dict(confirm='test student')), 'delete')
assert not db.q('SELECT 1 FROM students WHERE id=?', (me['id'],), one=True)
assert not db.q('SELECT 1 FROM sessions WHERE student_id=?', (me['id'],)) and not db.prior_scores(me['id'])
assert glob.glob('/tmp/backups/sat_mock-*before-deleting-%d.db' % me['id']), 'no backup before delete'
assert c.get('/').status_code == 302, 'a deleted student is signed out'
print('ALL SMOKE TESTS PASSED')
