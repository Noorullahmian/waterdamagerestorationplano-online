#!/usr/bin/env python3
"""Renderer for gen3.py — writes the Next.js app from parsed tabs + image manifest."""
import re, os, json, html
from gen3 import parse_tabs, classify_and_build, LINK_PHRASES, PHONE, TEL, DOMAIN, BRAND, clean_text

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
APP = os.path.join(BASE, 'app')
PUBLIC = os.path.join(BASE, 'public')

SERVICE_SLUGS = ['emergency-water-damage','water-extraction','structural-drying','burst-pipe-cleanup',
 'sewage-cleanup','slab-leak','water-heater-leak','ceiling-leak','flood-cleanup','commercial-water-damage',
 'hardwood-floor-drying','ac-overflow','cabinet-drying','laundry-overflow','crawl-space-drying',
 'appliance-leak','fire-sprinkler-cleanup','moisture-mapping','attic-insulation-drying','wall-drying']
AREA_SLUGS = ['west-plano','legacy-west','north-plano','central-plano','east-plano','frisco','allen','mckinney','richardson','murphy']
GUIDE_SLUGS = ['shut-off-valve','warm-spot-on-floor','ceiling-dripping','water-damage-cost','fans-wont-dry-walls',
 'storm-water-category-3','mold-after-water-damage','copper-pinhole-leaks','sagging-ceiling','water-damage-insurance-texas']
BEST_SERVICES = ['emergency-water-damage','water-extraction','structural-drying','burst-pipe-cleanup','slab-leak','sewage-cleanup']

HERO_TOPIC = {
 '': 'flooded-floor', 'emergency-water-damage': 'flooded-floor', 'water-extraction': 'wet-carpet',
 'structural-drying': 'moisture-meter', 'burst-pipe-cleanup': 'burst-pipe', 'sewage-cleanup': 'sewage-drain',
 'slab-leak': 'burst-pipe', 'water-heater-leak': 'plumber-work', 'ceiling-leak': 'ceiling-stain',
 'flood-cleanup': 'storm-flood', 'commercial-water-damage': 'commercial-office',
 'hardwood-floor-drying': 'hardwood-floor', 'ac-overflow': 'ceiling-stain', 'cabinet-drying': 'cabinet-kitchen',
 'laundry-overflow': 'laundry-room', 'crawl-space-drying': 'crawl-space', 'appliance-leak': 'appliance-fridge',
 'fire-sprinkler-cleanup': 'fire-sprinkler', 'moisture-mapping': 'moisture-meter',
 'attic-insulation-drying': 'attic-insulation', 'wall-drying': 'mold-wall',
 'west-plano': 'suburban-home', 'legacy-west': 'suburban-home', 'north-plano': 'suburban-home',
 'central-plano': 'suburban-home', 'east-plano': 'suburban-home', 'frisco': 'texas-home',
 'allen': 'suburban-home', 'mckinney': 'texas-home', 'richardson': 'suburban-home', 'murphy': 'suburban-home',
 'shut-off-valve': 'plumber-work', 'warm-spot-on-floor': 'burst-pipe', 'ceiling-dripping': 'ceiling-stain',
 'water-damage-cost': 'suburban-home', 'fans-wont-dry-walls': 'wet-carpet', 'storm-water-category-3': 'storm-flood',
 'mold-after-water-damage': 'mold-wall', 'copper-pinhole-leaks': 'burst-pipe', 'sagging-ceiling': 'ceiling-stain',
 'water-damage-insurance-texas': 'commercial-office', 'about': 'plumber-work', 'contact': 'suburban-home',
}
BODY_TOPICS = {
 'emergency-water-damage': ['flooded-floor','burst-pipe','plumber-work'],
 'water-extraction': ['wet-carpet','flooded-floor','hardwood-floor'],
 'structural-drying': ['moisture-meter','wet-carpet','drying-fan'],
 'burst-pipe-cleanup': ['burst-pipe','plumber-work','ceiling-stain'],
 'sewage-cleanup': ['sewage-drain','bathroom-leak','mold-wall'],
 'slab-leak': ['burst-pipe','hardwood-floor','mold-wall'],
 'water-heater-leak': ['plumber-work','water-heater','ceiling-stain'],
 'ceiling-leak': ['ceiling-stain','attic-insulation','burst-pipe'],
 'flood-cleanup': ['storm-flood','flooded-floor','sewage-drain'],
 'commercial-water-damage': ['commercial-office','fire-sprinkler','flooded-floor'],
 'hardwood-floor-drying': ['hardwood-floor','wet-carpet','flooded-floor'],
 'ac-overflow': ['ceiling-stain','attic-insulation','bathroom-leak'],
 'cabinet-drying': ['cabinet-kitchen','kitchen-leak','bathroom-leak'],
 'laundry-overflow': ['laundry-room','flooded-floor','wet-carpet'],
 'crawl-space-drying': ['crawl-space','mold-wall','sewage-drain'],
 'appliance-leak': ['appliance-fridge','kitchen-leak','laundry-room'],
 'fire-sprinkler-cleanup': ['fire-sprinkler','commercial-office','flooded-floor'],
 'moisture-mapping': ['moisture-meter','ceiling-stain','mold-wall'],
 'attic-insulation-drying': ['attic-insulation','ceiling-stain','plumber-work'],
 'wall-drying': ['mold-wall','crawl-space','ceiling-stain'],
}

def esc(s):
    return html.escape(s, quote=True)

def clean_alt(s):
    """Unescape once, then strip stock-sales language from Pexels alt text.
    The alt in images.json may literally contain '&#x27;' (pre-escaped);
    html.escape() alone would double-escape it to '&amp;#x27;' and the
    entity would render as visible text. Unescape first, escape once.
    Stock phrases are caption metadata, not doc words — stripping them
    never touches doc body content."""
    t = html.unescape(s or '')
    # Round 4: whole-alt listing-copy rewrites (the alt IS the sales
    # copy; stripping a tail would leave a fragment). Applied before
    # the generic strips below. Keys are the exact source alt text.
    _ALT_REWRITE = {
        'Lovely red brick suburban house with a well-maintained lawn under a bright blue sky.':
            'Red brick suburban house with a well-maintained lawn',
        'Serene stone residence with rustic charm in Texas.':
            'Stone suburban home in Texas',
        'A small bedroom with a unique ceiling design, featuring water stains and an eclectic bed setup.':
            'Water-stained bedroom wall',
        'Close-up of a metal wrench on a stainless steel sink with water droplets.':
            'Wet stainless steel sink with water droplets',
        'Explore this spacious unfinished basement perfect for renovation in an Ohio home.':
            'Spacious unfinished basement',
        'Abstract image of a cracked, stained concrete ceiling emphasizing texture.':
            'Stained concrete ceiling corner with a crack',
        'Close-up of a worn ceiling and hanging lamp in a deserted, dimly lit room.':
            'Worn ceiling with peeling paint and a hanging lamp',
        'Stylish and clean laundry space featuring a white washing machine with towels on top.':
            'White washing machine in a home laundry nook',
        'Explore a large, bright unfinished basement with modern potential in Ohio real estate.':
            'Unfinished basement with exposed joists',
        'Empty basement with exposed beams and plumbing pipes, ideal for renovation.':
            'Water heater tank in an unfinished basement with exposed beams',
        'Interior of modern apartment with washer near container under wicker basket placed near potted plant and bottle of soap':
            'Wooden laundry counter with a basket and soap',
        'Creative lamps hanging over table with chairs in spacious kitchen with modern furniture and appliances':
            'Modern kitchen with an island',
        'Contemporary kitchen interior with sleek white cabinets and island, perfect for a minimalist aesthetic.':
            'Contemporary kitchen with white cabinets and an island',
        'Spacious attic interior featuring exposed wooden beams and brick walls, perfect for renovation or design inspiration.':
            'Interior attic room with exposed beams and brick walls',
        'Close-up of a vintage industrial fan amidst outdoor junkyard setting, conveying industrial decay.':
            'Industrial air mover fan',
        'Spacious garage interior with storage shelves, tools, and a wheelbarrow, ideal for home organization.':
            'Garage interior with a concrete floor',
    }
    if t.strip() in _ALT_REWRITE:
        return _ALT_REWRITE[t.strip()]
    t = re.sub(r',?\s*perfect for (real estate|renovation)[^.]*\.?', '', t, flags=re.I)
    t = re.sub(r',?\s*ideal for (real estate|renovation)[^.]*\.?', '', t, flags=re.I)
    t = re.sub(r'Abstract image of ', '', t, flags=re.I)
    t = re.sub(r'Abstract background of ', '', t, flags=re.I)
    # Round 2 systemic caption tails: stock-site description language that
    # survives as visible page copy ("showcasing modern architecture",
    # "ideal for collaborative work environments", "capturing serene
    # residential architecture", "highlighting decay and neglect").
    t = re.sub(r',?\s*(showcasing|ideal for|capturing|highlighting)[^.]*\.?', '', t, flags=re.I)
    t = re.sub(r' emphasizing texture\.?', '', t, flags=re.I)
    t = re.sub(r' for efficient cleaning\.?', '', t, flags=re.I)
    t = re.sub(r', showcasing skilled manual work\.?', '', t, flags=re.I)
    t = re.sub(r', highlighting efficient home cleaning\.?', '', t, flags=re.I)
    t = re.sub(r', capturing a moment of household cleaning\.?', '', t, flags=re.I)
    # Round 3: stock-sales tail on the rusty-grate photos (2 pages).
    t = re.sub(r',?\s*offering a textured urban look\.?', '', t, flags=re.I)
    # Round 4: pixel-mismatched / sales tails flagged on viewed pixels.
    t = re.sub(r',?\s*depicting resilience\.?', '', t, flags=re.I)
    t = re.sub(r'\s+with visible water runoff', '', t, flags=re.I)
    t = re.sub(r'^Explore this ', '', t, flags=re.I)
    t = re.sub(r'\s+', ' ', t).strip().rstrip('.')
    return t

def alt_text(s):
    return esc(clean_alt(s))

# Responsive images (link-underline + image-optimization round): variant
# files {stem}-400.webp / {stem}-800.webp live in public/images next to
# the 1200w originals and are picked up by srcset ONLY when they exist on
# disk and are smaller than the original. Filenames, alt text and the
# 1200w src never change, so no link or audit breaks. Variants are NOT in
# images.json, so rotation never picks them as standalone images.
_IMG_IDX = None
def _img_index():
    global _IMG_IDX
    if _IMG_IDX is None:
        _IMG_IDX = {}
        try:
            _d = os.path.join(PUBLIC, 'images')
            for _f in os.listdir(_d):
                _p = os.path.join(_d, _f)
                if os.path.isfile(_p):
                    _IMG_IDX[_f] = os.path.getsize(_p)
        except OSError:
            pass
    return _IMG_IDX

def _stem(f):
    return f[:-5] if f.endswith('.webp') else f

def img_tag(file, alt, kind, eager=False, cls=None):
    idx = _img_index()
    orig = idx.get(file, 0)
    if kind == 'hero':
        cands = [(800, '800w')]
        sizes = '(max-width:820px) 90vw, 600px'
    elif kind == 'sticky':
        cands = [(400, '400w'), (800, '800w')]
        sizes = '(max-width:820px) 90vw, 380px'
    elif kind == 'card':
        cands = [(400, '400w'), (800, '800w')]
        sizes = '(max-width:520px) 90vw, (max-width:820px) 45vw, 390px'
    else:  # split / topup
        cands = [(400, '400w'), (800, '800w')]
        sizes = '(max-width:820px) 90vw, 1200px'
    parts = []
    for w, dw in cands:
        vf = f'{_stem(file)}-{w}.webp'
        vb = idx.get(vf)
        if vb and (not orig or vb < orig):
            parts.append(f'/images/{vf} {dw}')
    ss = ''
    if parts:
        parts.append(f'/images/{file} 1200w')
        ss = f' srcset="{", ".join(parts)}" sizes="{sizes}"'
    extra = ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    cl = f' className="{cls}"' if cls else ''
    return f'<img{cl} src="/images/{file}" alt="{alt}" width="1200" height="800"{ss}{extra} />'

def href_for(slug):
    return '/' if slug == '' else f'/{slug}/'

def render_seg_text(text, self_slug, in_link=False):
    """Render plain text with inline phrase links (max 2) + tel links."""
    if in_link:
        return esc(text)
    # Bracketed call text inside a paragraph/list ("[Call 24/7: (972)...]")
    # must never render as literal brackets — strip the brackets; the phone
    # number inside is then tel-linked by the split below.
    text = re.sub(r'\[([^\]]*Call[^\]]*)\]', r'\1', text)
    # tel link for phone numbers
    out = ''
    # first apply phrase links on the raw text (case-insensitive, longest first)
    # Work on segments split by phone numbers to keep tel handling simple.
    parts = re.split(r'(\(972\) 472-7917)', text)
    for part in parts:
        if part == '(972) 472-7917':
            out += f'<a href="{TEL}">(972) 472-7917</a>'
            continue
        # phrase links, at most 2 per part
        applied = 0
        rest = part
        while applied < 2:
            best = None
            for phrase, slug in LINK_PHRASES:
                if slug == self_slug:
                    continue
                m = re.search(r'(?<![A-Za-z-])' + re.escape(phrase) + r'(?![A-Za-z-])', rest, re.I)
                if m and (best is None or m.start() < best[0]):
                    best = (m.start(), m.end(), m.group(0), slug)
            if not best:
                break
            st, en, matched, slug = best
            out += esc(rest[:st]) + f'<a href="{href_for(slug)}">{esc(matched)}</a>'
            rest = rest[en:]
            applied += 1
        out += esc(rest)
    return out

def render_segs(segs, self_slug):
    out = ''
    for text, tgt in segs:
        if text in (', ', '.'):
            out += text
            continue
        piece = esc(text) if tgt is not None and tgt == self_slug else (
            f'<a href="{href_for(tgt)}">{esc(text)}</a>' if tgt is not None else render_seg_text(text, self_slug))
        # Join segments with a space unless punctuation already separates them.
        if out:
            visible_piece = re.sub(r'^<[^>]+>', '', piece)
            if visible_piece and visible_piece[0] not in ' ,.;:?!%)':
                if not out.endswith((' ', '(', '—', '–')):
                    out += ' '
        out += piece
    return out

def is_list_para(block):
    """A para made only of short phrases + 'and'/',' joiners is really a
    list (about/contact service lists) rendered run-on. Render it as <ul>.
    Sentence paras (long segs, or segs ending '.') never match."""
    segs = block['segs']
    # City enumerations end with a '.' seg and use only ', ' joiners; the
    # about/contact service lists have 'and' joiners and no trailing '.'
    # seg. Those two signals keep city paras as sentences.
    if any(t == '.' for t, _ in segs):
        return False
    if 'and' not in [t for t, _ in segs]:
        return False
    content = [t for t, _ in segs if t not in ('and', ',', ', ', '.')]
    if len(content) < 4:
        return False
    if any(len(t) >= 45 or t.endswith('.') for t in content):
        return False
    if sum(1 for _, tgt in segs if tgt is not None) < 2:
        return False
    return True

def list_para_items(segs):
    """Group list-para segs into items: a content seg following another
    content seg directly starts a new item; 'and'/',' segs join the item."""
    items = []
    cur = []
    for text, tgt in segs:
        if text in ('and', ',', ', '):
            cur.append((text, None))
            continue
        if text == '.':
            continue
        if cur and cur[-1][0] not in ('and', ',', ', '):
            items.append(cur)
            cur = []
        cur.append((text, tgt))
    if cur:
        items.append(cur)
    return items

def para_html(block, self_slug):
    if is_list_para(block):
        items = ''
        for it in list_para_items(block['segs']):
            items += f'<li>{render_segs(it, self_slug)}</li>'
        return f'<ul>{items}</ul>'
    inner = render_segs(block['segs'], self_slug)
    # clean spacing before punctuation (typographic only)
    inner = re.sub(r'\s+([,.;:?!])', r'\1', inner)
    # bold lead: short first sentence or 'Phrase:' lead
    m = re.match(r'^(<a[^>]+>[^<]+</a>|[^<]{1,65}?[:.])\s+(.{80,})$', inner, re.S)
    if m and (m.group(1).endswith(':') or m.group(1).endswith('.')):
        inner = f'<strong>{m.group(1)}</strong> {m.group(2)}'
    return f'<p>{inner}</p>'

def block_html(b, self_slug):
    t = b['type']
    if t == 'subhead':
        return f'<h3>{esc(b["text"])}</h3>'
    if t == 'para':
        return para_html(b, self_slug)
    if t == 'cta':
        return f'<p class="cta-row"><a class="btn-call" href="{TEL}">{esc(b["label"])}: <span className="nowrap">{PHONE}</span></a></p>'
    if t == 'trust':
        items = ''.join(f'<span class="check">✓ {esc(x)}</span>' for x in b['items'])
        return f'<div class="trust-band reveal">{items}</div>'
    if t == 'listhead':
        return f'<p class="listhead"><strong>{esc(b["text"])}</strong></p>'
    if t == 'list':
        items = ''
        for it in b['items']:
            items += f'<li>{render_seg_text(it, self_slug)}</li>'
        return f'<ul>{items}</ul>'
    if t == 'form':
        fields = ''
        for f in b['fields']:
            fl = f.strip()
            if fl.lower().startswith('type of property'):
                opts = [o.strip() for o in fl.split(':', 1)[1].split(',')]
                # last option may contain 'or' — keep as written, split on ',' and ' or '
                fields += '<label>Type of property<select name="property">' + ''.join(f'<option>{esc(o)}</option>' for o in opts) + '</select></label>'
            elif fl.lower().startswith('what happened'):
                opts = [o.strip() for o in fl.split(':', 1)[1].split(',')]
                fields += '<label>What happened<select name="happened">' + ''.join(f'<option>{esc(o)}</option>' for o in opts) + '</select></label>'
            elif fl.lower().startswith('is water still active'):
                fields += '<label>Is water still active? <span class="radio-row"><label><input type="radio" name="active" value="Yes" /> Yes</label><label><input type="radio" name="active" value="No" /> No</label></span></label>'
            elif fl.lower() == 'message':
                fields += '<label>Message<textarea name="message" rows="5"></textarea></label>'
            elif fl.lower() == 'email address':
                fields += '<label>Email address<input type="email" name="email" /></label>'
            elif fl.lower() == 'phone number':
                fields += f'<label>Phone number<input type="tel" name="phone" /></label>'
            else:
                fields += f'<label>{esc(fl)}<input type="text" name="{esc(fl.lower().replace(" ", "_"))}" /></label>'
        note = f'<p class="form-note">{esc(b["note"])}</p>' if b.get('note') else ''
        return f'<form class="contact-form" method="post">{fields}<button type="submit" class="btn-call">Send Message</button></form>{note}'
    return ''

def main():
    tabs = parse_tabs()
    by_slug = {t['slug']: t for t in tabs}
    manifest = json.load(open(os.path.join(BASE, 'images.json')))
    # Round 1 fix pass: files the hunters flagged on ANY page are banned
    # from every rotation pick, so a freed hero file (e.g. the European
    # street photo) cannot re-enter through another page's body rotation.
    BANNED = {
        'mold-wall-26387777.webp',      # pink door, 8 slots
        'mold-wall-17374615.webp',      # decaying abandoned entrance
        'plumber-work-7859953.webp',    # boiler/Grundfos
        'plumber-work-29226620.webp',   # radiator pipework
        'plumber-work-7220892.webp',    # blurred valve/sink pipe
        'ceiling-stain-18323819.webp',  # palace ceiling
        'texas-home-23930016.webp',     # Mediterranean cottages
        'flooded-floor-14216445.webp',  # palm street
        'flooded-floor-17667013.webp',  # Wabasha farm
        'flooded-floor-35302178.webp',  # European street scene
        'storm-flood-28447778.webp', 'storm-flood-28447775.webp', 'storm-flood-28447808.webp',
        'burst-pipe-20812917.webp', 'burst-pipe-34197979.webp',
        'bathroom-leak-12271457.webp', 'bathroom-leak-40016472.webp',
        'drying-fan-32702870.webp',
        'fire-sprinkler-6101250.webp',  # greenhouse sprinkler
        'laundry-room-9669475.webp', 'laundry-room-11213210.webp',
        'laundry-room-14361266.webp', 'laundry-room-17367256.webp', 'laundry-room-4386143.webp',
        'attic-insulation-1628417.webp',  # Christmas tree
        'kitchen-leak-8054736.webp',    # onions
        'hardwood-floor-9462136.webp', 'hardwood-floor-9462132.webp',
        'hardwood-floor-9462141.webp', 'hardwood-floor-9462148.webp',
        'wet-carpet-8273517.webp', 'wet-carpet-4107284.webp', 'wet-carpet-9462139.webp', 'wet-carpet-4107257.webp',
        'wet-carpet-4107278.webp', 'wet-carpet-4107280.webp', 'wet-carpet-8566420.webp',
        # Round 2 fix pass: files flagged on one slot that were reused in a
        # new wrong slot (ban by file, every slot, not just the flagged one).
        'plumber-work-33388390.webp',   # workshop technician (mold/water-heater/shut-off/insurance)
        'flooded-floor-10631759.webp',  # decaying abandoned room (west/east/richardson)
        'flooded-floor-18302377.webp',  # abandoned room, decay caption (mckinney + home hero)
        'attic-insulation-38749876.webp', # roof-insulation drill (attic/ceiling-dripping/sagging)
        'ceiling-stain-18132318.webp',  # moody grunge room (burst)
        'mold-wall-29181495.webp',      # partially tiled renovation wall (mold)
        'water-heater-33116799.webp',   # red-roofed rooftop tanks (water-heater)
        'hardwood-floor-10557495.webp', # broom-and-dustpan cleaning (hardwood)
        'ceiling-stain-7599120.webp',   # green abstract wall (ceiling-dripping hero)
        'kitchen-leak-34295406.webp',   # bathroom faucet, not AC drain (ac-overflow)
        'crawl-space-10847198.webp',    # showroom basement, not crawl space
        # Round 3 bans (flagged on every slot that used them, no clean use):
        'suburban-home-17091309.webp',  # coastal cityscape with sea (east hero + areas East card)
        'suburban-home-11301818.webp',  # curved-corner urban apartment block (about split + areas Legacy card)
        'water-heater-6436774.webp',   # bathroom sink, NO heater visible; images.json alt claim ("mirror reflecting water heater") is WRONG on viewed pixels (Round 3 re-view fail: was water-heater hero + attic body[1])
        # Round 4 bans (flagged on every slot that used them, or
        # one-file-many-slots pattern — ban + per-slot replacements
        # must cover EVERY slot, not one page at a time):
        'flooded-floor-28447774.webp',  # European-dormer flood house: home/emergency splits, flood hero, west/central/mckinney splits, all flood cards
        'hardwood-floor-9462163.webp',  # mopping activity: hardwood advice contradiction, warm-spot hero, shut-off/guides warm cards
        'attic-insulation-8082327.webp',# dry finished attic room: ceiling hero + ceiling cards + ceiling-dripping body
        'moisture-meter-8961700.webp',  # no meter visible, dry construction wall: structural split
        # NOTE on the remaining wider "ban by file" list: NOT applied
        # globally. plumber-work-35290675, hardwood-floor-3935327 and
        # mold-wall-9127236 each still hold hunter-clean slots; every
        # flagged slot using those files gets an explicit per-slot
        # override below instead (Round 4 re-check: 35290675 attic AC
        # slot is overridden, its about split is unflagged and stays).
    }
    manifest = [im for im in manifest if im['file'] not in BANNED]
    pools = {}
    for m in manifest:
        pools.setdefault(m['topic'], []).append(m)
    counters = {}
    def pick(topic, exclude):
        pool = pools.get(topic, [])
        if not pool:
            return None
        for _ in range(len(pool)):
            i = counters.get(topic, 0) % len(pool)
            counters[topic] = counters.get(topic, 0) + 1
            cand = pool[i]
            if cand['file'] not in exclude:
                return cand
        # Pool exhausted (e.g. fully banned topic): fail honestly instead
        # of duplicating pool[0] as a second page's hero.
        return None
    # Round 4 lock: heroes frozen for ALL pages (R4 changes + R1-R3 heroes
    # otherwise unchanged) so R4 bans cannot shift rotation picks on clean pages.
    HERO_FILE = {
        '': 'suburban-home-186077.webp',
        'emergency-water-damage': 'burst-pipe-15206136.webp',
        'water-extraction': 'water-extraction-6195949.webp',  # ROUND 6 NEW: PPE worker running a wet vacuum over a tiled living-room floor (was outdoor pipe SPRAYING water — opposite action)
        'structural-drying': 'moisture-meter-8293640.webp',  # ROUND 6 DELIBERATE SHARE: inspector kneeling at a baseboard with a probe (moisture inspection = step 1 of structural drying). No meter/drying-room photo exists on Pexels after ~35 queries + Unsplash search, and 7937963 is a spirit level, not a meter. Sharing with moisture-mapping body0 is cross-page only (moisture page carries no structural card; its structural card is guard-pinned below) — never a same-page duplicate. Do NOT revert to 7937963 (spirit level) or 8293746 (reopens the wall/moisture pair).
        'burst-pipe-cleanup': 'burst-pipe-4406597.webp',
        'sewage-cleanup': 'sewage-drain-15242228.webp',  # R5: drain subject (frozen-water caveat; no true backup photo in pool) — was clean sink 10961064 (7 lines, hero + 6 cards)
        'slab-leak': 'slab-leak-21366138.webp',  # ROUND 6 NEW: water-cooled concrete saw cutting a wet concrete slab — slab work with water (was dry garage 17181949)
        'water-heater-leak': 'water-heater-34593293.webp',  # R4 revised: solar tank kept as POOL-LIMITED (no attic tank in pool; hunter fallback) — basement tank as hero created a same-shoot grid pair with crawl hero
        'ceiling-leak': 'ceiling-stain-3708564.webp',
        'flood-cleanup': 'flooded-suburban-home-28447764.webp',  # ROUND 6 NEW: suburban house with floodwater across yard/driveway, green trees (was dry brick house, no water)
        'commercial-water-damage': 'drying-equipment-16243255.webp',
        'hardwood-floor-drying': 'hardwood-floor-3935327.webp',
        'ac-overflow': 'drying-fan-28726413.webp',
        'cabinet-drying': 'cabinet-kitchen-7535073.webp',
        'laundry-overflow': 'laundry-room-19846385.webp',
        'crawl-space-drying': 'crawl-space-4092026.webp',
        'appliance-leak': 'appliance-fridge-3958962.webp',
        'fire-sprinkler-cleanup': 'flooded-floor-7924140.webp',
        'moisture-mapping': 'thermal-imaging-7859781.webp',  # ROUND 6 NEW (partial): thermal imaging screen showing a heat image — measurement tech, not bare hands. Caveat: scan is of a person, not a damp wall; no wall scan exists on Pexels (was bare hands, no device at all)
        'attic-insulation-drying': 'attic-insulation-6124239.webp',
        'wall-drying': 'flood-cut-wall-8488031.webp',  # ROUND 6 NEW: interior wall with drywall cut open exposing studs/framing (was empty finished attic room; caveat: reconstruction context, no air mover visible)
        'west-plano': 'suburban-home-3990589.webp',  # R5: Texas brick + garage (was European estate 7587470)
        'legacy-west': 'texas-home-8278493.webp',
        'north-plano': 'suburban-home-26595553.webp',  # R5: brick + gable, no tile roof (was tile-roof 30707539)
        'central-plano': 'texas-home-8278494.webp',  # R5: Texas neighborhood street; low-profile ranch era still unmatched (was N-European gable 32711440)
        'east-plano': 'brick-ranch-8031875.webp',  # ROUND 6 NEW: single-storey white-painted brick ranch, shingle roof, lawn (was Mediterranean tile-roof house; caveat: painted brick, not red brick)
        'frisco': 'texas-home-8278494.webp',
        'allen': 'suburban-home-18280830.webp',
        'mckinney': 'brick-ranch-8031875.webp',  # ROUND 6 NEW, shared with east-plano hero (recorded): single-storey brick ranch with lawn/driveway, no Mediterranean tile roof (was Mediterranean stone crop)
        'richardson': 'suburban-home-3990589.webp',
        'murphy': 'suburban-home-15303808.webp',
        'shut-off-valve': 'water-shutoff-4494656.webp',  # ROUND 6 NEW: outdoor water meters and shut-off valves on supply pipes, no GAS label (was valve box labelled GAS)
        'warm-spot-on-floor': 'warm-floor-thermal-5853823.webp',  # ROUND 6 NEW (partial): bare feet on sunlit tile beside a floor vent — the line's own bare-foot alternative (was showroom kitchen; caveat: sunlight warmth cue, not a thermal scan)
        'ceiling-dripping': 'ceiling-stain-lived-in-8624466.webp',  # ROUND 6 NEW: furnished living room with a faint brown water stain on the white ceiling (was shabby bedroom with a WALL stain, wrong surface)
        'water-damage-cost': 'suburban-home-26595553.webp',
        'fans-wont-dry-walls': 'mold-wall-4597285.webp',
        'storm-water-category-3': 'flooded-suburban-home-28447764.webp',  # ROUND 6 NEW, shared with flood-cleanup hero (recorded): suburban home in floodwater, green trees (was red cabin + caravan, place fail for Plano)
        'mold-after-water-damage': 'indoor-mold-18063447.webp',  # ROUND 6 NEW: close-up of a white wall speckled with grey-black mold spots (was exterior algae wall; caveat: close-up, not a room scene)
        'copper-pinhole-leaks': 'burst-pipe-36571568.webp',
        'sagging-ceiling': 'sagging-ceiling-30499666.webp',  # ROUND 6 NEW: ceiling panels bowed sharply downward and split open, insulation exposed (was worn ceiling with no sag visible; caveat: grooved panels, not flat drywall)
        'water-damage-insurance-texas': 'insurance-claim-7731397.webp',  # ROUND 6 NEW: two people reviewing a home insurance policy form on a clipboard (was generic office desk + skyline)
        'about': 'plumber-work-6419128.webp',
        'contact': 'burst-pipe-2339722.webp',
    }
    # Round 4 lock: body splits frozen for ALL pages (R4 changes + R1-R3 bodies
    # otherwise unchanged) for the same rotation-churn reason as heroes.
    BODY_FILE = {
        'home': {0: 'suburban-home-31602311.webp', 1: 'burst-pipe-36571568.webp', 2: 'drying-equipment-16243255.webp'},
        'emergency-water-damage': {0: 'texas-home-8278494.webp', 1: 'plumber-work-6419128.webp', 2: 'ceiling-stain-8624464.webp'},
        'water-extraction': {0: 'flooded-floor-7924140.webp', 1: 'sewage-drain-3964564.webp', 2: 'moisture-meter-8961703.webp'},  # R5 body2: indoor wall moisture check (meter check, not behind-wall evidence)
        'structural-drying': {0: 'drying-equipment-16243255.webp', 1: 'drying-fan-28726413.webp', 2: 'moisture-meter-8961703.webp'},  # FINAL FIX body2: wall inspection step of the drying process (caveat: meter not clearly visible; was insulation-install 6124239)
        'burst-pipe-cleanup': {0: 'ceiling-stain-8624464.webp', 1: 'plumber-work-6419128.webp', 2: 'plumber-work-35290675.webp'},  # FINAL FIX body2: technician at pump/hose indoors (caveat: garage/heater not clearly visible; was worn ceiling 14032089)
        'sewage-cleanup': {0: 'sewage-drain-29608837.webp', 1: 'sewage-drain-13961561.webp', 2: 'sewage-drain-3964564.webp'},  # ROUND 6 pool swap body2: metal drainage pipe with visible water runoff (stormwater runoff, closer than the pipe yard; was stacked pipes 17375718)
        'slab-leak': {0: 'burst-pipe-11658940.webp', 1: 'hardwood-floor-3935327.webp', 2: 'mold-wall-9127236.webp'},
        'water-heater-leak': {0: 'plumber-work-6419128.webp', 1: 'attic-insulation-9043415.webp', 2: 'ceiling-stain-3708564.webp'},  # ROUND 6 pool swap body1: spacious bare attic interior with exposed beams (reads as attic space, closer than the furnished bedroom; was attic bedroom 271743); FINAL FIX body0 note kept: 14032089 cannot be body0 — it would flip this page's ceiling card from worn ceiling to skylight
        'ceiling-leak': {0: 'ceiling-stain-14032089.webp', 1: 'attic-insulation-6124239.webp', 2: 'attic-insulation-4482829.webp'},  # ROUND 6 pool swap body1: real insulation subject (install, closer than the finished bedroom; was attic bedroom 271743)
        'flood-cleanup': {0: 'burst-pipe-18274115.webp', 1: 'storm-flood-11537987.webp', 2: 'sewage-drain-3964564.webp'},  # FINAL FIX body1: outdoor floodwater at a residential yard (caveat: caravan/shed, not a Plano brick home or creek; was lobby stairs 7924140; also fixes the home Flood card fallback)
        'commercial-water-damage': {0: 'commercial-office-36631701.webp', 1: 'steel-studs-35496414.webp', 2: 'ceiling-stain-3708564.webp'},  # ROUND 6 NEW body1: exposed metal stud framing (was glass-partition office, no studs visible); body0 wet-office stays OPEN (no wet office photo found)
        # NOTE: fans/cost/wall pair-rule overrides live on their LATER dict entries below (duplicate keys: later wins) — do not re-add them here.
        'hardwood-floor-drying': {0: 'mold-wall-9127236.webp', 1: 'drying-equipment-16243255.webp', 2: 'flooded-floor-7924140.webp'},
        'ac-overflow': {0: 'ceiling-stain-14032089.webp', 1: 'attic-insulation-271743.webp', 2: 'sewage-drain-3964564.webp'},  # FINAL FIX body1: attic room (caveat: no AC unit/pan/water visible; was wall-cavity install 6124239)
        'cabinet-drying': {0: 'kitchen-leak-34295401.webp', 1: 'kitchen-leak-10961064.webp', 2: 'cabinet-kitchen-2398375.webp'},
        'laundry-overflow': {0: 'laundry-room-7282378.webp', 1: 'sewage-drain-3964564.webp', 2: 'ceiling-stain-3708564.webp'},  # FINAL FIX body2: ceiling water-stain detail (caveat: detail only, not a full downstairs room; was lobby stairs 7924140)
        'crawl-space-drying': {0: 'plumber-work-6419128.webp', 1: 'crawl-space-40440109.webp', 2: 'sewage-drain-13961561.webp'},
        'appliance-leak': {0: 'appliance-fridge-4469164.webp', 1: 'kitchen-leak-10961064.webp', 2: 'kitchen-leak-34295401.webp'},
        'fire-sprinkler-cleanup': {0: 'drying-equipment-16243255.webp', 1: 'fire-sprinkler-36631700.webp', 2: 'ceiling-stain-3708564.webp'},  # R5 body1: commercial interior w/ drop-tile ceiling (no sprinkler-discharge photo in pool; fixes home card per its wording)
        'moisture-mapping': {0: 'moisture-meter-8293640.webp', 1: 'ceiling-stain-8624464.webp', 2: 'ceiling-stain-14032089.webp'},
        'attic-insulation-drying': {0: 'attic-insulation-271743.webp', 1: 'crawl-space-4092030.webp', 2: 'attic-insulation-4482829.webp'},  # R5 body0: attic room (no joists/walkway photo in pool)
        'wall-drying': {0: 'thermal-imaging-7859781.webp', 1: 'moisture-meter-8961703.webp', 2: 'hardwood-floor-3935327.webp'},  # ROUND 6 PAIR RULE + NEWLY-NOTICED FIX: body0 (Check These 5 Things) was 8482824, a spirit-level man that pairs with the new structural hero 8293640 under the wall/moisture pair rule — replaced with the thermal screen (thermal imaging IS how you check whether walls got wet; shared with moisture hero + shut-off body2, recorded). Body1 bare-hands 8961703 stays OPEN (no device photo available; thermal cannot repeat on this page).
        'west-plano': {0: 'suburban-home-31602311.webp', 1: 'luxury-interior-36906952.webp', 2: 'greenbelt-home-12445995.webp'},  # ROUND 6 NEW body1: open-plan luxury interior, wide light wood planks + island (caveat: wood species + waterfall edge unverified); body2: rear of house with deck/lawn backed by mature trees + open land (caveat: not a labelled golf course)
        'legacy-west': {0: 'suburban-home-3990589.webp', 1: 'texas-home-23930020.webp', 2: 'texas-home-8278494.webp'},  # FINAL FIX body2: row of attached narrow-lot homes (caveat: pastel look, not Legacy West brick townhomes specifically; was lobby stairs 7924140)
        'north-plano': {0: 'suburban-home-15303808.webp', 1: 'copper-pipes-3721272.webp', 2: 'greenbelt-home-12445995.webp'},  # ROUND 6 NEW body1: copper pipe close-up (caveat: no slab context visible); body2: greenbelt-home shared with west-plano (recorded)
        'central-plano': {0: 'suburban-home-31602311.webp', 1: 'copper-pipes-3721272.webp', 2: 'suburban-home-186077.webp'},  # ROUND 6 NEW body1: copper pipe close-up, shared with north-plano (recorded; caveat: no cast-iron drain visible)
        'east-plano': {0: 'suburban-home-186077.webp', 1: 'pier-beam-home-26261510.webp', 2: 'sewage-drain-29608837.webp'},  # ROUND 6 NEW body1: historic white house with waterfront terrace raised on piers (caveat: terrace on piers, not a full pier-and-beam crawl view; was newer brick house, no piers)
        'frisco': {0: 'suburban-home-186077.webp', 1: 'texas-home-23930020.webp', 2: 'flooded-floor-7924140.webp'},
        'allen': {0: 'suburban-home-26595553.webp', 1: 'suburban-home-3990589.webp', 2: 'attic-insulation-271743.webp'},  # FINAL FIX body2: attic room (caveat: no AC pan/roof/wet insulation visible; was lobby stairs 7924140)
        'mckinney': {0: 'suburban-home-7587470.webp', 1: 'texas-home-33404353.webp', 2: 'suburban-home-186077.webp'},
        'richardson': {0: 'suburban-home-186077.webp', 1: 'suburban-home-30707539.webp', 2: 'copper-pipes-3721272.webp'},  # ROUND 6 CASCADE FIX: body2 is "Aging Copper and Slab Leaks" → copper pipe close-up (the line's first asked option; shared with north+central body1, recorded; was night office tower). Slab-saw was tried here first but it broke the richardson slab card (hero in page files → dedupe to a valve-box photo), so the slab card now renders the slab hero cleanly.
        'murphy': {0: 'suburban-home-32711440.webp', 1: 'texas-home-23928963.webp', 2: 'flooded-floor-7924140.webp'},
        'shut-off-valve': {0: 'burst-pipe-15206136.webp', 1: 'kitchen-leak-10961064.webp', 2: 'thermal-imaging-7859781.webp'},  # ROUND 6 CASCADE FIX: body2 is the "Warm Spot on the Floor" figure → thermal imaging screen (the line's thermal-camera option for finding a warm spot/slab leak; shared with moisture hero, recorded; caveat: person heat image, not a slab scan; was running kitchen faucet). Bare-feet tile was tried here first but it broke the shut-off warm-spot card (hero in page files → dedupe to a dripping-pipe photo), so that card now renders the warm-floor hero cleanly.
        'warm-spot-on-floor': {0: 'burst-pipe-15206136.webp', 1: 'burst-pipe-36571568.webp', 2: 'suburban-home-3990589.webp'},
        'ceiling-dripping': {0: 'ceiling-stain-14032089.webp', 1: 'ceiling-stain-3708564.webp', 2: 'attic-insulation-4482829.webp'},
        'water-damage-cost': {0: 'suburban-home-31602311.webp', 1: 'insurance-claim-7731397.webp', 2: 'plumber-work-6419128.webp'},  # ROUND 6 PAIR RULE: body1 (Why Day One Cuts Cost) was 8293746, same-shoot pair with the new structural hero 8293640 on this page — replaced with the policy-form photo (cost/claim theme; shared with insurance hero, recorded).
        'fans-wont-dry-walls': {0: 'moisture-meter-7937963.webp', 1: 'thermal-imaging-7859781.webp', 2: 'mold-wall-29701042.webp'},  # ROUND 6 PAIR RULE: body1 (Trap 1: Carpet Pad) was 8293746, same-shoot pair with the new structural hero 8293640 on this page — replaced with the thermal screen (hidden-moisture detection fits the unseen-wet-pad trap; shared, recorded). Body0 spirit level stays OPEN (last spirit-level slot).
        'storm-water-category-3': {0: 'flooded-floor-7924140.webp', 1: 'creek-overflow-32159924.webp', 2: 'suburban-home-186077.webp'},  # ROUND 6 NEW body1: water flooding over a creekside path (was dry drainpipe; body0 gallery stairs stays OPEN — no flooded-home-interior photo found)
        'mold-after-water-damage': {0: 'mold-wall-18351809.webp', 1: 'cabinet-kitchen-8146322.webp', 2: 'drying-equipment-16243255.webp'},  # ROUND 6 pool body0: real black mold spotting on a wall (moody abandoned-room look; manifest alt neutralised — no Vorkuta place claim; was peeling paint with NO mold visible); body1 warm/humid interior stays OPEN (none found)
        'copper-pinhole-leaks': {0: 'burst-pipe-4406597.webp', 1: 'suburban-home-3990589.webp', 2: 'plumber-work-6419128.webp'},
        'sagging-ceiling': {0: 'ceiling-stain-8624464.webp', 1: 'suburban-home-30707539.webp', 2: 'ceiling-crew-8293648.webp'},  # ROUND 6 NEW body2: professional worker in hard hat + hi-vis inspecting a ceiling with clipboard (was DIY homeowner painting — contradicted the safety guide's own advice; caveat: inspecting, not drying)
        'water-damage-insurance-texas': {0: 'moisture-meter-8293640.webp', 1: 'plumber-work-6419128.webp', 2: 'commercial-office-13068366.webp'},  # R5 body1: mitigation crew work (pipe work, not drying specifically)
        'about': {0: 'plumber-work-35290675.webp', 1: 'suburban-home-3990589.webp', 2: 'mold-wall-9127236.webp'},
        'contact': {0: 'plumber-work-35290675.webp', 1: 'suburban-home-26595553.webp', 2: 'plumber-work-6419128.webp'},  # R5: crew work + brick subdivision home (was Mediterranean 15303808 / villa 23930020)
    }
    # NOTE: 'home' slug key above is '' in the tab data; remapped below.
    pages = []
    used_heroes = set()
    for tab in tabs:
        slug = tab['slug']
        sections, faqs, faq_heading, _ = classify_and_build(tab)
        hero_topic = HERO_TOPIC.get(slug, 'flooded-floor')
        if slug in HERO_FILE:
            hero = next((im for im in manifest if im['file'] == HERO_FILE[slug]), None)
        else:
            hero = pick(hero_topic, used_heroes)
        if hero:
            used_heroes.add(hero['file'])
        used = {hero['file']} if hero else set()
        # body images: 3 distinct, rotating topics. Area pages use only the
        # area body pools (the old code first assigned default body images and
        # then overwrote them, wasting rotation picks and wrapping hero picks).
        if slug in AREA_SLUGS:
            body_imgs = []
            for bt in ['suburban-home', 'texas-home', 'flooded-floor']:
                im = pick(bt, used)
                if im: body_imgs.append(im); used.add(im['file'])
        else:
            body_topics = BODY_TOPICS.get(slug, [hero_topic, 'suburban-home', 'plumber-work'])
            body_imgs = []
            for bt in body_topics:
                im = pick(bt, used)
                if im:
                    body_imgs.append(im); used.add(im['file'])
        # Pad any emptied topic slot (banned topic, e.g. bathroom-leak)
        # with a neutral suburban exterior so override indices stay aligned.
        _fb = next((im for im in manifest if im['file'] == 'suburban-home-27852347.webp'), None)
        _fb2 = next((im for im in manifest if im['file'] == 'suburban-home-17091309.webp'), None)
        while len(body_imgs) < 3 and _fb:
            body_imgs.append(_fb if len(body_imgs) % 2 == 0 else (_fb2 or _fb))
        # Round 1 fix-pass body overrides (by split slot, not by old file).
        _ov = BODY_FILE.get(slug if slug else 'home', {})
        for _idx, _fname in _ov.items():
            if _idx < len(body_imgs):
                _cand = next((im for im in manifest if im['file'] == _fname), None)
                if _cand:
                    body_imgs[_idx] = _cand
                else:
                    print(f'WARNING: override file missing: {_fname} for {slug}')
        # Round 2 systemic: no file twice on one page — neither the hero
        # repeated as a split nor a split repeated (cabinet's two wrench
        # splits, storm's hero+split caravan pair). Replace any offender
        # with a rotation pick from a neutral topic, never the same file.
        _seen = {hero['file']} if hero else set()
        for _bi, _im in enumerate(body_imgs):
            if _im['file'] in _seen:
                _rep = None
                for _tp in ['suburban-home', 'texas-home', 'flooded-floor', 'ceiling-stain', 'plumber-work', 'moisture-meter']:
                    _rep = pick(_tp, _seen)
                    if _rep:
                        break
                if _rep:
                    print(f'DEDUPE: {slug} body[{_bi}] {_im["file"]} -> {_rep["file"]}')
                    body_imgs[_bi] = _rep
                else:
                    print(f'WARNING: dedupe failed for {slug} body[{_bi}] {_im["file"]}')
            _seen.add(body_imgs[_bi]['file'])
        # links used in body (for related cards)
        body_targets = []
        def collect(blocks):
            for b in blocks:
                if b['type'] == 'para':
                    for text, tgt in b['segs']:
                        if tgt is not None and tgt != slug and tgt not in body_targets:
                            body_targets.append(tgt)
        for s in sections:
            collect(s['blocks'])
        pages.append({'tab': tab, 'sections': sections, 'faqs': faqs, 'faq_heading': faq_heading,
                      'hero': hero, 'body_imgs': body_imgs, 'body_targets': body_targets})
    hero_by_slug = {p['tab']['slug']: p['hero'] for p in pages}
    body_by_slug = {p['tab']['slug']: p['body_imgs'] for p in pages}
    # ---------- write app files ----------
    os.makedirs(APP, exist_ok=True)
    for d in ['services', 'areas', 'guides']:
        os.makedirs(os.path.join(APP, d), exist_ok=True)
    write_favicon()
    write_layout()
    write_css()
    write_components()
    # Round 4 card override: the areas-hub East Plano card was flagged
    # (Mediterranean tile/olive trees at card size) while the east page
    # hero itself was explicitly NOT flagged. Cards linking to east use
    # east's own split image (a plain suburban exterior) instead of its
    # hero; page heroes are untouched (write_page uses hero_by_slug only
    # for cards, never for the page's own hero image).
    card_hero_by_slug = dict(hero_by_slug)
    if 'east-plano' in body_by_slug and body_by_slug['east-plano']:
        card_hero_by_slug['east-plano'] = body_by_slug['east-plano'][0]
    # FINAL FIX card-slot overrides: a card shows its target's hero by
    # default; these targets need a different card face than their hero,
    # WITHOUT changing the hero itself (heroes stay pool-limited where
    # flagged, e.g. water-heater solar hero). Values are manifest entries
    # (file + alt), so card alts stay honest. East override replaces the
    # old body0 rule above (body0 is the home hero, so the home East card
    # fell through to a drain-pipe photo).
    _by_file = {im['file']: im for im in manifest}
    for _tgt, _fname in {
        'east-plano': 'suburban-home-32711440.webp',  # daytime brick house (caveat: tall form, not a historic ranch) — was drain pipe on home grid
        'mckinney': 'suburban-home-186077.webp',  # US suburb home at dusk — was stone villa on areas hub + about card (ROUND 6: frisco override DELETED — it forced the dry-brick 31602311 face onto the areas frisco card; the card now renders the frisco hero)
        'richardson': 'suburban-home-30707539.webp',  # daytime brick home (caveat: clay-tile roof cue) — was night office tower on home + areas grids
        'water-heater-leak': 'plumber-work-35290675.webp',  # technician at pump/hose indoors (caveat: not a tank) — was rooftop solar on every water-heater card
        'attic-insulation-drying': 'attic-insulation-4482829.webp',  # ROUND 6 pool candidate: real foil-faced attic insulation around a skylight (better topic fit than the bedroom; still no wetness/removal shown — card lines stay OPEN-improved, not claimed best-ever)
        'wall-drying': 'flood-cut-wall-8488031.webp',  # ROUND 6 NEW: opened wall cavity with exposed studs (was dry insulation install on every wall card; caveat: reconstruction context, no air mover visible)
        'water-damage-insurance-texas': 'ceiling-stain-lived-in-8624466.webp',  # ROUND 6 NEW: furnished living room with a ceiling water stain — the sudden/gradual card face the R6 lines asked for (was shabby bedroom; guides hub still falls back to an inspector photo because the ceiling-dripping card takes this file first)
        'fire-sprinkler-cleanup': 'fire-sprinkler-36631700.webp',  # office interior with drop-tile ceiling (caveat: no sprinkler discharge or water visible; the R5-accepted home-card face) — was lobby stairs 7924140 on the services hub card, and restores the home fire card which the flood-body fix would otherwise flip to the lobby file
    }.items():
        if _fname in _by_file:
            card_hero_by_slug[_tgt] = _by_file[_fname]
        else:
            print(f'WARNING: card override file missing: {_fname} for {_tgt}')
    for p in pages:
        _cards = card_hero_by_slug
        # ROUND 6: the Final Fix flood guard is REMOVED — it pinned the
        # flood page's extraction card to the bare-hands photo (8961703).
        # The extraction hero is now the PPE wet-vac worker (6195949),
        # which is not among the flood page's files, so the card renders
        # it naturally with no lobby-file risk. This fixes the Round 6
        # flood extraction-card line (crew extracting standing water).
        if p['tab']['slug'] == 'moisture-mapping':
            # ROUND 6 guard: the structural hero is now 8293640, which is
            # this page's own body0 figure — without a guard the structural
            # card would dedupe to the worn outdoor fan (16243255). Pin it
            # to the PPE wet-vac worker (mitigation work) instead.
            # (Note: moisture page's related section currently renders only
            # the slab card, so this guard is defensive — it changes nothing
            # today; the cross-page share is structural cards + moisture body0.)
            _cards = dict(card_hero_by_slug)
            _cards['structural-drying'] = _by_file['water-extraction-6195949.webp']
        if p['tab']['slug'] == 'storm-water-category-3':
            # ROUND 6 guard: the flood hero IS this page's hero, so the
            # flood card dedupes to the flood bodies — spraying pipe,
            # caravan, dry downspout, all flagged. Pin it to the PPE
            # wet-vac worker (flood cleanup work) instead.
            _cards = dict(card_hero_by_slug)
            _cards['flood-cleanup'] = _by_file['water-extraction-6195949.webp']
        write_page(p, _cards, by_slug, body_by_slug)
    write_hub('services', 'Our Water Damage Services in Plano, TX', SERVICE_SLUGS, pages, card_hero_by_slug, by_slug, body_by_slug)
    write_hub('areas', 'Water Damage Restoration Areas Around Plano, TX', AREA_SLUGS, pages, card_hero_by_slug, by_slug, body_by_slug)
    write_hub('guides', 'Plano Water Damage Guides', GUIDE_SLUGS, pages, card_hero_by_slug, by_slug, body_by_slug)
    write_sitemap(pages)
    # summary for QA
    summ = []
    for p in pages:
        t = p['tab']
        summ.append({'slug': t['slug'], 'title': t['title'], 'h1': t['h1'], 'sections': len(p['sections']),
                     'faqs': len(p['faqs']), 'hero': p['hero']['file'] if p['hero'] else None,
                     'body_imgs': [i['file'] for i in p['body_imgs']], 'body_targets': p['body_targets']})
    json.dump(summ, open(os.path.join(BASE, 'pages-summary.json'), 'w'), indent=1)
    print(f"pages={len(pages)} heroes_unique={len(set(p['hero']['file'] for p in pages if p['hero']))} body_slots={sum(len(p['body_imgs']) for p in pages)}")
    return pages

def page_path(slug):
    if slug == '':
        return os.path.join(APP, 'page.jsx')
    return os.path.join(APP, slug, 'page.jsx')

def write_favicon():
    """Brand favicon: navy rounded square + white water drop + teal centre.
    No old-site or Tulsa mark. SVG for crispness + PNG 512 for browsers
    that request a raster icon. Both written into public/ (copied to out/)."""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
<rect width="512" height="512" rx="96" fill="#0e3a5c"/>
<path d="M256 84 C198 200 158 262 158 322 A98 98 0 1 0 354 322 C354 262 314 200 256 84 Z" fill="#ffffff"/>
<circle cx="256" cy="322" r="30" fill="#0e7a7b"/>
</svg>'''
    open(os.path.join(PUBLIC, 'favicon.svg'), 'w').write(svg)
    try:
        from PIL import Image, ImageDraw
        im = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, 511, 511], radius=96, fill='#0e3a5c')
        d.polygon([(256, 84), (196, 290), (316, 290)], fill='white')
        d.ellipse([158, 224, 354, 420], fill='white')
        d.ellipse([226, 292, 286, 352], fill='#0e7a7b')
        im.convert('RGB').save(os.path.join(PUBLIC, 'favicon.png'))
    except Exception as e:
        print(f'WARNING: favicon PNG failed ({e}); SVG still written')

def write_layout():
    open(os.path.join(APP, 'layout.jsx'), 'w').write('''import "./globals.css";
import Reveal from "./components";
export const metadata = { metadataBase: new URL("https://waterdamagerestorationplano.online"), title: { default: "Water Damage Restoration Plano, TX | 24/7 Water Removal" }, description: "Water damage in Plano, TX? 24/7 water extraction, thermal moisture mapping & structural drying across every Plano ZIP. Call (972) 472-7917 now.", icons: { icon: "/favicon.svg", apple: "/favicon.png" } };
export default function RootLayout({ children }) {
  return (<html lang="en"><body>
    <header className="site-header"><div className="wrap header-inner">
      <a className="brand" href="/">Water Damage Restoration <span>Plano</span></a>
      <nav className="main-nav" aria-label="Main">
        <a href="/">Home</a><a href="/services/">Services</a><a href="/areas/">Areas</a><a href="/guides/">Guides</a><a href="/about/">About</a><a href="/contact/">Contact</a>
      </nav>
      <a className="header-call" href="tel:+19724727917">Call 24/7: <span className="nowrap">(972) 472-7917</span></a>
    </div></header>
    <main>{children}</main>
    <footer className="site-footer"><div className="wrap footer-grid">
      <div><h3>Water Damage Restoration Plano</h3><p>Plano, TX &amp; Collin County<br /><a href="tel:+19724727917">(972) 472-7917</a><br />Open 24/7</p></div>
      <div><h3>Best Services</h3><ul>
        <li><a href="/emergency-water-damage/">24/7 Emergency Water Damage Cleanup</a></li>
        <li><a href="/water-extraction/">Standing Water Extraction</a></li>
        <li><a href="/structural-drying/">Structural Drying</a></li>
        <li><a href="/burst-pipe-cleanup/">Burst &amp; Frozen Pipe Cleanup</a></li>
        <li><a href="/slab-leak/">Slab Leak Water Damage</a></li>
        <li><a href="/sewage-cleanup/">Sewage Backup Cleanup</a></li>
      </ul></div>
      <div><h3>Quick Links</h3><ul>
        <li><a href="/services/">All Services</a></li><li><a href="/areas/">Service Areas</a></li>
        <li><a href="/guides/">Guides</a></li><li><a href="/about/">About Us</a></li><li><a href="/contact/">Contact Us</a></li>
      </ul></div>
      <div><h3>Emergency Help</h3><p>Water spreading right now? Call first, then shut off the water and power to wet rooms. Crews stage along US-75, the Dallas North Tollway, the George Bush Turnpike and SH-121.</p><p><a className="btn-call" href="tel:+19724727917">Call 24/7: <span className="nowrap">(972) 472-7917</span></a></p></div>
    </div>
    <div className="footer-bottom"><div className="wrap">Water Damage Restoration Plano · Plano, TX &amp; Collin County · (972) 472-7917 · Open 24/7<br />Services are provided through our network of local water mitigation technicians and restoration partners serving Plano and Collin County.</div></div>
    </footer>
    <a className="mobile-call-bar" href="tel:+19724727917">Call Now: (972) 472-7917</a>
    <Reveal />
  </body></html>);
}
''')

def write_components():
    open(os.path.join(APP, 'components.jsx'), 'w').write('''"use client";
import { useEffect } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";
// Tier 1 animation, actually running (Final added scope, 2026-11-04).
// Correction to the brief: a GSAP reveal WAS already wired (0.5s, 18px,
// hover-only card 3D, no Lenis) — that is why motion looked absent. This
// upgrade keeps the same progressive-enhancement rule (no CSS hiding:
// content is visible without JS; GSAP only animates FROM a translated /
// faded state when JS runs) and adds: Lenis smooth scroll, stronger
// scroll reveals (transform + opacity only, never layout properties,
// so no CLS), a scroll-into-view 3D tilt for cards that works on touch
// (hover 3D stays for pointer devices via CSS), and a homepage-only
// hero scrub (image scale/parallax + text fade/slide driven by scroll).
// No WebGL / R3F: held by the speed kill-switch, not added silently.
// Reduced motion: no Lenis, no reveals, no scrub — native scroll, static hero.
// Phone CTA / sticky call bar are never targeted by any animation.
export default function Reveal() {
  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) {
      window.__plano3Anim = { lenis: false, reduced: true, reveals: 0, heroScrub: false };
      document.documentElement.dataset.anim = "reduced-motion";
      return;
    }
    gsap.registerPlugin(ScrollTrigger);
    const lenis = new Lenis({ duration: 1.15, smoothWheel: true });
    lenis.on("scroll", ScrollTrigger.update);
    const raf = (time) => { lenis.raf(time * 1000); };
    gsap.ticker.add(raf);
    gsap.ticker.lagSmoothing(0);
    const els = gsap.utils.toArray(".reveal");
    els.forEach((el) => {
      const isCard = el.classList && el.classList.contains("card");
      const from = isCard
        ? { opacity: 0, y: 28, rotationX: 5, transformPerspective: 900 }
        : { opacity: 0, y: 28 };
      gsap.from(el, { ...from, duration: 0.9, ease: "power3.out", clearProps: "transform,opacity",
        scrollTrigger: { trigger: el, start: "top 88%", once: true } });
    });
    // Homepage hero scrub only (.hero-home exists on the home page alone).
    // Poster = the existing hero image; no video file is invented or needed.
    const hero = document.querySelector(".hero-home");
    let heroScrub = false;
    if (hero) {
      const img = hero.querySelector(".hero-img");
      const text = hero.querySelector(".hero-grid > div");
      if (img) {
        gsap.fromTo(img, { scale: 1, yPercent: 0 },
          { scale: 1.12, yPercent: -8, ease: "none",
            scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
        heroScrub = true;
      }
      if (text) {
        gsap.fromTo(text, { y: 0, opacity: 1 },
          { y: -50, opacity: 0.15, ease: "none",
            scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
        heroScrub = true;
      }
    }
    window.__plano3Anim = { lenis: true, reduced: false, reveals: els.length, heroScrub: heroScrub };
    document.documentElement.dataset.anim = "on";
    return () => {
      ScrollTrigger.getAll().forEach((t) => t.kill());
      gsap.ticker.remove(raf);
      lenis.destroy();
    };
  }, []);
  return null;
}
''')

def write_css():
    open(os.path.join(APP, 'globals.css'), 'w').write('''
:root{--ink:#0f2537;--navy:#0a3550;--teal:#0d7a6e;--ocean:#0a5f7a;--rust:#9a3412;--cta:#9a3412;--cta-hover:#7c2d12;--cream:#f7f3ea;--line:#d8e0e6}
*{box-sizing:border-box}html{scroll-behavior:auto}body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#1d2b36;background:#fff;font-size:19px;line-height:1.7}
/* Reveal: visible by default. GSAP (components.jsx) animates FROM a translated/faded state only when JS runs — content is never hidden by CSS, so crawlers and no-JS readers always see it. */
:focus-visible{outline:3px solid #0d7a6e;outline-offset:3px}
a{color:#064d73;text-decoration:none}a:hover,a:focus-visible{text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:2px}.brand:hover,.main-nav a:hover,.card-body h3 a:hover,.btn-call:hover,.header-call:hover,.mobile-call-bar:hover{text-decoration:none}p a[href^="tel:"]{text-decoration:none}p a[href^="tel:"]:hover,p a[href^="tel:"]:focus-visible{text-decoration:none}
a:hover{color:#084a70}.wrap{max-width:1240px;margin:0 auto;padding:0 20px}
.site-header{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid var(--line);box-shadow:0 2px 10px rgba(0,0,0,.06)}
.header-inner{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 20px;flex-wrap:wrap}
.brand{display:inline-block;padding:11px 0;font-weight:800;color:var(--ink);text-decoration:none;font-size:20px}.brand span{color:var(--teal)}
.main-nav{display:flex;gap:16px;flex-wrap:wrap}.main-nav a{color:var(--ink);text-decoration:none;font-weight:600;font-size:16px;padding:13px 6px}
.header-call,.btn-call{display:inline-block;background:var(--cta);color:#fff!important;text-decoration:none;font-weight:800;padding:12px 20px;border-radius:12px;border:0;cursor:pointer}.btn-call .nowrap,.header-call .nowrap{white-space:nowrap}a[href^="tel:"]{white-space:nowrap}
.header-call:hover,.btn-call:hover{background:var(--cta-hover)}
.contact-form button.btn-call:hover{background:var(--cta-hover)}
.hero{background:radial-gradient(ellipse 90% 120% at 85% 0%,rgba(45,212,191,.20),transparent 55%),linear-gradient(135deg,#041c2b 0%,#0a3550 48%,#0d7a6e 100%);color:#fff;padding:28px 0 32px;overflow:hidden}
.hero h1{font-size:44px;line-height:1.15;margin:0 0 14px;color:#fff;text-wrap:balance}
.hero p{font-size:19px;color:#e6f4f1}.hero a{color:#d9f4ff}
.hero-img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:14px;display:block;margin-top:18px}
.hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:28px;align-items:center}
@media(max-width:820px){.hero-grid{grid-template-columns:1fr}.hero h1{font-size:32px}body{font-size:18px}}
.trust-band{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}.trust-band .check{background:#e7f5f2;border:1px solid #bfe3dd;color:#084f49;font-weight:700;padding:8px 12px;border-radius:999px;font-size:15px}
section.block{padding:30px 0}section.block:nth-child(even){background:var(--cream)}
.section-kicker{font-size:14px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#475569;margin:0 0 8px}
h2{font-size:32px;line-height:1.25;color:#0a3550;margin:0 0 14px;border-left:6px solid #e4572e;padding-left:14px;text-wrap:balance}
h3{font-size:23px;color:#92400e;margin:26px 0 10px}
p{margin:0 0 14px}ul{margin:0 0 16px;padding-left:22px}li{margin-bottom:8px;line-height:1.7}
.listhead{margin:20px 0 6px}.cta-row{margin:18px 0}
.split{display:block;margin:28px 0;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}
.split img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;display:block}
.split figcaption{padding:18px;font-size:16px;color:#33475b;display:block}
.split.rev figcaption{order:0}
.split-sticky-fig{margin:28px 0 0}.split-sticky-fig img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;display:block;border-radius:14px}.split-sticky-fig figcaption{padding:14px 4px 0;font-size:16px;color:#33475b}
@media(min-width:821px){.split-sticky-sec .wrap{display:grid;grid-template-columns:1fr 380px;gap:28px;align-items:start}.split-sticky-fig{position:sticky;top:96px;margin:0}}
.topup-figure{display:block;margin:28px 0;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}.topup-figure img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;display:block}.topup-figure figcaption{padding:18px;font-size:16px;color:#33475b;display:block}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:10px 0 30px}
@media(max-width:820px){.cards{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.cards{grid-template-columns:1fr}}
.cards.thin{grid-template-columns:repeat(auto-fit,minmax(280px,360px));justify-content:center}
.card{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff;transition:transform .3s ease,box-shadow .3s ease;transform:perspective(900px) rotateX(0deg)}
@media(hover:hover){.card:hover{transform:perspective(900px) rotateX(3deg) translateY(-4px);box-shadow:0 14px 30px rgba(0,0,0,.12)}}
.card img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;display:block}
.card-body{padding:14px}.card-body h3{margin:0 0 6px;font-size:19px}.card-body h3 a{color:#0a3550;text-decoration:none;display:inline-block;padding:11px 0}
.faq-item{border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:14px;background:#fff}
.faq-item h3{margin:0 0 8px}.faq-item p{margin:0}
section.block.dark{background:#0a3550;color:#fff;padding:30px 0}section.block.dark h2{color:#fff}section.block.dark a{color:#a9dbff}section.block.dark p{color:#eaf3f8}
.site-footer{background:#0f2537;color:#dbe7ef;margin-top:0;padding:36px 0 0}.site-footer h3{color:#fff}.site-footer a{color:#a9dbff}.site-footer li a,.site-footer p a{display:inline-block;padding:11px 0}
.footer-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}
@media(max-width:820px){.footer-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:520px){.footer-grid{grid-template-columns:1fr}}
.footer-bottom{border-top:1px solid #2e4a61;margin-top:28px;padding:16px 0;font-size:14px}
.map-frame{width:100%;height:360px;border:0;border-radius:12px}
.mobile-call-bar{display:none}
@media(max-width:820px){.mobile-call-bar{display:block;position:fixed;left:0;right:0;bottom:0;z-index:60;background:var(--cta);color:#fff;text-align:center;font-weight:800;padding:14px;text-decoration:none}body{padding-bottom:52px}}
@media(max-width:520px){.header-inner{padding:8px 16px;gap:8px}.brand{font-size:18px;padding:11px 0}.main-nav{gap:10px}.main-nav a{font-size:14px;padding:14px 2px}.header-call{display:none}}
.contact-form{display:grid;gap:14px;max-width:640px}.contact-form label{font-weight:600;display:grid;gap:6px}
.contact-form input,.contact-form select,.contact-form textarea{padding:11px;border:1px solid #b9c6cf;border-radius:10px;font-size:17px;width:100%}
.radio-row{display:flex;gap:16px;align-items:center;flex-wrap:wrap}.radio-row label{display:flex;gap:6px;align-items:center;font-weight:600}.radio-row input{width:auto}
.form-note{font-size:16px;color:#33475b}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}.card{transition:none;transform:none}}
''')

def jsonld(obj):
    # JSON.stringify at runtime: avoids template-literal escaping breaking
    # JSON when a question/answer contains double quotes.
    return '<script type="application/ld+json" dangerouslySetInnerHTML={{__html: JSON.stringify(' + json.dumps(obj, ensure_ascii=False) + ')}} />'

# Round 2 per-slot figcaptions where the generic stock-tail purge leaves a
# caption that still does not fit its slot (moldy-wall photo under a
# storm/sewage section vs under a drywall-wicking section). Captions are
# metadata, never doc body words, so rewriting them touches no content.
SPLIT_CAPTION = {
    ('wall-drying', 1): 'Interior wall check during a moisture inspection',  # FINAL FIX: was a wicking claim for the old algae-wall file; new file is an interior wall check with no wicking visible
    ('burst-pipe-cleanup', 2): 'Technician adjusting a water pump indoors',  # FINAL FIX: was a worn-ceiling caption for the old ceiling file; new file is pump/hose work
    ('sagging-ceiling', 2): 'Ceiling work in a modern home interior',  # FINAL FIX: new file shows ceiling work (painting); caption claims no drying/removal
    # Round 3: both rusty-grate photos keep the photo but lose the stock
    # tail caption; the caption is metadata, never doc body words.
    ('sewage-cleanup', 1): 'Close-up photo of a rusty drain grate with moss',
    ('crawl-space-drying', 2): 'Close-up photo of a rusty drain grate with moss',
    # Round 5: Allen clay/slab split gets a topic caption, not the stock
    # listing copy the old white-modern-house file carried.
    ('allen', 1): 'Brick suburban home with garage and basketball hoop',  # ROUND 6: neutral pixels-only caption — old caption overclaimed a verified Allen home the pixels cannot prove
    ('mold-after-water-damage', 0): 'Black mold spotting on an interior wall',  # ROUND 6: neutral caption for the 18351809 mold figure — no place claim, no abandoned-building framing
}

# Top-up figures (link-underline + image-optimization round): one genuinely
# relevant figure per page below 5 content images (hero + splits). Every
# file was checked against the page's full image set (no same-page
# duplicate) and viewed-pixel verified where it is a new pool file.
# Captions describe only the pixels — no city, damage or job claim.
# 8 pages have NO fitting unused file and stay honestly at 4 content
# images: sewage-cleanup, water-heater-leak, ac-overflow,
# crawl-space-drying, fire-sprinkler-cleanup, water-damage-cost,
# water-damage-insurance-texas, shut-off-valve. Hubs already show 10-20
# card images and get no top-up. Deliberate shares (same fitting file on
# two pages): steel-studs wall/structural, ceiling-crew emergency/
# ceiling-leak, moisture-meter-8961703 moisture/about, greenbelt home/murphy,
# suburban homes across area pages.
TOPUP = {
    '': ('greenbelt-home-12445995.webp', 'Rear of a suburban home with deck and lawn backed by trees'),
    'emergency-water-damage': ('ceiling-crew-8293648.webp', 'Technician in safety vest inspecting a ceiling'),
    'burst-pipe-cleanup': ('burst-pipe-15206136.webp', 'Leaking plastic pipe with water dripping'),
    'slab-leak': ('plumber-work-6419128.webp', 'Plumber installing pipes'),
    'water-extraction': ('flooded-suburban-home-28447764.webp', 'Floodwater standing across a suburban home front yard'),
    'structural-drying': ('steel-studs-35496414.webp', 'Unfinished building with exposed metal stud framing'),
    'moisture-mapping': ('moisture-meter-8961703.webp', 'Technician checking a wall during inspection'),
    'attic-insulation-drying': ('attic-insulation-9043415.webp', 'Attic interior with exposed wooden beams'),
    'wall-drying': ('steel-studs-35496414.webp', 'Unfinished building with exposed metal stud framing'),
    'hardwood-floor-drying': ('luxury-interior-36906952.webp', 'Open-plan room with light wood plank floors'),
    'cabinet-drying': ('cabinet-kitchen-37030080.webp', 'Blue kitchen cabinet doors'),
    'laundry-overflow': ('laundry-room-4993073.webp', 'Laundry room with washing machine'),
    'appliance-leak': ('appliance-fridge-36671734.webp', 'Woman reaching into an open refrigerator'),
    'commercial-water-damage': ('commercial-office-22711217.webp', 'Office desk with computer and plant'),
    'flood-cleanup': ('flooded-floor-7924140.webp', 'Flooded area with stairs reflecting on water'),
    'mold-after-water-damage': ('mold-wall-4597285.webp', 'Old cement wall with mold blots'),
    'storm-water-category-3': ('storm-flood-11537987.webp', 'House and caravan surrounded by floodwaters'),
    'copper-pinhole-leaks': ('copper-pipes-3721272.webp', 'Copper pipe with elbow joint'),
    'sagging-ceiling': ('ceiling-stain-14032089.webp', 'Worn ceiling with hanging lamp in a dim room'),
    'fans-wont-dry-walls': ('drying-equipment-16243255.webp', 'Industrial fan'),
    'warm-spot-on-floor': ('thermal-imaging-7859781.webp', 'Thermal imaging screen showing heat patterns'),
    'ceiling-dripping': ('ceiling-stain-8624464.webp', 'Bedroom ceiling with water stains'),
    'ceiling-leak': ('ceiling-crew-8293648.webp', 'Technician in safety vest inspecting a ceiling'),
    'about': ('moisture-meter-8961703.webp', 'Technician checking a wall during inspection'),
    'contact': ('flood-cut-wall-8488031.webp', 'Interior wall cut open to expose studs during reconstruction'),
    'allen': ('suburban-home-7587470.webp', 'Brick house with garden and driveway'),
    'mckinney': ('suburban-home-18280830.webp', 'Suburban home exterior'),
    'richardson': ('suburban-home-32711440.webp', 'Brick house with large windows'),
    'murphy': ('greenbelt-home-12445995.webp', 'Rear of a suburban home with deck and lawn backed by trees'),
    'frisco': ('suburban-home-26595553.webp', 'Brick house with gable roof and greenery'),
    'west-plano': ('suburban-home-186077.webp', 'Suburban home exterior'),
    'north-plano': ('suburban-home-186077.webp', 'Suburban home exterior'),
    'central-plano': ('suburban-home-26595553.webp', 'Brick house with gable roof and greenery'),
    'east-plano': ('suburban-home-7587470.webp', 'Brick house with garden and driveway'),
    'legacy-west': ('suburban-home-32711440.webp', 'Brick house with large windows'),
}

def write_page(p, hero_by_slug, by_slug, body_by_slug=None):
    tab = p['tab']; slug = tab['slug']
    sections = p['sections']; faqs = p['faqs']
    hero = p['hero']; body_imgs = p['body_imgs']
    # hero intro: first para of first section
    hero_para = ''
    secs = []
    for s in sections:
        secs.append(s)
    if secs and secs[0]['blocks']:
        for bi, b in enumerate(secs[0]['blocks']):
            if b['type'] == 'para':
                hero_para = para_html(b, slug)
                secs[0] = dict(secs[0]); secs[0]['blocks'] = secs[0]['blocks'][:bi] + secs[0]['blocks'][bi+1:]
                break
    # Final CTA sections (heading contains the call phone) render AFTER the
    # FAQ, matching doc order: sections, FAQ, final CTA.
    trailing_secs = []
    cut = None
    for ti, s in enumerate(secs):
        if s['heading'] and 'Call (972)' in s['heading']:
            cut = ti; break
    if cut is not None:
        trailing_secs = secs[cut:]
        secs = secs[:cut]
    # build sections html
    out_sections = []
    split_idx = 0
    sec_count = 0
    # Round 5 group-intro carry-over: the storm/mold group-intro sections
    # (H2 + one label para) render as lone beige bands. Instead of
    # emitting their own band, stash (heading, label) and prepend them
    # as kicker + lead paragraph to the NEXT section's band. Section
    # indices (si) are untouched, so split placement after sections
    # 1/3/5 does not shift. Scoped to the two _GROUP_INTRO headings.
    _GROUP_INTRO = {('storm-water-category-3', 'How the Water Got In Decides What Has to Happen'),
                    ('mold-after-water-damage', 'Hour-by-Hour: What Happens Inside Wet Walls and Floors')}
    pending_group = None
    for si, s in enumerate(secs):
        if s['heading'] is None and not s['blocks']:
            continue
        # A section containing ONLY a lone Call button (no heading, no copy)
        # renders as a gaping empty band duplicating the hero/header CTA.
        # Suppress it: hero, header, footer and sticky bar already carry
        # the phone, so no doc words are lost by dropping the duplicate.
        if s['heading'] is None and s['blocks'] and all(b['type'] == 'cta' for b in s['blocks']):
            # Round 5: the contact exception is DELETED. The '[Tap to
            # Call]' button is moved into the Emergency section by
            # gen3.py (j3), so 'tap' still appears on the page and no
            # lone button band can ever render again. Every lone-CTA
            # section is suppressed: hero, header, footer and sticky
            # bar already carry the phone.
            continue
        # Round 3: a section holding ONLY trust pills + a lone Call button
        # (home trust band after hero-para removal) renders as a lone
        # button row under the pills. Drop the duplicate button; the hero
        # CTA row, header, footer and sticky bar already carry the phone,
        # and the CTA label is UI, never doc words.
        if s['heading'] is None and s['blocks'] and any(b['type'] == 'trust' for b in s['blocks']) and all(b['type'] in ('trust', 'cta') for b in s['blocks']):
            s = dict(s, blocks=[b for b in s['blocks'] if b['type'] != 'cta'])
        # Round 5 group-intro carry-over (see above): stash and skip.
        # This section's index is 2 on both pages — not a split index
        # (1/3/5) — so no split is lost and later splits stay attached
        # to the same sections as today.
        if ((slug, s['heading']) in _GROUP_INTRO and len(s['blocks']) == 1
                and s['blocks'][0]['type'] == 'para'):
            pending_group = (s['heading'],
                             ' '.join(t for t, _ in s['blocks'][0]['segs']))
            continue
        inner = ''
        if pending_group is not None:
            _gh, _gt = pending_group
            inner += f'<p className="section-kicker">{esc(_gh)}</p>'
            inner += f'<p>{esc(_gt)}</p>'
            pending_group = None
        # Round 3: a calendar parent holding only a cost heading is a
        # layout fold, not a section — render the parent as a small kicker
        # above the cost H2 instead of an H2 promising a calendar section.
        if s.get('parent') and 'Calendar' in s['parent'] and s['heading'] and 'Cost' in s['heading']:
            inner += f'<p className="section-kicker">{esc(s["parent"])}</p>'
            inner += f'<h2>{esc(s["heading"])}</h2>'
        # Round 4: "Quick Diagnosis Table" as a parent H2 promises table
        # rows that do not exist (the body is an essay). Render it as a
        # kicker above the real H2 instead — words preserved, no false
        # table promise.
        elif s.get('parent') == 'Quick Diagnosis Table' and s['heading']:
            inner += f'<p className="section-kicker">{esc(s["parent"])}</p>'
            inner += f'<h2>{esc(s["heading"])}</h2>'
        elif s.get('parent'):
            inner += f'<h2>{esc(s["parent"])}</h2>'
            if s['heading']:
                inner += f'<h3>{esc(s["heading"])}</h3>'
        elif s['heading']:
            inner += f'<h2>{esc(s["heading"])}</h2>'
        for b in s['blocks']:
            inner += block_html(b, slug)
        if not inner.strip():
            continue
        # Round 3: a heading + exactly one subhead block (area at-a-glance
        # shells, group intros) is a layout fold — render as a plain
        # heading pair with NO section band, so no empty cream band opens.
        # Words and order are preserved; the pair flows into the following
        # section's content. Covers the 10 area at-a-glance shells plus
        # warm-spot / fans / storm / mold group intros (same pattern).
        _subhead_only = bool(s['heading']) and s['blocks'] and all(b['type'] == 'subhead' for b in s['blocks'])
        if _subhead_only:
            out_sections.append(f'<div className="wrap">{inner}</div>')
        else:
            out_sections.append(f'<section className="block reveal"><div className="wrap">{inner}</div></section>')
        sec_count += 1
        # split images after sections 1 and 3 (and 5) — at least 2 per page
        if si in (1, 3, 5) and split_idx < len(body_imgs):
            im = body_imgs[split_idx]
            cap = SPLIT_CAPTION.get((slug, split_idx), alt_text(im['alt']))
            split_idx += 1
            rev = ' rev' if split_idx % 2 == 0 else ''
            _cap_html = esc(cap) if (slug, split_idx - 1) in SPLIT_CAPTION else cap
            # Sticky split: long sections (>=800 chars of text) get the
            # figure inside the section, sticky on desktop, so the image
            # stays visible while its paragraph scrolls. A hidden parity
            # placeholder keeps the section-band (nth-child) order identical.
            _text_len = len(re.sub(r'<[^>]+>', '', inner).strip())
            if _text_len >= 800 and out_sections and out_sections[-1].startswith('<section'):
                out_sections[-1] = f'<section className="block reveal split-sticky-sec"><div className="wrap"><div className="sticky-text">{inner}</div><figure className="split-sticky-fig">{img_tag(im["file"], alt_text(im["alt"]), "sticky")}<figcaption>{_cap_html}</figcaption></figure></div></section>'
                out_sections.append('<div className="wrap" aria-hidden="true" hidden></div>')
            else:
                out_sections.append(f'<div className="wrap"><figure className="split{rev}">{img_tag(im["file"], alt_text(im["alt"]), "split")}<figcaption>{_cap_html}</figcaption></figure></div>')
        # homepage cards — exclude the page's own hero + splits so no card
        # repeats a photo already on the home page (Round 2 systemic).
        _page_files = ({hero['file']} if hero else set()) | {i['file'] for i in body_imgs}
        if slug == '' and s['heading'] == 'Water Damage Restoration Services in Plano, TX':
            out_sections.append(cards_html('Our Services in Plano, TX', SERVICE_SLUGS, hero_by_slug, by_slug, exclude=_page_files, body_by_slug=body_by_slug))
        if slug == '' and s['heading'] and s['heading'].startswith('Serving Every Plano ZIP Code'):
            out_sections.append(cards_html('Areas We Serve Around Plano', AREA_SLUGS, hero_by_slug, by_slug, exclude=_page_files, body_by_slug=body_by_slug))
    if pending_group is not None:
        # Safety: group-intro was the last section (never happens on
        # storm/mold today) — emit its words rather than dropping them.
        _gh, _gt = pending_group
        out_sections.append(f'<div className="wrap"><p className="section-kicker">{esc(_gh)}</p><p>{esc(_gt)}</p></div>')
        pending_group = None
    # remaining body images if fewer sections
    while split_idx < min(2, len(body_imgs)) and sec_count >= 1:
        im = body_imgs[split_idx]
        cap = SPLIT_CAPTION.get((slug, split_idx), alt_text(im['alt']))
        split_idx += 1
        out_sections.append(f'<div className="wrap"><figure className="split">{img_tag(im["file"], alt_text(im["alt"]), "split")}<figcaption>{esc(cap) if (slug, split_idx - 1) in SPLIT_CAPTION else cap}</figcaption></figure></div>')
    # top-up figure: pages below 5 content images (hero + splits) get one
    # genuinely relevant figure, viewed-pixel verified, never a wrong-topic
    # filler. 8 pages have no fitting unused file and stay honestly at 4
    # (sewage, water-heater, ac-overflow, crawl-space, fire-sprinkler,
    # water-damage-cost, water-damage-insurance-texas, shut-off-valve).
    _top = TOPUP.get(slug)
    if _top:
        _tf, _tcap = _top
        out_sections.append(f'<div className="wrap"><figure className="topup-figure">{img_tag(_tf, _tcap, "split")}<figcaption>{esc(_tcap)}</figcaption></figure></div>')
    # trailing final-CTA sections (rendered after FAQ, see below)
    trailing_sections_html = ''
    for s in trailing_secs:
        inner = ''
        if s.get('parent'):
            inner += f'<h2>{esc(s["parent"])}</h2>'
            if s['heading']:
                inner += f'<h3>{esc(s["heading"])}</h3>'
        elif s['heading']:
            inner += f'<h2>{esc(s["heading"])}</h2>'
        for b in s['blocks']:
            inner += block_html(b, slug)
        if inner.strip():
            trailing_sections_html += f'<section className="block dark"><div className="wrap">{inner}</div></section>'
    # related cards before FAQ (non-home)
    if slug != '':
        rel = []
        for tgt in p['body_targets']:
            if tgt in SERVICE_SLUGS or tgt in AREA_SLUGS or tgt in GUIDE_SLUGS:
                rel.append(tgt)
            if len(rel) >= 6:
                break
        # Round 3: appliance-leak has NO Related section because its links
        # sit outside para blocks (body_targets misses them). Fall back to
        # genuinely related cards wired to the page's existing links.
        # body_targets collection is NOT widened globally — that would
        # change related grids on other pages.
        if slug == 'appliance-leak' and not rel:
            rel = [t for t in ['cabinet-drying', 'hardwood-floor-drying', 'wall-drying', 'shut-off-valve']
                   if t in SERVICE_SLUGS or t in AREA_SLUGS or t in GUIDE_SLUGS]
        if rel:
            # Thin related grids (1-2 cards) centre instead of leaving
            # empty columns — never padded with irrelevant cards.
            # The top-up file (if any) is excluded too, so no related
            # card repeats the top-up figure on the same page.
            _page_files = ({hero['file']} if hero else set()) | {i['file'] for i in body_imgs} | ({TOPUP[slug][0]} if slug in TOPUP else set())
            out_sections.append(cards_html('Related Services & Guides', rel, hero_by_slug, by_slug, thin=len(rel) < 3, exclude=_page_files, body_by_slug=body_by_slug))
    # FAQ — split a final CTA that was absorbed into the last answer:
    # a sentence containing 'Call (972) 472-7917.' that is not the answer's
    # first sentence, followed by more text, belongs after the FAQ.
    trailing_html = ''
    faqs = [dict(f) for f in faqs]
    if faqs:
        last_a = clean_text(faqs[-1]['a'])
        m = re.search(r'(?<!^)([A-Z][^.!?]*?Call \(972\) 472-7917\.)\s+(.{20,})$', last_a, re.S)
        if m and last_a[:m.start(1)].strip():
            faqs[-1]['a'] = last_a[:m.start(1)].strip()
            trailing_html = f'<section className="block dark"><div className="wrap"><h2>{esc(m.group(1))}</h2><p>{render_seg_text(m.group(2), slug)}</p><p><a className="btn-call" href="{TEL}">Call 24/7: <span className="nowrap">{PHONE}</span></a></p></div></section>'
    # FAQ
    faq_html = ''
    if faqs:
        items = ''
        faq_objs = []
        for f in faqs:
            q = clean_text(f['q']); a = clean_text(f['a'])
            # strip trailing link fragments that were absorbed: keep as written (schema must match visible)
            items += f'<div className="faq-item"><h3>{esc(q)}</h3><p>{render_seg_text(a, slug)}</p></div>'
            faq_objs.append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'<[^>]+>', '', render_seg_text(a, slug))}})
        faq_html = f'<section className="block"><div className="wrap"><h2>{esc(p["faq_heading"] or "Frequently Asked Questions")}</h2>{items}</div></section>'
        faq_schema = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': faq_objs}
    else:
        faq_schema = None
    # schemas
    schemas = []
    if faq_schema:
        schemas.append(faq_schema)
    schemas.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': DOMAIN + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': tab['title'], 'item': DOMAIN + href_for(slug)}]})
    if slug in SERVICE_SLUGS:
        schemas.append({'@context': 'https://schema.org', '@type': 'Service', 'name': tab['title'],
                        'provider': {'@type': 'LocalBusiness', 'name': BRAND, 'telephone': PHONE, 'areaServed': 'Plano, TX'},
                        'areaServed': 'Plano, TX'})
    if slug == '' or slug == 'contact':
        schemas.append({'@context': 'https://schema.org', '@type': 'LocalBusiness', 'name': BRAND,
                        'telephone': PHONE, 'areaServed': 'Plano, TX', 'openingHours': 'Mo-Su 00:00-24:00',
                        'url': DOMAIN + '/', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Plano', 'addressRegion': 'TX', 'addressCountry': 'US'}})
    schema_tags = '\n'.join(jsonld(s) for s in schemas)
    # footer map: every page except area pages
    map_html = ''
    if slug not in AREA_SLUGS:
        q = 'Plano, TX' if slug not in ('frisco','allen','mckinney','richardson','murphy') else {'frisco':'Frisco, TX','allen':'Allen, TX','mckinney':'McKinney, TX','richardson':'Richardson, TX','murphy':'Murphy, TX'}[slug]
        map_html = f'<section className="block"><div className="wrap"><h2>Find Us in {esc(q)}</h2><iframe className="map-frame" loading="lazy" title="Map of {esc(q)}" src="https://www.google.com/maps?q={q.replace(" ", "%20")}&output=embed"></iframe></div></section>'
    hero_img = img_tag(hero['file'], alt_text(hero['alt']), 'hero', eager=True, cls='hero-img') if hero else ''
    og_images = f'["/images/{hero["file"]}"]' if hero else '[]'
    hero_cls = 'hero hero-home' if slug == '' else 'hero'  # homepage hero only: the scroll-scrub target; inner pages + hubs keep plain 'hero'
    meta_title_j = json.dumps(tab["meta_title"] or tab["h1"])
    meta_desc_j = json.dumps(tab["meta_desc"])
    content = f'''export const metadata = {{ title: {meta_title_j}, description: {meta_desc_j}, alternates: {{ canonical: "{DOMAIN}{href_for(slug)}" }}, openGraph: {{ title: {meta_title_j}, description: {meta_desc_j}, url: "{DOMAIN}{href_for(slug)}", images: {og_images} }} }};
export default function Page() {{
  return (<>
    {schema_tags}
    <div className="{hero_cls}"><div className="wrap hero-grid"><div>
      <h1>{esc(tab["h1"])}</h1>
      {hero_para}
      <p><a className="btn-call" href="{TEL}">Call Now: <span className="nowrap">{PHONE}</span></a></p>
    </div>{hero_img}</div></div>
    {''.join(out_sections)}
    {faq_html}
    {trailing_sections_html}
    {trailing_html}
    {map_html}
  </>);
}}
'''
    path = page_path(slug)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(content)

def cards_html(title, slugs, hero_by_slug, by_slug, thin=False, exclude=None, body_by_slug=None):
    """Round 2 systemic: a card image must never repeat a photo already on
    the same page (split+card, hero+card). When the target's hero is in the
    page's exclude set (or already chosen in this grid), swap the card to
    the target's first body image that is free on this page.
    Round 5: the chosen-set rule now applies on hubs too (exclude=None).
    Two hub targets can share one hero file (west/richardson, central/
    frisco after the R5 Texas-brick swaps), and without the chosen rule
    the hub grid showed the same photo twice."""
    cards = ''
    chosen = set()
    for s in slugs:
        t = by_slug.get(s)
        if not t:
            continue
        h = hero_by_slug.get(s)
        img_file = h['file'] if h else None
        img_alt = h['alt'] if h else ''
        if img_file and (img_file in chosen or (exclude and img_file in exclude)):
            swapped = False
            for alt_im in (body_by_slug or {}).get(s, []):
                if (not exclude or alt_im['file'] not in exclude) and alt_im['file'] not in chosen:
                    img_file, img_alt = alt_im['file'], alt_im['alt']
                    swapped = True
                    break
            if not swapped:
                print(f'WARNING: card duplicate unresolved for {s} in "{title}" (hero {img_file})')
        if img_file:
            chosen.add(img_file)
        img = img_tag(img_file, alt_text(img_alt), 'card') if img_file else ''
        cards += f'<article className="card reveal">{img}<div className="card-body"><h3><a href="{href_for(s)}">{esc(t["title"])}</a></h3></div></article>'
    cls = 'cards thin' if thin else 'cards'
    return f'<section className="block"><div className="wrap"><h2>{esc(title)}</h2><div className="{cls}">{cards}</div></div></section>'

def write_hub(slug, title, slugs, pages, hero_by_slug, by_slug, body_by_slug=None):
    cards = cards_html(title, slugs, hero_by_slug, by_slug, body_by_slug=body_by_slug)
    # Hubs are not area pages, so the Find Us map section applies here too.
    map_html = '<section className="block"><div className="wrap"><h2>Find Us in Plano, TX</h2><iframe className="map-frame" loading="lazy" title="Map of Plano, TX" src="https://www.google.com/maps?q=Plano,%20TX&output=embed"></iframe></div></section>'
    content = f'''export const metadata = {{ title: {json.dumps(title + " | Water Damage Restoration Plano, TX")}, description: {json.dumps(title + " — Water Damage Restoration Plano, TX. Call (972) 472-7917.")}, alternates: {{ canonical: "{DOMAIN}/{slug}/" }} }};
export default function Page() {{
  return (<><div className="hero"><div className="wrap"><h1>{esc(title)}</h1><p><a className="btn-call" href="{TEL}">Call Now: <span className="nowrap">{PHONE}</span></a></p></div></div>
  {cards}
  {map_html}
  </>);
}}
'''
    path = os.path.join(APP, slug, 'page.jsx')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(content)

def write_sitemap(pages):
    urls = ['']
    urls += [p['tab']['slug'] for p in pages if p['tab']['slug']]
    urls += ['services', 'areas', 'guides']
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        loc = DOMAIN + '/' if u == '' else f'{DOMAIN}/{u}/'
        lines.append(f'<url><loc>{loc}</loc><lastmod>2026-11-04</lastmod></url>')
    lines.append('</urlset>')
    open(os.path.join(PUBLIC, 'sitemap.xml'), 'w').write('\n'.join(lines))
    open(os.path.join(PUBLIC, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')

if __name__ == '__main__':
    main()
