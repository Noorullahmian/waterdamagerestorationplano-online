"""Round 5 fix-pass DOM checks on built out/ HTML (static, no browser).
Adapted from r4_dom_check.py: same generic gates + R5-specific assertions
(group-intro kickers, mold/insurance list tails, contact fragments,
cost factor hierarchy, swapped split/card chains, allen topic caption).
R5 adds NO global file ban: every R5-flagged file that still renders does
so only in an unflagged slot or a pool-limited OPEN slot (see BLUNDER_HUNT.md).
"""
import json, os, re, ast, html
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'out')
FAIL, OK = [], []
def check(name, cond, detail=''):
    (OK if cond else FAIL).append(f"{name} {detail if not cond else ''}")
def read(slug):
    p = os.path.join(OUT, 'index.html') if slug == '' else os.path.join(OUT, slug, 'index.html')
    return open(p).read()
def main_text(h):
    m = re.search(r'<main>(.*?)</main>', h, re.S)
    return m.group(1) if m else h
def strip_tags(t):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html.unescape(t))).strip()
tree = ast.parse(open(os.path.join(BASE, 'gen3_render.py')).read())
BANNED = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'BANNED' for t in node.targets):
        BANNED = {e.value for e in node.value.elts if isinstance(e, ast.Constant)}
check('banned set parsed', len(BANNED) >= 40, str(len(BANNED)))
BAD_CAPTIONS = ['depicting resilience', 'visible water runoff', 'metal wrench on a stainless steel sink',
 'Serene stone residence with rustic charm', 'Lovely red brick suburban house', 'unique ceiling design', 'eclectic bed setup',
 'Stylish and clean laundry space', 'Explore this spacious unfinished basement', 'deserted, dimly lit room', 'Abstract image of',
 'offering a textured urban look', 'washer near container under wicker basket', 'Creative lamps hanging over table']
slugs = [''] + sorted([d for d in os.listdir(OUT) if os.path.isdir(os.path.join(OUT, d)) and d not in ('_next', '404', 'images')])
check('46 slugs', len(slugs) == 46, str(len(slugs)))
for slug in slugs:
    try: h = read(slug)
    except FileNotFoundError: FAIL.append(f'{slug or "home"} MISSING'); continue
    t = main_text(h)
    imgs = re.findall(r'<img[^>]+src="/images/([^"]+)"', t)
    check(f'{slug or "home"} no same-page dup img', len(imgs) == len(set(imgs)), str(imgs))
    check(f'{slug or "home"} no banned file', not any(f in BANNED for f in imgs), str([f for f in imgs if f in BANNED]))
    check(f'{slug or "home"} no dot bullets', '•' not in strip_tags(t))
    check(f'{slug or "home"} no dangling See H2', not any(x.rstrip().endswith('See') for x in re.findall(r'<h2>(.*?)</h2>', t)))
    check(f'{slug or "home"} no H2 >150 chars', not any(len(x) > 150 for x in re.findall(r'<h2>(.*?)</h2>', t)))
    s = set(imgs)
    check(f'{slug or "home"} no inspector same-shoot pair', not ({'moisture-meter-8293640.webp', 'moisture-meter-8293746.webp'} <= s), str(s))
    check(f'{slug or "home"} no wall/moisture same-shoot pair', not ({'moisture-meter-8482824.webp', 'moisture-meter-8293640.webp'} <= s), str(s))
    check(f'{slug or "home"} no crawl same-shoot pair', not ({'crawl-space-4092026.webp', 'crawl-space-4092030.webp'} <= s), str(s))
    for bad in BAD_CAPTIONS:
        if bad in h:
            check(f'{slug or "home"} no caption {bad!r}', False, bad)
def figs(slug):
    t = main_text(read(slug))
    return re.findall(r'<figure[^>]*><img src="/images/([^"]+)"[^>]*><figcaption>(.*?)</figcaption>', t)
def hero_img(slug):
    t = main_text(read(slug))
    m = re.search(r'<img className="hero-img"|class="hero-img"[^>]*src="/images/([^"]+)"', t)
    if not m:
        m = re.search(r'<img[^>]+src="/images/([^"]+)"[^>]*fetchpriority="high"', t)
    return m.group(1) if m else None
def card_img(page_slug, target):
    t = main_text(read(page_slug))
    for m in re.finditer(r'<article[^>]*><img src="/images/([^"]+)"[^>]*><div class="card-body"><h3><a href="/([^/]+)/">', t):
        if m.group(2) == target: return m.group(1)
    return None
# --- R5 swapped heroes ---
check('sewage hero = drain', hero_img('sewage-cleanup') == 'sewage-drain-15242228.webp', str(hero_img('sewage-cleanup')))
check('west hero = brick', hero_img('west-plano') == 'suburban-home-3990589.webp', str(hero_img('west-plano')))
check('north hero = brick gable', hero_img('north-plano') == 'suburban-home-26595553.webp', str(hero_img('north-plano')))
check('central hero = texas street', hero_img('central-plano') == 'texas-home-8278494.webp', str(hero_img('central-plano')))
check('east hero UNCHANGED pool-limited', hero_img('east-plano') == 'brick-ranch-8031875.webp', str(hero_img('east-plano')))  # ROUND 6: east hero replaced 25798114 (Mediterranean tile roof) -> brick ranch per the R6 east hero line; shared with mckinney hero, recorded
# --- R5 swapped splits (figure order) ---
def figfiles(slug): return [f for f, _ in figs(slug)]
check('commercial figs', figfiles('commercial-water-damage') == ['commercial-office-36631701.webp', 'steel-studs-35496414.webp', 'ceiling-stain-3708564.webp', 'commercial-office-22711217.webp'], str(figfiles('commercial-water-damage')))  # ROUND 6: body1 swapped 9300768 (glass office, no studs) -> steel-studs per the R6 commercial Steel Studs line; LINK-UNDERLINE ROUND: + top-up office-desk figure (viewed-pixel verified) appended last
check('attic fig0', figfiles('attic-insulation-drying')[0] == 'attic-insulation-271743.webp', str(figfiles('attic-insulation-drying')))
check('wall fig0 different shoot', figfiles('wall-drying')[0] == 'thermal-imaging-7859781.webp', str(figfiles('wall-drying')))  # ROUND 6: fig0 was 8482824 (spirit-level man) — replaced with the thermal screen because 8482824 pairs with the new structural hero 8293640 under the wall/moisture pair rule; thermal is a different shoot from the moisture figure, so the check's intent still holds
check('wall figs no 8293746', 'moisture-meter-8293746.webp' not in figfiles('wall-drying'), str(figfiles('wall-drying')))
check('fans fig0', figfiles('fans-wont-dry-walls')[0] == 'moisture-meter-7937963.webp', str(figfiles('fans-wont-dry-walls')))
check('allen figs + topic caption', figfiles('allen') == ['suburban-home-26595553.webp', 'suburban-home-3990589.webp', 'attic-insulation-271743.webp', 'suburban-home-7587470.webp'] and figs('allen')[1][1] == 'Brick suburban home with garage and basketball hoop', str(figs('allen')))  # ROUND 6: caption rewritten to pixels-only per the R6 Allen caption line (old caption overclaimed a verified Allen home the pixels cannot prove); figs unchanged; LINK-UNDERLINE ROUND: + top-up brick-home figure appended last
check('allen no old listing caption', 'modern white house with large glass windows' not in main_text(read('allen')))
check('mold fig1 interior', figfiles('mold-after-water-damage')[1] == 'cabinet-kitchen-8146322.webp', str(figfiles('mold-after-water-damage')))
check('insurance fig1 mitigation', figfiles('water-damage-insurance-texas')[1] == 'plumber-work-6419128.webp', str(figfiles('water-damage-insurance-texas')))
check('contact figs', figfiles('contact')[:2] == ['plumber-work-35290675.webp', 'suburban-home-26595553.webp'], str(figfiles('contact')))
check('laundry fig1 drain', figfiles('laundry-overflow')[1] == 'sewage-drain-3964564.webp', str(figfiles('laundry-overflow')))
check('fire fig1 office', figfiles('fire-sprinkler-cleanup')[1] == 'fire-sprinkler-36631700.webp', str(figfiles('fire-sprinkler-cleanup')))
check('water-ext fig2 meter check', figfiles('water-extraction')[2] == 'moisture-meter-8961703.webp', str(figfiles('water-extraction')))
check('ac fig2 drain', figfiles('ac-overflow')[2] == 'sewage-drain-3964564.webp', str(figfiles('ac-overflow')))
check('ceiling fig1 attic room', figfiles('ceiling-leak')[1] == 'attic-insulation-6124239.webp', str(figfiles('ceiling-leak')))  # ROUND 6: body1 swapped 271743 (finished bedroom) -> 6124239 (real insulation) per the R6 ceiling Sponge line's own pool proposal
# --- R5 swapped cards ---
check('home commercial card', card_img('', 'commercial-water-damage') == 'commercial-office-36631701.webp', str(card_img('', 'commercial-water-damage')))
check('home fire card', card_img('', 'fire-sprinkler-cleanup') == 'fire-sprinkler-36631700.webp', str(card_img('', 'fire-sprinkler-cleanup')))
check('home sewage card', card_img('', 'sewage-cleanup') == 'sewage-drain-15242228.webp', str(card_img('', 'sewage-cleanup')))
check('services sewage card', card_img('services', 'sewage-cleanup') == 'sewage-drain-15242228.webp', str(card_img('services', 'sewage-cleanup')))
check('storm sewage card', card_img('storm-water-category-3', 'sewage-cleanup') == 'sewage-drain-15242228.webp', str(card_img('storm-water-category-3', 'sewage-cleanup')))
check('central sewage card', card_img('central-plano', 'sewage-cleanup') == 'sewage-drain-15242228.webp', str(card_img('central-plano', 'sewage-cleanup')))
check('east sewage card', card_img('east-plano', 'sewage-cleanup') == 'sewage-drain-15242228.webp', str(card_img('east-plano', 'sewage-cleanup')))
check('crawl sewage card', card_img('crawl-space-drying', 'sewage-cleanup') == 'sewage-drain-15242228.webp', str(card_img('crawl-space-drying', 'sewage-cleanup')))
check('fire commercial card', card_img('fire-sprinkler-cleanup', 'commercial-water-damage') == 'commercial-office-36631701.webp', str(card_img('fire-sprinkler-cleanup', 'commercial-water-damage')))
check('flood extraction card', card_img('flood-cleanup', 'water-extraction') == 'water-extraction-6195949.webp', str(card_img('flood-cleanup', 'water-extraction')))  # ROUND 6: Final Fix guard removed — card now renders the extraction hero (PPE wet-vac worker), fixing the R6 flood extraction-card line; bare-hands 8961703 no longer forced
# --- R5 parser fixes ---
mo = main_text(read('mold-after-water-damage'))
check('mold symptom li not H2', '<h2>Allergy-like symptoms' not in mo and 'Allergy-like symptoms in one area of the house</li>' in mo)
check('mold kicker present', '<p class="section-kicker">Hour-by-Hour: What Happens Inside Wet Walls and Floors</p>' in mo)
check('mold label not H2', '<h2>Why Plano Homes Are at Higher Risk' not in mo and 'Why Plano Homes Are at Higher Risk.' in strip_tags(mo))
st = main_text(read('storm-water-category-3'))
check('storm kicker present', '<p class="section-kicker">How the Water Got In Decides What Has to Happen</p>' in st)
check('storm label not H2', '<h2>Why Plano Homes Take On Storm Water' not in st and 'Why Plano Homes Take On Storm Water.' in strip_tags(st))
ins = main_text(read('water-damage-insurance-texas'))
check('insurance drip li not H2', '<h2>Letting a slow drip' not in ins and 'Letting a slow drip continue after you notice it</li>' in ins)
ct = main_text(read('contact'))
check('contact no service-area H2', '<h2>Service area:' not in ct and '<strong>Service area:' in ct)
check('contact What Happens H2', '<h2>What Happens After You Call</h2>' in ct)
check('contact what-to-have 7 items', all(x in strip_tags(ct) for x in ['Your address and ZIP code', 'Where the water came from', 'Whether the water is still running', 'Which rooms and floors are wet', 'What kind of floors', "Whether it's clean water, gray water or sewage", 'Your insurance company, if you plan to file a claim']))
i = ct.find('Send Us a Message (Non-Emergency)</h2>')
check('contact form intro echo stripped', ct[i:i+400].find('<p>Use this form for questions') != -1)
check('contact form intro count 1', strip_tags(ct).count('Use this form for questions') == 1)
secs = re.findall(r'<section class="block[^"]*">(.*?)</section>', ct, re.S)
check('contact no lone tap section', not any(txt.startswith('Tap to Call') and len(txt) < 120 for txt in (strip_tags(s) for s in secs)))
em = [s for s in secs if 'Emergency in Your Plano Home? Call First' in strip_tags(s)]
check('contact tap inside Emergency section', len(em) == 1 and 'Tap to Call' in em[0])
co = main_text(read('water-damage-cost'))
check('cost factors all H3', all(x in co for x in ['<h3>1. Square Footage and Room Size</h3>', '<h3>2. Water Category</h3>', '<h3>3. How Hard It Is to Dry</h3>', '<h3>4. How Many Days</h3>']))
# --- heroes unique (informational: 3 R5-mandated shared pairs) ---
heroes = {}
for slug in slugs:
    if slug in ('services', 'areas', 'guides'): continue
    heroes[slug or 'home'] = hero_img(slug)
from collections import Counter
dup = {f: c for f, c in Counter(heroes.values()).items() if c > 1}
check('heroes unique except 3 R5 pairs', dup == {'suburban-home-3990589.webp': 2, 'suburban-home-26595553.webp': 2, 'texas-home-8278494.webp': 2, 'brick-ranch-8031875.webp': 2, 'flooded-suburban-home-28447764.webp': 2}, str(dup))  # ROUND 6: +2 DELIBERATE shares (east+mckinney brick ranch; flood+storm flooded home), both recorded in gen3_render.py; the 3 R5 pairs unchanged
# --- sitemap ---
sm = open(os.path.join(OUT, 'sitemap.xml')).read()
urls = re.findall(r'<loc>(.*?)</loc>', sm)
check('sitemap 46 urls 0 image entries', len(urls) == 46 and '<image:' not in sm, f'{len(urls)}')
print(f'R5 DOM CHECK: {len(OK)} OK, {len(FAIL)} FAIL')
for f in FAIL: print('FAIL:', f)
json.dump({'ok': len(OK), 'fail': FAIL}, open(os.path.join(BASE, 'r5_dom_check.json'), 'w'), indent=1)
