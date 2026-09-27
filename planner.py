"""Per-student calendar: what happened (past), today, and what is planned (future), with a plain-language reason for every
planned item so a parent can see why the plan looks the way it does.

The plan is recomputed from the student's current data every time it is shown, so it shifts as the student improves.
A snapshot of each day's plan is kept (plan_snapshots) so the calendar can say what changed since the last look and why.

The rules (RULES below is the parent-facing wording of exactly what plan() does):
  1. Tutoring happens on Sundays. The 1st-4th Sunday of a month is a lesson plus practice on one focus skill; a 5th
     Sunday is a timed hour-long mock (pool.mock_plan scaling, same as the app's mock).
  2. Until the student has a starting point (the diagnostic or an official/Bluebook score), the next session is the
     diagnostic.
  3. Each lesson's focus is the skill with the highest expected score gain: its share of the section's questions times
     the chance of missing a medium question at the current level (the same number analytics.recommendations uses).
     After a skill is scheduled (or was taught in the last three weeks, per the saved daily plans) its priority is cut in
     half, so the plan moves on instead of repeating, and it comes back if it is still weak. No more than two lessons in
     a row on the same section.
  4. Homework on the Wednesday after each lesson, on that lesson's skill (spaced practice).
  5. A skill whose accuracy is slipping gets a short refresher on a Friday, at most one a week.
  6. With a test date set: a full-length practice test 8-14 days before it, light review only in the final week.
  7. Anything the tutor adds (an event, or a Sunday with no session) takes priority; skipped lessons move forward.
"""
import datetime
import json

import analytics
import db
import scoring as S
from bank.skills import DOMAINS, SECTION_NAME, SKILLS

RULES = [
    ("Sundays are tutoring days.", "The 1st to 4th Sunday of each month is a lesson and practice on one focus skill. A 5th Sunday is a timed, hour-long practice test that shows progress under real conditions."),
    ("A starting point comes first.", "Until there is a diagnostic result or an official score, the next session is the 1-hour diagnostic. Everything else is planned from it."),
    ("Each lesson targets the most points available.", "Every skill gets a priority: how much of its section it covers on the real SAT, times how often the student is missing medium-difficulty questions on it right now. The highest priority goes first."),
    ("The plan keeps moving.", "Once a skill has a lesson, its priority is halved for later weeks, so the next lesson moves on. If the skill is still weak later, it comes back. No more than two lessons in a row go to the same section, so both Reading and Writing and Math improve."),
    ("Homework follows each lesson.", "Midweek practice on the same skill, three days after the lesson, is what makes a new method stick."),
    ("Slipping skills get a refresher.", "If accuracy on a skill that used to be fine drops, a short refresher is added that week."),
    ("The last weeks before the SAT are different.", "About two weeks out there is a full-length practice test as a dress rehearsal. The final week is light review only, with no new material."),
    ("It updates itself.", "The plan is recalculated from the latest results every time it is opened, so it responds to how things are actually going. When something moves, the calendar says what changed and why."),
]

KIND_LABEL = {'lesson': 'Lesson', 'homework': 'Homework', 'refresher': 'Refresher', 'mock': 'Practice test', 'diagnostic': 'Diagnostic',
              'fullmock': 'Full-length test', 'review': 'Light review', 'sat': 'SAT', 'official': 'Official score', 'practice': 'Practice',
              'custom': 'Note', 'skip': 'No session'}
# color family (a CSS class); every chip also carries its text label, so color is never the only cue
KIND_FAMILY = {'lesson': 'learn', 'practice': 'learn', 'homework': 'reinforce', 'refresher': 'reinforce', 'review': 'reinforce',
               'mock': 'measure', 'diagnostic': 'measure', 'fullmock': 'measure', 'sat': 'measure', 'official': 'measure',
               'custom': 'neutral', 'skip': 'neutral'}
HORIZON_WEEKS = 8
MAX_WEEKS = 26


def _d(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d').date()


def sundays(start, end):
    d = start + datetime.timedelta(days=(6 - start.weekday()) % 7)
    while d <= end:
        yield d
        d += datetime.timedelta(days=7)


def priorities(d):
    """Every skill with its expected-gain priority and the numbers behind it (for the explanation)."""
    by_key = dict((s['skill'], s) for s in d['skills'])
    est = {'rw': d['rw'], 'math': d['math']}
    out = []
    for sec in ('rw', 'math'):
        for dom, share in DOMAINS[sec].items():
            keys = [k for k, v in SKILLS.items() if v['section'] == sec and v['domain'] == dom]
            for k in keys:
                s = by_key.get(k)
                known = bool(s and s['n'] >= 3)
                p = s['p_medium'] if known else S._sig(est[sec]['theta'] - S.B[1])
                out.append(dict(skill=k, name=SKILLS[k]['name'], section=sec, share=share / len(keys), p=p, known=known,
                                n=s['n'] if s else 0, trend=s['trend'] if s else 'new', acc=s['acc'] if s else None,
                                acc_early=s.get('acc_early') if s else None, acc_late=s.get('acc_late') if s else None,
                                gain=share / len(keys) * (1 - p) * (1.25 if s and s['trend'] == 'slipping' else 1.0)))
    out.sort(key=lambda x: -x['gain'])
    for i, x in enumerate(out): x['rank'] = i + 1
    return out


def _why_lesson(x, first_name, total, note=''):
    share = round(x['share'] * 100)
    if x['known']:
        level = 'gets about %d%% of medium questions on it right now' % round(x['p'] * 100)
    elif x['n']:
        level = 'has answered only %d question%s on it, so it is estimated from the overall %s level' % (x['n'], '' if x['n'] == 1 else 's', SECTION_NAME[x['section']])
    else:
        level = 'has not practiced it yet, so it is estimated from the overall %s level' % SECTION_NAME[x['section']]
    base = 'Priority #%d of %d. It is about %d%% of %s questions, and %s %s.' % (x['rank'], total, share, SECTION_NAME[x['section']], first_name, level)
    if x['trend'] == 'slipping' and x['acc_early'] is not None:
        base += ' Accuracy has slipped from %d%% to %d%% lately.' % (round(x['acc_early'] * 100), round(x['acc_late'] * 100))
    return base + (' ' + note if note else '')


def plan(student_id, today=None):
    """Returns dict(items=[...], past=[...], changes=[...], start, end). Each item: day, kind, title, why, status, skill, link."""
    today = today or datetime.date.today()
    st = db.q('SELECT * FROM students WHERE id=?', (student_id,), one=True)
    d = analytics.dashboard(student_id)
    first = st['name'].split(' ')[0]
    items = []

    # ---------------- past: what actually happened
    sess = db.q('SELECT * FROM sessions WHERE student_id=? ORDER BY created', (student_id,))
    sheets = dict((r['session_id'], r) for r in db.q('SELECT * FROM hw_sheets WHERE student_id=? AND session_id IS NOT NULL', (student_id,)))
    done_hw = set()  # (day, kind) of homework whose answers were entered: shown as done on its due date, and that slot is filled
    for s in sess:
        day = datetime.date.fromtimestamp(s['created'])
        rows = db.q('SELECT r.correct, r.answer FROM responses r JOIN items i ON i.id=r.item_id JOIN modules m ON m.id=i.module_id WHERE m.session_id=?', (s['id'],))
        n, right = len(rows), sum(1 for r in rows if r['correct'])
        if s['mode'] == 'homework':
            sh = sheets.get(s['id'])
            kind = sh['kind'] if sh else 'homework'
            if sh and sh['due']: day = _d(sh['due'])
            skill = sh['skill'] if sh else None
            done_hw.add((day, kind))
            items.append(dict(day=day, kind=kind, title='%s: %s' % (KIND_LABEL[kind], SKILLS[skill]['name']) if skill else s['label'],
                              why='Answers entered %s: %d right out of %d answered.' % (datetime.date.fromtimestamp(s['created']).strftime('%b %d').replace(' 0', ' '), right, n),
                              status='done', skill=skill, session_id=s['id']))
            continue
        kind = 'diagnostic' if s['purpose'] == 'diagnostic' else ('mock' if s['mode'] == 'exam' else 'practice')
        why = ('%d of %d right on the first try.' % (right, n) if n else 'Started, no answers yet.') + ('' if s['finished'] else ' Not finished.')
        items.append(dict(day=day, kind=kind, title=s['label'], why=why, status='done' if s['finished'] else 'open', skill=None, session_id=s['id']))
    for p in d['priors']:
        items.append(dict(day=_d(p['taken']), kind='official', title=p['test'], why='Reading and Writing %d + Math %d = %d.' % (p['rw'], p['math'], p['rw'] + p['math']),
                          status='done', skill=None))

    # ---------------- tutor-entered events
    ev = db.q('SELECT * FROM events WHERE student_id=? ORDER BY day', (student_id,))
    skip_days = set()
    for e in ev:
        day = _d(e['day'])
        if e['kind'] == 'skip': skip_days.add(day)
        items.append(dict(day=day, kind=e['kind'], title=e['title'] or KIND_LABEL[e['kind']], why=e['note'] or '', status='event', skill=None, event_id=e['id']))

    # ---------------- future: the plan
    test_day = _d(st['test_date']) if st['test_date'] else None
    if test_day and test_day <= today: test_day = None
    end = test_day if test_day else today + datetime.timedelta(weeks=HORIZON_WEEKS)
    end = min(end, today + datetime.timedelta(weeks=MAX_WEEKS))
    has_start = st['onboard'] in ('diagnostic', 'prior') or bool(d['priors'])
    diag_done = any(s['purpose'] == 'diagnostic' and s['finished'] for s in sess)
    done_today = any(datetime.date.fromtimestamp(s['created']) == today for s in sess if s['mode'] != 'homework')
    pr = priorities(d)
    gains = dict((x['skill'], x['gain']) for x in pr)
    for k, n in recent_lessons(student_id, today).items():  # rule 3 also covers lessons already held, not just planned ones
        if k in gains: gains[k] *= 0.5 ** n
    info = dict((x['skill'], x) for x in pr)
    recent_sections, lesson_no, refresher_weeks = [], 0, set()
    slipping = [x for x in pr if x['trend'] == 'slipping']
    start = today if not done_today else today + datetime.timedelta(days=1)
    for sun in sundays(start, end):
        if sun in skip_days:
            continue  # rule 7: the tutor's calendar wins; the next lesson simply moves to the following Sunday
        nth = (sun.day - 1) // 7 + 1
        to_test = (test_day - sun).days if test_day else None
        if not has_start and not diag_done:
            items.append(dict(day=sun, kind='diagnostic', title='1-hour diagnostic', status='planned', skill=None,
                              why='%s does not have a starting point yet. The diagnostic measures both sections so every later lesson can be aimed at the most points.' % first))
            has_start = True
            continue
        if to_test == 0:
            continue  # test day holds only the SAT itself (added below)
        if to_test is not None and 0 < to_test <= 7:
            items.append(dict(day=sun, kind='review', title='Light review and test-day plan', status='planned', skill=None,
                              why='The SAT is %d day%s away. No new material this close to the test: a short review of strategies, pacing, and what to bring.' % (to_test, '' if to_test == 1 else 's')))
            continue
        if to_test is not None and 8 <= to_test <= 14:
            items.append(dict(day=sun, kind='fullmock', title='Full-length practice test', status='planned', skill=None,
                              why='A dress rehearsal about two weeks before the SAT: all four modules, full timing, so there is still time to act on the results.'))
            continue
        if nth == 5:
            items.append(dict(day=sun, kind='mock', title='Hour-long practice test', status='planned', skill=None,
                              why='Fifth Sunday of the month: a timed practice test measures progress under real conditions and refreshes the score estimate.'))
            continue
        # rule 3: highest remaining priority, with the section-balance rule
        ranked = sorted(pr, key=lambda x: -gains[x['skill']])
        pick, note = ranked[0], ''
        if len(recent_sections) >= 2 and recent_sections[-1] == recent_sections[-2] == pick['section']:
            other = [x for x in ranked if x['section'] != pick['section']][0]
            note = 'Switched to %s this week so both sections keep moving (two %s lessons in a row before this).' % (SECTION_NAME[other['section']], SECTION_NAME[pick['section']])
            pick = other
        elif lesson_no and gains[pick['skill']] < info[pick['skill']]['gain']:
            note = 'Scheduled again because it is still the biggest opportunity after the earlier lesson on it.'
        lesson_no += 1
        items.append(dict(day=sun, kind='lesson', title=pick['name'], status='planned', skill=pick['skill'],
                          why=_why_lesson(pick, first, len(pr), note)))
        gains[pick['skill']] *= 0.5
        recent_sections.append(pick['section'])
        wed = sun + datetime.timedelta(days=3)
        if wed <= end and wed not in skip_days:
            items.append(dict(day=wed, kind='homework', title='Homework: %s' % pick['name'], status='planned', skill=pick['skill'],
                              why='About 30 minutes on Sunday&rsquo;s skill, three days later. Practicing after a short gap is what makes a new method stick.'))
        week = sun.isocalendar()[1]
        if slipping and week not in refresher_weeks:
            x = slipping.pop(0)
            if x['skill'] != pick['skill']:
                fri = sun + datetime.timedelta(days=5)
                if fri <= end:
                    items.append(dict(day=fri, kind='refresher', title='Refresher: %s' % x['name'], status='planned', skill=x['skill'],
                                      why='Accuracy on this skill dropped from %d%% to %d%% lately. A short set now keeps it from sliding further.' % (
                                          round((x['acc_early'] or 0) * 100), round((x['acc_late'] or 0) * 100))))
                    refresher_weeks.add(week)
    if test_day:
        items.append(dict(day=test_day, kind='sat', title='SAT', status='planned', skill=None, why='Test day. The plan above counts down to this date.'))
    items = [i for i in items if not (i['status'] == 'planned' and (i['day'], i['kind']) in done_hw)]  # already handed in
    items.sort(key=lambda x: (x['day'], x['kind']))
    for it in items:
        if it['status'] == 'planned' and it['day'] < today: it['status'] = 'missed'
        it['label'] = KIND_LABEL.get(it['kind'], it['kind'].capitalize())
        it['family'] = KIND_FAMILY.get(it['kind'], 'neutral')
    changes = _changes(student_id, items, today)
    return dict(items=items, changes=changes, start=min([i['day'] for i in items] + [today]), end=end, test_day=test_day,
                priorities=pr, dashboard=d, student=st)


def recent_lessons(student_id, today, days=21):
    """Skills that had a lesson on a Sunday in the last `days` days: the lesson on the plan as it stood on that Sunday
    (the latest saved snapshot from on or before that day). Returns {skill: count}."""
    by_name = dict((v['name'], k) for k, v in SKILLS.items())
    snaps = [(r['day'], json.loads(r['plan_json'])) for r in db.q(
        'SELECT day, plan_json FROM plan_snapshots WHERE student_id=? AND day<? ORDER BY day', (student_id, today.isoformat()))]
    out = {}
    for sun in sundays(today - datetime.timedelta(days=days), today - datetime.timedelta(days=1)):
        iso = sun.isoformat()
        before = [p for day, p in snaps if day <= iso]
        if not before: continue
        for x in before[-1]:
            if x['day'] == iso and x['kind'] == 'lesson' and x['title'] in by_name:
                out[by_name[x['title']]] = out.get(by_name[x['title']], 0) + 1
    return out


def _changes(student_id, items, today):
    """Compare today's upcoming lessons with the last saved plan from an earlier day; save today's plan."""
    fut = [dict(day=i['day'].isoformat(), kind=i['kind'], title=i['title']) for i in items if i['status'] == 'planned' and i['kind'] != 'homework']
    prev = db.q('SELECT * FROM plan_snapshots WHERE student_id=? AND day<? ORDER BY day DESC LIMIT 1', (student_id, today.isoformat()), one=True)
    db.x('INSERT INTO plan_snapshots(student_id, day, plan_json) VALUES (?,?,?) ON CONFLICT(student_id, day) DO UPDATE SET plan_json=excluded.plan_json',
         (student_id, today.isoformat(), json.dumps(fut)))
    if not prev: return None
    old = dict((x['day'], x) for x in json.loads(prev['plan_json']) if x['day'] >= today.isoformat())
    new = dict((x['day'], x) for x in fut)
    why = dict((i['day'].isoformat(), i['why']) for i in items if i['status'] == 'planned')
    out = []
    for day in sorted(set(old) | set(new)):
        a, b = old.get(day), new.get(day)
        if a and b and (a['title'] != b['title'] or a['kind'] != b['kind']):
            out.append(dict(day=_d(day), before=a['title'], after=b['title'], why=why.get(day, '')))
        elif a and not b:
            out.append(dict(day=_d(day), before=a['title'], after=None, why='Removed, because of a change to the calendar or the test date.'))
    return dict(since=_d(prev['day']), items=out)


def month_grid(year, month, items, today):
    """Weeks (Sunday first) of day dicts for one month: day, in_month, items, is_today, is_past."""
    first = datetime.date(year, month, 1)
    start = first - datetime.timedelta(days=(first.weekday() + 1) % 7)
    by_day = {}
    for it in items: by_day.setdefault(it['day'], []).append(it)
    weeks, d = [], start
    while True:
        wk = []
        for _ in range(7):
            wk.append(dict(day=d, in_month=d.month == month, items=by_day.get(d, []), is_today=d == today, is_past=d < today))
            d += datetime.timedelta(days=1)
        weeks.append(wk)
        if d.month != month and d > first: break
    return weeks
