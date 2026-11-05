"""Round 5 reshoot for the 3 h2 anchors that timed out on scroll_into_view
(mold/storm group-intro kickers, cost factors): scroll via JS instead."""
import os, sys, subprocess, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright
BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 'review5sec')
PLAN = {
    'mold-after-water-damage': ['Hour-by-Hour'],
    'storm-water-category-3': ['How the Water Got In'],
    'water-damage-cost': ['The 4 Things That Set the Price'],
}
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8917', '--directory', OUT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
done, missing = [], []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.path.expanduser('~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'), args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'])
        for slug, texts in PLAN.items():
            url = f'http://127.0.0.1:8917/{slug}/'
            for label, w, h in (('desktop', 1440, 900), ('mobile', 390, 844)):
                ctx = browser.new_context(viewport={'width': w, 'height': h})
                pg = ctx.new_page()
                pg.goto(url, wait_until='load', timeout=60000)
                pg.wait_for_timeout(1500)
                for text in texts:
                    try:
                        loc = pg.locator('h2', has_text=text).first
                        n = loc.count()
                        loc.evaluate('el => el.scrollIntoView({block: "center"})')
                        pg.wait_for_timeout(1200)
                        fname = f"{slug}-h2-{text}-{label}.png"
                        pg.screenshot(path=os.path.join(SHOT, fname))
                        done.append(fname)
                    except Exception as e:
                        missing.append(f'{slug}-{text}-{label}: {str(e)[:120]}')
                ctx.close()
        browser.close()
finally:
    srv.terminate()
print('reshoot done:', done)
print('reshoot missing:', missing if missing else 'NONE')
