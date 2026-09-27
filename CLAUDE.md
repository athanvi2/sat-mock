# sat_mock

A local Flask app for in-person Digital SAT tutoring. Runs on the tutor's Mac; students use their own devices over the tutor's home Wi-Fi. Two roles: **student** (signs in with name + 4-digit PIN, self-registers) and **instructor** (only reachable from the Mac itself, behind Touch ID or a 6-digit PIN). Stores everything in a single SQLite file. No build step, no frontend framework: server-rendered Jinja templates plus a couple of hand-written JS files.

Read this file before making changes. It exists so you don't have to rediscover the architecture, the conventions, or the parts that are easy to break, each session.

## Running it

```
source .venv/bin/activate
python app.py
```
Listens on all interfaces on port **80** when it is free (macOS lets ordinary users bind it), else **5050** (5000 is taken by macOS AirPlay Receiver); `PORT`/`HOST` env vars override, see `pick_port()`. The instructor uses http://localhost/instructor on the Mac (Touch ID needs `localhost`, not `127.0.0.1`; the app redirects). Students use the `.local` / LAN address printed at startup and shown on the instructor page. `SAT_DB` env var overrides the sqlite file path (tests use `/tmp/*.db` so they never touch real student data).

## Testing

Run these after any change to `bank/`, `app.py`, `scoring.py`, `analytics.py`, or a template:

```
python tests/portable_check.py   # confirms code still parses as Python 3.8 (see "Python version" below)
python tests/fuzz_math.py        # every math generator, every difficulty, hundreds of seeds, no crashes/duplicate choices
python tests/fuzz_rw.py          # same for reading & writing
python tests/smoke.py            # end-to-end: join, diagnostic, assist levels, adaptive routing, instructor lock + CRUD, every skill's pages
python tests/score_check.py      # simulated students: 80% ranges cover ~80%, no bias, edge cases (drilling, skipping, priors, recency)
python tests/plan_check.py       # the calendar follows every rule in planner.RULES (the text parents read)
python tests/hw_check.py         # Desktop homework folders, in a temp dir: create, keep, replace on plan change, roll weekly, rename
python tests/rw_quality.py       # RW answer choices give no length giveaway (see "Distractor rule")
python tests/bank_report.py      # prints how many distinct questions each skill can produce at each difficulty
```

`tests/smoke.py` is the one that actually exercises the Flask app (via `app.test_client()`), including the adaptive module-2 routing logic (asserts a 97%-accuracy student gets both harder Module 2s and a 5% one both easier), the instructor lock (404 from non-local addresses, PIN lockout), and that students never receive answer keys. Don't skip it after touching `app.py`. Run `tests/score_check.py` after touching `scoring.py` or `analytics.py`.

There's no visual regression test. After CSS/template changes, actually load the page in a browser and look at it, especially the exam runner (`templates/runner.html` + `static/runner.js`) since it has floating panels, a timer, and keyboard handling that's easy to silently break.

## Architecture

```
bank/
  skills.py       Skill taxonomy: DOMAINS (weights), SKILLS dict (name/see/how/traps/formulas per skill), REFERENCE_HTML
  math_gen.py     19 Math skills x 3 difficulties, parametric generators. GEN dict: skill_key -> fn(rng, difficulty, spr) -> question dict
  rw_gen.py       11 RW skills. Mix of parametric generators and pickers over hand-authored content (rw_content.py / rw_content2.py)
  rw_content.py ... rw_content7.py   Hand-written passages/items for skills that can't be parameterized (main idea, inference, rhetorical synthesis, etc.)
  pool.py         Joins math_gen + rw_gen into one GEN dict. build_module() assembles a domain-weighted, difficulty-mixed module in official test order.
                  mock_plan() / full_plan() / session_plan() compute question counts and time limits.
scoring.py        IRT-style (Rasch + guessing floor) score estimation. Documented in its own docstring as an ESTIMATE, not a real College Board model. The docstring lists each evidence rule and the failure it guards against.
db.py             SQLite. Tables: students, sessions, modules, items, responses, prior_scores, settings, creds, events, plan_snapshots,
                  hw_items + hw_sheets (homework questions handed out / their saved sheets), flags + retired (reported and retired questions). MIGRATIONS adds columns to older files on startup. No ORM, just q()/x() helpers.
auth.py           Instructor PIN (pbkdf2) + lockout, per-install cookie secret, and a minimal WebAuthn (Touch ID, ES256 only) verifier: small CBOR reader + pure-Python P-256 ECDSA. No crypto dependency.
analytics.py      Dashboard payload (estimates, timeline incl. reported scores, weekly activity, per-skill mastery, recommendations,
                  timing findings) + server-side SVG charts.
planner.py        Per-student calendar: past sessions, tutor events, and a plan recomputed on every view with a "why" per item. RULES is the
                  parent-facing wording of exactly what plan() does; change both together (tests/plan_check.py asserts the rules).
pdfout.py         HTML -> PDF through a local headless Chrome (parent report, guide, homework). No Python PDF dependency; CHROME_PATH overrides.
hwsync.py         Keeps ~/Desktop/<Name>_HW in step with each student's calendar: this week's homework PDF at the top (replaced when the
                  plan changes or the due date passes), every sheet + answer key kept in History/<timestamp>/. Background thread;
                  triggered by finished sessions, score/event/student changes, and hourly. Writes to the Desktop ONLY when SAT_DB is
                  unset (the real database) or HW_ROOT is set, so tests never touch it.
tools/build_guide_pdf.py   Regenerates docs/Parent-Guide.pdf from templates/guide.html.
app.py            Flask routes: student flow (join, /start diagnostic, practice, runner APIs), instructor (/instructor/*). Read module_score_ratio()/advance() for adaptive routing and api_check() for assist levels before touching them.
templates/        Jinja. base.html is the shell (nav differs for student/instructor). report.html and guide.html are standalone print-first documents. runner.html + static/runner.js is the exam-taking UI, the most complex piece. _progress.html is the shared progress report (student, tutor, parent views). instructor/ holds the instructor pages.
static/app.css    Single stylesheet, hand-rolled design system (see the comment block at the top for the rationale, don't restyle without reading it).
static/calc.js    Offline fallback graphing calculator (used when Desmos's CDN can't load). Has its own expression parser, don't confuse with Desmos integration in runner.js.
```

## Conventions that matter

**Question dict shape.** Every generator returns a dict with at least: `type` (`mc` or `spr`), `passage` (HTML, can be empty string), `q` (the stem), `choices` (list of 4, for mc), `answer` (a letter A-D for mc, or the numeric value/tolerance for spr), `expl` (HTML explanation), `uid` (a string used for de-duplication). `pool.make()` adds `skill`, `d`, `seed`, `section`, `domain`, `skill_name` on top. Don't strip these when refactoring, `app.py` and the templates read them by key.

**uid and repeat-avoidance.** `db.seen_uids()` returns `{uid: when}` for everything a student was given in the last 45 days: items in app sessions plus questions on Desktop homework sheets (`hw_items`, written by `hwsync` when a sheet is made; a sheet withdrawn before its due date gives its questions back). `pool.make_safe()` then prefers, in order: a fresh question at the requested difficulty, a fresh one at the nearest other difficulty, the question given longest ago. Nothing ever repeats inside one set. If you add a new generator, give it a real uid (not the md5-of-text fallback in `pool.make()`) so repeat-avoidance actually works instead of treating every random variant as unique.

**Python 3.8 compatibility.** `tests/portable_check.py` parses every `.py` file against the 3.8 grammar. Don't use walrus-in-weird-places, `match` statements, or anything newer than 3.8 allows. This is intentional: the tutor's machine and any future packaging shouldn't require chasing a Python upgrade.

**The compression scheme (`pool.mock_plan()`).** The real Digital SAT is 134 minutes, 98 questions, two modules per section with adaptive routing. `mock_plan(minutes)` scales question count and per-question time by `minutes/134`, uniformly, so pacing and domain weights match the real test at any length. This was explicitly surfaced to the tutor as a designed tradeoff, not an arbitrary shortcut, don't change the scaling approach without understanding why (see the git history / prior conversation context) it was built this way.

**Roles.** `need_student()` for student pages; `need_instructor()` for `/instructor/*` (404 unless the request comes from 127.0.0.1/::1). Results, review, lecture and homework work for either; answer keys and lecture answers are instructor-only (students get Hint / Show answer reveals). In templates `s` is always the signed-in student (drives the nav) and `st` is the student being viewed; don't pass a viewed student as `s` on instructor pages.

**First attempts are what get scored.** `responses.correct` is always the first try. Assist levels (`sessions.assist`: `end`/`hint`/`answer`) only change what the student sees; a second try after a hint goes in `retry_answer`/`retry_correct`. Blanks in a submitted *timed* module count as wrong (`db.response_rows`); blanks in untimed practice are ignored.

**Adaptive routing (`app.py: module_score_ratio`, `advance`).** Module 2 becomes the harder variant if the difficulty-weighted share correct in Module 1 is >= `ROUTE_THRESHOLD` (currently 0.60), else the easier variant. This is a deliberate stand-in for the College Board's undisclosed real model. If you change the threshold or the weighting, update `tests/smoke.py`'s routing assertions to match.

**Scoring is explicitly an estimate.** `scoring.py`'s docstring says so. Don't let score numbers creep into the UI or copy as if they were authoritative; "likely range" and "estimate" language is intentional throughout `analytics.py` and the templates.

**Paper homework.** `hwsync` saves each sheet's exact questions in `hw_sheets` (a re-made PDF reuses them, so the printout and the answer entry always match). Students (or the tutor, from the student page) enter answers at `/homework/answers/<id>`; `enter_sheet_answers()` turns them into a finished, untimed session with `mode='homework'`. Blanks are left out, and `scoring.W_HOMEWORK` (x0.5, on top of x0.6 for one skill) keeps paper work from outweighing timed practice. The planner shows it as done on its due date and treats that homework slot as filled; hwsync then moves to the next sheet. An entered sheet is never "forgotten" when the plan changes.

**Reported questions: manual only.** Students report from their review page (`flags`); the tutor retires (`retired`, loaded into `pool.RETIRED`, which `make_safe` never serves) or dismisses at `/instructor/questions`, or retires straight from any review page. Nothing is retired or re-labelled automatically; the tutor asked for it that way.

**Timing.** `analytics.timing()` uses only in-app answers from sets with assist `end` (the clock then measures thinking, not reading explanations) and never paper homework. Findings need five answers behind them and 20 answers per section before anything is said. `svg_timing` draws median seconds by difficulty with the real test's average as a dashed reference line.

## Question bank depth (check `tests/bank_report.py` before assuming otherwise)

Passage-based RW skills (`text_structure_purpose`, `central_ideas`, `coe_textual`, `inferences`, `rhetorical_synthesis`) have 20 hand-written items per difficulty across `rw_content.py` to `rw_content7.py` (60 per skill); hard `cross_text` has 20. That is still the thinnest part of the bank, so single-skill RW practice is capped at `app.RW_SKILL_MAX` (15) questions: about 4 sets, or 4 homework sheets, on one skill before anything repeats inside the 45-day window. Add more with `rec()` / `rs()` in a NEW file (loaded last in `rw_gen.py`) or at the END of the newest one: authored uids are `skill:index`, so inserting in the middle renumbers every later item and breaks repeat-avoidance history. Same rule for `TPAIRS` (transitions), the `B_*` punctuation lists, `XT`, and other indexed lists in `rw_gen.py`.

**Distractor rule.** `tests/rw_quality.py` fails if, in any skill, the correct choice is the longest or the shortest more than 40% of the time, or at either extreme less than 30%. Wrong answers must be as specific as the key (a misread detail, an overreach, true-but-off-goal), and rhetorical-synthesis distractors are full sentences built from the notes. Run it after adding RW items.

Math generators are deep except a few spots in the 40-80 range (`right_tri_trig` easy/hard, `area_volume` hard, `percentages` hard, `circles` easy). Math uids fall back to a hash of the stem plus the sorted choices, so a reshuffled question counts as the same question.

## Charts and themes

Light and dark are both first-class. Every color in `static/app.css` is a token defined once for light, once for dark (OS setting or the Theme button, `static/theme.js`), and print always uses light. Never write a literal color in a template, SVG, or JS: add or reuse a token. Chart roles (`--c-s1..3`, `--div-pos/neg/mid`, `--c-goal`, `--band-op`) come from the dataviz skill's validated palette (colorblind-safe, contrast-checked against these surfaces). Charts follow its rules: one y-axis per chart (the old weekly chart with two axes was split in two), a legend for 2+ series, `data-tip` on marks for hover/keyboard tooltips (`static/charts.js`), and color never the only cue (calendar chips always show a label). Desmos gets `invertedColors` in dark; `static/calc.js` reads the tokens when drawing.

## Frontend notes

No build step by design, plain CSS and vanilla JS. `static/app.css`'s header comment documents the design rationale (booklet/answer-sheet/desk metaphor, specific color tokens); don't introduce a generic SaaS look when extending it. KaTeX is vendored locally under `static/vendor/katex/` (no CDN dependency for math rendering). Desmos loads from its CDN with an API key (`DESMOS_API_KEY` env var); `static/calc.js` is the offline fallback and needs to stay functionally equivalent (graphing, pan/zoom, intersections/intercepts) if Desmos changes.

**Onboarding.** New students go to `/start`: the 1-hour diagnostic (`start_diagnostic`, `mock_plan(60)`, `sessions.purpose='diagnostic'`) or entering an official/Bluebook score (`prior_scores`, used as the estimate's prior). `students.onboard` tracks which.

## Where this is headed

Currently a single-tutor local tool. Longer-term intent (not yet started, don't build toward it prematurely): possible iOS app or commercial product after a few months of real-world use and iteration on UI, backend, and question generation. Keep that in mind as a soft constraint (don't hardcode single-user assumptions any deeper than necessary) but don't over-engineer for multi-tenancy now.
