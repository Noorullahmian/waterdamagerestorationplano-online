"""Round 2 fix-pass re-view part 2: scrolled VIEWPORT shots (not element
crops) for parser sections, plus figure shots for image-swap slots."""
import os, subprocess, sys, time
os.environ['TMPDIR'] = os.path.expanduser('~/workspace/plano3-water-damage/tmp-chrome')
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
OUT = os.path.join(BASE, 'out')
SHOT = os.path.join(BASE, 'screenshots', 'review2')
os.makedirs(SHOT, exist_ok=True)

# (slug, heading substring, tag) -> viewport shot with heading near top
VIEWPORTS = [
    ("about", "What We Help With", "help-list-vp"),
    ("about", "Honest About Insurance", "insurance-vp"),
    ("about", "We built this site so", "two-things-vp"),
    ("contact", "What We Can Help With", "help-list-vp"),
    ("contact", "Areas We Cover", "areas-vp"),
    ("ceiling-dripping", "What Happens When a Crew Arrives", "crew-list-vp"),
    ("ceiling-dripping", "Specific Help by Source", "source-list-vp"),
    ("copper-pinhole-leaks", "After the Repair", "repair-list-vp"),
    ("", "Nearby Collin County Cities", "cities-list-vp"),
    ("", "Our Services in Plano", "services-cards-vp"),
]
# (slug, figure index 0-based among figure.split on page, tag)
FIGURES = [
    ("mold-after-water-damage", 0, "mold-clock-fig"),
    ("mold-after-water-damage", 2, "hidden-water-fig"),
    ("water-heater-leak", 0, "burst-steps-fig"),
    ("water-heater-leak", 1, "attic-fig"),
    ("hardwood-floor-drying", 1, "cupping-fig"),
    ("burst-pipe-cleanup", 2, "garage-fig"),
    ("shut-off-valve", 2, "fixture-fig"),
    ("water-damage-insurance-texas", 2, "documentation-fig"),
    ("west-plano", 2, "greenbelt-fig"),
    ("east-plano", 2, "sewer-lines-fig"),
    ("richardson", 2, "telecom-fig"),
    ("mckinney", 2, "creek-fig"),
    ("ac-overflow", 2, "drains-fig"),
    ("attic-insulation-drying", 1, "attic-heater-fig"),
    ("sagging-ceiling", 2, "crew-fig"),
    ("crawl-space-drying", 1, "crawl-fig"),
    ("fans-wont-dry-walls", 1, "carpet-pad-fig"),
    ("cabinet-drying", 2, "back-wall-fig"),
    ("storm-water-category-3", 2, "storm-split-fig"),
]
# (slug, tag) hero image shots
HEROS = [("ceiling-dripping", "hero"), ("sagging-ceiling", "hero"),
         ("mold-after-water-damage", "hero"), ("", "hero")]

srv = subprocess.Popen([sys.executable, "-m", "http.server", "8912", "--directory", OUT],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"),
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"])
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        page = ctx.new_page()
        for slug, heading, tag in VIEWPORTS:
            name = slug or "home"
            url = f"http://127.0.0.1:8912/{slug}/" if slug else "http://127.0.0.1:8912/"
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(1000)
            # slow scroll first so lazy images load and layout settles,
            # otherwise the heading position is measured pre-load and the
            # shot lands sections early (review2b first attempt did this)
            total = page.evaluate("document.body.scrollHeight")
            y = 0
            while y < total:
                page.evaluate(f"window.scrollTo(0,{y})")
                page.wait_for_timeout(150)
                y += 900
            page.wait_for_timeout(500)
            ok = page.evaluate("""(txt) => {
              const h = [...document.querySelectorAll('h2')].find(e => e.textContent.includes(txt));
              if (!h) return false;
              window.scrollTo(0, window.scrollY + h.getBoundingClientRect().top - 110);
              return true; }""", heading)
            page.wait_for_timeout(1200)
            if ok:
                page.screenshot(path=os.path.join(SHOT, f"{name}-{tag}.png"))
            else:
                print(f"HEADING NOT FOUND {name} {heading}")
        for slug, idx, tag in FIGURES:
            name = slug or "home"
            url = f"http://127.0.0.1:8912/{slug}/" if slug else "http://127.0.0.1:8912/"
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(500)
            figs = page.locator("figure.split")
            if figs.count() > idx:
                try:
                    figs.nth(idx).scroll_into_view_if_needed(timeout=5000)
                    page.wait_for_timeout(300)
                    figs.nth(idx).screenshot(path=os.path.join(SHOT, f"{name}-{tag}.png"))
                except Exception as e:
                    print(f"FIG FAIL {name}-{tag}: {e}")
            else:
                print(f"FIG MISSING {name}-{tag}: only {figs.count()} figures")
        for slug, tag in HEROS:
            name = slug or "home"
            url = f"http://127.0.0.1:8912/{slug}/" if slug else "http://127.0.0.1:8912/"
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(500)
            try:
                page.locator("img.hero-img").first.screenshot(path=os.path.join(SHOT, f"{name}-{tag}.png"))
            except Exception as e:
                print(f"HERO FAIL {name}: {e}")
        browser.close()
finally:
    srv.terminate()
print("done, shots:", len(os.listdir(SHOT)))
