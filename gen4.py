#!/usr/bin/env python3
"""Plano 3 FULL REBUILD generator (2026-11-05) — parses the FRESH Google Docs
API tabs JSON directly (real H2/H3 styles, real bullets, real tables,
hyperlink runs + paren-style link refs). Does NOT read extracted.txt or any
doc-rematch file (stale old content).

Design system carried forward exactly (hero theme): deep teal-navy hero
gradient, white H1, ONE button colour #9a3412 / hover #7c2d12, H2 #0b5563
with teal accent bar, body link #064d73, content links underline-free
default / underline on hover-focus, paragraph tel links underline-free in
all states, no visible figcaptions (alt intact), sticky-split desktop
>=821px / stacks mobile, .doc-table horizontal scroll <=820px, contrast
>=4.5:1 body, dark-section links ~7:1.

Layout rule (this order): ONE container pattern — text on one side, image
on the other — 6 content images per page integrated inside split sections,
never standalone blocks. Images sized to the column (400w file for a ~380px
slot), WebP, lazy except hero.

Doc-fidelity rules:
- Visible doc words render verbatim (dashes preserved as written; the old
  dash-stripping was a text-pipeline artifact and is NOT applied here —
  the new doc's own punctuation stands).
- Schema/Developer-Notes sections (heading "Schema (paste in <head>)" or
  "Developer Notes: ...") are head instructions, NOT visible copy: excluded
  from visible rendering and from the word-diff doc side. Their FAQPage
  subsets are NOT used: FAQ schema is generated from the visible FAQs so
  visible == schema exactly.
- Bracket markers are UI instructions: [Call ...] renders as a tel button
  (words kept), [Send Message] renders as the form button, "Form fields:"
  label is dropped (field labels render as form labels).
- Paren slug refs "(/slug/)" are link notation, not words: the slug token
  is stripped, the preceding phrase becomes the link anchor.
- Homepage hyperlink runs point to claude.ai placeholder URLs: NEVER
  rendered as claude.ai. They are remapped to site pages by anchor (see
  CLAUDE_MAP); the Murphy anchor has no page and renders plain.
- No page links to itself from body content (self refs render plain).
- No Murphy page: the new doc has no Murphy tab. Murphy refs render plain
  and are reported as unlinked.
- Tab 31 duplicates tab 26 (East Plano, byte-identical): built once.
"""
import re, os, json, html, sys

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
APP = os.path.join(BASE, 'app')
PUBLIC = os.path.join(BASE, 'public')
PHONE = '(972) 472-7917'
TEL = 'tel:+19724727917'
DOMAIN = 'https://waterdamagerestorationplano.online'
BRAND = 'Water Damage Restoration Plano'

SERVICE_SLUGS = ['emergency-water-damage', 'water-extraction', 'structural-drying', 'burst-pipe-cleanup',
                 'sewage-cleanup', 'slab-leak', 'water-heater-leak', 'ceiling-leak', 'flood-cleanup',
                 'commercial-water-damage', 'hardwood-floor-drying', 'ac-overflow', 'cabinet-drying',
                 'laundry-overflow', 'crawl-space-drying', 'appliance-leak', 'fire-sprinkler-cleanup',
                 'moisture-mapping', 'attic-insulation-drying', 'wall-drying']
AREA_SLUGS = ['west-plano', 'legacy-west', 'north-plano', 'central-plano', 'east-plano',
              'frisco', 'allen', 'mckinney', 'richardson', 'murphy']  # murphy = preserved old page (user order 2026-11-05)
AREA_NAMES = {'west-plano': 'West Plano', 'legacy-west': 'Legacy West', 'north-plano': 'North Plano',
              'central-plano': 'Central Plano', 'east-plano': 'East Plano', 'frisco': 'Frisco',
              'allen': 'Allen', 'mckinney': 'McKinney', 'richardson': 'Richardson', 'murphy': 'Murphy'}
GUIDE_SLUGS = ['shut-off-valve', 'warm-spot-on-floor', 'ceiling-dripping', 'water-damage-cost',
               'fans-wont-dry-walls', 'storm-water-category-3', 'mold-after-water-damage',
               'copper-pinhole-leaks', 'sagging-ceiling', 'water-damage-insurance-texas']
BEST_SERVICES = ['emergency-water-damage', 'water-extraction', 'structural-drying',
                 'burst-pipe-cleanup', 'slab-leak', 'sewage-cleanup']
NO_MAP_SLUGS = set(AREA_SLUGS)  # area/city pages: no map (footer-map rule)

# Paren-slug aliases: doc variant slug -> canonical page slug.
ALIAS = {
    'water-heater-leak-cleanup': 'water-heater-leak',
    'ac-overflow-cleanup': 'ac-overflow',
    'plano-main-water-shut-off-valve': 'shut-off-valve',
    'slab-leak-water-damage': 'slab-leak',
    'wall-cavity-drying': 'wall-drying',
    'ceiling-leak-water-damage': 'ceiling-leak',
    'sagging-wet-ceiling-safety': 'sagging-ceiling',
    'murphy-parker-wylie': 'murphy',  # user-ordered 2026-11-05: new-doc refs to Murphy/Parker/Wylie link to the preserved /murphy/ page
}
# Homepage claude.ai placeholder paths -> canonical page slug (None = no page).
CLAUDE_MAP = {
    'ac-overflow-water-damage-plano': 'ac-overflow',
    'burst-pipe-water-damage-plano': 'burst-pipe-cleanup',
    'ceiling-leak-water-damage-plano': 'ceiling-leak',
    'commercial-water-damage-plano': 'commercial-water-damage',
    'emergency-water-damage-cleanup-plano': 'emergency-water-damage',
    'flood-cleanup-plano': 'flood-cleanup',
    'hardwood-floor-water-damage-plano': 'hardwood-floor-drying',
    'plano-main-water-shut-off-valve': 'shut-off-valve',
    'sagging-wet-ceiling-safety': 'sagging-ceiling',
    'sewage-backup-cleanup-plano': 'sewage-cleanup',
    'slab-leak-water-damage-plano': 'slab-leak',
    'structural-drying-plano': 'structural-drying',
    'water-damage-allen': 'allen',
    'water-damage-central-plano': 'central-plano',
    'water-damage-east-plano': 'east-plano',
    'water-damage-frisco': 'frisco',
    'water-damage-legacy-west': 'legacy-west',
    'water-damage-mckinney': 'mckinney',
    'water-damage-murphy-parker-wylie': 'murphy',  # user-ordered 2026-11-05: home claude.ai Murphy anchor links to the preserved /murphy/ page
    'water-damage-north-plano': 'north-plano',
    'water-damage-richardson': 'richardson',
    'water-damage-west-plano': 'west-plano',
    'water-extraction-plano': 'water-extraction',
    'water-heater-leak-cleanup-plano': 'water-heater-leak',
    'why-fans-wont-dry-water-damage': 'fans-wont-dry-walls',
}

HERO_FILE = {
    '': 'suburban-home-186077.webp',
    'emergency-water-damage': 'burst-pipe-15206136.webp',
    'water-extraction': 'water-extraction-6195949.webp',
    'structural-drying': 'moisture-meter-8293640.webp',
    'burst-pipe-cleanup': 'burst-pipe-8488035.webp',  # HERO FIX 2026-11-05: indoor wall pipes/valves under repair (viewed); was muddy outdoor pipe (rejected, now banned)
    'sewage-cleanup': 'shower-drain-5768318.webp',  # HERO FIX 2026-11-05: indoor shower-floor drain in white tile (viewed); was outdoor drainpipes 15242228
    'slab-leak': 'wet-tile-9376351.webp',  # HERO FIX 2026-11-05: water pooled on indoor tile floor, B&W (viewed); was concrete saw 21366138
    'water-heater-leak': 'water-heater-19980200.webp',  # HERO FIX 2026-11-05: tank water heater in home laundry/utility room (viewed); was rooftop solar 34593293
    'ceiling-leak': 'ceiling-stain-3708564.webp',
    'flood-cleanup': 'flooded-suburban-home-28447764.webp',
    'commercial-water-damage': 'drying-equipment-16243255.webp',
    'hardwood-floor-drying': 'hardwood-floor-3935327.webp',
    'ac-overflow': 'ceiling-crew-8293648.webp',  # HERO FIX 2026-11-05: technician indoors pointing up at a ceiling (viewed, existing pool); was outdoor condensers 28726413
    'murphy': 'greenbelt-home-12445995.webp',  # old Murphy hero, preserved
    'cabinet-drying': 'cabinet-kitchen-7535073.webp',
    'laundry-overflow': 'laundry-room-19846385.webp',
    'crawl-space-drying': 'crawl-space-4092026.webp',
    'appliance-leak': 'appliance-fridge-3958962.webp',
    'fire-sprinkler-cleanup': 'flooded-floor-7924140.webp',
    'moisture-mapping': 'thermal-imaging-7859781.webp',
    'attic-insulation-drying': 'attic-insulation-6124239.webp',
    'wall-drying': 'flood-cut-wall-8488031.webp',
    'west-plano': 'suburban-home-3990589.webp',
    'legacy-west': 'texas-home-8278493.webp',
    'north-plano': 'suburban-home-26595553.webp',
    'central-plano': 'texas-home-8278494.webp',
    'east-plano': 'brick-ranch-8031875.webp',
    'frisco': 'texas-home-8278494.webp',
    'allen': 'suburban-home-18280830.webp',
    'mckinney': 'brick-ranch-8031875.webp',
    'richardson': 'suburban-home-3990589.webp',
    'shut-off-valve': 'water-shutoff-4494656.webp',
    'warm-spot-on-floor': 'warm-floor-thermal-5853823.webp',
    'ceiling-dripping': 'ceiling-stain-lived-in-8624466.webp',
    'water-damage-cost': 'suburban-home-26595553.webp',
    'fans-wont-dry-walls': 'mold-wall-4597285.webp',
    'storm-water-category-3': 'flooded-suburban-home-28447764.webp',
    'mold-after-water-damage': 'indoor-mold-18063447.webp',
    'copper-pinhole-leaks': 'copper-pipes-6123308.webp',  # HERO FIX 2026-11-05: exposed copper pipes + brass valves above a bathtub indoors (viewed); was corroded outdoor pipe 36571568
    'sagging-ceiling': 'sagging-ceiling-30499666.webp',
    'water-damage-insurance-texas': 'insurance-claim-7731397.webp',
    'about': 'plumber-work-6419128.webp',
    'contact': 'burst-pipe-2339722.webp',
}
# Legacy hunter-verified body files (first-choice pool per page; a file is
# used only when its topic fits the section it illustrates).
BODY_FILE = {
    'home': ['suburban-home-31602311.webp', 'burst-pipe-36571568.webp', 'drying-equipment-16243255.webp'],
    'emergency-water-damage': ['texas-home-8278494.webp', 'plumber-work-6419128.webp', 'ceiling-stain-8624464.webp'],
    'water-extraction': ['flooded-floor-7924140.webp', 'sewage-drain-3964564.webp', 'moisture-meter-8961703.webp'],
    'structural-drying': ['drying-equipment-16243255.webp', 'drying-fan-28726413.webp', 'moisture-meter-8961703.webp'],
    'burst-pipe-cleanup': ['ceiling-stain-8624464.webp', 'plumber-work-6419128.webp', 'plumber-work-35290675.webp'],
    'sewage-cleanup': ['sewage-drain-29608837.webp', 'sewage-drain-13961561.webp', 'sewage-drain-3964564.webp'],
    'slab-leak': ['burst-pipe-11658940.webp', 'hardwood-floor-3935327.webp', 'mold-wall-9127236.webp'],
    'water-heater-leak': ['plumber-work-6419128.webp', 'attic-insulation-9043415.webp', 'ceiling-stain-3708564.webp'],
    'ceiling-leak': ['ceiling-stain-14032089.webp', 'attic-insulation-6124239.webp', 'attic-insulation-4482829.webp'],
    'murphy': ['suburban-home-32711440.webp', 'texas-home-23928963.webp', 'flooded-floor-7924140.webp'],  # old Murphy body picks, preserved
    'flood-cleanup': ['burst-pipe-18274115.webp', 'storm-flood-11537987.webp', 'sewage-drain-3964564.webp'],
    'commercial-water-damage': ['commercial-office-36631701.webp', 'steel-studs-35496414.webp', 'ceiling-stain-3708564.webp'],
    'hardwood-floor-drying': ['mold-wall-9127236.webp', 'drying-equipment-16243255.webp', 'flooded-floor-7924140.webp'],
    'ac-overflow': ['ceiling-stain-14032089.webp', 'attic-insulation-271743.webp', 'sewage-drain-3964564.webp'],
    'cabinet-drying': ['kitchen-leak-34295401.webp', 'kitchen-leak-10961064.webp', 'cabinet-kitchen-2398375.webp'],
    'laundry-overflow': ['laundry-room-7282378.webp', 'sewage-drain-3964564.webp', 'ceiling-stain-3708564.webp'],
    'crawl-space-drying': ['plumber-work-6419128.webp', 'crawl-space-40440109.webp', 'sewage-drain-13961561.webp'],
    'appliance-leak': ['appliance-fridge-4469164.webp', 'kitchen-leak-10961064.webp', 'kitchen-leak-34295401.webp'],
    'fire-sprinkler-cleanup': ['drying-equipment-16243255.webp', 'fire-sprinkler-36631700.webp', 'ceiling-stain-3708564.webp'],
    'moisture-mapping': ['moisture-meter-8293640.webp', 'ceiling-stain-8624464.webp', 'ceiling-stain-14032089.webp'],
    'attic-insulation-drying': ['attic-insulation-271743.webp', 'crawl-space-4092030.webp', 'attic-insulation-4482829.webp'],
    'wall-drying': ['thermal-imaging-7859781.webp', 'moisture-meter-8961703.webp', 'hardwood-floor-3935327.webp'],
    'west-plano': ['suburban-home-31602311.webp', 'luxury-interior-36906952.webp', 'greenbelt-home-12445995.webp'],
    'legacy-west': ['suburban-home-3990589.webp', 'texas-home-23930020.webp', 'texas-home-8278494.webp'],
    'north-plano': ['suburban-home-15303808.webp', 'copper-pipes-3721272.webp', 'greenbelt-home-12445995.webp'],
    'central-plano': ['suburban-home-31602311.webp', 'copper-pipes-3721272.webp', 'suburban-home-186077.webp'],
    'east-plano': ['suburban-home-186077.webp', 'pier-beam-home-26261510.webp', 'sewage-drain-29608837.webp'],
    'frisco': ['suburban-home-186077.webp', 'texas-home-23930020.webp', 'flooded-floor-7924140.webp'],
    'allen': ['suburban-home-26595553.webp', 'suburban-home-3990589.webp', 'attic-insulation-271743.webp'],
    'mckinney': ['suburban-home-7587470.webp', 'texas-home-33404353.webp', 'suburban-home-186077.webp'],
    'richardson': ['suburban-home-186077.webp', 'suburban-home-30707539.webp', 'copper-pipes-3721272.webp'],
    'shut-off-valve': ['burst-pipe-15206136.webp', 'kitchen-leak-10961064.webp', 'thermal-imaging-7859781.webp'],
    'warm-spot-on-floor': ['burst-pipe-15206136.webp', 'burst-pipe-36571568.webp', 'suburban-home-3990589.webp'],
    'ceiling-dripping': ['ceiling-stain-14032089.webp', 'ceiling-stain-3708564.webp', 'attic-insulation-4482829.webp'],
    'water-damage-cost': ['suburban-home-31602311.webp', 'insurance-claim-7731397.webp', 'plumber-work-6419128.webp'],
    'fans-wont-dry-walls': ['moisture-meter-7937963.webp', 'thermal-imaging-7859781.webp', 'mold-wall-29701042.webp'],
    'storm-water-category-3': ['flooded-floor-7924140.webp', 'creek-overflow-32159924.webp', 'suburban-home-186077.webp'],
    'mold-after-water-damage': ['mold-wall-18351809.webp', 'cabinet-kitchen-8146322.webp', 'drying-equipment-16243255.webp'],
    'copper-pinhole-leaks': ['copper-pipes-3721272.webp', 'suburban-home-3990589.webp', 'plumber-work-6419128.webp'],
    'sagging-ceiling': ['ceiling-stain-8624464.webp', 'suburban-home-30707539.webp', 'ceiling-crew-8293648.webp'],
    'water-damage-insurance-texas': ['moisture-meter-8293640.webp', 'plumber-work-6419128.webp', 'commercial-office-13068366.webp'],
    'about': ['plumber-work-35290675.webp', 'suburban-home-3990589.webp', 'mold-wall-9127236.webp'],
    'contact': ['plumber-work-35290675.webp', 'suburban-home-26595553.webp', 'plumber-work-6419128.webp'],
}
# Files flagged on viewed pixels in earlier rounds: banned from every slot.
BANNED = {
    'mold-wall-26387777.webp', 'mold-wall-17374615.webp', 'plumber-work-7859953.webp',
    'plumber-work-29226620.webp', 'plumber-work-7220892.webp', 'ceiling-stain-18323819.webp',
    'texas-home-23930016.webp', 'flooded-floor-14216445.webp', 'flooded-floor-17667013.webp',
    'flooded-floor-35302178.webp', 'storm-flood-28447778.webp', 'storm-flood-28447775.webp',
    'storm-flood-28447808.webp', 'burst-pipe-20812917.webp', 'burst-pipe-34197979.webp',
    'bathroom-leak-12271457.webp', 'bathroom-leak-40016472.webp', 'drying-fan-32702870.webp',
    'laundry-room-9669475.webp', 'laundry-room-11213210.webp',
    'laundry-room-14361266.webp', 'laundry-room-17367256.webp', 'laundry-room-4386143.webp',
    'attic-insulation-1628417.webp', 'kitchen-leak-8054736.webp', 'hardwood-floor-9462136.webp',
    'hardwood-floor-9462132.webp', 'hardwood-floor-9462141.webp', 'hardwood-floor-9462148.webp',
    'wet-carpet-8273517.webp', 'wet-carpet-4107284.webp', 'wet-carpet-9462139.webp',
    'wet-carpet-4107257.webp', 'wet-carpet-4107278.webp', 'wet-carpet-4107280.webp',
    'wet-carpet-8566420.webp', 'plumber-work-33388390.webp', 'flooded-floor-10631759.webp',
    'flooded-floor-18302377.webp', 'attic-insulation-38749876.webp', 'ceiling-stain-18132318.webp',
    'mold-wall-29181495.webp', 'water-heater-33116799.webp', 'hardwood-floor-10557495.webp',
    'ceiling-stain-7599120.webp', 'kitchen-leak-34295406.webp', 'crawl-space-10847198.webp',
    'suburban-home-17091309.webp', 'suburban-home-11301818.webp', 'water-heater-6436774.webp',
    'flooded-floor-28447774.webp', 'hardwood-floor-9462163.webp', 'attic-insulation-8082327.webp',
    'moisture-meter-8961700.webp',
    'drying-equipment-7464727.webp', 'drying-equipment-7464724.webp',
    'drying-equipment-34585139.webp', 'drying-equipment-6479995.webp',
    'drying-equipment-7464199.webp', 'drying-equipment-7464198.webp',
    'drying-equipment-34585118.webp', 'crawl-space-17181949.webp',
    'water-heater-11211127.webp', 'water-heater-17854867.webp',
    'drying-fan-37080286.webp', 'burst-pipe-4406597.webp',  # PURGE 2026-11-05: rejected muddy outdoor pipe, was burst hero + copper split + water-extraction split
    'sagging-ceiling-30499666.webp',  # BAN 2026-11-05: destroyed/ruined-ceiling gallery shot (collapsed panels, insulation exposed), was sagging-ceiling hero + guides/contact card; replaced by sagging-ceiling-water-stain-plano-8624465.webp
    # COMBINED ROUND 2026-11-05: retire files whose every usage is covered by a new override
    'burst-pipe-18274115.webp', 'drying-fan-37634966.webp', 'commercial-office-13068366.webp',
    'texas-home-33404353.webp', 'sewage-drain-29608837.webp', 'sewage-drain-3964564.webp',
    'sewage-drain-15242228.webp',
}

def esc(s):
    return html.escape(s or '', quote=True)

def words_of(t):
    return re.findall(r"[A-Za-z0-9'\u2019\-]+", (t or '').lower())

# ---------------- doc parsing ----------------

def ptext(p):
    return ''.join(e.get('textRun', {}).get('content', '') for e in p.get('elements', []))

def pruns(p):
    """[(text, url_or_None, bold)] per run."""
    out = []
    for e in p.get('elements', []):
        tr = e.get('textRun')
        if tr:
            ts = tr.get('textStyle', {}) or {}
            out.append((tr.get('content', ''), (ts.get('link') or {}).get('url'), bool(ts.get('bold'))))
    return out

def canon_slug(raw, page_slugs):
    """Canonical page slug for a paren slug, or None when no page exists."""
    s = (raw or '').strip().strip('/')
    if s == '':
        return ''
    if s in page_slugs:
        return s
    if s in ALIAS:
        return ALIAS[s]
    return None

PAREN_RE = re.compile(r'\((/([a-z0-9\-]*)/?)\)')
DELIMS = ['. ', ': ', '; ', ', ', ' and ', ' or ', '\n']

def split_paren_links(text, self_slug, page_slugs, links, in_faq):
    """Split plain text on paren refs. Returns segments [(text, target_or_None)].
    The slug token itself is notation, never a word. The anchor is the phrase
    after the last delimiter before the paren (leading 'See ' stays plain).
    Unlinked (Murphy) and self refs stay plain and are recorded."""
    segs = []
    pos = 0
    for m in PAREN_RE.finditer(text):
        pre = text[pos:m.start()]
        raw_slug = m.group(1).strip('/')
        tgt = canon_slug(raw_slug, page_slugs)
        # anchor = pre after last delimiter
        cut = 0
        for d in DELIMS:
            idx = pre.rfind(d)
            if idx >= 0:
                cut = max(cut, idx + len(d))
        anchor = pre[cut:]
        head = pre[:cut]
        see = ''
        if anchor.lower().startswith('see '):
            see = anchor[:4]
            anchor = anchor[4:]
        anchor = anchor.strip()
        if head:
            segs.append((head, None))
        if see:
            segs.append((see, None))
        if anchor:
            if tgt is None:
                segs.append((anchor, None))
                links.append({'anchor': anchor, 'target': None, 'in_faq': in_faq, 'kind': 'unlinked'})
            elif tgt == self_slug:
                segs.append((anchor, None))
                links.append({'anchor': anchor, 'target': tgt, 'in_faq': in_faq, 'kind': 'self'})
            else:
                segs.append((anchor, tgt))
                links.append({'anchor': anchor, 'target': tgt, 'in_faq': in_faq, 'kind': 'paren'})
        pos = m.end()
    tail = text[pos:]
    if tail:
        segs.append((tail, None))
    return segs

def runs_to_segs(runs, self_slug, page_slugs, links, in_faq):
    """Merge runs into segments, converting hyperlink runs (tab 1) and
    paren refs (all tabs) into link segments. Plain runs keep bold flags
    only as (text, None, bold) triples internally — caller normalises."""
    # First merge adjacent same-URL runs (anchor split across runs).
    merged = []
    for (t, url, bold) in runs:
        if merged and url is not None and merged[-1][1] == url:
            merged[-1] = (merged[-1][0] + t, url, merged[-1][2])
        else:
            merged.append((t, url, bold))
    segs = []  # (text, target_or_None, bold)
    for (t, url, bold) in merged:
        if url:
            tgt = None
            if url.startswith('https://claude.ai/'):
                path = url[len('https://claude.ai/'):].strip('/')
                tgt = CLAUDE_MAP.get(path, 'UNKNOWN:' + path)
            elif url.startswith('https://waterdamagerestorationplano.online/'):
                tgt = canon_slug(url[len('https://waterdamagerestorationplano.online/'):], page_slugs)
            else:
                tgt = 'EXTERNAL:' + url
            # Docs splits runs at style boundaries, so a link run often
            # carries its surrounding spaces (" AC overflow..."). Stripping
            # them glues words in the rendered HTML ("andAC"), so preserve
            # them as plain segments around the anchor core.
            anchor = t.strip()
            if not anchor:
                continue
            lead = t[:len(t) - len(t.lstrip())]
            trail = t[len(t.rstrip()):]
            if lead:
                segs.append((lead, None, False))
            if tgt is None or (isinstance(tgt, str) and tgt.startswith(('UNKNOWN', 'EXTERNAL'))):
                segs.append((anchor, None, False))
                links.append({'anchor': anchor, 'target': tgt, 'in_faq': in_faq, 'kind': 'unlinked'})
            elif tgt == self_slug:
                segs.append((anchor, None, False))
                links.append({'anchor': anchor, 'target': tgt, 'in_faq': in_faq, 'kind': 'self'})
            else:
                segs.append((anchor, tgt, False))
                links.append({'anchor': anchor, 'target': tgt, 'in_faq': in_faq, 'kind': 'run'})
            if trail:
                segs.append((trail, None, False))
        else:
            # plain run: paren refs inside it become links
            for (txt, tgt) in split_paren_links(t, self_slug, page_slugs, links, in_faq):
                segs.append((txt, tgt, bold))
    return segs

def segs_plain(segs):
    out = ''
    for (t, _tg, _b) in segs:
        out += t
    return out

def parse_tabs(doc_path):
    d = json.load(open(doc_path))
    tabs_raw = list(d['tabs'])
    # USER-ORDERED EXCEPTION (refinements 2026-11-05): preserve the old Murphy
    # area page, which the new doc dropped. Its full-fidelity tab comes from the
    # old doc API snapshot (doc-rematch/doc_api.json, tab titled
    # 'Murphy, Parker & Wylie City Page'); nothing else is read from that file.
    _has_murphy = any(
        (lambda ps: ps and ''.join(e.get('textRun', {}).get('content', '') for e in ps[0].get('elements', [])).strip() == 'Murphy, Parker & Wylie City Page')(
            [el['paragraph'] for el in t['documentTab']['body']['content'] if 'paragraph' in el])
        for t in tabs_raw)
    if not _has_murphy:
        try:
            _old = json.load(open(os.path.join(BASE, 'doc-rematch', 'doc_api.json')))
            for _ot in _old['tabs']:
                _ps = [el['paragraph'] for el in _ot['documentTab']['body']['content'] if 'paragraph' in el]
                _t0 = ''.join(e.get('textRun', {}).get('content', '') for e in _ps[0].get('elements', [])) if _ps else ''
                if _t0.strip() == 'Murphy, Parker & Wylie City Page':
                    tabs_raw.append(_ot)
                    break
        except FileNotFoundError:
            pass
    # First pass: slugs + titles (tab 31 duplicates tab 26 -> skipped later).
    metas = []
    for t in tabs_raw:
        paras = [el['paragraph'] for el in t['documentTab']['body']['content'] if 'paragraph' in el]
        meta = {}
        cur = None
        buf = ''
        for (txt, ts) in [(r[0], r[1]) for r in
                          [(e.get('textRun', {}).get('content', ''), e.get('textRun', {}).get('textStyle', {}))
                           for e in paras[1].get('elements', [])]]:
            if ts.get('bold') and txt.strip().rstrip(':') in ('Meta Title', 'Meta Description', 'URL', 'H1'):
                if cur:
                    meta[cur] = buf.strip()
                cur = txt.strip().rstrip(':')
                buf = ''
            else:
                buf += txt
        if cur:
            meta[cur] = buf.strip()
        # Old-format meta (Murphy tab): Meta Description/URL/H1 live in
        # separate paragraphs after the Meta Title paragraph.
        for pi in (2, 3, 4):
            if pi < len(paras):
                _txt = ptext(paras[pi]).strip()
                for _label in ('Meta Description', 'URL', 'H1'):
                    if _txt.startswith(_label + ':') and _label not in meta:
                        meta[_label] = _txt[len(_label) + 1:].strip()
        slug = meta.get('URL', '').replace('waterdamagerestorationplano.online', '').strip().strip('/')
        metas.append({'title': ptext(paras[0]).strip(), 'meta': meta, 'slug': slug})
    page_slugs = set(m['slug'] for m in metas)
    pages = []
    seen_slugs = set()
    dup_tabs = []
    for ti, (t, meta) in enumerate(zip(tabs_raw, metas)):
        slug = meta['slug']
        if slug in seen_slugs:
            dup_tabs.append((ti + 1, slug))
            continue
        seen_slugs.add(slug)
        links = []
        # Walk body blocks in order (elements include tables inline).
        elements = t['documentTab']['body']['content']
        blocks = []  # raw: ('para', style, paragraph_dict) | ('table', rows)
        for el in elements:
            if 'paragraph' in el:
                blocks.append(('para', el['paragraph'].get('paragraphStyle', {}).get('namedStyleType', ''), el['paragraph']))
            elif 'table' in el:
                rows = []
                for row in el['table'].get('tableRows', []):
                    cells = []
                    for cell in row.get('tableCells', []):
                        cparas = []
                        for cp in cell.get('content', []):
                            if 'paragraph' in cp:
                                cparas.append(cp['paragraph'])
                        cells.append(cparas)
                    rows.append(cells)
                blocks.append(('table', '', rows))
        # Drop title (blocks[0]) + meta (blocks[1]); schema section -> end.
        body = blocks[2:]
        # Strip leading old-format meta paras (Murphy) + blank paras.
        while body and body[0][0] == 'para' and (not ptext(body[0][2]).strip() or any(ptext(body[0][2]).strip().startswith(lbl) for lbl in ('Meta Title:', 'Meta Description:', 'URL:', 'H1:'))):
            body = body[1:]
        schema_at = None
        for bi, b in enumerate(body):
            if b[0] == 'para' and b[1].startswith('HEADING') and re.match(r'^(Schema|Developer Notes)', ptext(b[2]).strip()):
                schema_at = bi
                break
        if schema_at is not None:
            body = body[:schema_at]
        # Build sections.
        intro_blocks = []
        sections = []
        cur_sec = None
        faqs = []
        faq_heading = None
        in_faq = False
        cur_q = None
        cur_a = []
        cur_a_segs = []
        pending_bullets = []
        def flush_bullets():
            nonlocal pending_bullets
            if pending_bullets:
                items = [segs_plain(sg) for sg in pending_bullets]
                item_segs = pending_bullets
                blk = {'type': 'list', 'items': items, 'item_segs': item_segs}
                if cur_sec is None:
                    intro_blocks.append(blk)
                else:
                    cur_sec['blocks'].append(blk)
                pending_bullets = []
        def add_block(blk):
            if cur_sec is None:
                intro_blocks.append(blk)
            else:
                cur_sec['blocks'].append(blk)
        def close_faq():
            nonlocal cur_q, cur_a, cur_a_segs
            if cur_q is not None:
                faqs.append({'q': cur_q, 'a': ' '.join(a for a in cur_a).strip(),
                             'a_segs': list(cur_a_segs)})
                cur_q = None
                cur_a = []
                cur_a_segs = []
        for b in body:
            if b[0] == 'table':
                flush_bullets()
                rows = []
                for row in b[2]:
                    cells = []
                    for cparas in row:
                        cpara_segs = []
                        for cp in cparas:
                            txt = ptext(cp).strip()
                            if not txt:
                                continue
                            cpara_segs.append(runs_to_segs(pruns(cp), slug, page_slugs, links, in_faq))
                        csegs = [sg for cl in cpara_segs for sg in cl]
                        # Bare "/slug/" cell (contact Areas table Page column)
                        # is a link reference: anchor = the path text itself.
                        cell_txt = segs_plain(csegs).strip()
                        bm = re.fullmatch(r'/([a-z0-9\-]+)/', cell_txt)
                        if bm:
                            tgt = canon_slug(bm.group(1), page_slugs)
                            if tgt is None:
                                links.append({'anchor': cell_txt, 'target': None, 'in_faq': in_faq, 'kind': 'unlinked'})
                            elif tgt == slug:
                                links.append({'anchor': cell_txt, 'target': tgt, 'in_faq': in_faq, 'kind': 'self'})
                            else:
                                cpara_segs = [[(cell_txt, tgt, False)]]
                                links.append({'anchor': cell_txt, 'target': tgt, 'in_faq': in_faq, 'kind': 'table-bare'})
                        cells.append(cpara_segs)
                    rows.append(cells)
                add_block({'type': 'table', 'rows': rows})
                continue
            style, p = b[1], b[2]
            txt = ptext(p).strip()
            if not txt:
                flush_bullets()
                continue
            if style.startswith('HEADING'):
                flush_bullets()
                if style == 'HEADING_2':
                    close_faq()
                    if re.search(r'FAQs?\s*$', txt):
                        in_faq = True
                        faq_heading = txt
                        cur_sec = None
                        continue
                    in_faq = False
                    cur_sec = {'heading': txt, 'blocks': []}
                    sections.append(cur_sec)
                elif style == 'HEADING_3':
                    if in_faq:
                        close_faq()
                        cur_q = txt
                    else:
                        add_block({'type': 'subhead', 'text': txt})
                continue
            if in_faq:
                # FAQ answer paragraph(s); links recorded with in_faq=True.
                segs = runs_to_segs(pruns(p), slug, page_slugs, links, True)
                cur_a.append(segs_plain(segs))
                cur_a_segs.append(segs)
                continue
            bullet = 'bullet' in p
            if bullet:
                segs = runs_to_segs(pruns(p), slug, page_slugs, links, False)
                pending_bullets.append(segs)
                continue
            flush_bullets()
            if txt == 'Form fields:':
                continue  # instruction label; fields render as form labels
            if re.fullmatch(r'\[Send Message\]', txt):
                continue  # form button renders this
            m = re.fullmatch(r'\[(Call|Tap to Call)[^\]]*\]', txt)
            if m:
                add_block({'type': 'cta', 'label': txt[1:-1]})
                continue
            segs = runs_to_segs(pruns(p), slug, page_slugs, links, False)
            plain = segs_plain(segs)
            if '·' in plain and plain.count('·') >= 3 and len(plain) < 260:
                items = [x.strip() for x in plain.split('·') if x.strip()]
                add_block({'type': 'trust', 'items': items})
            else:
                add_block({'type': 'para', 'segs': segs})
        flush_bullets()
        close_faq()
        # Contact form: intro/section blocks hold field bullets after the
        # "Send Us a Message" H2 — convert that list block into a form block.
        if slug == 'contact':
            for sec in sections:
                if sec['heading'] == 'Send Us a Message (Non-Emergency)':
                    fields = []
                    note = ''
                    new_blocks = []
                    for blk in sec['blocks']:
                        if blk['type'] == 'list' and not fields:
                            fields = blk['items']
                        elif blk['type'] == 'para' and fields and not note:
                            note = segs_plain(blk['segs'])
                        else:
                            new_blocks.append(blk)
                    if fields:
                        new_blocks.append({'type': 'form', 'fields': fields, 'note': note})
                    sec['blocks'] = new_blocks
        pages.append({'slug': slug, 'tab_title': meta['title'],
                      'meta_title': meta['meta'].get('Meta Title', ''),
                      'meta_desc': meta['meta'].get('Meta Description', ''),
                      'h1': meta['meta'].get('H1', ''),
                      'intro': intro_blocks, 'sections': sections,
                      'faqs': faqs, 'faq_heading': faq_heading,
                      'links': links, 'tab_no': ti + 1})
    return pages, dup_tabs

# ---------------- rendering ----------------

def href_for(slug):
    return '/' if slug == '' else f'/{slug}/'

PHONE_RE = re.compile(r'(\(972\) 472-7917|972-472-7917)')

def render_segs(segs):
    """HTML for segments: link segments -> <a>, tel numbers -> tel links,
    short leading bold runs -> <strong>. Bracket-call remnants stripped."""
    out = ''
    for (t, tgt, bold) in segs:
        t = re.sub(r'\[([^\]]*Call[^\]]*)\]', r'\1', t)
        if tgt is not None:
            out += f'<a href="{href_for(tgt)}">{esc(t)}</a>'
            continue
        parts = PHONE_RE.split(t)
        for part in parts:
            if PHONE_RE.fullmatch(part or ''):
                out += f'<a href="{TEL}">{esc(part)}</a>'
            elif part:
                out += f'<strong>{esc(part)}</strong>' if (bold and len(part.strip()) <= 80) else esc(part)
    # typographic spacing before punctuation (presentation only)
    out = re.sub(r'\s+([,.;:?!])', r'\1', out)
    return out

def render_plain_with_links(text_segs):
    return render_segs(text_segs)

def table_html(rows):
    """Verbatim doc table: first row -> <th> when every first-row cell has
    a bold run; else <td>. Cell paren refs render as links via segs."""
    def cell_has_bold(cell):
        # cell = list of seg-lists (one per doc para)
        return any(b for csegs in cell for (_t, _tg, b) in csegs)
    first_is_header = bool(rows) and all(cell_has_bold(cell) for cell in rows[0])
    trs = []
    for ri, row in enumerate(rows):
        tds = []
        for cell in row:
            paras = []
            # cell = list of seg-lists (one per doc para); join paras with space? No: separate <p>.
            for csegs in cell:
                txt = segs_plain(csegs).strip()
                if txt:
                    paras.append(f'<p>{render_segs(csegs)}</p>')
            inner = ''.join(paras)
            if ri == 0 and first_is_header:
                tds.append(f'<th scope="col">{inner}</th>')
            else:
                tds.append(f'<td>{inner}</td>')
        trs.append(f'<tr>{"".join(tds)}</tr>')
    return f'<div className="table-wrap"><table className="doc-table"><tbody>{"".join(trs)}</tbody></table></div>'

def block_html(b):
    t = b['type']
    if t == 'subhead':
        return f'<h3>{esc(b["text"])}</h3>'
    if t == 'para':
        return f'<p>{render_segs(b["segs"])}</p>'
    if t == 'table':
        return table_html(b['rows'])
    if t == 'cta':
        label = b['label']
        m = re.match(r'^(.*?):\s*(\(972\) 472-7917|972-472-7917)\s*$', label)
        if m:
            return (f'<p className="cta-row"><a className="btn-call" href="{TEL}">{esc(m.group(1))}: '
                    f'<span className="nowrap">{esc(m.group(2))}</span></a></p>')
        return f'<p className="cta-row"><a className="btn-call" href="{TEL}">{esc(label)}</a></p>'
    if t == 'trust':
        items = ''.join(f'<span className="check">✓ {esc(x)}</span>' for x in b['items'])
        return f'<div className="trust-band reveal">{items}</div>'
    if t == 'list':
        items = ''
        for item_segs in b['item_segs']:
            items += f'<li>{render_segs(item_segs)}</li>'
        return f'<ul>{items}</ul>'
    if t == 'form':
        fields = ''
        for f in b['fields']:
            fl = f.strip()
            low = fl.lower()
            if low.startswith('type of property'):
                opts = [o.strip() for o in fl.split(':', 1)[1].split(',')]
                fields += '<label>Type of property<select name="property">' + ''.join(f'<option>{esc(o)}</option>' for o in opts) + '</select></label>'
            elif low.startswith('what happened'):
                opts = [o.strip() for o in fl.split(':', 1)[1].split(',')]
                fields += '<label>What happened<select name="happened">' + ''.join(f'<option>{esc(o)}</option>' for o in opts) + '</select></label>'
            elif low.startswith('is water still active'):
                fields += '<label>Is water still active? <span className="radio-row"><label><input type="radio" name="active" value="Yes" /> Yes</label><label><input type="radio" name="active" value="No" /> No</label></span></label>'
            elif low == 'message':
                fields += '<label>Message<textarea name="message" rows="5"></textarea></label>'
            elif low == 'email address':
                fields += '<label>Email address<input type="email" name="email" /></label>'
            elif low == 'phone number':
                fields += '<label>Phone number<input type="tel" name="phone" /></label>'
            else:
                fields += f'<label>{esc(fl)}<input type="text" name="{esc(low.replace(" ", "_"))}" /></label>'
        note = f'<p className="form-note">{esc(b["note"])}</p>' if b.get('note') else ''
        return f'<form className="contact-form" method="post">{fields}<button type="submit" className="btn-call">Send Message</button></form>{note}'
    return ''

# ---------------- images ----------------

def clean_alt(s):
    t = html.unescape(s or '')
    _REWRITE = {
        'Lovely red brick suburban house with a well-maintained lawn under a bright blue sky.':
            'Red brick suburban house with a well-maintained lawn',
        'Serene stone residence with rustic charm in Texas.': 'Stone suburban home in Texas',
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
    if t.strip() in _REWRITE:
        return _REWRITE[t.strip()]
    t = re.sub(r',?\s*perfect for (real estate|renovation)[^.]*\.?', '', t, flags=re.I)
    t = re.sub(r',?\s*ideal for (real estate|renovation)[^.]*\.?', '', t, flags=re.I)
    t = re.sub(r'Abstract image of ', '', t, flags=re.I)
    t = re.sub(r'Abstract background of ', '', t, flags=re.I)
    t = re.sub(r',?\s*(showcasing|ideal for|capturing|highlighting)[^.]*\.?', '', t, flags=re.I)
    t = re.sub(r' emphasizing texture\.?', '', t, flags=re.I)
    t = re.sub(r' for efficient cleaning\.?', '', t, flags=re.I)
    t = re.sub(r', showcasing skilled manual work\.?', '', t, flags=re.I)
    t = re.sub(r', highlighting efficient home cleaning\.?', '', t, flags=re.I)
    t = re.sub(r', capturing a moment of household cleaning\.?', '', t, flags=re.I)
    t = re.sub(r',?\s*offering a textured urban look\.?', '', t, flags=re.I)
    t = re.sub(r',?\s*depicting resilience\.?', '', t, flags=re.I)
    t = re.sub(r'\s+with visible water runoff', '', t, flags=re.I)
    t = re.sub(r'^Explore this ', '', t, flags=re.I)
    t = re.sub(r'\s+', ' ', t).strip().rstrip('.')
    return t

_IMG_IDX = None
_IMG_DIMS = {}
def img_index():
    global _IMG_IDX
    if _IMG_IDX is None:
        _IMG_IDX = {}
        d = os.path.join(PUBLIC, 'images')
        for f in os.listdir(d):
            p = os.path.join(d, f)
            if os.path.isfile(p):
                _IMG_IDX[f] = os.path.getsize(p)
    return _IMG_IDX

def img_dims(f):
    if f not in _IMG_DIMS:
        try:
            from PIL import Image
            with Image.open(os.path.join(PUBLIC, 'images', f)) as im:
                _IMG_DIMS[f] = im.size
        except Exception:
            _IMG_DIMS[f] = (1200, 800)
    return _IMG_DIMS[f]

def img_tag(file, alt, kind, eager=False):
    idx = img_index()
    orig = idx.get(file, 0)
    if kind == 'hero':
        # Refinement 3 (2026-11-05): mobile heroes must not serve 800w for a
        # ~350px slot — include the 400w candidate so mobile picks 400w.
        cands = [(400, '400w'), (800, '800w')]
        sizes = '(max-width:820px) 90vw, 600px'
    elif kind == 'card':
        cands = [(400, '400w'), (800, '800w')]
        sizes = '(max-width:520px) 90vw, (max-width:820px) 45vw, 390px'
    else:  # split: column ~380px
        cands = [(400, '400w'), (800, '800w')]
        sizes = '(max-width:820px) 90vw, 380px'
    parts = []
    for w, dw in cands:
        vf = f'{file[:-5]}-{w}.webp' if file.endswith('.webp') else f'{file}-{w}.webp'
        vb = idx.get(vf)
        if vb and (not orig or vb < orig):
            parts.append(f'/images/{vf} {dw}')
    ss = ''
    if parts:
        parts.append(f'/images/{file} 1200w')
        ss = f' srcset="{", ".join(parts)}" sizes="{sizes}"'
    extra = ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    w, h = img_dims(file)
    # HERO FIX 2026-11-05: hero img MUST carry class="hero-img" so the
    # .hero-img rule (height:auto; aspect-ratio:16/9) applies. Without it only
    # img{max-width:100%} applied and width/height attrs forced 800px-tall
    # heroes (557x800 @1440, 350x800 @390). Split/card imgs keep no class
    # (their own .split-fig img / .card img rules apply).
    cls = ' className="hero-img"' if kind == 'hero' else ''
    return f'<img{cls} src="/images/{file}" alt="{esc(clean_alt(alt))}" width="{w}" height="{h}"{ss}{extra} />'

def ensure_variants(files):
    """Generate missing -400/-800 WebP variants (PIL, EXIF stripped)."""
    from PIL import Image
    d = os.path.join(PUBLIC, 'images')
    made = []
    for f in files:
        src = os.path.join(d, f)
        if not os.path.exists(src):
            print(f'WARNING: image missing on disk: {f}')
            continue
        stem = f[:-5] if f.endswith('.webp') else f
        with Image.open(src) as im:
            im = im.convert('RGB')
            for w in (400, 800):
                vf = f'{stem}-{w}.webp'
                vp = os.path.join(d, vf)
                if os.path.exists(vp):
                    continue
                if im.size[0] <= w:
                    continue
                ratio = w / im.size[0]
                small = im.resize((w, max(1, round(im.size[1] * ratio))), Image.LANCZOS)
                small.save(vp, 'WEBP', quality=82, method=6)
                made.append(vf)
    img_index.cache_clear() if hasattr(img_index, 'cache_clear') else None
    global _IMG_IDX
    _IMG_IDX = None
    return made

# Section-heading -> pool topics (ordered preference).
def topics_for_heading(heading, slug):
    h = (heading or '').lower()
    if any(k in h for k in ('ceiling', 'sagging', 'drip', 'bubble', 'blister')):
        return ['ceiling-stain', 'ceiling-stain-lived-in', 'sagging-ceiling', 'attic-insulation']
    if any(k in h for k in ('slab', 'copper', 'pinhole', 'warm spot', 'warm floor')):
        return ['slab-leak', 'burst-pipe', 'copper-pipes', 'hardwood-floor']
    if 'water heater' in h or 'attic' in h:
        return ['water-heater', 'attic-insulation', 'plumber-work']
    if any(k in h for k in ('sewage', 'drain', 'toilet', 'backup')):
        return ['sewage-drain', 'bathroom-leak', 'mold-wall']
    if 'hardwood' in h or 'wood floor' in h:
        return ['hardwood-floor', 'wet-carpet', 'luxury-interior']
    if any(k in h for k in ('cabinet', 'kitchen')):
        return ['cabinet-kitchen', 'kitchen-leak']
    if any(k in h for k in ('laundry', 'washer', 'washing')):
        return ['laundry-room', 'flooded-floor']
    if any(k in h for k in ('crawl', 'pier')):
        return ['crawl-space', 'pier-beam-home', 'mold-wall']
    if any(k in h for k in ('appliance', 'fridge', 'ice maker', 'dishwasher')):
        return ['appliance-fridge', 'kitchen-leak']
    if any(k in h for k in ('sprinkler', 'commercial', 'office', 'business')):
        return ['fire-sprinkler', 'commercial-office']
    if any(k in h for k in ('moisture', 'thermal', 'mapping', 'hidden', 'detect')):
        return ['moisture-meter', 'thermal-imaging', 'ceiling-stain']
    if any(k in h for k in ('wall', 'cavity', 'flood cut', 'baseboard')):
        return ['flood-cut-wall', 'mold-wall', 'steel-studs']
    if 'mold' in h:
        return ['indoor-mold', 'mold-wall']
    if any(k in h for k in ('cost', 'price', 'insurance', 'claim')):
        return ['insurance-claim', 'suburban-home', 'commercial-office']
    if any(k in h for k in ('emergency', 'extract', 'standing water', 'first visit', 'response')):
        return ['water-extraction', 'flooded-floor', 'burst-pipe']
    if any(k in h for k in ('dry', 'dehumidif', 'air mover', 'equipment')):
        return ['drying-equipment', 'drying-fan', 'moisture-meter']
    if any(k in h for k in ('flood', 'storm', 'creek', 'category 3')):
        return ['storm-flood', 'flooded-suburban-home', 'flooded-floor']
    if any(k in h for k in ('shut-off', 'shutoff', 'valve', 'plumb')):
        return ['water-shutoff', 'plumber-work', 'burst-pipe']
    if any(k in h for k in ('fan', 'shop-vac', 'diy')):
        return ['drying-fan', 'drying-equipment', 'wet-carpet']
    if slug in AREA_SLUGS:
        return ['suburban-home', 'texas-home', 'brick-ranch', 'greenbelt-home', 'pier-beam-home']
    return ['suburban-home', 'plumber-work', 'flooded-floor']

def pick_images(page, manifest, pools):
    """Hero (frozen) + 6 split images on evenly-spread content sections.
    Returns (hero_entry, [(section_index, entry)]) with no file repeated
    on the page and no banned file."""
    slug = page['slug']
    by_file = {m['file']: m for m in manifest if m['file'] not in BANNED}
    hero = by_file.get(HERO_FILE.get(slug, ''))
    used = {hero['file']} if hero else set()
    content_secs = [i for i, s in enumerate(page['sections'])
                    if not (s['heading'] and 'Call (972)' in s['heading'])]
    if len(content_secs) < 6:
        content_secs = list(range(len(page['sections'])))
    if not content_secs:
        return hero, []
    # evenly spread 6 indices
    n = len(content_secs)
    if n <= 6:
        chosen_idx = content_secs
    else:
        chosen_idx = sorted({content_secs[round(i * (n - 1) / 5)] for i in range(6)})
        while len(chosen_idx) < 6:  # rounding collisions
            for ci in content_secs:
                if ci not in chosen_idx:
                    chosen_idx.append(ci)
                    if len(chosen_idx) == 6:
                        break
            chosen_idx = sorted(chosen_idx)
    legacy = BODY_FILE.get(slug if slug else 'home', [])
    legacy_entries = [by_file[f] for f in legacy if f in by_file]
    picks = []
    counters = {}
    for si in chosen_idx:
        sec = page['sections'][si]
        topics = topics_for_heading(sec['heading'], slug)
        entry = None
        # legacy first-choice when its topic fits this section
        for le in legacy_entries:
            if le['file'] not in used and le['topic'] in topics:
                entry = le
                break
        if entry is None:
            for tp in topics:
                pool = pools.get(tp, [])
                for _ in range(len(pool)):
                    j = counters.get(tp, 0) % len(pool) if pool else 0
                    counters[tp] = counters.get(tp, 0) + 1
                    if not pool:
                        break
                    cand = pool[j]
                    if cand['file'] not in used and cand['file'] in by_file:
                        entry = cand
                        break
                if entry:
                    break
        if entry is None:
            # neutral fallback (never a banned file, never a repeat)
            for tp in ['suburban-home', 'texas-home', 'plumber-work', 'flooded-floor']:
                for cand in pools.get(tp, []):
                    if cand['file'] not in used and cand['file'] in by_file:
                        entry = cand
                        break
                if entry:
                    break
        if entry:
            picks.append((si, entry))
            used.add(entry['file'])
    # Test-1 viewed-pixel overrides: (slug, section_index) -> file (all pixels verified 2026-11-05)
    overrides = {
        ('structural-drying', 5): 'moisture-meter-8293746.webp',
        ('structural-drying', 6): 'suburban-home-31602311.webp',
        ('warm-spot-on-floor', 4): 'drying-equipment-16243255.webp',
        ('fans-wont-dry-walls', 4): 'mold-wall-18351809.webp',
        ('fans-wont-dry-walls', 5): 'moisture-meter-8293746.webp',
        ('copper-pinhole-leaks', 6): 'drying-equipment-16243255.webp',
        ('copper-pinhole-leaks', 0): 'copper-pipes-3721272.webp',  # TOUCH-UP 2026-11-05: indoor copper-pipe close-up (viewed) replaces muddy outdoor pipe (rejected, now banned) in first split
        ('water-extraction', 6): 'plumber-work-6419128.webp',  # PURGE 2026-11-05: technician hands on indoor pipes/valves (viewed) replaces rejected muddy outdoor pipe in 'Water Extraction Across Plano' split
        ('about', 5): 'drying-equipment-16243255.webp',
        ('crawl-space-drying', 4): 'pier-beam-home-26261510.webp',
        ('water-heater-leak', 5): 'plumber-work-35290675.webp',
        ('water-heater-leak', 6): 'suburban-home-7587470.webp',
        ('fire-sprinkler-cleanup', 1): 'fire-sprinkler-6101250.webp',
        ('fans-wont-dry-walls', 6): 'mopping-tile-floor-6196566.webp',  # COMBINED ROUND 2026-11-05: mopping a tile floor (viewed) replaces banned industrial-wall photo in 'Fans Won't Dry Walls' closing split
        # COMBINED ROUND 2026-11-05: 23 viewed-pixel overrides (19 new Pexels + 4 pool; 1 more repoint above)
        ('about', 3): 'moisture-meter-8482824.webp',
        ('appliance-leak', 1): 'stainless-steel-refrigerator-kitchen-4221389.webp',
        ('attic-insulation-drying', 6): 'suburban-house-exterior-8583638.webp',
        ('emergency-water-damage', 3): 'moisture-inspection-8292797.webp',
        ('fire-sprinkler-cleanup', 5): 'apartment-building-balconies-18153132.webp',
        ('flood-cleanup', 2): 'flooded-street-homes-28447806.webp',
        ('hardwood-floor-drying', 1): 'towel-blotting-wood-floor-4440573.webp',
        ('hardwood-floor-drying', 3): 'uneven-wood-floorboards-39377275.webp',
        ('hardwood-floor-drying', 6): 'moisture-meter-8293746.webp',
        ('hardwood-floor-drying', 7): 'hardwood-floor-living-room-35430055.webp',
        ('laundry-overflow', 2): 'laundry-room-washer-dryer-3935334.webp',
        ('mckinney', 2): 'suburban-home-4832530.webp',
        ('moisture-mapping', 4): 'moisture-meter-7937963.webp',
        ('mold-after-water-damage', 4): 'moisture-meter-8961703.webp',
        ('sewage-cleanup', 0): 'protective-gear-bathroom-4098579.webp',
        ('sewage-cleanup', 3): 'protective-suit-disinfecting-4099463.webp',
        ('sewage-cleanup', 4): 'respirator-containment-6474117.webp',
        ('slab-leak', 9): 'moisture-meter-floor-32497162.webp',
        ('wall-drying', 4): 'exposed-wall-studs-4642438.webp',
        ('water-damage-insurance-texas', 0): 'home-insurance-policy-7731333.webp',
        ('water-damage-insurance-texas', 2): 'copper-pipes-3721272.webp',
        ('water-extraction', 3): 'wet-vacuum-carpet-38325.webp',
        ('water-extraction', 4): 'wet-dry-vacuum-3616735.webp',
    }
    # Apply overrides against the FINAL set (a file freed by one override
    # must be usable by another): start from hero + non-overridden picks.
    oset = {si for (s, si) in overrides if s == slug}
    final_used = {hero['file']} if hero else set()
    for si, entry in picks:
        if si not in oset:
            final_used.add(entry['file'])
    out = []
    for si, entry in picks:
        f = overrides.get((slug, si))
        if f and f in by_file and f not in final_used:
            out.append((si, by_file[f]))
            final_used.add(f)
        else:
            out.append((si, entry))
            final_used.add(entry['file'])
    return hero, out

# ---------------- CSS (hero theme, carried forward + split-sec grid) ----------------

CSS = '''
:root{--ink:#0f2537;--navy:#0a3550;--teal:#0d7a6e;--ocean:#0a5f7a;--rust:#9a3412;--cta:#9a3412;--cta-hover:#7c2d12;--cream:#f7f3ea;--line:#d8e0e6}
*{box-sizing:border-box}html{scroll-behavior:auto}body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#1d2b36;background:#fff;font-size:19px;line-height:1.7}
:focus-visible{outline:3px solid #0d7a6e;outline-offset:3px}
a{color:#064d73;text-decoration:none}a:hover,a:focus-visible{text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:2px}.brand:hover,.main-nav a:hover,.card-body h3 a:hover,.btn-call:hover,.header-call:hover,.mobile-call-bar:hover{text-decoration:none}p a[href^="tel:"]{text-decoration:none}p a[href^="tel:"]:hover,p a[href^="tel:"]:focus-visible{text-decoration:none}
a:hover{color:#084a70}.wrap{max-width:1240px;margin:0 auto;padding:0 20px}
.site-header{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid var(--line);box-shadow:0 2px 10px rgba(0,0,0,.06)}
.header-inner{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 20px;flex-wrap:wrap}
.brand{display:inline-block;padding:11px 0;font-weight:800;color:var(--ink);text-decoration:none;font-size:20px}.brand span{color:var(--teal)}
.main-nav{display:flex;gap:16px;flex-wrap:wrap}.main-nav a{color:var(--ink);text-decoration:none;font-weight:600;font-size:16px;padding:13px 6px}
.header-call,.btn-call{display:inline-block;background:var(--cta);color:#fff!important;text-decoration:none;font-weight:800;padding:12px 20px;border-radius:12px;border:0;cursor:pointer;min-height:44px}.btn-call .nowrap,.header-call .nowrap{white-space:nowrap}a[href^="tel:"]{white-space:nowrap}
.header-call:hover,.btn-call:hover{background:var(--cta-hover)}
.contact-form button.btn-call:hover{background:var(--cta-hover)}
.hero{background:radial-gradient(ellipse 90% 120% at 85% 0%,rgba(45,212,191,.20),transparent 55%),linear-gradient(135deg,#041c2b 0%,#0a3550 48%,#0d7a6e 100%);color:#fff;padding:28px 0 32px;overflow:hidden}
.hero h1{font-size:clamp(24px,2.9vw,32px);line-height:1.15;margin:0 0 14px;color:#fff;text-wrap:balance}
.hero p{font-size:19px;color:#e6f4f1}.hero a{color:#d9f4ff}
.hero-img{width:100%;max-width:520px;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:14px;display:block;margin-top:18px}
.hero-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:28px;align-items:center}.hero-grid>*{min-width:0}
@media(max-width:820px){.hero-grid{grid-template-columns:1fr}.hero h1{font-size:clamp(12.5px,4vw,24px)}h2{font-size:28px}body{font-size:18px}}
.trust-band{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}.trust-band .check{background:#e7f5f2;border:1px solid #bfe3dd;color:#084f49;font-weight:700;padding:8px 12px;border-radius:999px;font-size:15px}
section.block{padding:30px 0}section.block.alt{background:var(--cream)}
.section-kicker{font-size:14px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#475569;margin:0 0 8px}
h2{font-size:32px;line-height:1.25;color:#0b5563;margin:0 0 14px;border-left:6px solid #0d7a6e;padding-left:14px;text-wrap:balance}h2 .nobr{white-space:nowrap}
h3{font-size:23px;color:#92400e;margin:26px 0 10px}
p{margin:0 0 14px}ul{margin:0 0 16px;padding-left:22px}ol{margin:0 0 16px;padding-left:22px}li::marker{color:#0d7a6e;font-weight:700}.doc-table tbody tr:nth-child(even) td{background:#eef6f4}li{margin-bottom:8px;line-height:1.7}
.cta-row{margin:18px 0}
/* Split-container pattern: ONE container, text one side + image other side.
   Desktop >=821px: 2 columns, figure sticky while long text scrolls.
   Mobile: stacks, text first, image after. No visible figcaption ever. */
.split-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,380px);gap:28px;align-items:start}.split-text,.split-fig{min-width:0}
.split-sec.rev .split-grid{grid-template-columns:minmax(0,380px) minmax(0,1fr)}.split-sec.rev .split-text{grid-column:2}.split-sec.rev .split-fig{grid-column:1;grid-row:1}
.split-fig{margin:0}.split-fig img{width:100%;height:auto;display:block;border-radius:14px}img{max-width:100%}
@media(min-width:821px){.split-fig{position:sticky;top:96px}}
@media(max-width:820px){.split-grid{grid-template-columns:minmax(0,1fr)}.split-sec.rev .split-text{grid-column:auto}.split-sec.rev .split-fig{grid-column:auto;grid-row:auto}}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin:10px 0 30px}
@media(max-width:820px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:520px){.cards{grid-template-columns:minmax(0,1fr)}h2{font-size:24px}}
.cards.thin{grid-template-columns:repeat(auto-fit,minmax(280px,360px));justify-content:center}
/* TAB 44 2026-11-05: cards beautiful — soft shadow, clean lift + image zoom on hover (tilt removed). */
.card{border:1px solid #dfe7ec;border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 2px 10px rgba(10,53,80,.07);transition:transform .3s ease,box-shadow .3s ease}
@media(hover:hover){.card:hover{transform:translateY(-6px);box-shadow:0 18px 36px rgba(10,53,80,.16)}.card:hover img{transform:scale(1.04)}}
.card img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;display:block;transition:transform .45s ease}
.card-body{padding:18px 18px 16px}.card-body h3{margin:0 0 6px;font-size:20px;line-height:1.3}.card-body h3 a{color:#0a3550;text-decoration:none;display:inline-block;padding:11px 0}
.faq-item{border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:14px;background:#fff}
.faq-item h3{margin:0 0 8px}.faq-item p{margin:0}
section.block.dark{background:#0a3550;color:#fff;padding:40px 0}.block.dark .cta-row{margin:20px 0 22px}.block.dark .btn-call{padding:14px 26px}.block.dark .trust-band{align-items:center;margin:20px 0 16px}.block.dark p:last-child{margin-bottom:0}section.block.dark h2{color:#fff}section.block.dark a{color:#a9dbff}section.block.dark p{color:#eaf3f8}
.site-footer{background:#0f2537;color:#dbe7ef;margin-top:0;padding:36px 0 0}.site-footer h3{color:#fff}.site-footer a{color:#a9dbff}.site-footer li a,.site-footer p a{display:inline-block;padding:11px 0}.site-footer p a.btn-call{padding:12px 20px} /* FOOTER-BTN FIX 2026-11-05: footer link rule (11px 0) was zeroing the call button's side padding so the label touched both edges; restore designed 12px 20px */
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
.radio-row{display:flex;gap:16px;align-items:center;flex-wrap:wrap}.radio-row label{display:flex;gap:6px;align-items:center;font-weight:600;padding:10px 0}.radio-row input{width:22px;height:22px;accent-color:#0d7a6e;flex:none}
.form-note{font-size:16px;color:#33475b}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}.card{transition:none;transform:none}}
/* TAB 44 2026-11-05: tables restyled — crafted look, not AI-flat: teal gradient header, soft borders, teal-tinted striping, rounded wrapper. */
.table-wrap{overflow-x:auto;border-radius:14px;border:1px solid #d7e3e0;margin:18px 0;box-shadow:0 2px 10px rgba(10,53,80,.06)}
.doc-table{width:100%;border-collapse:collapse;margin:0;font-size:17px;line-height:1.5}
.doc-table th,.doc-table td{border:1px solid #dce7e3;padding:12px 14px;vertical-align:top;text-align:left}
.doc-table th{background:linear-gradient(135deg,#0a3550,#0d7a6e);color:#fff;font-weight:700;letter-spacing:.01em}
.doc-table tbody tr:nth-child(even) td{background:#eef6f4}
.doc-table td p{margin:0 0 8px}.doc-table td p:last-child{margin-bottom:0}
.doc-table a{color:#064d73}
/* TAB 44 2026-11-05: H1 stylish on DESKTOP too — accent bar + gold location now apply at every width (were mobile-only). Desktop font-size unchanged. */
.hero-accent{display:block;width:56px;height:4px;border-radius:2px;background:linear-gradient(90deg,#2dd4bf,#d4a017);margin-bottom:12px}
.hero h1 .h1-loc{color:#f5c86b}
@media(max-width:480px){.hero h1{font-size:22px;line-height:1.28;letter-spacing:-.01em;font-weight:800}}
/* TAB 44 2026-11-05: Quick Answer card, at-a-glance box, related-current line, homepage polish. */
.qa-card{background:linear-gradient(180deg,#eef7f5 0%,#e3f2ef 100%);border:1px solid #bfe3dd;border-left:6px solid #0d7a6e;border-radius:16px;padding:24px 26px;margin:6px 0 8px;box-shadow:0 4px 16px rgba(10,53,80,.08)}
.qa-card h2{border-left:0;padding-left:0;margin:0 0 10px;color:#084f49}
.qa-card p:last-child{margin-bottom:0}
@media(max-width:820px){.qa-card{padding:20px}}
.glance-box{background:linear-gradient(135deg,#0a3550 0%,#0d7a6e 100%);color:#fff;border-radius:16px;padding:22px 26px;margin:8px 0 18px;box-shadow:0 6px 20px rgba(10,53,80,.18)}
.glance-box p{margin:0 0 10px;color:#fff}
.glance-box p strong{color:#f5c86b;font-size:19px;letter-spacing:.02em;text-transform:uppercase}
.glance-box ul{margin:0}
.glance-box li{color:#eaf3f8}
.glance-box li::marker{color:#f5c86b}
.glance-box a{color:#a9dbff}
.related-current{font-size:15px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#0b5563;margin:2px 0 14px}
.hero-home{padding:40px 0 40px}
.hero-home .hero-img{box-shadow:0 18px 44px rgba(0,0,0,.28)}
'''

# TAB 44 2026-11-05 (user-ordered exceptions, counted for the gates log):
#  - Items 1+5 (CORRECTED ~18:43 PKT — the word is "Quick Answer"): the entire
#    "(Quick Answer)" label (words + brackets) is removed from H2s at render
#    time in write_page().
#  - Item 3: the single "Done? Call..." line is removed from the home page only.
#  - CLEANUP 2026-11-05 ~19:31 PKT (user: "Han, dono hata do"): the bare
#    ": Quick Answer" suffix (no parens) is removed from the 9 area H2s
#    (colon included, no trailing colon left), and the short "Done? Call
#    (972) 472-7917." line is removed from emergency + the same 9 area pages.
TAB44 = {'qa_labels': 0, 'done_removed': 0, 'glance_boxes': 0, 'qa_cards': 0,
         'bare_qa': 0, 'short_done': 0}

DONE_LINE = 'Done? Call (972) 472-7917. Help can be on the way while you read the rest of this page.'
SHORT_DONE_LINE = 'Done? Call (972) 472-7917.'
SHORT_DONE_SLUGS = {'emergency-water-damage', 'west-plano', 'legacy-west', 'north-plano',
                    'central-plano', 'east-plano', 'frisco', 'allen', 'mckinney', 'richardson'}

def jsonld(obj):
    return '<script type="application/ld+json" dangerouslySetInnerHTML={{__html: JSON.stringify(' + json.dumps(obj, ensure_ascii=False) + ')}} />'

def nobr_h2(html_text):
    def _wrap(m):
        inner = re.sub(r'\(\d{5}(?:, \d{5})*\)',
                       lambda mm: f'<span className="nobr">{mm.group(0)}</span>', m.group(1))
        return f'<h2>{inner}</h2>'
    return re.sub(r'<h2>(.*?)</h2>', _wrap, html_text, flags=re.S)

def blocks_html(blocks):
    """Render blocks, grouping an 'at a glance' para + following list(s) into
    one styled box (TAB 44 item 9)."""
    out = ''
    i = 0
    while i < len(blocks):
        b = blocks[i]
        if b['type'] == 'para' and re.search(r'at a glance:\s*$', segs_plain(b['segs']).strip(), re.I):
            parts = [block_html(b)]
            j = i + 1
            while j < len(blocks) and blocks[j]['type'] == 'list':
                parts.append(block_html(blocks[j]))
                j += 1
            out += f'<div className="glance-box">{"".join(parts)}</div>'
            TAB44['glance_boxes'] += 1
            i = j
        else:
            out += block_html(b)
            i += 1
    return out

def section_inner(sec):
    inner = ''
    if sec.get('heading'):
        inner += f'<h2>{esc(sec["heading"])}</h2>'
    inner += blocks_html(sec['blocks'])
    if sec.get('heading') and 'Quick Answer' in sec['heading']:
        # TAB 44 item 2: the Quick Answer section becomes a beautiful card.
        # (The "(Quick Answer)" label itself is stripped at render time in
        # write_page; detection here uses the raw heading, parens or bare.)
        TAB44['qa_cards'] += 1
        return f'<div className="qa-card">{inner}</div>'
    return inner

def cards_html(title, slugs, by_slug, hero_by_slug, exclude, body_by_slug, neutral=None, chosen=None, pre_html=None):
    cards = ''
    # HERO FIX 2026-11-05: 'chosen' is a shared set when a page renders two
    # card sections (home: services + areas). Previously each call had its
    # own set, so a swapped image could repeat across the two sections —
    # home showed flooded-floor-7924140.webp on both the appliance-leak
    # service card and the Richardson area card.
    if chosen is None:
        chosen = set()
    for s in slugs:
        t = by_slug.get(s)
        if not t:
            continue
        h = hero_by_slug.get(s)
        img_file = h['file'] if h else None
        img_alt = h['alt'] if h else ''
        if img_file and (img_file in chosen or img_file in exclude):
            swapped = False
            for alt_im in (body_by_slug or {}).get(s, []):
                if alt_im['file'] not in exclude and alt_im['file'] not in chosen:
                    img_file, img_alt = alt_im['file'], alt_im['alt']
                    swapped = True
                    break
            if not swapped:
                img_file = None
        if not img_file:
            # Last resort: a neutral suburban exterior not on this page,
            # so no card ever renders imageless.
            for (nf, na) in (neutral or []):
                if nf not in exclude and nf not in chosen:
                    img_file, img_alt = nf, na
                    break
        if img_file:
            chosen.add(img_file)
        img = img_tag(img_file, img_alt, 'card') if img_file else ''
        cards += (f'<article className="card reveal">{img}<div className="card-body">'
                  f'<h3><a href="{href_for(s)}">{esc(t["meta_title"])}</a></h3></div></article>')
    cls = 'cards thin' if len(slugs) < 3 else 'cards'
    return f'<section className="block cards-sec"><div className="wrap"><h2>{esc(title)}</h2>{pre_html or ""}<div className="{cls}">{cards}</div></div></section>'

def h1_html(h1):
    # MOBILE H1 STYLE 2026-11-05: wrap the trailing location phrase (e.g.
    # " in Plano, TX") in a span so it renders gold on mobile only. Words
    # unchanged — textContent is identical, qa4 H1-exact unaffected.
    core, trail = h1, ''
    if core.endswith('?'):
        core, trail = core[:-1], '?'
    m = re.search(r' (in .+, TX)$', core)
    if not m:
        m = re.search(r' ([A-Z][A-Za-z]+, TX)$', core)
    if not m:
        return esc(h1)
    loc = m.group(0)
    return esc(core[:-len(loc)]) + f'<span className="h1-loc">{esc(loc)}</span>' + esc(trail)

def write_page(page, hero, picks, by_slug, hero_by_slug, body_by_slug, neutral=None):
    slug = page['slug']
    sections = page['sections']
    pick_by_sec = dict(picks)
    page_files = ({hero['file']} if hero else set()) | {e['file'] for (_i, e) in picks}
    if slug == '' or slug in SHORT_DONE_SLUGS:
        # TAB 44 item 3: remove the single "Done? Call..." line from the home page only.
        # CLEANUP 2026-11-05: also drop the short "Done? Call (972) 472-7917." line
        # from emergency + the 9 area pages (user: "Han, dono hata do").
        def _drop_done(blocks):
            kept = []
            for b in blocks:
                if b.get('type') == 'para':
                    _txt = segs_plain(b.get('segs', [])).strip()
                    if _txt == DONE_LINE:
                        TAB44['done_removed'] += 1
                        continue
                    if slug in SHORT_DONE_SLUGS and _txt == SHORT_DONE_LINE:
                        TAB44['short_done'] += 1
                        continue
                kept.append(b)
            return kept
        page['intro'] = _drop_done(page['intro'])
        for _sec in sections:
            _sec['blocks'] = _drop_done(_sec['blocks'])
    # Hero: first intro para + intro CTA label as the hero button.
    hero_para = ''
    intro_rest = []
    hero_cta_label = 'Call Now'
    for b in page['intro']:
        if b['type'] == 'para' and not hero_para:
            hero_para = block_html(b)
        elif b['type'] == 'cta':
            hero_cta_label = b['label'].split(':')[0].strip()
        else:
            intro_rest.append(b)
    hero_cta_html = f'<p><a className="btn-call" href="{TEL}">{esc(hero_cta_label)}: <span className="nowrap">{PHONE}</span></a></p>'
    hero_img = img_tag(hero['file'], hero['alt'], 'hero', eager=True) if hero else ''
    hero_cls = 'hero hero-home' if slug == '' else 'hero'
    out_sections = []
    home_cards = set()  # HERO FIX 2026-11-05: shared across home's two card sections so a swapped image can't repeat (see cards_html).
    if intro_rest:
        inner = blocks_html(intro_rest)
        out_sections.append(f'<section className="block"><div className="wrap">{inner}</div></section>')
    band = 0
    for si, sec in enumerate(sections):
        if not sec['blocks'] and not sec.get('heading'):
            continue
        inner = section_inner(sec)
        if not inner.strip():
            continue
        dark = bool(sec.get('heading') and 'Call (972)' in sec['heading'])
        if si in pick_by_sec:
            im = pick_by_sec[si]
            rev = ' rev' if (len(out_sections) % 2 == 1) else ''
            alt_cls = ' alt' if (band % 2 == 1) else ''
            dark_cls = ' dark' if dark else ''
            out_sections.append(
                f'<section className="block split-sec{rev}{alt_cls}{dark_cls}"><div className="wrap split-grid">'
                f'<div className="split-text">{inner}</div>'
                f'<figure className="split-fig">{img_tag(im["file"], im["alt"], "split")}</figure>'
                f'</div></section>')
        else:
            alt_cls = ' alt' if (band % 2 == 1) else ''
            cls = 'block dark' if dark else f'block{alt_cls}'
            out_sections.append(f'<section className="{cls}"><div className="wrap">{inner}</div></section>')
        band += 1
        # Home grids after their anchor sections.
        if slug == '' and sec.get('heading') == 'Water Damage Restoration Services in Plano, TX':
            out_sections.append(cards_html('Our Services in Plano, TX', SERVICE_SLUGS, by_slug, hero_by_slug, page_files, body_by_slug, neutral, home_cards))
        if slug == '' and sec.get('heading') and sec['heading'].startswith('Serving Every Plano ZIP Code'):
            out_sections.append(cards_html('Areas We Serve Around Plano', AREA_SLUGS, by_slug, hero_by_slug, page_files, body_by_slug, neutral, home_cards))
    # Related cards (non-home): TAB 44 2026-11-05 — per page type, doc order,
    # doc-existing links only, never invented; home target never a card.
    if slug != '':
        rel = []
        for lk in page['links']:
            if lk['kind'] in ('paren', 'run', 'table-bare') and lk['target'] and lk['target'] not in rel and lk['target'] != slug:
                rel.append(lk['target'])
        if slug in SERVICE_SLUGS:
            # Item 7: only the 2 most relevant services = first 2 service links in doc order.
            keep = [t for t in rel if t in SERVICE_SLUGS][:2]
            if keep:
                out_sections.append(cards_html('Related Services', keep, by_slug, hero_by_slug, page_files, body_by_slug, neutral))
        elif slug in AREA_SLUGS:
            # Item 11: related AREAS (not services), 3-4 = all doc-linked areas
            # (each area page has 3-4 in the doc; nothing invented, nothing dropped).
            keep = [t for t in rel if t in AREA_SLUGS][:4]
            if keep:
                # Item 12: current area name as plain text, never a self-link.
                cur = AREA_NAMES.get(slug, slug.replace('-', ' ').title())
                out_sections.append(cards_html('Related Areas', keep, by_slug, hero_by_slug, page_files, body_by_slug, neutral,
                                               pre_html=f'<p className="related-current">{esc(cur)}</p>'))
        elif slug in GUIDE_SLUGS:
            # Item 13 (FLAGGED reading): guides show 3 most-relevant cards = first 3 in doc order.
            keep = rel[:3]
            if keep:
                out_sections.append(cards_html('Related Services & Guides', keep, by_slug, hero_by_slug, page_files, body_by_slug, neutral))
        else:
            # about / contact: unchanged (first 6 in doc order, mixed).
            keep = rel[:6]
            if keep:
                out_sections.append(cards_html('Related Services & Guides', keep, by_slug, hero_by_slug, page_files, body_by_slug, neutral))
    # FAQ
    faq_html = ''
    faq_schema = None
    if page['faqs']:
        items = ''
        faq_objs = []
        for f in page['faqs']:
            a_html_parts = []
            for segs in f['a_segs']:
                a_html_parts.append(render_segs(segs))
            a_html = ' '.join(a_html_parts)
            items += f'<div className="faq-item"><h3>{esc(f["q"])}</h3><p>{a_html}</p></div>'
            faq_objs.append({'@type': 'Question', 'name': f['q'],
                             'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}})
        faq_html = (f'<section className="block faq-sec"><div className="wrap">'
                    f'<h2>{esc(page["faq_heading"] or "Frequently Asked Questions")}</h2>{items}</div></section>')
        faq_schema = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': faq_objs}
    schemas = []
    if faq_schema:
        schemas.append(faq_schema)
    _crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': DOMAIN + '/'}]
    if slug != '':
        _crumbs.append({'@type': 'ListItem', 'position': 2, 'name': page['meta_title'], 'item': DOMAIN + href_for(slug)})
    schemas.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': _crumbs})
    if slug in SERVICE_SLUGS:
        schemas.append({'@context': 'https://schema.org', '@type': 'Service', 'name': page['meta_title'],
                        'description': page['meta_desc'],
                        'provider': {'@type': 'LocalBusiness', 'name': BRAND, 'telephone': PHONE, 'areaServed': 'Plano, TX'},
                        'areaServed': 'Plano, TX'})
    if slug == '' or slug == 'contact':
        schemas.append({'@context': 'https://schema.org', '@type': 'LocalBusiness', 'name': BRAND,
                        'telephone': PHONE, 'areaServed': 'Plano, TX', 'openingHours': 'Mo-Su 00:00-24:00',
                        'url': DOMAIN + '/', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Plano', 'addressRegion': 'TX', 'addressCountry': 'US'}})
    if slug == 'about':
        schemas.append({'@context': 'https://schema.org', '@type': 'AboutPage', 'name': page['meta_title'],
                        'url': DOMAIN + '/about/'})
    schema_tags = '\n'.join(jsonld(s) for s in schemas)
    map_html = ''
    if slug not in NO_MAP_SLUGS:
        map_html = ('<section className="block map-sec"><div className="wrap"><h2>Find Us in Plano, TX</h2>'
                    '<iframe className="map-frame" loading="lazy" title="Map of Plano, TX" '
                    'src="https://www.google.com/maps?q=Plano,%20TX&output=embed"></iframe></div></section>')
    og_images = f'["/images/{hero["file"]}"]' if hero else '[]'
    meta_title_j = json.dumps(page['meta_title'] or page['h1'])
    meta_desc_j = json.dumps(page['meta_desc'])
    content = f'''export const metadata = {{ title: {meta_title_j}, description: {meta_desc_j}, alternates: {{ canonical: "{DOMAIN}{href_for(slug)}" }}, openGraph: {{ type: \"website\", title: {meta_title_j}, description: {meta_desc_j}, url: "{DOMAIN}{href_for(slug)}", images: {og_images} }} }};
export default function Page() {{
  return (<>
    {schema_tags}
    <div className="{hero_cls}"><div className="wrap hero-grid"><div>
      <div className="hero-accent" aria-hidden="true"></div>
      <h1>{h1_html(page["h1"])}</h1>
      {hero_para}
      {hero_cta_html}
    </div>{hero_img}</div></div>
    {''.join(out_sections)}
    {faq_html}
    {map_html}
  </>);
}}
'''
    # TAB 44 items 1+5 (CORRECTED — the word is "Quick Answer"): remove the
    # entire "(Quick Answer)" label (words + brackets) from H2s, sitewide.
    content, _n_qa = re.subn(r'\s*\(Quick Answer\)', '', content)
    TAB44['qa_labels'] += _n_qa
    # CLEANUP 2026-11-05 (user: "Han, dono hata do"): remove the bare
    # ": Quick Answer" suffix (no parens) from the 9 area H2s, colon included.
    content, _n_bare = re.subn(r':\s*Quick Answer', '', content)
    TAB44['bare_qa'] += _n_bare
    content = nobr_h2(content)
    path = os.path.join(APP, 'page.jsx') if slug == '' else os.path.join(APP, slug, 'page.jsx')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(content)

# HERO FIX 2026-11-05: hub pages were text-only 181px heroes. Each hub now
# gets a fitting hero image from the EXISTING pool (viewed-verified; file is
# NOT any card hero on that hub, and is excluded from its cards so the page
# never shows the same file twice).
HUB_HERO = {
    'services': ('plumber-work-6419128.webp', "Close-up of a plumber's hands installing steel pipes indoors, showcasing skilled manual work."),
    'areas': ('suburban-home-186077.webp', 'Suburban home exterior in a residential neighborhood'),
    'guides': ('thermal-imaging-7859781.webp', "A thermal imaging screen in the foreground showing a person's heat image in orange, yellow and blue, held in front of a man indoors"),
}

def write_hub(slug, title, slugs, by_slug, hero_by_slug, body_by_slug, neutral=None):
    hero_file, hero_alt = HUB_HERO[slug]
    cards = cards_html(title, slugs, by_slug, hero_by_slug, {hero_file}, body_by_slug, neutral)
    hero_img = img_tag(hero_file, hero_alt, 'hero', eager=True)
    map_html = ('<section className="block map-sec"><div className="wrap"><h2>Find Us in Plano, TX</h2>'
                '<iframe className="map-frame" loading="lazy" title="Map of Plano, TX" '
                'src="https://www.google.com/maps?q=Plano,%20TX&output=embed"></iframe></div></section>')
    _hub_schema = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': DOMAIN + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': title, 'item': DOMAIN + f'/{slug}/'}]}
    content = f'''export const metadata = {{ title: {json.dumps(title + " | Water Damage Restoration Plano, TX")}, description: {json.dumps(title + " — Water Damage Restoration Plano, TX. Call (972) 472-7917.")}, alternates: {{ canonical: "{DOMAIN}/{slug}/" }}, openGraph: {{ type: \"website\", title: {json.dumps(title + " | Water Damage Restoration Plano, TX")}, description: {json.dumps(title + " — Water Damage Restoration Plano, TX. Call (972) 472-7917.")}, url: "{DOMAIN}/{slug}/", images: ["{DOMAIN}/images/{hero_file[:-5]}-800.webp"] }} }};
export default function Page() {{
  return (<><div className="hero"><div className="wrap hero-grid"><div><div className="hero-accent" aria-hidden="true"></div><h1>{h1_html(title)}</h1><p><a className="btn-call" href="{TEL}">Call Now: <span className="nowrap">{PHONE}</span></a></p></div>{hero_img}</div></div>
  {cards}
  {map_html}
  {jsonld(_hub_schema)}
  </>);
}}
'''
    content = nobr_h2(content)
    path = os.path.join(APP, slug, 'page.jsx')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(content)

def write_sitemap(pages):
    urls = [''] + [p['slug'] for p in pages if p['slug']] + ['services', 'areas', 'guides']
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        loc = DOMAIN + '/' if u == '' else f'{DOMAIN}/{u}/'
        lines.append(f'<url><loc>{loc}</loc><lastmod>2026-11-05</lastmod></url>')
    lines.append('</urlset>')
    open(os.path.join(PUBLIC, 'sitemap.xml'), 'w').write('\n'.join(lines))
    open(os.path.join(PUBLIC, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
    return urls

def main():
    doc_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, 'rebuild-doc-tabs.json')
    pages, dup_tabs = parse_tabs(doc_path)
    print(f'pages={len(pages)} dup_tabs={dup_tabs}')
    manifest = [m for m in json.load(open(os.path.join(BASE, 'images.json'))) if m['file'] not in BANNED]
    pools = {}
    for m in manifest:
        pools.setdefault(m['topic'], []).append(m)
    by_slug = {p['slug']: p for p in pages}
    hero_by_slug = {}
    body_by_slug = {}
    page_imgs = {}
    for p in pages:
        hero, picks = pick_images(p, manifest, pools)
        hero_by_slug[p['slug']] = hero
        body_by_slug[p['slug']] = [e for (_i, e) in picks]
        page_imgs[p['slug']] = (hero, picks)
    # Variants for every used file (hero + splits + card heroes + hub heroes).
    used_files = set()
    for slug, (hero, picks) in page_imgs.items():
        if hero:
            used_files.add(hero['file'])
        for (_i, e) in picks:
            used_files.add(e['file'])
    for _hf, _ha in HUB_HERO.values():
        used_files.add(_hf)
    made = ensure_variants(sorted(used_files))
    print(f'variants generated: {len(made)}')
    neutral = [(m['file'], m['alt']) for m in manifest if m['topic'] in ('suburban-home', 'texas-home')]
    # CSS (layout.jsx / components.jsx are carried forward untouched).
    open(os.path.join(APP, 'globals.css'), 'w').write(CSS)
    for p in pages:
        hero, picks = page_imgs[p['slug']]
        write_page(p, hero, picks, by_slug, hero_by_slug, body_by_slug, neutral)
    tab44_log = {'qa_labels_removed': TAB44['qa_labels'], 'done_line_removed': TAB44['done_removed'],
                 'glance_boxes': TAB44['glance_boxes'], 'qa_cards': TAB44['qa_cards'],
                 'bare_qa_removed': TAB44['bare_qa'], 'short_done_removed': TAB44['short_done']}
    json.dump(tab44_log, open(os.path.join(BASE, 'tab44-log.json'), 'w'), indent=1)
    print(f"TAB44 qa_labels={TAB44['qa_labels']} done_removed={TAB44['done_removed']} glance_boxes={TAB44['glance_boxes']} qa_cards={TAB44['qa_cards']} bare_qa={TAB44['bare_qa']} short_done={TAB44['short_done']}")
    write_hub('services', 'Our Water Damage Services in Plano, TX', SERVICE_SLUGS, by_slug, hero_by_slug, body_by_slug, neutral)
    write_hub('areas', 'Water Damage Restoration Areas Around Plano, TX', AREA_SLUGS, by_slug, hero_by_slug, body_by_slug, neutral)
    write_hub('guides', 'Plano Water Damage Guides', GUIDE_SLUGS, by_slug, hero_by_slug, body_by_slug, neutral)
    urls = write_sitemap(pages)
    # NOTE (refinements 2026-11-05): the old stale-Murphy deletion was removed —
    # Murphy is now a preserved page (old content, /murphy/) by user order.
    summ = []
    for p in pages:
        hero, picks = page_imgs[p['slug']]
        summ.append({'slug': p['slug'], 'tab_no': p['tab_no'], 'h1': p['h1'],
                     'sections': len(p['sections']), 'faqs': len(p['faqs']),
                     'hero': hero['file'] if hero else None,
                     'splits': [(si, e['file'], e['topic']) for (si, e) in picks],
                     'doc_links': len([l for l in p['links'] if l['kind'] in ('paren', 'run')]),
                     'unlinked': len([l for l in p['links'] if l['kind'] == 'unlinked']),
                     'self': len([l for l in p['links'] if l['kind'] == 'self'])})
    json.dump(summ, open(os.path.join(BASE, 'rebuild-summary.json'), 'w'), indent=1)
    print(f"sitemap urls={len(urls)}")
    for s in summ:
        print(f"{s['slug'] or '/':32} secs={s['sections']:2} faqs={s['faqs']:2} splits={len(s['splits'])} hero={s['hero']} links={s['doc_links']} unlinked={s['unlinked']} self={s['self']}")

if __name__ == '__main__':
    main()
