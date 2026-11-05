"""Round 3 fix-pass re-view: serve out/, scroll-settle lazy images,
check broken images, and take desktop+mobile FULL-PAGE screenshots for
every page (43 doc pages + 3 hubs) into screenshots/review3/.
Writes review3_broken.json."""
import os, sys, json, subprocess, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 'review3')
os.makedirs(SHOT, exist_ok=True)
pages = json.load(open(os.path.join(BASE, 'pages-summary.json')))
slugs = [''] + [p['slug'] for p in pages] + ['services', 'areas', 'guides']
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8911', '--directory', OUT],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
broken = {}
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            executable_path=os.path.expanduser('~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'),
            args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'])
        for slug in slugs:
            name = slug or 'home'
            url = f'http://127.0.0.1:8911/{slug}/' if slug else 'http://127.0.0.1:8911/'
            for label, w, h in (('desktop', 1440, 900), ('mobile', 390, 844)):
                ctx = browser.new_context(viewport={'width': w, 'height': h})
                pg = ctx.new_page()
                pg.goto(url, wait_until='load', timeout=60000)
                # stepwise scroll to settle lazy images
                pg.evaluate("""async () => {
                    const H = document.documentElement.scrollHeight;
                    for (let y = 0; y <= H; y += 800) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
                    window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 400));
                }""")
                bad = pg.evaluate("""() => [...document.querySelectorAll('img')]
                    .filter(i => !i.complete || i.naturalWidth === 0)
                    .map(i => i.getAttribute('src'))""")
                if bad:
                    broken.setdefault(name, {})[label] = bad
                pg.screenshot(path=os.path.join(SHOT, f'{name}-{label}.png'), full_page=True)
                ctx.close()
            print(f'done {name} broken={broken.get(name, {})}')
        browser.close()
finally:
    srv.terminate()
json.dump(broken, open(os.path.join(BASE, 'review3_broken.json'), 'w'), indent=1)
print('BROKEN PAGES:', broken if broken else 'NONE')
print('shots:', len(os.listdir(SHOT)))
