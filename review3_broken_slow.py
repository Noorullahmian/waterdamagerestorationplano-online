"""Slow-settle broken-image check, all 46 pages (desktop viewport):
scroll 400px/300ms + 3s at bottom + scroll to top + 1s, then check
naturalWidth. Supersedes the fast-scroll review3_broken.json artifact."""
import os, sys, json, subprocess, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
PAGES = [''] + sorted(d for d in os.listdir(OUT)
                      if os.path.isdir(os.path.join(OUT, d)) and d not in ('images',))
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8916', '--directory', OUT],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
res = {}
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=os.path.expanduser('~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'),
                               args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'])
        for slug in PAGES:
            name = slug or 'home'
            ctx = b.new_context(viewport={'width': 1440, 'height': 900})
            pg = ctx.new_page()
            pg.goto(f'http://127.0.0.1:8916/{slug}/' if slug else 'http://127.0.0.1:8916/',
                    wait_until='load', timeout=60000)
            pg.evaluate("""async () => {
                const H = document.documentElement.scrollHeight;
                for (let y = 0; y <= H; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 300)); }
                window.scrollTo(0, document.documentElement.scrollHeight);
                await new Promise(r => setTimeout(r, 3000));
                window.scrollTo(0, 0);
                await new Promise(r => setTimeout(r, 1000));
            }""")
            bad = pg.evaluate("""() => [...document.querySelectorAll('img')]
                .filter(i => !i.complete || i.naturalWidth === 0)
                .map(i => i.getAttribute('src'))""")
            total = pg.evaluate("() => document.querySelectorAll('img').length")
            res[name] = {'imgs': total, 'broken': bad}
            print(name, total, 'broken:', bad if bad else 'NONE', flush=True)
            ctx.close()
        b.close()
finally:
    srv.terminate()
json.dump(res, open(os.path.join(BASE, 'review3_broken_slow.json'), 'w'), indent=1)
nbad = sum(len(v['broken']) for v in res.values())
print('TOTAL broken:', nbad, 'pages:', len(res))
