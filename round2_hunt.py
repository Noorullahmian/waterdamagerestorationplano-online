import json, os, re, subprocess, sys, time
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser("~/workspace/plano3-water-damage")
OUT = os.path.join(BASE, "out")
SHOT = os.path.join(BASE, "screenshots", "round2")
os.makedirs(SHOT, exist_ok=True)
os.makedirs(os.path.join(SHOT, "sections"), exist_ok=True)

SLUGS = ["", "emergency-water-damage", "water-extraction", "structural-drying",
 "burst-pipe-cleanup", "sewage-cleanup", "slab-leak", "water-heater-leak",
 "ceiling-leak", "flood-cleanup", "commercial-water-damage",
 "hardwood-floor-drying", "ac-overflow", "cabinet-drying", "laundry-overflow",
 "crawl-space-drying", "appliance-leak", "fire-sprinkler-cleanup",
 "moisture-mapping", "attic-insulation-drying", "wall-drying",
 "west-plano", "legacy-west", "north-plano", "central-plano", "east-plano",
 "frisco", "allen", "mckinney", "richardson", "murphy",
 "shut-off-valve", "warm-spot-on-floor", "ceiling-dripping", "water-damage-cost",
 "fans-wont-dry-walls", "storm-water-category-3", "mold-after-water-damage",
 "copper-pinhole-leaks", "sagging-ceiling", "water-damage-insurance-texas",
 "about", "contact", "services", "areas", "guides"]
NAME = lambda s: "home" if s == "" else s

def lum(rgb):
    def f(c):
        c /= 255
        return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    r, g, b = rgb
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b)
def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi+0.05)/(lo+0.05)

def parse_rgb(s):
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", s or "")
    return tuple(int(x) for x in m.groups()) if m else None

results = {}
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8896"],
                       cwd=OUT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"),
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"])
        for slug in SLUGS:
            url = f"http://localhost:8896/{slug}/" if slug else "http://localhost:8896/"
            name = NAME(slug)
            rec = {"slug": slug}
            for label, w, h in [("desktop", 1440, 900), ("mobile", 390, 844)]:
                ctx = browser.new_context(viewport={"width": w, "height": h},
                    reduced_motion="reduce" if label == "mobile" else "no-preference")
                page = ctx.new_page()
                page.goto(url, wait_until="networkidle", timeout=60000)
                page.wait_for_timeout(800)
                # slow scroll to trigger lazy + GSAP
                total = page.evaluate("document.body.scrollHeight")
                y = 0
                while y < total:
                    page.evaluate(f"window.scrollTo(0,{y})")
                    page.wait_for_timeout(250)
                    y += 700
                page.evaluate("window.scrollTo(0,0)")
                page.wait_for_timeout(600)
                page.screenshot(path=os.path.join(SHOT, f"{name}-{label}.png"))
                # section viewport shots: at each h2 + hero + footer
                if label == "desktop":
                    secs = page.evaluate("""() => {
                      const out=[];
                      document.querySelectorAll('h2').forEach(h=>{
                        const r=h.getBoundingClientRect(); out.push([h.textContent.trim().slice(0,50), window.scrollY+r.top]);
                      });
                      return out; }""")
                    rec["h2s"] = [s[0] for s in secs]
                    # capture a few mid-page viewports (every ~1800px) for visual scan
                    total = page.evaluate("document.body.scrollHeight")
                    idx = 0
                    yy = 900
                    while yy < total - 200:
                        page.evaluate(f"window.scrollTo(0,{yy})")
                        page.wait_for_timeout(400)
                        page.screenshot(path=os.path.join(SHOT, "sections", f"{name}-s{idx}.png"))
                        idx += 1
                        yy += 1800
                    rec["section_shots"] = idx
                    page.evaluate("window.scrollTo(0,0)")
                    page.wait_for_timeout(400)
                # DOM audit (desktop pass only for most, both for overflow)
                audit = page.evaluate("""() => {
                  const txt = document.body.innerText || '';
                  const lis = [...document.querySelectorAll('li')].map(li=>li.innerText.trim());
                  const strayDot = lis.filter(t=>t==='.'||t==='•'||t==='. .').length;
                  const strayBullet = lis.filter(t=>t===''||t==='•').length;
                  const paras = [...document.querySelectorAll('p')].map(pp=>pp.innerText.trim());
                  const leadColon = paras.filter(t=>t.startsWith(':')).length;
                  const leadComma = paras.filter(t=>t.startsWith(',')).length;
                  const ent = (document.body.innerHTML.match(/&#x27;|&amp;#x27;/g)||[]).length;
                  const h1 = document.querySelectorAll('h1').length;
                  const imgs = [...document.querySelectorAll('img')].map(i=>({src:(i.getAttribute('src')||'').split('/').pop(), alt:(i.getAttribute('alt')||'').slice(0,120), nat:i.naturalWidth+'x'+i.naturalHeight, disp:Math.round(i.getBoundingClientRect().width)+'x'+Math.round(i.getBoundingClientRect().height)}));
                  const broken = imgs.filter(i=>i.nat.startsWith('0x')).length;
                  const map = !!document.querySelector('iframe[src*="google.com/maps"]');
                  const mapSrc = (document.querySelector('iframe[src*="google.com/maps"]')||{}).src || '';
                  const fav = !!document.querySelector('link[rel*="icon"]');
                  const overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
                  const telLinks = [...document.querySelectorAll('a[href^="tel:"]')].length;
                  const oldPhone = txt.includes('945-2118');
                  const oldDom = document.documentElement.innerHTML.includes('waterdamagerestorationplano.org');
                  const newPhone = (txt.match(/\\(972\\) 472-7917/g)||[]).length;
                  const faqBtns = document.querySelectorAll('button[aria-expanded]').length;
                  const radios = [...document.querySelectorAll('input[type=radio]')].map(r=>{const lb=r.closest('label'); return lb? Math.round(lb.getBoundingClientRect().height):-1});
                  const splitFigs = [...document.querySelectorAll('.split figure, figure.split')].length;
                  const footerBtn = document.querySelector('footer a[href^="tel:"]');
                  let footerBtnLines = 0;
                  if (footerBtn){ const r=footerBtn.getBoundingClientRect(); footerBtnLines = Math.round(r.height/20); }
                  return {strayDot, strayBullet, leadColon, leadComma, ent, h1, broken, map, mapSrc, fav, overflow, telLinks, oldPhone, oldDom, newPhone, faqBtns, radios, splitFigs, footerBtnLines, imgCount: imgs.length, lis: lis.length};
                }""")
                rec[label] = audit
                # per-page image list (desktop only)
                if label == "desktop":
                    rec["imgs"] = page.evaluate("""() => [...document.querySelectorAll('img')].map(i=>({src:(i.getAttribute('src')||'').split('/').pop(), alt:(i.getAttribute('alt')||'').slice(0,130)}))""")
                    # overflow at 320/768 too
                    for w2 in (320, 768):
                        page.set_viewport_size({"width": w2, "height": 844})
                        page.wait_for_timeout(400)
                        rec[f"overflow{w2}"] = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                    page.set_viewport_size({"width": 1440, "height": 900})
                # home CTA pill contrast (desktop + mobile)
                if slug == "":
                    rec[f"cta_{label}"] = page.evaluate("""() => {
                      const secs=[...document.querySelectorAll('section')];
                      const dark=secs[secs.length-3]||secs[secs.length-1];
                      const cs=getComputedStyle(dark);
                      const pills=[...dark.querySelectorAll('*')].filter(e=>e.children.length===0 && e.innerText && e.innerText.trim().length>0 && e.innerText.trim().length<60).map(e=>{const c=getComputedStyle(e); return {t:e.innerText.trim(), fg:c.color, bg:c.backgroundColor, fs:c.fontSize}});
                      return {bg:cs.backgroundColor, color:cs.color, pills: pills.slice(0,12)};
                    }""")
                ctx.close()
            results[slug] = rec
            print(f"DONE {name} ov_d={rec['desktop']['overflow']} ov_m={rec['mobile']['overflow']} ov320={rec.get('overflow320')} ov768={rec.get('overflow768')} strayDot={rec['desktop']['strayDot']} leadColon={rec['desktop']['leadColon']} leadComma={rec['desktop']['leadComma']} ent={rec['desktop']['ent']} broken={rec['desktop']['broken']} map={rec['desktop']['map']} imgs={rec['desktop']['imgCount']}", flush=True)
finally:
    srv.terminate()
with open(os.path.join(BASE, "round2_audit.json"), "w") as f:
    json.dump(results, f, indent=1)
print("ALL DONE")
