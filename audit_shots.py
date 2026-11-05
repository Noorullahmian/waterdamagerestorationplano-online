#!/usr/bin/env python3
"""Section shots for the combined-round image audit. One shard per invocation.
Usage: python3 audit_shots.py <shard> <port>
Shots (desktop 1440x900 viewport unless noted):
  <slug>-hero.png, <slug>-fig<i>.png (split section incl. heading+text+image),
  <slug>-cards<k>.png (full element screenshot of each cards section).
Also writes audit/slotmap-<shard>.json: hero/split/card slots with file + heading/title.
"""
import os, sys, json, subprocess, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright
BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHARDS = {
 'a': ['emergency-water-damage', 'water-extraction', 'structural-drying', 'burst-pipe-cleanup',
       'sewage-cleanup', 'slab-leak', 'water-heater-leak', 'ceiling-leak', 'flood-cleanup',
       'commercial-water-damage'],
 'b': ['hardwood-floor-drying', 'ac-overflow', 'cabinet-drying', 'laundry-overflow',
       'crawl-space-drying', 'appliance-leak', 'fire-sprinkler-cleanup', 'moisture-mapping',
       'attic-insulation-drying', 'wall-drying'],
 'c': ['', 'west-plano', 'legacy-west', 'north-plano', 'central-plano', 'east-plano',
       'frisco', 'allen', 'mckinney', 'richardson', 'murphy', 'services', 'areas', 'guides'],
 'd': ['shut-off-valve', 'warm-spot-on-floor', 'ceiling-dripping', 'water-damage-cost',
       'fans-wont-dry-walls', 'storm-water-category-3', 'mold-after-water-damage',
       'copper-pinhole-leaks', 'sagging-ceiling', 'water-damage-insurance-texas',
       'about', 'contact'],
}
shard, port = sys.argv[1], int(sys.argv[2])
SHOT = os.path.join(BASE, 'screenshots', f'audit-{shard}')
os.makedirs(SHOT, exist_ok=True)
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--directory', OUT],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
slotmap = {}
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--no-sandbox'])
        for slug in SHARDS[shard]:
            name = slug or 'home'
            url = f'http://127.0.0.1:{port}/' if slug == '' else f'http://127.0.0.1:{port}/{slug}/'
            ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
            pg = ctx.new_page()
            try:
                pg.goto(url, wait_until='load', timeout=60000)
                pg.evaluate("""async () => {
                    const H = document.documentElement.scrollHeight;
                    for (let y = 0; y <= H; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
                    window.scrollTo(0, document.documentElement.scrollHeight);
                    await new Promise(r => setTimeout(r, 1200));
                }""")
                info = pg.evaluate("""() => {
                  const f = (u) => u ? u.split('/').pop() : null;
                  const hero = document.querySelector('.hero img');
                  const figs = [...document.querySelectorAll('figure.split-fig')].map((fig, i) => {
                    const sec = fig.closest('section');
                    const h = sec ? (sec.querySelector('h2, h3') || {}).textContent || '' : '';
                    return {i, file: f(fig.querySelector('img') ? fig.querySelector('img').currentSrc : ''), heading: h.trim().slice(0, 120)};
                  });
                  const cardsSecs = [...document.querySelectorAll('section.cards-sec')].map((sec, k) => ({
                    k, title: (sec.querySelector('h2') || {}).textContent || '',
                    cards: [...sec.querySelectorAll('article.card')].map(a => ({
                      href: (a.querySelector('a') || {}).getAttribute ? a.querySelector('a').getAttribute('href') : '',
                      title: (a.querySelector('h3') || {}).textContent || '',
                      file: f(a.querySelector('img') ? a.querySelector('img').currentSrc : '')
                    }))
                  }));
                  return {hero: hero ? f(hero.currentSrc) : null,
                          hero_alt: hero ? hero.alt : '',
                          figs, cardsSecs};
                }""")
                slotmap[name] = info
                # hero viewport shot
                pg.locator('.hero').first.scroll_into_view_if_needed(timeout=10000)
                pg.wait_for_timeout(500)
                pg.screenshot(path=os.path.join(SHOT, f'{name}-hero.png'))
                # one viewport shot per split figure
                nfig = pg.locator('figure.split-fig').count()
                for i in range(nfig):
                    pg.locator('figure.split-fig').nth(i).scroll_into_view_if_needed(timeout=10000)
                    pg.wait_for_timeout(400)
                    pg.screenshot(path=os.path.join(SHOT, f'{name}-fig{i}.png'))
                # full-element shot per cards section
                ncs = pg.locator('section.cards-sec').count()
                for k in range(ncs):
                    try:
                        pg.locator('section.cards-sec').nth(k).screenshot(path=os.path.join(SHOT, f'{name}-cards{k}.png'))
                    except Exception as e:
                        print(f'{name} cards{k} shot failed: {str(e)[:80]}', flush=True)
                print(f'{name}: hero={info["hero"]} figs={len(info["figs"])} cardsSecs={len(info["cardsSecs"])}', flush=True)
            except Exception as e:
                print(f'{name}: ERROR {str(e)[:120]}', flush=True)
                slotmap[name] = {'error': str(e)}
            ctx.close()
        browser.close()
finally:
    srv.terminate()
json.dump(slotmap, open(os.path.join(BASE, 'audit', f'slotmap-{shard}.json'), 'w'), indent=1)
print(f'shard {shard} done -> {SHOT}')
