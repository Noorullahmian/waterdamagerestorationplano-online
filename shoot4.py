#!/usr/bin/env python3
"""Round/pass screenshots + DOM measures for the Plano 3 rebuild.
Serves out/ locally, scrolls slowly (settles lazy images + GSAP reveals),
then takes desktop (1440) + mobile (390) full-page screenshots and measures:
overflow at 1440/768/390/320, H1 lines at each width, tap targets <44px,
CLS via layout-shift observer, console errors, split-img served sizes.
Usage: python3 shoot4.py <shotdir> [slug ...]  (no slugs = all pages)
"""
import os, sys, json, time, subprocess, signal
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
PORT = 8931

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

def measure_page(page, url):
    errs = []
    page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.evaluate("""() => {
      window.__cls = 0;
      try {
        new PerformanceObserver((list) => {
          for (const e of list.getEntries()) {
            if (!e.hadRecentInput) window.__cls += e.value;
          }
        }).observe({type: 'layout-shift', buffered: true});
      } catch (e) {}
    }""")
    page.goto(url, wait_until='load', timeout=60000)
    # slow scroll to settle lazy images + reveals
    h = page.evaluate('document.body.scrollHeight')
    y = 0
    while y < h:
        y += 700
        page.evaluate(f'window.scrollTo(0, {y})')
        page.wait_for_timeout(120)
        h = page.evaluate('document.body.scrollHeight')
    page.wait_for_timeout(600)
    page.evaluate('window.scrollTo(0, 0)')
    page.wait_for_timeout(400)
    data = page.evaluate("""() => {
      const out = {};
      out.cls = window.__cls || 0;
      const h1 = document.querySelector('main h1') || document.querySelector('h1');
      if (h1) {
        const cs = getComputedStyle(h1);
        out.h1_lines = Math.round(h1.getBoundingClientRect().height / parseFloat(cs.lineHeight));
        out.h1_text = h1.textContent.trim().slice(0, 80);
      }
      out.splits = [...document.querySelectorAll('figure.split-fig img')].map(img => ({
        src: img.currentSrc.split('/').pop(), w: Math.round(img.getBoundingClientRect().width),
        nat: img.naturalWidth, alt: !!img.alt
      }));
      out.hero = [...document.querySelectorAll('.hero img')].map(img => ({
        src: img.currentSrc.split('/').pop(), w: Math.round(img.getBoundingClientRect().width), nat: img.naturalWidth
      }));
      out.small_targets = [];
      for (const el of document.querySelectorAll('a, button, input, select, textarea')) {
        const r = el.getBoundingClientRect();
        if (r.width > 0 && r.height > 0 && (r.height < 44 || r.width < 44)) {
          out.small_targets.push({tag: el.tagName, h: Math.round(r.height), w: Math.round(r.width),
                                  txt: (el.textContent || el.name || '').trim().slice(0, 40)});
        }
      }
      return out;
    }""")
    data['console_errors'] = errs
    return data

def main():
    shotdir = sys.argv[1]
    only = sys.argv[2:]
    os.makedirs(shotdir, exist_ok=True)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--directory', OUT],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    results = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=['--no-sandbox'])
            for slug in PAGES:
                if only and slug not in only and slugname(slug) not in only:
                    continue
                url = f'http://127.0.0.1:{PORT}/' if slug == '' else f'http://127.0.0.1:{PORT}/{slug}/'
                rec = {'url': url}
                # screenshots + measures at desktop/mobile
                for name, vw, vh in (('desktop', 1440, 900), ('mobile', 390, 844)):
                    ctx = browser.new_context(viewport={'width': vw, 'height': vh})
                    page = ctx.new_page()
                    try:
                        d = measure_page(page, url)
                        rec[name] = d
                        page.screenshot(path=os.path.join(shotdir, f'{slugname(slug)}-{name}.png'), full_page=True)
                    except Exception as e:
                        rec[name] = {'error': str(e)}
                    ctx.close()
                # overflow + h1 lines at 4 widths (fresh contexts, no scroll needed)
                rec['widths'] = {}
                for w in (1440, 768, 390, 320):
                    ctx = browser.new_context(viewport={'width': w, 'height': 900})
                    page = ctx.new_page()
                    try:
                        page.goto(url, wait_until='load', timeout=60000)
                        page.wait_for_timeout(500)
                        rec['widths'][str(w)] = page.evaluate("""() => {
                          const h1 = document.querySelector('main h1') || document.querySelector('h1');
                          const cs = h1 ? getComputedStyle(h1) : null;
                          return {
                            overflow: document.documentElement.scrollWidth - window.innerWidth,
                            h1_lines: h1 ? Math.round(h1.getBoundingClientRect().height / parseFloat(cs.lineHeight)) : null
                          };
                        }""")
                    except Exception as e:
                        rec['widths'][str(w)] = {'error': str(e)}
                    ctx.close()
                results[slug] = rec
                print(f"{slugname(slug):32} desktop_cls={rec.get('desktop', {}).get('cls')} "
                      f"mobile_cls={rec.get('mobile', {}).get('cls')} "
                      f"ov={[rec['widths'][str(w)].get('overflow') for w in (1440, 768, 390, 320)]} "
                      f"h1={[rec['widths'][str(w)].get('h1_lines') for w in (1440, 768, 390, 320)]} "
                      f"smallD={len(rec.get('desktop', {}).get('small_targets', []))} "
                      f"smallM={len(rec.get('mobile', {}).get('small_targets', []))} "
                      f"errs={len(rec.get('desktop', {}).get('console_errors', []))}")
    finally:
        srv.terminate()
    json.dump(results, open(os.path.join(shotdir, 'dom.json'), 'w'), indent=1)
    print(f'shots -> {shotdir}')

if __name__ == '__main__':
    main()
