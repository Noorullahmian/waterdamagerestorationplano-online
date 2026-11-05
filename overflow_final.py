import os, sys, json, subprocess, time
os.environ['TMPDIR']=os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright
BASE=os.path.expanduser('~/workspace/plano3-water-damage'); OUT=os.path.join(BASE,'out')
pages=json.load(open(os.path.join(BASE,'pages-summary.json')))
slugs=['']+[p['slug'] for p in pages]
srv=subprocess.Popen([sys.executable,'-m','http.server','8910','--directory',OUT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
res=[]
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=os.path.expanduser('~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome'), args=['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'])
        for slug in slugs:
            name=slug or 'home'
            url=f'http://127.0.0.1:8910/{slug}/' if slug else 'http://127.0.0.1:8910/'
            for w in (320,390,768,1440):
                ctx=browser.new_context(viewport={'width':w,'height':900}); pg=ctx.new_page()
                pg.goto(url, wait_until='load', timeout=30000)
                ov=pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                res.append({'slug':name,'viewport':f'w{w}','overflow_px':ov})
                ctx.close()
        browser.close()
finally:
    srv.terminate()
json.dump(res, open(os.path.join(BASE,'overflow-final.json'),'w'), indent=1)
print('entries', len(res), 'overflow>0:', [r for r in res if r['overflow_px']>0])
