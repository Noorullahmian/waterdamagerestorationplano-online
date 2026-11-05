"""Round 2 fix-pass re-view: desktop+mobile screenshots for every page,
plus element/section shots for the fixed sections (parser fixes, image
swaps, captions, duplicates). Serves out/ on localhost, Playwright."""
import json, os, subprocess, sys, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 'review2')
os.makedirs(SHOT, exist_ok=True)

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

# Fixed-section element shots: (page slug, css selector description, locator js)
ELEMENTS = [
    ("about", "help-list", "h2:has-text('What We Help With')"),
    ("about", "insurance", "h2:has-text('Honest About Insurance')"),
    ("contact", "help-list", "h2:has-text('What We Can Help With')"),
    ("ceiling-dripping", "crew-list", "h2:has-text('What Happens When a Crew Arrives')"),
    ("ceiling-dripping", "source-list", "h2:has-text('Specific Help by Source')"),
    ("copper-pinhole-leaks", "repair-list", "h2:has-text('After the Repair')"),
    ("home", "cities-list", "h2:has-text('Nearby Collin County Cities')"),
    ("home", "final-cta", "h2:has-text('Stop the Damage Before It Spreads')"),
]

srv = subprocess.Popen([sys.executable, "-m", "http.server", "8911", "--directory", OUT],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
broken = {}
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"),
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"])
        for slug in SLUGS:
            url = f"http://127.0.0.1:8911/{slug}/" if slug else "http://127.0.0.1:8911/"
            name = NAME(slug)
            for label, w, h in [("desktop", 1440, 900), ("mobile", 390, 844)]:
                ctx = browser.new_context(viewport={"width": w, "height": h})
                page = ctx.new_page()
                page.goto(url, wait_until="networkidle", timeout=60000)
                page.wait_for_timeout(800)
                total = page.evaluate("document.body.scrollHeight")
                y = 0
                while y < total:
                    page.evaluate(f"window.scrollTo(0,{y})")
                    page.wait_for_timeout(200)
                    y += 700
                page.evaluate("window.scrollTo(0,0)")
                page.wait_for_timeout(500)
                bad = page.evaluate("""() => [...document.querySelectorAll('img')].filter(i => i.naturalWidth === 0).map(i => i.getAttribute('src'))""")
                broken[f"{name}-{label}"] = bad
                page.screenshot(path=os.path.join(SHOT, f"{name}-{label}.png"))
                ctx.close()
            # element shots on desktop
            ctx = browser.new_context(viewport={"width": 1440, "height": 900})
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(600)
            for pslug, tag, sel in ELEMENTS:
                if pslug != slug:
                    continue
                try:
                    el = page.locator(sel).first
                    el.scroll_into_view_if_needed(timeout=5000)
                    page.wait_for_timeout(400)
                    el.screenshot(path=os.path.join(SHOT, f"{name}-{tag}.png"))
                except Exception as e:
                    print(f"ELEMENT FAIL {name}-{tag}: {e}")
            ctx.close()
        browser.close()
finally:
    srv.terminate()
print("broken images:", {k: v for k, v in broken.items() if v})
print("shots in", SHOT, len(os.listdir(SHOT)))
