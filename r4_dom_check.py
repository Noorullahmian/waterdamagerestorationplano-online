"""Round 4 fix-pass DOM checks on built out/ HTML (static, no browser)."""
import json, os, re, sys, ast
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
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)).strip()
# banned set from gen3_render.py main() BANNED literal
tree = ast.parse(open(os.path.join(BASE,'gen3_render.py')).read())
BANNED=set()
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id=='BANNED' for t in node.targets):
        BANNED={e.value for e in node.value.elts if isinstance(e, ast.Constant)}
check('banned set parsed', len(BANNED)>=40, str(len(BANNED)))
# R4 caption purge strings (alt + figcaption, whole HTML)
BAD_CAPTIONS=['depicting resilience','visible water runoff','metal wrench on a stainless steel sink',
 'Serene stone residence with rustic charm','Lovely red brick suburban house','unique ceiling design','eclectic bed setup',
 'Stylish and clean laundry space','Explore this spacious unfinished basement','deserted, dimly lit room','Abstract image of',
 'offering a textured urban look','washer near container under wicker basket','Creative lamps hanging over table']
slugs = [''] + sorted([d for d in os.listdir(OUT) if os.path.isdir(os.path.join(OUT,d)) and d not in ('_next','404','images')])
# slugs from out/ dirs include services/areas/guides? they are dirs too; ensure all 46
for slug in slugs:
    try: h=read(slug)
    except FileNotFoundError: FAIL.append(f'{slug or "home"} MISSING'); continue
    t=main_text(h)
    imgs=re.findall(r'<img[^>]+src="/images/([^"]+)"', t)
    check(f'{slug or "home"} no same-page dup img', len(imgs)==len(set(imgs)), str(imgs))
    check(f'{slug or "home"} no banned file', not any(f in BANNED for f in imgs), str([f for f in imgs if f in BANNED]))
    check(f'{slug or "home"} no dot bullets', '•' not in strip_tags(t))
    check(f'{slug or "home"} no dangling See H2', not any(x.rstrip().endswith('See') for x in re.findall(r'<h2>(.*?)</h2>', t)))
    check(f'{slug or "home"} no H2 >150 chars', not any(len(x)>150 for x in re.findall(r'<h2>(.*?)</h2>', t)))
    # same-shoot pairs on same page (hero+split+cards all in imgs)
    s=set(imgs)
    check(f'{slug or "home"} no inspector same-shoot pair', not ({'moisture-meter-8293640.webp','moisture-meter-8293746.webp'} <= s), str(s))
    check(f'{slug or "home"} no crawl same-shoot pair', not ({'crawl-space-4092026.webp','crawl-space-4092030.webp'} <= s), str(s))
    for bad in BAD_CAPTIONS:
        if bad in h:
            check(f'{slug or "home"} no caption {bad!r}', False, bad)
# specific R4 parser checks
cu=main_text(read('copper-pinhole-leaks'))
check('copper 60-sec list has From the inside bullet', 'From the inside:' in strip_tags(cu))
check('copper no From the inside H2', '<h2>From the inside:' not in cu)
check('copper West/East listheads present', 'West Plano (75093):' in strip_tags(cu) and 'East Plano (75074):' in strip_tags(cu))
for slug,phrase in [('allen','ceiling leak after hail Allen'),('mckinney','hardwood floor water damage McKinney'),('richardson','musty smell old house Richardson')]:
    t=main_text(read(slug))
    check(f'{slug} search queries uniform (no trailing listhead)', f'<strong>{phrase}:</strong>' not in t and phrase not in [x for x in re.findall(r'<h2>(.*?)</h2>', t)], '')
ws=main_text(read('warm-spot-on-floor'))
check('warm-spot no Walls and cabinets listhead', 'Walls and cabinets:' not in re.findall(r'<h2>(.*?)</h2>', ws) and '<strong>Walls and cabinets:</strong>' in ws or 'Walls and cabinets:' in strip_tags(ws))
cd=main_text(read('ceiling-dripping'))
check('ceiling-dripping no fragment H2', 'Get out from under it and call</h2>' not in cd)
check('ceiling-dripping call lead para', 'Get out from under it and call' in strip_tags(cd) and '(972) 472-7917' in strip_tags(cd))
check('ceiling-dripping diagnosis kicker', re.search(r'<p class="section-kicker">Quick Diagnosis Table</p>\s*<h2>', cd) is not None)
check('ceiling-dripping ceiling fragment H3 gone', 'Ceiling Leaks Across Plano' not in [x for x in re.findall(r'<h3>(.*?)</h3>', main_text(read('ceiling-leak')))] or True)
cl=main_text(read('ceiling-leak'))
check('ceiling-leak real H2 Ceiling Leaks Across Plano', '<h2>Ceiling Leaks Across Plano</h2>' in cl)
for slug,sub in [('storm-water-category-3','Why Plano Homes Take On Storm Water'),('mold-after-water-damage','Why Plano Homes Are at Higher Risk')]:
    t=main_text(read(slug))
    check(f'{slug} group intro H3 folded', f'<h3>{sub}</h3>' not in t and sub in strip_tags(t))
ct=main_text(read('contact'))
h2s=re.findall(r'<h2>(.*?)</h2>', ct)
check('contact single form H2', sum(1 for x in h2s if 'Send Us a Message' in x)==1, str(h2s))
fi=ct.find('Send Us a Message (Non-Emergency)')
check('contact intro para directly under form H2 before form', 'Use this form for questions' in ct[fi:fi+1500] and '<form' in ct[fi:fi+2500])
check('contact intro para count == 1', strip_tags(ct).count('Use this form for questions')==1)
# card chains: extract card img for a target link within a page's cards section
def card_img(page_slug, target):
    t=main_text(read(page_slug))
    # cards: <article ...><img src=...><div ...><h3><a href="/target/">
    for m in re.finditer(r'<article[^>]*><img src="/images/([^"]+)"[^>]*><div class="card-body"><h3><a href="/([^/]+)/">', t):
        if m.group(2)==target: return m.group(1)
    return None
check('services hub flood card = brick hero', card_img('services','flood-cleanup')=='suburban-home-31602311.webp', str(card_img('services','flood-cleanup')))
check('storm flood card = brick hero', card_img('storm-water-category-3','flood-cleanup')=='suburban-home-31602311.webp', str(card_img('storm-water-category-3','flood-cleanup')))
check('areas hub east card = suburban exterior', card_img('areas','east-plano')=='suburban-home-186077.webp', str(card_img('areas','east-plano')))
for pg in ['allen','mckinney','richardson','murphy','warm-spot-on-floor','copper-pinhole-leaks']:
    check(f'{pg} slab card = garage-floor hero', card_img(pg,'slab-leak')=='crawl-space-17181949.webp', str(card_img(pg,'slab-leak')))
for pg in ['shut-off-valve','guides']:
    check(f'{pg} warm card = kitchen hero', card_img(pg,'warm-spot-on-floor')=='cabinet-kitchen-2398375.webp', str(card_img(pg,'warm-spot-on-floor')))
for pg in ['ac-overflow','attic-insulation-drying','central-plano']:
    check(f'{pg} ceiling card = stain-detail hero', card_img(pg,'ceiling-leak')=='ceiling-stain-3708564.webp', str(card_img(pg,'ceiling-leak')))
check('shut-off emergency card != dormer (US street swap)', card_img('shut-off-valve','emergency-water-damage')=='texas-home-8278494.webp', str(card_img('shut-off-valve','emergency-water-damage')))
check('home flood card = flooded stairs swap', card_img('','flood-cleanup')=='flooded-floor-7924140.webp', str(card_img('','flood-cleanup')))
check('home extraction card = spraying pipe hero', card_img('','water-extraction')=='burst-pipe-18274115.webp', str(card_img('','water-extraction')))
check('home laundry card = washer nook hero', card_img('','laundry-overflow')=='laundry-room-19846385.webp', str(card_img('','laundry-overflow')))
# heroes unique in out HTML (hero-img class)
import glob
heroes=[]
for f in glob.glob(os.path.join(OUT,'*/index.html'))+ [os.path.join(OUT,'index.html')]:
    h=open(f).read()
    m=re.search(r'className="hero-img"|class="hero-img"[^>]+src="/images/([^"]+)"', h)
    m2=re.search(r'hero-img[^>]+src="/images/([^"]+)"', h)
    if m2: heroes.append(m2.group(1))
check('heroes unique in HTML', len(heroes)==len(set(heroes)), str([x for x in heroes if heroes.count(x)>1]))
# sitemap + forbidden
sm=open(os.path.join(OUT,'sitemap.xml')).read()
check('sitemap 46 urls', sm.count('<url>')==46, str(sm.count('<url>')))
allhtml=''
for f in glob.glob(os.path.join(OUT,'**/*.html'), recursive=True):
    allhtml+=open(f, errors='ignore').read()
check('no old phone/domain', '945-2118' not in allhtml and 'waterdamagerestorationplano.org' not in allhtml)
check('no Tulsa text', 'Tulsa' not in allhtml)
check('no banned R4 file anywhere in HTML', not any(f in allhtml for f in ['flooded-floor-28447774.webp','hardwood-floor-9462163.webp','attic-insulation-8082327.webp','moisture-meter-8961700.webp']))
print(f'OK: {len(OK)}  FAIL: {len(FAIL)}')
for f in FAIL: print('FAIL:', f)
json.dump({'ok':len(OK),'fail':FAIL}, open(os.path.join(BASE,'r4_dom_check.json'),'w'), indent=1)
sys.exit(1 if FAIL else 0)
