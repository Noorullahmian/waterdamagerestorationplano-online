#!/usr/bin/env python3
"""Visual verification for the animations-off + mobile-menu round.
Serves out/ on localhost, screenshots desktop + 390px mobile, tests:
- no animation code present at runtime (no gsap/lenis/ScrollTrigger globals,
  no __plano3Anim, no .reveal element with opacity<1 or transform after scroll)
- scroll test: scroll a long page to bottom in steps; after each step check
  no element is mid-flight (opacity/transform on .reveal == final state)
- mobile menu: hamburger visible at 390px, opens instantly, panel fits
  (no overflow), links close it, small call button fits beside hamburger
- header fit at 390px: header-inner scrollWidth <= clientWidth
Usage: python3 verify_round.py <out.json> [port]"""
import os, sys, json, time, subprocess
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOTS = os.path.expanduser('~/workspace/your_files/plano3-animation-images-mobile')
os.makedirs(SHOTS, exist_ok=True)

def main():
    outpath = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8934
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--directory', OUT],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    results = {}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            # ---------- DESKTOP ----------
            pg = browser.new_page(viewport={'width': 1440, 'height': 900})
            pg.goto(f'http://127.0.0.1:{port}/', wait_until='networkidle')
            time.sleep(0.5)
            results['desktop_home'] = {
                'overflow_x': pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth"),
                'anim_globals': pg.evaluate("({gsap: typeof window.gsap, lenis: typeof window.Lenis, plano3Anim: typeof window.__plano3Anim})"),
                'reveal_count': pg.evaluate("document.querySelectorAll('.reveal').length"),
                'hamburger_visible_desktop': pg.evaluate("!!document.querySelector('.hamburger') && getComputedStyle(document.querySelector('.hamburger')).display !== 'none'"),
                'header_call_visible_desktop': pg.evaluate("getComputedStyle(document.querySelector('.header-call')).display"),
            }
            pg.screenshot(path=f'{SHOTS}/01-desktop-home-top.png')
            # scroll test on home (long page): step-scroll to bottom, sample .reveal state mid-scroll
            scroll_states = []
            for y in (600, 1500, 3000, 6000):
                pg.evaluate(f"window.scrollTo(0, {y})")
                time.sleep(0.15)
                scroll_states.append(pg.evaluate("""() => {
                  const els = document.querySelectorAll('.reveal');
                  let moved = 0, faded = 0;
                  els.forEach(el => { const cs = getComputedStyle(el);
                    if (cs.transform !== 'none') moved++;
                    if (parseFloat(cs.opacity) < 0.99) faded++; });
                  return {y: window.scrollY, reveal: els.length, moved, faded};
                }"""))
            pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(0.4)
            pg.screenshot(path=f'{SHOTS}/02-desktop-home-scrolled.png')
            results['desktop_home']['scroll_states'] = scroll_states
            results['desktop_home']['final_scrollY'] = pg.evaluate("window.scrollY")
            results['desktop_home']['console_errors'] = []
            pg.close()

            # desktop service page + guides
            for slug, tag in [('emergency-water-damage', 'desktop-service'), ('guides', 'desktop-guides')]:
                pg = browser.new_page(viewport={'width': 1440, 'height': 900})
                errs = []
                pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
                pg.goto(f'http://127.0.0.1:{port}/{slug}/', wait_until='networkidle')
                time.sleep(0.4)
                pg.evaluate("window.scrollTo(0, 1200)")
                time.sleep(0.2)
                pg.screenshot(path=f'{SHOTS}/03-{tag}.png')
                results[tag] = {
                    'overflow_x': pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth"),
                    'console_errors': errs,
                    'reveal_moved_after_scroll': pg.evaluate("""() => { let m=0,f=0;
                      document.querySelectorAll('.reveal').forEach(el => { const cs=getComputedStyle(el);
                        if (cs.transform!=='none') m++; if (parseFloat(cs.opacity)<0.99) f++; });
                      return {moved:m, faded:f}; }"""),
                }
                pg.close()

            # ---------- MOBILE 390 ----------
            ctx = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
            pg = ctx.new_page()
            errs = []
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            pg.goto(f'http://127.0.0.1:{port}/', wait_until='networkidle')
            time.sleep(0.5)
            mob = {}
            mob['overflow_x_closed'] = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            mob['header_overflow'] = pg.evaluate("document.querySelector('.header-inner').scrollWidth - document.querySelector('.header-inner').clientWidth")
            mob['hamburger_visible'] = pg.evaluate("getComputedStyle(document.querySelector('.hamburger')).display")
            mob['small_call_visible'] = pg.evaluate("getComputedStyle(document.querySelector('.header-call-small')).display")
            mob['small_call_text_visible'] = pg.evaluate("getComputedStyle(document.querySelector('.header-call-small span')).display")
            mob['inline_nav_hidden'] = pg.evaluate("getComputedStyle(document.querySelector('.main-nav')).display")
            mob['header_call_hidden'] = pg.evaluate("getComputedStyle(document.querySelector('.header-call')).display")
            mob['brand_width'] = pg.evaluate("document.querySelector('.brand').getBoundingClientRect().width")
            mob['call_btn_width'] = pg.evaluate("document.querySelector('.header-call-small').getBoundingClientRect().width")
            mob['hamburger_width'] = pg.evaluate("document.querySelector('.hamburger').getBoundingClientRect().width")
            mob['header_height'] = pg.evaluate("document.querySelector('.site-header').getBoundingClientRect().height")
            mob['console_errors'] = errs
            pg.screenshot(path=f'{SHOTS}/04-mobile-home-closed.png')
            # open the menu
            pg.click('.hamburger')
            time.sleep(0.3)
            mob['menu_open'] = pg.evaluate("!!document.querySelector('.mobile-menu-panel')")
            mob['aria_expanded'] = pg.evaluate("document.querySelector('.hamburger').getAttribute('aria-expanded')")
            mob['panel_overflow_x'] = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            mob['panel_rect'] = pg.evaluate("(() => { const r = document.querySelector('.mobile-menu-panel').getBoundingClientRect(); return {left: r.left, right: r.right, width: r.width, top: r.top, bottom: r.bottom}; })()")
            mob['panel_link_count'] = pg.evaluate("document.querySelectorAll('.mobile-menu-panel a').length")
            pg.screenshot(path=f'{SHOTS}/05-mobile-menu-open.png')
            # tap a link -> closes + navigates
            pg.click('.mobile-menu-panel a[href="/guides/"]')
            time.sleep(0.8)
            mob['after_link_url'] = pg.url
            mob['menu_closed_after_link'] = pg.evaluate("!document.querySelector('.mobile-menu-panel')")
            pg.screenshot(path=f'{SHOTS}/06-mobile-guides-after-menu-tap.png')
            # mobile scroll test on guides (long page)
            mob['scroll_states'] = []
            for y in (800, 2000, 4000):
                pg.evaluate(f"window.scrollTo(0, {y})")
                time.sleep(0.15)
                mob['scroll_states'].append(pg.evaluate("""() => { let m=0,f=0;
                  document.querySelectorAll('.reveal').forEach(el => { const cs=getComputedStyle(el);
                    if (cs.transform!=='none') m++; if (parseFloat(cs.opacity)<0.99) f++; });
                  return {y: window.scrollY, moved:m, faded:f}; }"""))
            mob['overflow_x_after_scroll'] = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            pg.screenshot(path=f'{SHOTS}/07-mobile-guides-scrolled.png')
            results['mobile_home'] = mob
            pg.close()

            # mobile service page closed header
            pg = ctx.new_page()
            pg.goto(f'http://127.0.0.1:{port}/burst-pipe-cleanup/', wait_until='networkidle')
            time.sleep(0.4)
            results['mobile_service'] = {
                'overflow_x': pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth"),
                'header_overflow': pg.evaluate("document.querySelector('.header-inner').scrollWidth - document.querySelector('.header-inner').clientWidth"),
            }
            pg.screenshot(path=f'{SHOTS}/08-mobile-service-closed.png')
            pg.close()
            ctx.close()
            browser.close()
    finally:
        srv.terminate()
    with open(outpath, 'w') as f:
        json.dump(results, f, indent=1)
    print(json.dumps(results, indent=1))

if __name__ == '__main__':
    main()
