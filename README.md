# Mock SAT (local)

A Flask app for one-on-one Digital SAT tutoring. It runs on your computer, stores everything in one SQLite file (`sat_mock.db`), and needs no internet except for the Desmos calculator (a built-in graphing calculator takes over when offline).

## Run it

    pip install flask
    python app.py          # then open http://127.0.0.1:5000

`run.sh` (macOS/Linux) and `run.bat` (Windows) do the same. Back up `sat_mock.db` to keep student history.

## Weekly use

- **Regular Sunday** (1st to 4th): open *Skills and lectures*, teach one skill from its lecture sheet (30 min), then *Practice > 30-minute session* with feedback on (30 min). The results page names the session's weakest skill and links to a printable **homework sheet** (10 to 15 problems, sized to about 30 minutes, with the "How to do this:" and "What can u see" cover sheet).
- **5th Sunday**: *Mock exam > Hour-long mock*. The home page shows which Sundays are mock days.
- **Dashboard**: score range, weakest and strongest skills, improvement per skill, pacing. *Parent summary* shows the plain-language version and prints cleanly.

## How the pieces map to the official Digital SAT

| Official | Here |
|---|---|
| Reading and Writing: 2 modules, 27 questions, 32 min each | same (full-length mock and full-module practice) |
| Math: 2 modules, 22 questions, 35 min each | same |
| Second module easier or harder based on first | rule in `app.py`: harder if the difficulty-weighted share correct in Module 1 is 60% or more |
| Domain weights (RW 28/26/26/20, Math 35/35/15/15) | every module is built with largest-remainder apportionment to those weights |
| Timer with 5-minute warning, mark for review, cross out, reference sheet, Desmos | all included; the warning scales down in the compressed mock |

**Hour-long mock**: official test length is 134 minutes, so the mock multiplies question counts and time by 55/134 = 0.41. That gives 11 + 11 Reading and Writing questions (13:02 per module) and 9 + 9 Math questions (14:19 per module): 54.7 minutes of testing. Per-question pace and domain shares match the real test. Change the minutes on the setup page to rescale.

## Scoring is an estimate

The College Board does not publish its scoring. `scoring.py` uses a simple item-response model (difficulty levels, a guessing floor, recent answers weighted more) and reports an 80% range that narrows as answers accumulate. Use it to see direction and gaps, and calibrate against a real Bluebook practice test when you have one.

## Questions

All questions are original (not College Board items). Math has parametric generators for all 19 skills at three difficulties. Reading and Writing mixes parametric generators (punctuation, grammar, transitions, data questions, cross-text) with hand-written passages. Difficulty labels are judgments, not measured.

`python tests/bank_report.py` prints how many distinct questions each skill can produce. Some Reading and Writing skills built from hand-written passages have only 4 items per difficulty; add more in `bank/rw_content.py` or `bank/rw_content2.py` with `rec(skill, difficulty, passage, question, correct, wrong1, wrong2, wrong3)`. The app avoids repeating a question a student saw in the last 45 days when it can.

## Desmos

`app.py` loads Desmos with the demo key in `DESMOS_API_KEY`. Get your own free key at desmos.com/api and set the environment variable before running. If Desmos cannot load, the built-in calculator (graphing, intersections, intercepts) appears instead.

## Tests

    python tests/smoke.py       # end-to-end run of practice, adaptive mock, results, dashboard, homework
    python tests/fuzz_math.py   # generators build valid, non-duplicate-choice questions
    python tests/fuzz_rw.py
