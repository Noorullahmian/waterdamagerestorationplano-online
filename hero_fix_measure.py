#!/usr/bin/env python3
"""Hero-fix verification: measure every hero (46 routes) at 1440 + 390 and
shoot hero viewport screenshots into screenshots/hero-fix/ (same naming as
hero-audit/). Records hero section box, hero img box, computed style
(height/aspect-ratio/object-fit/max-width/class), text-col box, hero img
count + src, and served file. Writes hero-fix.json.
Usage: python3 hero_fix_measure.py [port]
"""
import os, sys, json, time, subprocess
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 'hero-fix')
os.makedirs(SHOT, exist_ok=True)
PAGES = [''] + ['emergency-water-damage', 'water-extraction', 'structural-drying', 'burst-pipe-cleanup',
                'sewage-cleanup', 'slab-leak', 'water-heater-leak', 'ceiling-leak', 'flood-cleanup',
                'commercial-water-damage', 'hardwood-floor-drying', 'ac-overflow', 'cabinet-drying',
                'laundry-overflow', 'crawl-space-drying', 'appliance-leak', 'fire-sprinkler-cleanup',
                'moisture-mapping', 'attic-insulation-drying', 'wall-drying', 'west-plano', 'legacy-west',
                'north-plano', 'central-plano', 'east-plano', 'frisco', 'allen', 'mckinney', 'richardson', 'murphy',
                'shut-off-valve', 'warm-spot-on-floor', 'ceiling-dripping', 'water-damage-cost',
                'fans-wont-dry-walls', 'storm-water-category-3', 'mold-after-water-damage',
                'copper-pinhole-leaks', 'sagging-ceiling', 'water-damage-insurance-texas',
                'about', 'contact', 'services', 'areas', 'guides']

def slugname(s):
    return s if s else 'home'

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8935
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--directory', OUT],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    results = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=['--no-sandbox'])
            for slug in PAGES:
                url = f'http://127.0.0.1:{port}/' if slug == '' else f'http://127.0.0.1:{port}/{slug}/'
                rec = {'slug': slug}
                for w, h in ((1440, 900), (390, 844)):
                    ctx = browser.new_context(viewport={'width': w, 'height': h})
                    page = ctx.new_page()
                    page.goto(url, wait_until='load', timeout=60000)
                    page.wait_for_timeout(500)
                    m = page.evaluate("""() => {
                      const hero = document.querySelector('main .hero') || document.querySelector('.hero');
                      const img = hero ? hero.querySelector('img') : null;
                      const cs = img ? getComputedStyle(img) : null;
                      const r = (el) => el ? {x: Math.round(el.getBoundingClientRect().x), y: Math.round(el.getBoundingClientRect().y), w: Math.round(el.getBoundingClientRect().width), h: Math.round(el.getBoundingClientRect().height)} : null;
                      const grid = hero ? hero.querySelector('.hero-grid') : null;
                      const textCol = grid ? grid.children[0] : null;
                      return {
                        hero_section: r(hero),
                        img: img ? {...r(img), src: (img.getAttribute('src')||'').split('/').pop(), currentSrc: (img.currentSrc||'').split('/').pop(), alt: img.getAttribute('alt'), cls: img.getAttribute('class'), natural: [img.naturalWidth, img.naturalHeight], complete: img.complete} : null,
                        computed: cs ? {height: cs.height, aspectRatio: cs.aspectRatio, objectFit: cs.objectFit, maxWidth: cs.maxWidth, width: cs.width} : null,
                        text_col: r(textCol),
                        hero_img_count: hero ? hero.querySelectorAll('img').length : 0,
                        footer_bottom: (document.querySelector('.footer-bottom')||{}).innerText || ''
                      };
                    }""")
                    rec[str(w)] = m
                    page.screenshot(path=os.path.join(SHOT, f'{slugname(slug)}-hero-{w}.png'))
                    ctx.close()
                results[slug] = rec
                m14, m39 = rec['1440'], rec['390']
                print(f"{slugname(slug):32} 1440 img={m14['img']['w']}x{m14['img']['h']} sec_h={m14['hero_section']['h']} cls={m14['img']['cls']} ar={m14['computed']['aspectRatio']} obj={m14['computed']['objectFit']} | 390 img={m39['img']['w']}x{m39['img']['h']} sec_h={m39['hero_section']['h']} served={m14['img']['currentSrc']}")
    finally:
        srv.terminate()
    json.dump(results, open(os.path.join(BASE, 'hero-fix.json'), 'w'), indent=1)
    # summary
    bad = [s for s, r in results.items() if r['1440']['img']['h'] > 320 or r['390']['img']['h'] > 230]
    print('pages with hero img taller than 320px @1440 or 230px @390:', bad)
    print('1440 img widths:', sorted({r['1440']['img']['w'] for r in results.values()}))
    print('1440 section heights: min', min(r['1440']['hero_section']['h'] for r in results.values()), 'max', max(r['1440']['hero_section']['h'] for r in results.values()))
    print('390 section heights: min', min(r['390']['hero_section']['h'] for r in results.values()), 'max', max(r['390']['hero_section']['h'] for r in results.values()))

if __name__ == '__main__':
    main()
