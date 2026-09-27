"""HTML -> PDF with a locally installed Chrome/Chromium in headless mode. No Python PDF dependency: the pages already have
print styles (app.css @media print forces the light palette), and Chrome runs KaTeX before printing, so math renders.
Set CHROME_PATH to use a specific browser. If none is found, callers fall back to the browser's own Print > Save as PDF."""
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CANDIDATES = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
]


def chrome():
    p = os.environ.get('CHROME_PATH')
    if p and os.path.exists(p): return p
    for c in CANDIDATES:
        if os.path.exists(c): return c
    for name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome'):
        w = shutil.which(name)
        if w: return w
    return None


def available():
    return chrome() is not None


def html_to_pdf(html, timeout=60):
    """Render an HTML string (which references /static/...) to PDF bytes."""
    exe = chrome()
    if not exe: raise RuntimeError('No Chrome or Chromium found for PDF export (set CHROME_PATH).')
    static = 'file://' + os.path.join(HERE, 'static').replace(os.sep, '/')
    if not static.startswith('file:///'): static = 'file:///' + static[len('file://'):]
    html = html.replace('"/static/', '"%s/' % static)
    d = tempfile.mkdtemp(prefix='satpdf-')
    try:
        src, out = os.path.join(d, 'page.html'), os.path.join(d, 'page.pdf')
        with open(src, 'w', encoding='utf-8') as fh: fh.write(html)
        subprocess.run([exe, '--headless=new', '--disable-gpu', '--no-first-run', '--allow-file-access-from-files',
                        '--no-pdf-header-footer', '--virtual-time-budget=6000', '--print-to-pdf=' + out, 'file://' + src.replace(os.sep, '/')],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout, check=False)
        if not os.path.exists(out) or os.path.getsize(out) < 500:
            raise RuntimeError('Chrome did not produce a PDF.')
        with open(out, 'rb') as fh: return fh.read()
    finally:
        shutil.rmtree(d, ignore_errors=True)
