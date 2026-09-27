"""Regenerate docs/Parent-Guide.pdf from templates/guide.html. Run:  python tools/build_guide_pdf.py
The app also serves the same PDF live at /guide.pdf; this keeps a copy in the repo to email or print."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault('SAT_DB', os.path.join(ROOT, '.guide-build.db'))  # never touch student data
import app as A  # noqa: E402
import pdfout  # noqa: E402
import planner  # noqa: E402

with A.app.test_request_context('/guide'):
    html = A.render_template('guide.html', pdf=True, rules=planner.RULES, can_pdf=False)
out = os.path.join(ROOT, 'docs', 'Parent-Guide.pdf')
with open(out, 'wb') as fh:
    fh.write(pdfout.html_to_pdf(html))
for f in (os.environ['SAT_DB'],):
    if f.endswith('.guide-build.db') and os.path.exists(f): os.remove(f)
print('wrote', out, os.path.getsize(out), 'bytes')
