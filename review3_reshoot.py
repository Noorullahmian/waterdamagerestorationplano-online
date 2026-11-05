"""Round 3 fix-pass RE-SHOOT after the final rebuild (water-heater/attic/phrase
changes): viewport shots with slow scroll settle, desktop 1440x900 +
mobile 390x844. Port 8915 (overflow run uses 8910; this build is final, so
both read the same out/). Output suffix -r2 so the pre-fix shots stay as
evidence of the failure. Does NOT touch review3sec.json."""
import os, sys, json, subprocess, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 'review3sec')
os.makedirs(SHOT, exist_ok=True)

PLAN = {
    'water-heater-leak': ['hero'],
    'attic-insulation-drying': ['fig-1'],
    '': ['card-/water-heater-leak/'],
    'moisture-mapping': ['h2-Common Hidden Leaks'],
}

def locator_for(pg, anchor):
    if anchor == 'hero':
        return pg.locator('.hero-img')
    if anchor.startswith('fig-'):
        return pg.locator('figure.split').nth(int(anchor.split('-')[1]))
    if anchor.startswith('h2-'):
        return pg.locator('h2', has_text=anchor[3:])
    if anchor.startswith('card-'):
        href = anchor[5:]
        return pg.locator(f'article:has(a[href="{href}"])')
    raise ValueError(anchor)

srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8915', '--directory', OUT],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
done, missing = [], []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            executable_path=os.path.expanduser('~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'),
            args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'])
        for slug, anchors in PLAN.items():
            name = slug or 'home'
            url = f'http://127.0.0.1:8915/{slug}/' if slug else 'http://127.0.0.1:8915/'
            for label, w, h in (('desktop', 1440, 900), ('mobile', 390, 844)):
                ctx = browser.new_context(viewport={'width': w, 'height': h})
                pg = ctx.new_page()
                pg.goto(url, wait_until='load', timeout=60000)
                pg.evaluate("""async () => {
                    const H = document.documentElement.scrollHeight;
                    for (let y = 0; y <= H; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 200)); }
                    window.scrollTo(0, document.documentElement.scrollHeight);
                    await new Promise(r => setTimeout(r, 1500));
                }""")
                for a in anchors:
                    try:
                        loc = locator_for(pg, a)
                        loc.first.scroll_into_view_if_needed(timeout=10000)
                        pg.wait_for_timeout(700)
                        pg.screenshot(path=os.path.join(SHOT, f'{name}-{a}-{label}-r2.png'))
                        done.append(f'{name}-{a}-{label}-r2')
                    except Exception as e:
                        missing.append(f'{name}-{a}-{label}-r2: {str(e)[:100]}')
                ctx.close()
            print(f'done {name}')
        browser.close()
finally:
    srv.terminate()
print('shots:', len(done), 'missing:', missing if missing else 'NONE')
json.dump({'done': done, 'missing': missing}, open(os.path.join(BASE, 'review3_reshoot.json'), 'w'), indent=1)
