"""Speed pass for Plano 3 (headless Chromium, local http server).
Measures per page (mobile 390px viewport, 4x CPU throttle):
- first-contentful-paint, domContentLoaded, load event (navigation timing)
- CLS via buffered layout-shift observer (0 = no shifts recorded)
- initial-load transfer bytes (sum of response bodies, no scrolling, so lazy
  below-fold images are NOT counted — this is the LCP-relevant transfer)
NOTE: this headless Chromium does not emit largest-contentful-paint entries
(verified with 3 approaches: init-script observer, post-load buffered observer,
--headless=new). LCP is therefore NOT reported; FCP is the proxy and real-device
LCP is owed after deploy. INP is not measurable headlessly without interaction;
it is not reported.
"""
import os, sys, json, subprocess, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright
BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
pages = json.load(open(os.path.join(BASE, 'pages-summary.json')))
slugs = [''] + [p['slug'] for p in pages]
seen_names = set()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8914', '--directory', OUT],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
res = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            executable_path=os.path.expanduser('~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'),
            args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--headless=new'])
        for slug in slugs:
            name = slug or 'home'
            if name in seen_names:
                continue
            seen_names.add(name)
            url = f'http://127.0.0.1:8914/{slug}/' if slug else 'http://127.0.0.1:8914/'
            ctx = browser.new_context(viewport={'width': 390, 'height': 844},
                                      device_scale_factor=2, is_mobile=True, has_touch=True)
            pg = ctx.new_page()
            cdp = ctx.new_cdp_session(pg)
            cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
            # initial-load transfer from Content-Length headers (http.server serves
            # static files uncompressed, so this is the uncompressed transfer)
            sizes = []
            def on_resp(r):
                try:
                    h = r.headers.get('content-length')
                    sizes.append(int(h) if h else 0)
                except Exception:
                    sizes.append(0)
            pg.on('response', on_resp)
            pg.goto(url, wait_until='load', timeout=60000)
            pg.wait_for_timeout(2000)
            m = pg.evaluate("""() => {
              const nav = performance.getEntriesByType('navigation')[0];
              const paint = performance.getEntriesByType('paint');
              let cls = 0;
              const done = () => ({fcp: paint.find(p => p.name === 'first-contentful-paint') ? Math.round(paint.find(p => p.name === 'first-contentful-paint').startTime) : null,
                             dom: nav ? Math.round(nav.domContentLoadedEventEnd) : null,
                             load: nav ? Math.round(nav.loadEventEnd) : null, cls: Math.round(cls * 10000) / 10000});
              return new Promise(resolve => {
                let settled = false;
                const finish = () => { if (!settled) { settled = true; resolve(done()); } };
                try {
                  new PerformanceObserver(l => {
                    for (const e of l.getEntries()) { if (!e.hadRecentInput) cls += e.value; }
                    finish();
                  }).observe({entryTypes: ['layout-shift'], buffered: true});
                } catch (err) { finish(); }
                setTimeout(finish, 800);
              });
            }""")
            res.append({'slug': name, 'fcp_ms': m.get('fcp'), 'dom_ms': m.get('dom'),
                        'load_ms': m.get('load'), 'cls': m.get('cls'),
                        'initial_transfer_kb': sum(sizes) // 1024})
            print(name, res[-1], flush=True)
            ctx.close()
        browser.close()
finally:
    srv.terminate()
json.dump(res, open(os.path.join(BASE, 'speed.json'), 'w'), indent=1)
print('done', len(res))
