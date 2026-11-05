#!/usr/bin/env python3
"""Fast DOM measures only (no screenshots): overflow + H1 lines at 4 widths,
refined tap targets (non-inline only: links/buttons outside <p>/<li>),
split-img served files + display widths, CLS, console errors.
Usage: python3 measure4.py <out.json> [port]"""
import os, sys, json, time, subprocess
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
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

def main():
    outpath = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8933
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--directory', OUT],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    results = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=['--no-sandbox'])
            for slug in PAGES:
                url = f'http://127.0.0.1:{port}/' if slug == '' else f'http://127.0.0.1:{port}/{slug}/'
                rec = {'widths': {}}
                for w in (1440, 768, 390, 320):
                    ctx = browser.new_context(viewport={'width': w, 'height': 900})
                    page = ctx.new_page()
                    page.goto(url, wait_until='load', timeout=60000)
                    page.wait_for_timeout(400)
                    rec['widths'][str(w)] = page.evaluate("""() => {
                      const h1 = document.querySelector('main h1') || document.querySelector('h1');
                      const cs = h1 ? getComputedStyle(h1) : null;
                      return {
                        overflow: document.documentElement.scrollWidth - window.innerWidth,
                        h1_lines: h1 ? Math.round(h1.getBoundingClientRect().height / parseFloat(cs.lineHeight)) : null,
                        h1_w: h1 ? Math.round(h1.getBoundingClientRect().width) : null
                      };
                    }""")
                    ctx.close()
                # desktop deep measure with scroll + CLS + targets + split imgs
                ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
                page = ctx.new_page()
                errs = []
                page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
                page.on('pageerror', lambda e: errs.append(str(e)))
                page.evaluate("""() => { window.__cls = 0;
                  try { new PerformanceObserver((l) => { for (const e of l.getEntries()) { if (!e.hadRecentInput) window.__cls += e.value; } }).observe({type: 'layout-shift', buffered: true}); } catch (e) {} }""")
                page.goto(url, wait_until='load', timeout=60000)
                h = page.evaluate('document.body.scrollHeight')
                y = 0
                while y < h:
                    y += 700
                    page.evaluate(f'window.scrollTo(0, {y})')
                    page.wait_for_timeout(100)
                    h = page.evaluate('document.body.scrollHeight')
                page.wait_for_timeout(500)
                rec['desktop'] = page.evaluate("""() => {
                  const isInline = (el) => !!el.closest('p, li');
                  const small = [];
                  for (const el of document.querySelectorAll('a, button, input, select, textarea')) {
                    if (isInline(el)) continue;
                    const r = el.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0 && (r.height < 44 || r.width < 44)) {
                      small.push({tag: el.tagName, h: Math.round(r.height), w: Math.round(r.width),
                                  txt: (el.textContent || el.name || '').trim().slice(0, 50)});
                    }
                  }
                  return {
                    cls: window.__cls || 0,
                    small_targets: small,
                    splits: [...document.querySelectorAll('figure.split-fig img')].map(img => ({
                      src: img.currentSrc.split('/').pop(), w: Math.round(img.getBoundingClientRect().width), nat: img.naturalWidth })),
                    hero: [...document.querySelectorAll('.hero img')].map(img => ({
                      src: img.currentSrc.split('/').pop(), w: Math.round(img.getBoundingClientRect().width), nat: img.naturalWidth }))
                  };
                }""")
                rec['desktop']['console_errors'] = errs
                ctx.close()
                results[slug] = rec
                print(f"{slug or 'home':32} ov={[rec['widths'][str(w)]['overflow'] for w in (1440, 768, 390, 320)]} "
                      f"h1={[rec['widths'][str(w)]['h1_lines'] for w in (1440, 768, 390, 320)]} "
                      f"cls={rec['desktop']['cls']} small={len(rec['desktop']['small_targets'])} errs={len(errs)}")
    finally:
        srv.terminate()
    json.dump(results, open(outpath, 'w'), indent=1)
    print('->', outpath)

if __name__ == '__main__':
    main()
