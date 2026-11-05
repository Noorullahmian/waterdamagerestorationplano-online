"""Round 5 reshoot B: correct locators — group-intro headings are now
kicker <p> elements (not H2), and cost '4 Things' is an H3 (not H2).
That is why the first reshoot's h2 anchors found nothing."""
import os, sys, subprocess, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright
BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 'review5sec')
# (slug, selector, has_text, filename-stem)
PLAN = [
    ('mold-after-water-damage', 'p.section-kicker', 'Hour-by-Hour', 'mold-after-water-damage-kicker-Hour-by-Hour'),
    ('storm-water-category-3', 'p.section-kicker', 'How the Water Got In', 'storm-water-category-3-kicker-How-the-Water-Got-In'),
    ('water-damage-cost', 'h3', 'The 4 Things That Set the Price', 'water-damage-cost-h3-The-4-Things'),
]
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8918', '--directory', OUT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
done, missing = [], []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.path.expanduser('~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'), args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'])
        for slug, sel, text, stem in PLAN:
            url = f'http://127.0.0.1:8918/{slug}/'
            for label, w, h in (('desktop', 1440, 900), ('mobile', 390, 844)):
                ctx = browser.new_context(viewport={'width': w, 'height': h})
                pg = ctx.new_page()
                pg.goto(url, wait_until='load', timeout=60000)
                pg.wait_for_timeout(1500)
                loc = pg.locator(sel, has_text=text).first
                if loc.count() == 0:
                    missing.append(f'{stem}-{label}: count 0')
                else:
                    loc.evaluate('el => el.scrollIntoView({block: "center"})')
                    pg.wait_for_timeout(1200)
                    fname = f'{stem}-{label}.png'
                    pg.screenshot(path=os.path.join(SHOT, fname))
                    done.append(fname)
                ctx.close()
        browser.close()
finally:
    srv.terminate()
print('reshootB done:', done)
print('reshootB missing:', missing if missing else 'NONE')
