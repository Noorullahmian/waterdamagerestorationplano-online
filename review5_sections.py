"""Round 4 fix-pass SECTION re-view (viewport shots, not full-page):
same method as Round 3: slow scroll pass settles lazy images + fires
ScrollTriggers, then one viewport shot per fixed section.
Desktop 1440x900 + mobile 390x844.
Shots: screenshots/review5sec/<page>-<anchor>-<desktop|mobile>.png
Anchors: top | hero | fig-N | h2-SUBSTR | card-HREF | form | text-SUBSTR"""
import os, sys, json, subprocess, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright
BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 'review5sec')
os.makedirs(SHOT, exist_ok=True)
PLAN = {
    '': ['card-/commercial-water-damage/', 'card-/fire-sprinkler-cleanup/', 'card-/sewage-cleanup/'],
    'sewage-cleanup': ['hero'],
    'commercial-water-damage': ['fig-0', 'fig-1'],
    'fire-sprinkler-cleanup': ['fig-1', 'card-/commercial-water-damage/'],
    'water-extraction': ['fig-2'],
    'flood-cleanup': ['card-/water-extraction/'],
    'attic-insulation-drying': ['fig-0'],
    'wall-drying': ['fig-0'],
    'fans-wont-dry-walls': ['fig-0'],
    'allen': ['fig-1'],
    'mold-after-water-damage': ['fig-1', 'h2-Signs the Clock Has Already Run Out', 'h2-Hour-by-Hour'],
    'water-damage-insurance-texas': ['fig-1', 'h2-Mistakes That Can Hurt a Claim'],
    'contact': ['top', 'h2-How to Reach Us', 'h2-What to Have Ready When You Call', 'h2-What Happens After You Call', 'form'],
    'laundry-overflow': ['fig-1'],
    'ac-overflow': ['fig-2'],
    'ceiling-leak': ['fig-1'],
    'west-plano': ['hero'],
    'north-plano': ['hero'],
    'central-plano': ['hero', 'card-/sewage-cleanup/'],
    'crawl-space-drying': ['card-/sewage-cleanup/'],
    'east-plano': ['card-/sewage-cleanup/'],
    'storm-water-category-3': ['h2-How the Water Got In', 'card-/sewage-cleanup/'],
    'services': ['card-/sewage-cleanup/'],
    'areas': ['card-/frisco/', 'card-/mckinney/', 'card-/richardson/'],
    'water-damage-cost': ['h2-The 4 Things That Set the Price'],
}
def locator_for(pg, anchor):
    if anchor == 'top': return pg.locator('body')
    if anchor == 'hero': return pg.locator('.hero-img')
    if anchor == 'form': return pg.locator('form')
    if anchor.startswith('fig-'): return pg.locator('figure.split').nth(int(anchor.split('-')[1]))
    if anchor.startswith('h2-'): return pg.locator('h2', has_text=anchor[3:])
    if anchor.startswith('card-'):
        href = anchor[5:]
        return pg.locator(f'article:has(a[href="{href}"])')
    if anchor.startswith('text-'): return pg.locator('p', has_text=anchor[5:])
    raise ValueError(anchor)
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8915', '--directory', OUT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
done, missing = [], []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.path.expanduser('~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'), args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'])
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
                        pg.screenshot(path=os.path.join(SHOT, f'{name}-{a}-{label}.png'))
                        done.append(f'{name}-{a}-{label}')
                    except Exception as e:
                        missing.append(f'{name}-{a}-{label}: {str(e)[:100]}')
                ctx.close()
            print(f'done {name}', flush=True)
        browser.close()
finally:
    srv.terminate()
print('shots:', len(done), 'missing:', missing if missing else 'NONE')
json.dump({'done': done, 'missing': missing}, open(os.path.join(BASE, 'review5sec.json'), 'w'), indent=1)
