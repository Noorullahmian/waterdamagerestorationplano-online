"""Fix-pass re-view screenshots: desktop 1440 + mobile 390 viewports for
every page, plus element shots of the key fixed sections and a computed
style check of the home final CTA (background + text colour)."""
import json, os, subprocess, sys, time
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 're-view')
os.makedirs(SHOT, exist_ok=True)
PORT = 8899

PAGES = ["", "emergency-water-damage", "water-extraction", "structural-drying",
         "burst-pipe-cleanup", "sewage-cleanup", "slab-leak", "water-heater-leak",
         "ceiling-leak", "flood-cleanup", "commercial-water-damage",
         "hardwood-floor-drying", "ac-overflow", "cabinet-drying", "laundry-overflow",
         "crawl-space-drying", "appliance-leak", "fire-sprinkler-cleanup",
         "moisture-mapping", "attic-insulation-drying", "wall-drying",
         "west-plano", "legacy-west", "north-plano", "central-plano", "east-plano",
         "frisco", "allen", "mckinney", "richardson", "murphy",
         "shut-off-valve", "warm-spot-on-floor", "ceiling-dripping",
         "water-damage-cost", "fans-wont-dry-walls", "storm-water-category-3",
         "mold-after-water-damage", "copper-pinhole-leaks", "sagging-ceiling",
         "water-damage-insurance-texas", "about", "contact",
         "services", "areas", "guides"]

srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)],
                       cwd=OUT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
results = {}
try:
    with sync_playwright() as pw:
        bw = pw.chromium.launch(args=['--no-sandbox', '--disable-gpu',
                                      '--disable-dev-shm-usage'])
        for slug in PAGES:
            name = slug or 'home'
            url = f'http://localhost:{PORT}/{slug}/' if slug else f'http://localhost:{PORT}/'
            for label, w, h in [('desktop', 1440, 900), ('mobile', 390, 844)]:
                pg = bw.new_page(viewport={'width': w, 'height': h})
                pg.goto(url, wait_until='networkidle', timeout=30000)
                pg.wait_for_timeout(400)
                pg.screenshot(path=os.path.join(SHOT, f'{name}-{label}.png'))
                pg.close()
            results[name] = 'shot'
        # Element shots + computed CTA colours on home
        pg = bw.new_page(viewport={'width': 1440, 'height': 900})
        pg.goto(f'http://localhost:{PORT}/', wait_until='networkidle')
        pg.wait_for_timeout(400)
        cta = pg.locator('section.block.dark').last
        cta.screenshot(path=os.path.join(SHOT, 'home-final-cta.png'))
        results['home_cta_style'] = pg.evaluate(
            "() => { const el = document.querySelector('section.block.dark');"
            " const cs = getComputedStyle(el); const h = el.querySelector('h2');"
            " return {bg: cs.backgroundColor, color: cs.color,"
            " h2color: h ? getComputedStyle(h).color : null}; }")
        pg.close()
        # Contact radios
        pg = bw.new_page(viewport={'width': 1440, 'height': 900})
        pg.goto(f'http://localhost:{PORT}/contact/', wait_until='networkidle')
        pg.wait_for_timeout(400)
        pg.locator('.radio-row').first.screenshot(path=os.path.join(SHOT, 'contact-radios.png'))
        results['contact_radio_layout'] = pg.evaluate(
            "() => { const r = document.querySelector('.radio-row');"
            " return r ? getComputedStyle(r).display : 'missing'; }")
        pg.close()
        # Hub map
        pg = bw.new_page(viewport={'width': 1440, 'height': 900})
        pg.goto(f'http://localhost:{PORT}/services/', wait_until='networkidle')
        pg.wait_for_timeout(400)
        pg.locator('.map-frame').screenshot(path=os.path.join(SHOT, 'services-hub-map.png'))
        pg.close()
        # Insurance thin related grid
        pg = bw.new_page(viewport={'width': 1440, 'height': 900})
        pg.goto(f'http://localhost:{PORT}/water-damage-insurance-texas/', wait_until='networkidle')
        pg.wait_for_timeout(400)
        pg.locator('.cards.thin').screenshot(path=os.path.join(SHOT, 'insurance-thin-grid.png'))
        pg.close()
        # McKinney hero H1
        pg = bw.new_page(viewport={'width': 1440, 'height': 900})
        pg.goto(f'http://localhost:{PORT}/mckinney/', wait_until='networkidle')
        pg.wait_for_timeout(400)
        pg.locator('.hero h1').screenshot(path=os.path.join(SHOT, 'mckinney-hero-h1.png'))
        results['mckinney_h1_lines'] = pg.evaluate(
            "() => { const h = document.querySelector('.hero h1');"
            " const r = h.getBoundingClientRect(); const lh = parseFloat(getComputedStyle(h).lineHeight);"
            " return Math.round(r.height / lh); }")
        pg.close()
        bw.close()
finally:
    srv.terminate()
json.dump(results, open(os.path.join(SHOT, 'review-checks.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in results.items() if k not in PAGES and k != 'home'}, indent=1))
print('pages shot:', sum(1 for k in results if k in PAGES or k == 'home'))
