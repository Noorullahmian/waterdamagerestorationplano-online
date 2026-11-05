#!/usr/bin/env python3
"""Purge-round checks: (1) footer 'Call 24/7' button overflow measurement at
1440 + 390 — computed button width vs text width, padding, and whether the
button overflows its footer column; (2) fresh desktop screenshots of the
water-extraction page (the only page changed by the 4406597 purge).
Serves out/ over http.server, drives headless Chromium via Playwright.
Usage: python3 footer_btn_measure.py [port]
Writes screenshots/purge-4406597/footer-btn.json + PNGs.
"""
import os, sys, json, time, subprocess
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 'purge-4406597')
os.makedirs(SHOT, exist_ok=True)

MEASURE_JS = """() => {
  const btn = document.querySelector('footer .btn-call');
  if (!btn) return {found: false};
  const cs = getComputedStyle(btn);
  const r = btn.getBoundingClientRect();
  const span = btn.querySelector('.nowrap');
  const sr = span ? span.getBoundingClientRect() : null;
  const col = btn.closest('div');
  const cr = col ? col.getBoundingClientRect() : null;
  const grid = btn.closest('.footer-grid');
  const gr = grid ? grid.getBoundingClientRect() : null;
  // text width: measure the full label as one line via a Range over the <a>
  const range = document.createRange();
  range.selectNodeContents(btn);
  const tr = range.getBoundingClientRect();
  return {
    found: true,
    label: btn.textContent.trim(),
    btn: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
          right: Math.round(r.right), scrollW: btn.scrollWidth, clientW: btn.clientWidth,
          scrollH: btn.scrollHeight, clientH: btn.clientHeight},
    text_range: {w: Math.round(tr.width), h: Math.round(tr.height)},
    nowrap_span: sr ? {x: Math.round(sr.x), w: Math.round(sr.width), right: Math.round(sr.right)} : null,
    computed: {paddingLeft: cs.paddingLeft, paddingRight: cs.paddingRight,
               paddingTop: cs.paddingTop, paddingBottom: cs.paddingBottom,
               fontSize: cs.fontSize, fontWeight: cs.fontWeight,
               whiteSpace: cs.whiteSpace, display: cs.display},
    column: cr ? {x: Math.round(cr.x), w: Math.round(cr.width), right: Math.round(cr.right)} : null,
    footer_grid: gr ? {x: Math.round(gr.x), w: Math.round(gr.width), right: Math.round(gr.right)} : null,
    // gaps: text edge to button inner edge (padding actually present)
    text_to_right_edge: sr ? Math.round(r.right - sr.right) : null,
    text_to_left_edge: Math.round(r.x + parseFloat(cs.paddingLeft) - tr.x),
    btn_overflows_column: cr ? (Math.round(r.right) > Math.round(cr.right) || Math.round(r.x) < Math.round(cr.x)) : null,
    text_overflows_btn: btn.scrollWidth > btn.clientWidth,
    doc_overflow_x: document.documentElement.scrollWidth > document.documentElement.clientWidth
  };
}"""

def main():
    port = int(sys.argv[1]) if len(sys.argv[1:]) else 8941
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--directory', OUT],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    results = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=['--no-sandbox'])
            # --- footer button at 1440 + 390 ---
            for w, h in ((1440, 900), (390, 844)):
                ctx = browser.new_context(viewport={'width': w, 'height': h})
                page = ctx.new_page()
                page.goto(f'http://127.0.0.1:{port}/', wait_until='load', timeout=60000)
                page.wait_for_timeout(500)
                m = page.evaluate(MEASURE_JS)
                results[f'footer_btn_{w}'] = m
                footer = page.query_selector('footer')
                if footer:
                    footer.screenshot(path=os.path.join(SHOT, f'footer-{w}.png'))
                ctx.close()
            # --- water-extraction desktop screenshots ---
            ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
            page = ctx.new_page()
            page.goto(f'http://127.0.0.1:{port}/water-extraction/', wait_until='load', timeout=60000)
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(SHOT, 'water-extraction-desktop.png'), full_page=True)
            # clip the replaced split section via element screenshot (robust to scroll)
            sec_el = page.evaluate_handle("""() => {
              const figs = [...document.querySelectorAll('.split-fig img')];
              const img = figs.find(i => (i.getAttribute('src')||'').includes('plumber-work-6419128'));
              return img ? img.closest('section') : null;
            }""")
            sec = None
            if sec_el:
                try:
                    sec_el.as_element().screenshot(path=os.path.join(SHOT, 'water-extraction-split-across-plano.png'))
                    sec = page.evaluate("""() => {
                      const figs = [...document.querySelectorAll('.split-fig img')];
                      const img = figs.find(i => (i.getAttribute('src')||'').includes('plumber-work-6419128'));
                      if (!img) return null;
                      const h = img.closest('section').querySelector('h2');
                      return {section_heading: h ? h.textContent.trim() : null,
                              img_src: img.getAttribute('src'), img_alt: img.getAttribute('alt')};
                    }""")
                except Exception as e:
                    sec = {'error': str(e)}
            results['water_extraction_split_clip'] = sec
            ctx.close()
            browser.close()
    finally:
        srv.terminate()
    json.dump(results, open(os.path.join(SHOT, 'footer-btn.json'), 'w'), indent=1)
    for k, v in results.items():
        if k.startswith('footer_btn_'):
            print(k, '->', json.dumps(v))
    print('shots in', SHOT)

if __name__ == '__main__':
    main()
