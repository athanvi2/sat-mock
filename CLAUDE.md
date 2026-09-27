# sat_mock

A local Flask app for 1-on-1 Digital SAT tutoring. One tutor, one student at a time, runs entirely on the tutor's machine, stores everything in a single SQLite file. No build step, no frontend framework: server-rendered Jinja templates plus a couple of hand-written JS files.

Read this file before making changes. It exists so you don't have to rediscover the architecture, the conventions, or the parts that are easy to break, each session.

## Running it

```
source .venv/bin/activate
python app.py
```
Opens on http://127.0.0.1:5000. `SAT_DB` env var overrides the sqlite file path (tests use `/tmp/*.db` so they never touch real student data).

## Testing

Run these after any change to `bank/`, `app.py`, `scoring.py`, `analytics.py`, or a template:

```
python tests/portable_check.py   # confirms code still parses as Python 3.8 (see "Python version" below)
python tests/fuzz_math.py        # every math generator, every difficulty, hundreds of seeds, no crashes/duplicate choices
python tests/fuzz_rw.py          # same for reading & writing
python tests/smoke.py            # end-to-end: practice, adaptive mock routing, results, review, dashboard, homework, every skill's pages
python tests/bank_report.py      # prints how many distinct questions each skill can produce at each difficulty
```

`tests/smoke.py` is the one that actually exercises the Flask app (via `app.test_client()`), including the adaptive module-2 routing logic (plays a high-accuracy and low-accuracy student and checks the harder/easier module gets picked correctly). Don't skip it after touching `app.py`.

There's no visual regression test. After CSS/template changes, actually load the page in a browser and look at it, especially the exam runner (`templates/runner.html` + `static/runner.js`) since it has floating panels, a timer, and keyboard handling that's easy to silently break.

## Architecture

```
bank/
  skills.py       Skill taxonomy: DOMAINS (weights), SKILLS dict (name/see/how/traps/formulas per skill), REFERENCE_HTML
  math_gen.py     19 Math skills x 3 difficulties, parametric generators. GEN dict: skill_key -> fn(rng, difficulty, spr) -> question dict
  rw_gen.py       11 RW skills. Mix of parametric generators and pickers over hand-authored content (rw_content.py / rw_content2.py)
  rw_content.py, rw_content2.py   Hand-written passages/items for skills that can't be parameterized (main idea, inference, rhetorical synthesis, etc.)
  pool.py         Joins math_gen + rw_gen into one GEN dict. build_module() assembles a domain-weighted, difficulty-mixed module in official test order.
                  mock_plan() / full_plan() / session_plan() compute question counts and time limits.
scoring.py        IRT-style (Rasch + guessing floor) score estimation. Documented in its own docstring as an ESTIMATE, not a real College Board model.
db.py             SQLite. Tables: students, sessions, modules, items, responses. No ORM, just q()/x() helpers.
analytics.py      Builds the dashboard payload from db rows + scoring.py. Also renders the SVG ruler/timeline charts server-side (no JS chart lib).
app.py            Flask routes. This is the thickest file; read module_score_ratio()/advance() for the adaptive routing logic before touching it.
templates/        Jinja. base.html is the shell. runner.html + static/runner.js is the exam-taking UI, the most complex piece.
static/app.css    Single stylesheet, hand-rolled design system (see the comment block at the top for the rationale, don't restyle without reading it).
static/calc.js    Offline fallback graphing calculator (used when Desmos's CDN can't load). Has its own expression parser, don't confuse with Desmos integration in runner.js.
```

## Conventions that matter

**Question dict shape.** Every generator returns a dict with at least: `type` (`mc` or `spr`), `passage` (HTML, can be empty string), `q` (the stem), `choices` (list of 4, for mc), `answer` (a letter A-D for mc, or the numeric value/tolerance for spr), `expl` (HTML explanation), `uid` (a string used for de-duplication). `pool.make()` adds `skill`, `d`, `seed`, `section`, `domain`, `skill_name` on top. Don't strip these when refactoring, `app.py` and the templates read them by key.

**uid and repeat-avoidance.** `db.seen_uids()` collects uids a student has answered in the last 45 days; `pool.make_safe()` retries with new seeds to avoid handing out the same uid again. If you add a new generator, give it a real uid (not the md5-of-text fallback in `pool.make()`) so repeat-avoidance actually works instead of treating every random variant as unique.

**Python 3.8 compatibility.** `tests/portable_check.py` parses every `.py` file against the 3.8 grammar. Don't use walrus-in-weird-places, `match` statements, or anything newer than 3.8 allows. This is intentional: the tutor's machine and any future packaging shouldn't require chasing a Python upgrade.

**The compression scheme (`pool.mock_plan()`).** The real Digital SAT is 134 minutes, 98 questions, two modules per section with adaptive routing. `mock_plan(minutes)` scales question count and per-question time by `minutes/134`, uniformly, so pacing and domain weights match the real test at any length. This was explicitly surfaced to the tutor as a designed tradeoff, not an arbitrary shortcut, don't change the scaling approach without understanding why (see the git history / prior conversation context) it was built this way.

**Adaptive routing (`app.py: module_score_ratio`, `advance`).** Module 2 becomes the harder variant if the difficulty-weighted share correct in Module 1 is >= `ROUTE_THRESHOLD` (currently 0.60), else the easier variant. This is a deliberate stand-in for the College Board's undisclosed real model. If you change the threshold or the weighting, update `tests/smoke.py`'s routing assertions to match.

**Scoring is explicitly an estimate.** `scoring.py`'s docstring says so. Don't let score numbers creep into the UI or copy as if they were authoritative; "likely range" and "estimate" language is intentional throughout `analytics.py` and the templates.

## Known thin spots (check `tests/bank_report.py` before assuming otherwise)

Five RW skills are hand-authored with only 4 items per difficulty (12 total each) and will start repeating on a heavy weekly cadence: `text_structure_purpose`, `central_ideas`, `coe_textual`, `inferences`, `rhetorical_synthesis`. `cross_text`'s hard tier is also thin (4 items). Add more via `rec()` calls in `rw_content.py` / `rw_content2.py` rather than trying to parameterize these, they're inherently passage-based.

A few Math skills are thinner at specific difficulties: `percentages`, `right_tri_trig` (medium), `two_var_data` (easy), `circles` (easy).

## Frontend notes

No build step by design, plain CSS and vanilla JS. `static/app.css`'s header comment documents the design rationale (booklet/answer-sheet/desk metaphor, specific color tokens); don't introduce a generic SaaS look when extending it. KaTeX is vendored locally under `static/vendor/katex/` (no CDN dependency for math rendering). Desmos loads from its CDN with an API key (`DESMOS_API_KEY` env var); `static/calc.js` is the offline fallback and needs to stay functionally equivalent (graphing, pan/zoom, intersections/intercepts) if Desmos changes.

## Where this is headed

Currently a single-tutor local tool. Longer-term intent (not yet started, don't build toward it prematurely): possible iOS app or commercial product after a few months of real-world use and iteration on UI, backend, and question generation. Keep that in mind as a soft constraint (don't hardcode single-user assumptions any deeper than necessary) but don't over-engineer for multi-tenancy now.
