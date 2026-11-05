"""Round 5 reshoot C: contact hero/Emergency/form-H2 shots. The earlier
contact 'top' shot landed at page bottom (body anchor does not scroll),
so the post-hero strip + form intro were never actually pictured."""
import os, sys, subprocess, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright
BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 'review5sec')
PLAN = [('contact', 'hero'), ('contact', 'h2-Emergency in Your Plano Home'), ('contact', 'h2-Send Us a Message')]
def locator_for(pg, anchor):
    if anchor == 'hero': return pg.locator('.hero-img')
    if anchor.startswith('h2-'): return pg.locator('h2', has_text=anchor[3:])
    raise ValueError(anchor)
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8919', '--directory', OUT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
done, missing = [], []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.path.expanduser('~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'), args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'])
        for slug, anchor in PLAN:
            url = f'http://127.0.0.1:8919/{slug}/'
            for label, w, h in (('desktop', 1440, 900), ('mobile', 390, 844)):
                ctx = browser.new_context(viewport={'width': w, 'height': h})
                pg = ctx.new_page()
                pg.goto(url, wait_until='load', timeout=60000)
                pg.wait_for_timeout(1500)
                try:
                    loc = locator_for(pg, anchor)
                    loc.first.scroll_into_view_if_needed(timeout=10000)
                    pg.wait_for_timeout(700)
                    fname = f'{slug}-{anchor}-{label}.png'
                    pg.screenshot(path=os.path.join(SHOT, fname))
                    done.append(fname)
                except Exception as e:
                    missing.append(f'{slug}-{anchor}-{label}: {str(e)[:120]}')
                ctx.close()
        browser.close()
finally:
    srv.terminate()
print('reshootC done:', done)
print('reshootC missing:', missing if missing else 'NONE')
