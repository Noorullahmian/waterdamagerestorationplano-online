"""Round 4 fix-pass SECTION re-view (viewport shots, not full-page):
same method as Round 3: slow scroll pass settles lazy images + fires
ScrollTriggers, then one viewport shot per fixed section.
Desktop 1440x900 + mobile 390x844.
Shots: screenshots/review4sec/<page>-<anchor>-<desktop|mobile>.png
Anchors: top | hero | fig-N | h2-SUBSTR | card-HREF | form | text-SUBSTR"""
import os, sys, json, subprocess, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright
BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 'review4sec')
os.makedirs(SHOT, exist_ok=True)
PLAN = {
    '': ['top', 'fig-0', 'fig-2', 'card-/water-extraction/', 'card-/laundry-overflow/', 'card-/flood-cleanup/'],
    'emergency-water-damage': ['hero', 'fig-0', 'fig-1', 'fig-2', 'card-/water-extraction/'],
    'water-extraction': ['hero', 'fig-0', 'fig-1', 'fig-2'],
    'structural-drying': ['fig-0'],
    'burst-pipe-cleanup': ['hero', 'fig-0', 'fig-2'],
    'sewage-cleanup': ['hero', 'fig-0', 'fig-2'],
    'slab-leak': ['hero', 'fig-0', 'fig-1', 'fig-2'],
    'water-heater-leak': ['hero', 'fig-0', 'fig-2'],
    'ceiling-leak': ['hero', 'fig-0', 'fig-1', 'fig-2'],
    'flood-cleanup': ['hero', 'fig-0'],
    'commercial-water-damage': ['hero', 'fig-0', 'fig-1', 'fig-2'],
    'hardwood-floor-drying': ['fig-0', 'fig-1'],
    'ac-overflow': ['hero', 'fig-2', 'card-/ceiling-leak/'],
    'cabinet-drying': ['fig-0', 'fig-1', 'fig-2'],
    'laundry-overflow': ['hero', 'fig-0', 'fig-1'],
    'crawl-space-drying': ['hero', 'fig-0', 'fig-1'],
    'appliance-leak': ['fig-0', 'fig-1', 'fig-2'],
    'fire-sprinkler-cleanup': ['hero', 'fig-0', 'fig-1', 'fig-2'],
    'moisture-mapping': ['fig-1'],
    'attic-insulation-drying': ['fig-0', 'fig-1', 'fig-2', 'card-/ceiling-leak/'],
    'wall-drying': ['hero', 'fig-0', 'fig-1', 'fig-2'],
    'west-plano': ['fig-0', 'fig-2'],
    'legacy-west': ['card-/flood-cleanup/', 'fig-1'],
    'north-plano': ['card-/flood-cleanup/'],
    'central-plano': ['fig-1', 'fig-2', 'card-/ceiling-leak/'],
    'east-plano': ['fig-1', 'card-/flood-cleanup/'],
    'frisco': ['card-/flood-cleanup/', 'fig-1'],
    'allen': ['card-/flood-cleanup/', 'card-/slab-leak/', 'h2-What Allen Homeowners Search'],
    'mckinney': ['fig-2', 'card-/flood-cleanup/', 'card-/slab-leak/', 'h2-What McKinney Homeowners Search'],
    'richardson': ['hero', 'card-/flood-cleanup/', 'card-/slab-leak/', 'h2-What Richardson Residents Search'],
    'murphy': ['card-/flood-cleanup/', 'card-/slab-leak/'],
    'warm-spot-on-floor': ['hero', 'card-/slab-leak/', 'h2-How Under-Floor Drying Works'],
    'ceiling-dripping': ['hero', 'fig-0', 'fig-2', 'text-Get out from under it and call', 'h2-Why Fixing the Source'],
    'water-damage-cost': ['fig-0'],
    'copper-pinhole-leaks': ['h2-The 60-Second Answer', 'h2-Which Plano Homes Are Most at Risk'],
    'shut-off-valve': ['card-/emergency-water-damage/', 'card-/warm-spot-on-floor/'],
    'storm-water-category-3': ['h2-How the Water Got In', 'card-/flood-cleanup/'],
    'mold-after-water-damage': ['h2-Hour-by-Hour', 'fig-2'],
    'about': ['fig-2'],
    'contact': ['h2-Send Us a Message', 'form'],
    'services': ['card-/flood-cleanup/'],
    'areas': ['card-/east-plano/'],
    'guides': ['card-/warm-spot-on-floor/'],
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
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8914', '--directory', OUT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
done, missing = [], []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.path.expanduser('~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'), args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'])
        for slug, anchors in PLAN.items():
            name = slug or 'home'
            url = f'http://127.0.0.1:8914/{slug}/' if slug else 'http://127.0.0.1:8914/'
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
json.dump({'done': done, 'missing': missing}, open(os.path.join(BASE, 'review4sec.json'), 'w'), indent=1)
