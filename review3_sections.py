"""Round 3 fix-pass SECTION re-view (viewport shots, not full-page):
full-page stitching hides below-fold .reveal sections (opacity 0 until
ScrollTrigger fires) and late lazy images, so each fixed section gets
its own viewport shot after a slow scroll pass that settles lazy loads
and fires all ScrollTriggers. Desktop 1440x900 + mobile 390x844.
Shots: screenshots/review3sec/<page>-<anchor>-<desktop|mobile>.png
Anchors: top | hero | fig-N (figure.split nth N) | h2-SUBSTR |
card-HREF (article containing that link) | trust | form"""
import os, sys, json, subprocess, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 'review3sec')
os.makedirs(SHOT, exist_ok=True)

# page -> anchors
PLAN = {
    '': ['top', 'fig-1', 'fig-2', 'card-/water-extraction/', 'h2-Our 5-Step'],
    'emergency-water-damage': ['top', 'card-/water-extraction/'],
    'water-extraction': ['hero', 'fig-2'],
    'structural-drying': ['hero', 'h2-While Your Home Is Drying', 'fig-1', 'fig-2'],
    'burst-pipe-cleanup': ['hero', 'fig-1', 'fig-2'],
    'sewage-cleanup': ['fig-0', 'fig-1', 'fig-2'],
    'slab-leak': ['hero', 'fig-0', 'fig-1', 'fig-2', 'h2-What Can Be Saved After a Slab Leak'],
    'water-heater-leak': ['hero', 'fig-0', 'fig-1'],
    'ceiling-leak': ['hero', 'fig-1', 'fig-2'],
    'flood-cleanup': ['h2-What Can Be Saved After Storm Flooding', 'fig-0'],
    'hardwood-floor-drying': ['fig-0'],
    'cabinet-drying': ['h2-The Leaks We See Most'],
    'crawl-space-drying': ['fig-2'],
    'appliance-leak': ['fig-2', 'h2-Related Services'],
    'fire-sprinkler-cleanup': ['h2-Who We Help'],
    'moisture-mapping': ['fig-0', 'fig-1', 'h2-Common Hidden Leaks', 'fig-2'],
    'attic-insulation-drying': ['hero', 'fig-1'],
    'wall-drying': ['fig-0'],
    'west-plano': ['h2-at a Glance', 'h2-Water Damage Cost Estimates in West Plano'],
    'legacy-west': ['h2-at a Glance'],
    'north-plano': ['h2-at a Glance', 'h2-Water Damage Cost Estimates in North Plano', 'fig-2'],
    'central-plano': ['h2-at a Glance', 'h2-Water Damage Cost Estimates in Central Plano', 'fig-0'],
    'east-plano': ['hero', 'h2-at a Glance', 'h2-Water Damage Cost Estimates in East Plano'],
    'frisco': ['h2-at a Glance', 'h2-Water Damage Cost Estimates in Frisco', 'fig-0'],
    'warm-spot-on-floor': ['hero', 'fig-2'],
    'fans-wont-dry-walls': ['hero', 'h2-Signs Your DIY Drying'],
    'water-damage-cost': ['h2-The 4 Things That Set the Price', 'fig-0'],
    'storm-water-category-3': ['fig-0', 'fig-1', 'h2-How the Water Got In'],
    'mold-after-water-damage': ['h2-Hour-by-Hour', 'fig-1'],
    'sagging-ceiling': ['h2-The 6 Safety Steps', 'fig-1'],
    'water-damage-insurance-texas': ['fig-0', 'fig-1', 'fig-2'],
    'about': ['fig-1', 'h2-East Plano (75074)'],
    'contact': ['top', 'h2-Send Us a Message', 'fig-1'],
    'areas': ['top', 'card-/east-plano/', 'card-/legacy-west/'],
    'copper-pinhole-leaks': ['hero', 'fig-0'],
    'murphy': ['hero'],
    'richardson': ['hero', 'fig-0'],
}

def locator_for(pg, anchor):
    if anchor == 'top':
        return pg.locator('body')
    if anchor == 'hero':
        return pg.locator('.hero-img')
    if anchor == 'trust':
        return pg.locator('.trust-band')
    if anchor == 'form':
        return pg.locator('form')
    if anchor.startswith('fig-'):
        return pg.locator('figure.split').nth(int(anchor.split('-')[1]))
    if anchor.startswith('h2-'):
        return pg.locator('h2', has_text=anchor[3:])
    if anchor.startswith('card-'):
        href = anchor[5:]
        return pg.locator(f'article:has(a[href="{href}"])')
    raise ValueError(anchor)

srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8914', '--directory', OUT],
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
            url = f'http://127.0.0.1:8914/{slug}/' if slug else 'http://127.0.0.1:8914/'
            for label, w, h in (('desktop', 1440, 900), ('mobile', 390, 844)):
                ctx = browser.new_context(viewport={'width': w, 'height': h})
                pg = ctx.new_page()
                pg.goto(url, wait_until='load', timeout=60000)
                # slow scroll pass: settle lazy images + fire ScrollTriggers
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
            print(f'done {name}')
        browser.close()
finally:
    srv.terminate()
print('shots:', len(done), 'missing:', missing if missing else 'NONE')
json.dump({'done': done, 'missing': missing}, open(os.path.join(BASE, 'review3sec.json'), 'w'), indent=1)
