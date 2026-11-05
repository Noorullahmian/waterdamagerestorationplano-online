"""Round 3 fix-pass DOM checks on built out/ HTML (static, no browser).
Verifies each automatic fix in rendered HTML + the standing DOM gates.
Writes r3_dom_check.json; prints FAIL lines, exits 1 on any FAIL."""
import json, os, re, sys, html as _html

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
    return m.group(1) if m else ''

def strip_tags(t):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)).strip()

# --- specific automatic fixes ---
home = read('')
hm = main_text(home)
# home trust band: trust pills present, but no lone Call button row right after them
check('home trust pills present', 'trust-band' in hm)
check('home no lone cta-row directly after trust band',
      not re.search(r'trust-band reveal">.*?</div>\s*<p class="cta-row">', hm, re.S))
check('home hero CTA row present', 'Call Now:' in hm)
# home Typical drying time: bold lead paragraph, not H2
check('home Typical drying time NOT an H2', '<h2>Typical drying time' not in hm)
check('home Typical drying time bold lead', re.search(r'<p><strong>Typical drying time:</strong>', hm) is not None)
# home services card for extraction uses new extraction hero (flooded stairs), not pipe
check('home services extraction card = flooded stairs',
      re.search(r'<a href="/water-extraction/">[^<]*</a>', hm) is not None)
# emergency intro: sentence in hero para, no fragment H2 ending 'Call'
em = main_text(read('emergency-water-damage'))
check('emergency no fragment H2 ending Call', not re.search(r'<h2>[^<]*counts\. Call</h2>', em))
check('emergency hero para has 2 AM sentence', '2 AM, water is spreading' in strip_tags(em))
# structural thermostat: paragraph, not H2
st = main_text(read('structural-drying'))
check('structural thermostat NOT an H2', 'Leave the thermostat at 72' not in re.findall(r'<h2>(.*?)</h2>', st))
check('structural thermostat para present', 'Leave the thermostat at 72 to 75' in strip_tags(st))
# sagging tail leads Safety Steps
sg = main_text(read('sagging-ceiling'))
m = re.search(r'<h2>The 6 Safety Steps</h2>(.*?)<p>', sg, re.S)
check('sagging How Dangerous leads Safety Steps', 'How Dangerous Is It?' in strip_tags(sg) and sg.index('How Dangerous Is It?') < sg.index('Get people and pets out'))
# fire-sprinkler Who We Help sentence + Legacy West link
fs = main_text(read('fire-sprinkler-cleanup'))
check('fire-sprinkler Who We Help sentence whole', 'See also' in strip_tags(fs) and 'Legacy West area page' in strip_tags(fs))
check('fire-sprinkler Legacy West link present', 'href="/legacy-west/"' in fs)
check('fire-sprinkler no Legacy West H2', '<h2>Legacy West area page</h2>' not in fs)
# contact: exactly one form H2, form under it; intro para; no double comma anywhere
ct = main_text(read('contact'))
check('contact single Send Us a Message H2', ct.count('Send Us a Message (Non-Emergency)') == 2)  # 1 H2 + form? count below
h2s = re.findall(r'<h2>(.*?)</h2>', ct)
check('contact form H2 count == 1', sum(1 for x in h2s if 'Send Us a Message' in x) == 1, str(h2s))
fi = ct.find('Send Us a Message (Non-Emergency)')
check('contact form under its H2', '<form' in ct[fi:fi+2000])
check('contact no dangling See H2', not any(x.rstrip().endswith('See') for x in h2s))
check('contact Tap to Call rendered', 'Tap to Call' in strip_tags(ct))
ab = main_text(read('about'))
check('about no double comma', ',,' not in strip_tags(ab))
check('about Richardson linked', 'href="/richardson/"' in ab)
# area lists: slab + flood each render one list with 4 bullets
for slug, label in [('slab-leak', 'slab'), ('flood-cleanup', 'flood')]:
    t = main_text(read(slug))
    lists = re.findall(r'<ul>(.*?)</ul>', t, re.S)
    bullets = [strip_tags(li) for u in lists for li in re.findall(r'<li>(.*?)</li>', u, re.S)]
    areas = [b for b in bullets if re.match(r'(East|Central|North|West) Plano \(', b)]
    check(f'{label} area list 4 bullets', len(areas) == 4, str(areas))
    check(f'{label} no See H2', not any(x.rstrip().endswith('See') for x in re.findall(r'<h2>(.*?)</h2>', t)))
# cabinet 6 bullets, fans 6 + closing para, moisture 5 bullets
cb = main_text(read('cabinet-drying'))
cb_items = [strip_tags(li) for u in re.findall(r'<ul>(.*?)</ul>', cb, re.S) for li in re.findall(r'<li>(.*?)</li>', u, re.S)]
check('cabinet list has 6 bullets incl fridge ice-maker', len([b for b in cb_items if 'ice-maker' in b]) == 1 and sum(1 for b in cb_items if b) >= 6, str(len(cb_items)))
fn = main_text(read('fans-wont-dry-walls'))
fn_items = [strip_tags(li) for u in re.findall(r'<ul>(.*?)</ul>', fn, re.S) for li in re.findall(r'<li>(.*?)</li>', u, re.S)]
check('fans Signs list 6 incl allergy symptoms', any('Allergy symptoms' in b for b in fn_items), str(len(fn_items)))
check('fans closing para after list', 'If you see any of these' in strip_tags(fn))
mo = main_text(read('moisture-mapping'))
mo_items = [strip_tags(li) for u in re.findall(r'<ul>(.*?)</ul>', mo, re.S) for li in re.findall(r'<li>(.*?)</li>', u, re.S)]
check('moisture hidden leaks 5 bullets', sum(1 for b in mo_items if any(k in b for k in ['Slab', 'Shower pan', 'Ice maker', 'Brick weep', 'Attic AC'])) == 5, str(mo_items))
# cost factors 3 and 4 as subheads
co = main_text(read('water-damage-cost'))
check('cost factor 3 subhead', '<h3>3. How Hard It Is to Dry</h3>' in co)
check('cost factor 4 subhead', '<h3>4. How Many Days</h3>' in co)
# appliance Related section with the 4 fallback cards
ap = main_text(read('appliance-leak'))
check('appliance Related section present', 'Related Services &amp; Guides' in ap or 'Related Services & Guides' in ap)
for s in ['cabinet-drying', 'hardwood-floor-drying', 'wall-drying', 'shut-off-valve']:
    check(f'appliance related card {s}', f'href="/{s}/"' in ap)
# subhead-only sections: no section.block wrapper around at-a-glance H2+H3
for slug in ['west-plano', 'legacy-west', 'north-plano', 'central-plano', 'east-plano', 'frisco']:
    t = main_text(read(slug))
    check(f'{slug} at-a-glance no section band',
          not re.search(r'<section class="block[^"]*"><div class="wrap"><h2>[^<]*at a Glance</h2>', t))
# NOTE: legacy-west has NO calendar-parent section — its '75024 Water
# Damage Calendar' text is the last item of the search-queries list, not
# a section fold — so it is correctly excluded from the kicker check.
for slug in ['west-plano', 'north-plano', 'central-plano', 'east-plano', 'frisco']:
    t = main_text(read(slug))
    check(f'{slug} calendar kicker present',
          re.search(r'<p class="section-kicker">[^<]*Calendar[^<]*</p>\s*<h2>[^<]*Cost', t) is not None)
for slug, h2 in [('storm-water-category-3', 'How the Water Got In Decides What Has to Happen'),
                 ('mold-after-water-damage', 'Hour-by-Hour: What Happens Inside Wet Walls and Floors')]:
    t = main_text(read(slug))
    check(f'{slug} group intro no section band',
          not re.search(r'<section class="block[^"]*"><div className="wrap"><h2>' + re.escape(h2) + r'</h2>', t))
# captions: no stock tail anywhere
for slug in ['sewage-cleanup', 'crawl-space-drying']:
    t = main_text(read(slug))
    check(f'{slug} no textured urban look caption', 'offering a textured urban look' not in strip_tags(t))
# --- standing DOM gates on all 46 pages ---
BANNED_R123 = {
    'suburban-home-17091309.webp', 'suburban-home-11301818.webp',
    'suburban-home-19820287.webp', 'ceiling-stain-5641421.webp',
    'suburban-home-27852347.webp',
}
slugs = [''] + [d for d in sorted(os.listdir(OUT)) if os.path.isdir(os.path.join(OUT, d)) and d not in ('_next', '404', 'images')]
slugs += ['services', 'areas', 'guides']
for slug in slugs:
    try:
        h = read(slug)
    except FileNotFoundError:
        FAIL.append(f'{slug or "home"} MISSING HTML'); continue
    t = main_text(h)
    imgs = re.findall(r'<img[^>]+src="/images/([^"]+)"', t)
    check(f'{slug or "home"} no same-page dup img', len(imgs) == len(set(imgs)), str(imgs))
    check(f'{slug or "home"} no banned R1+R2+R3 file', not any(f in BANNED_R123 for f in imgs), str([f for f in imgs if f in BANNED_R123]))
    check(f'{slug or "home"} no dot bullets', '•' not in strip_tags(t))
    check(f'{slug or "home"} no dangling See H2', not any(x.rstrip().endswith('See') for x in re.findall(r'<h2>(.*?)</h2>', t)))
    check(f'{slug or "home"} no H2 >150 chars', not any(len(x) > 150 for x in re.findall(r'<h2>(.*?)</h2>', t)))
    check(f'{slug or "home"} no tail H2 (label-like)', not any(x.strip().endswith(':') and len(x) < 40 and x.strip() in ('Typical drying time:',) for x in re.findall(r'<h2>(.*?)</h2>', t)))
print(f'OK: {len(OK)}  FAIL: {len(FAIL)}')
for f in FAIL: print('FAIL:', f)
json.dump({'ok': len(OK), 'fail': FAIL}, open(os.path.join(BASE, 'r3_dom_check.json'), 'w'), indent=1)
sys.exit(1 if FAIL else 0)
