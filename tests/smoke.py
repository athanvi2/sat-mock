import os, sys, json, re, random, time
os.environ['SAT_DB'] = '/tmp/smoke.db'
if os.path.exists('/tmp/smoke.db'): os.remove('/tmp/smoke.db')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app as A, db

c = A.app.test_client()
def ok(r, what):
    assert r.status_code in (200, 302), (what, r.status_code, r.data[:500])
    return r

ok(c.get('/', follow_redirects=False), 'root')
r = ok(c.post('/students/new', data=dict(name='Test Student', goal='1300')), 'new student')
for path in ['/', '/practice', '/exam', '/dashboard', '/dashboard?view=parent', '/skills']:
    r = ok(c.get(path), path); assert b'Traceback' not in r.data, path

def payload(html):
    m = re.search(r'items: (\[.*?\]), remaining:', html, re.S)
    return json.loads(m.group(1))

def play(mid, acc, rng, feedback):
    """answer every item in module `mid` with probability acc of being right, using the server DB for the key"""
    r = ok(c.get('/module/%d' % mid), 'module page'); html = r.data.decode()
    items = payload(html)
    for it in items:
        row = db.q('SELECT qjson FROM items WHERE id=?', (it['id'],), one=True)
        qd = json.loads(row['qjson'])
        if rng.random() < acc: ans = qd['answer']
        else:
            ans = 'A' if qd['type'] == 'mc' and qd['answer'] != 'A' else ('B' if qd['type'] == 'mc' else '999')
        j = c.post('/api/save', json=dict(item_id=it['id'], answer=ans, time_ms=60000, flagged=rng.random() < .1, struck=[])).get_json()
        assert j['ok'], j
        if feedback:
            j = c.post('/api/check', json=dict(item_id=it['id'], answer=ans, time_ms=1000)).get_json()
            assert j['ok'] and 'expl' in j
    j = c.post('/api/finish', json=dict(module_id=mid)).get_json()
    assert j['ok']

def drive(sid, acc, rng, feedback):
    for _ in range(12):
        r = c.get('/run/%d' % sid, follow_redirects=False)
        loc = r.headers.get('Location', '')
        if '/results/' in loc: return loc
        if '/intro' in loc:
            mid = int(re.search(r'/module/(\d+)/intro', loc).group(1))
            assert c.get(loc).status_code == 200
            ok(c.post(loc), 'start'); play(mid, acc, rng, feedback)
        elif '/module/' in loc:
            mid = int(re.search(r'/module/(\d+)', loc).group(1)); play(mid, acc, rng, feedback)
        else: raise AssertionError(loc)
    raise AssertionError('loop')

rng = random.Random(4)
# practice: several kinds
for form in [dict(section='math', what='m1', length='session', timed='1', feedback='1'),
             dict(section='rw', what='m1', length='session', timed='1', feedback='1'),
             dict(section='math', what='full', length='session', timed='1', feedback='1'),
             dict(section='rw', what='domain:Standard English Conventions', length='custom', custom_n='8', difficulty='mixed', timed='0', feedback='0'),
             dict(section='math', what='skill:systems_2lin', length='custom', custom_n='6', difficulty='2', timed='1', feedback='1'),
             dict(section='math', what='hard', length='module', timed='1', feedback='1')]:
    r = ok(c.post('/practice', data=form), 'practice ' + str(form)); sid = int(r.headers['Location'].rstrip('/').split('/')[-1])
    loc = drive(sid, 0.6, rng, form['feedback'] == '1')
    for path in [loc, '/review/%d' % sid, '/review/%d?only=missed' % sid]:
        r = ok(c.get(path), path); assert b'Traceback' not in r.data and b'jinja' not in r.data.lower(), path
    print('practice ok', form['what'], sid)

# exam: compressed mock, strong then weak student to verify routing
for acc in (0.9, 0.3):
    r = ok(c.post('/exam', data=dict(kind='mock', minutes='55')), 'exam'); sid = int(r.headers['Location'].rstrip('/').split('/')[-1])
    loc = drive(sid, acc, rng, False)
    mods = db.q('SELECT section, module_no, variant, n, limit_sec FROM modules WHERE session_id=? ORDER BY seq', (sid,))
    print('exam acc', acc, [(m['section'], m['module_no'], m['variant'], m['n'], m['limit_sec']) for m in mods])
    r = ok(c.get(loc), 'exam results'); assert b'Traceback' not in r.data

r = ok(c.get('/dashboard'), 'dash'); html = r.data.decode(); assert 'Where the score is likely' in html and '<svg' in html
ok(c.get('/dashboard?view=parent'), 'parent')
for sk in ['systems_2lin', 'boundaries', 'two_var_data', 'coe_quant']:
    r = ok(c.get('/homework?skill=%s&key=1' % sk), 'hw'); assert b'How to do this:' in r.data and b'What can u see' in r.data
    r = ok(c.get('/lecture/%s' % sk), 'lec')
# every skill page renders
for k in A.SKILLS:
    ok(c.get('/homework?skill=%s' % k), k); ok(c.get('/lecture/%s' % k), k)
print('ALL SMOKE TESTS PASSED')
