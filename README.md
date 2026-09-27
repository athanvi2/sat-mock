# Mock SAT (local)

A Flask app for one-on-one Digital SAT tutoring. It runs on your computer, stores everything in one SQLite file (`sat_mock.db`), and needs no internet except for the Desmos calculator (a built-in graphing calculator takes over when offline).

## Run it

    pip install flask
    python app.py

It prints two addresses:

- **Instructor (this Mac):** http://localhost:5050/instructor. The first visit asks you to choose a 6-digit PIN; then turn on Touch ID in Settings. Instructor view only opens on this Mac.
- **Students (same Wi-Fi):** the `http://<your-mac>.local:5050` address. Students add themselves on the welcome screen with a name and 4-digit PIN. If a device cannot connect, allow Python in System Settings > Network > Firewall.

Port 5050 is used because macOS AirPlay Receiver holds 5000. `run.sh` (macOS/Linux) and `run.bat` (Windows) do the same. Everything is in `sat_mock.db`; the instructor Settings page has a backup button, and a backup is saved automatically before a student is deleted.

## How a student starts

1. Adds themselves (name, PIN, grade, test date, goal).
2. Takes the **1-hour diagnostic** (a scaled adaptive mock: 24 Reading and Writing + 20 Math questions, about 60 minutes), or enters an official SAT/PSAT or Bluebook score instead.
3. Home shows **Up next**: the skills where practice should move the score most, with one-click recommended practice at a difficulty matched to their level.

In practice the student chooses the help level: **hint first** (a wrong first try gets a hint and one more try), **show the answer** after the first try, or **locked until the end**. Only the first try ever counts toward the score estimate.

## Weekly use

- **Regular Sunday** (1st to 4th): teach one skill from its lecture sheet (students see worked examples behind Hint / Show answer; the instructor sees them open), then 30 minutes of practice. The results page names the session's weakest skill and links to a homework sheet; only the instructor can print its answer key.
- **5th Sunday**: *Mock exam > Hour-long mock*.
- **Instructor > student**: score range and timeline (with official scores marked), weekly practice, per-skill mastery, sessions, and a printable **parent summary**.

## For families

- **Guide for families**: `docs/Parent-Guide.pdf` (also at `/guide` in the app, with a live PDF download). It explains the test, the weekly rhythm, the help levels, the score estimate, how the plan is chosen, and privacy. Rebuild it after editing `templates/guide.html` with `python tools/build_guide_pdf.py`.
- **Parent report**: Instructor > student > *Parent report*. Score range and change, practice in the last 30 days, strengths and focus areas, the next four weeks of the plan with the reason for each item, and your note. *Download PDF* uses the Chrome on this Mac.
- **Plan and calendar**: every student has one (*My plan* for students; Instructor > student > *Plan and calendar*). It shows past sessions, today, and the plan, each planned item with a "why", and what changed since the last look. Add notes or "no session" days from the instructor view.
- **Dark mode**: follows the device, or pick Light/Dark with the Theme button (remembered per device). Printouts and PDFs are always light.

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

The College Board does not publish its scoring. `scoring.py` uses a simple item-response model and reports an 80% range. It is built to stay honest: first tries only; blanks in timed sets count as wrong; untimed and single-topic practice count less; no skill or domain can dominate the evidence; untested domains widen the range; an official or Bluebook score anchors it, loosening with time since that test. `python tests/score_check.py` checks, on simulated students, that the 80% range contains the true score about 80% of the time. Entering a real Bluebook practice score is the best calibration available.

## Questions

All questions are original (not College Board items). Math has parametric generators for all 19 skills at three difficulties. Reading and Writing mixes parametric generators (punctuation, grammar, transitions, data questions, cross-text) with hand-written passages. Difficulty labels are judgments, not measured.

`python tests/bank_report.py` prints how many distinct questions each skill can produce. Some Reading and Writing skills built from hand-written passages have only 4 items per difficulty; add more in `bank/rw_content.py` or `bank/rw_content2.py` with `rec(skill, difficulty, passage, question, correct, wrong1, wrong2, wrong3)`. The app avoids repeating a question a student saw in the last 45 days when it can.

## Desmos

`app.py` loads Desmos with the demo key in `DESMOS_API_KEY`. Get your own free key at desmos.com/api and set the environment variable before running. If Desmos cannot load, the built-in calculator (graphing, intersections, intercepts) appears instead.

## Tests

    python tests/smoke.py       # end-to-end: join, diagnostic, assist levels, adaptive routing, instructor lock and student management
    python tests/score_check.py # the score estimate on simulated students
    python tests/plan_check.py  # the calendar follows the rules the parent guide describes
    python tests/fuzz_math.py   # generators build valid, non-duplicate-choice questions
    python tests/fuzz_rw.py
