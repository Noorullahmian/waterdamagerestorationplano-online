#!/usr/bin/env python3
"""Hero-fix round: STRICT backlink audit (Order 2, 2026-11-05).

Compares EVERY doc link (gen4.parse_tabs over rebuild-doc-tabs.json, the
fresh Google Docs API tabs JSON) against the rendered out/ HTML, per page:
  - multiset (anchor, target) counts, not just anchor sets (qa4 collapses dups)
  - ordered sequence (same place = same document order)
  - content zone = hero + body sections + FAQ (header/footer/cards/map excluded)
Template links (header, footer, hub cards, related cards, hero CTA tel) are
inventoried separately and NEVER counted as content links.
Footer visible text is listed and checked against doc plain text (report only).
Usage: python3 hero-fix-backlink-audit.py [outdir] -> hero-fix-backlink-audit.json
"""
import sys, os, re, json, html
from collections import Counter
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen4 import parse_tabs

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'out')

def norm(s):
    s = (s or '').replace('\u2014', ' ').replace('\u2013', ' ')
    s = s.replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    s = re.sub(r'\s+', ' ', s).strip().lower()
    s = re.sub(r'\s+([,.;:?!])', r'\1', s)
    return s

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, zone_hint)
        self.zone = 'outside'
        self.links = []  # (zone, anchor, href)
        self._a = None
        self._a_text = ''
        self.footer_text = ''
        self._in_footer = False
    def _zone_for(self, tag, attrs):
        cls = dict(attrs).get('class', '')
        if tag == 'header': return 'header'
        if tag == 'footer': return 'footer'
        if 'hero' in cls.split(): return 'hero'
        if 'cards-sec' in cls: return 'cards'
        if 'map-sec' in cls: return 'map'
        if 'faq-sec' in cls: return 'faq'
        return None
    VOID = {'img', 'br', 'meta', 'link', 'input', 'hr', 'source'}
    def handle_startendtag(self, tag, attrs):
        # void/self-closing tags (img, br) must not touch the zone stack:
        # the default impl calls starttag+endtag, which would pop a level.
        return
    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        z = self._zone_for(tag, attrs)
        self.stack.append(z or self.zone)
        if z: self.zone = z
        if tag == 'footer': self._in_footer = True
        if tag == 'a':
            self._a = dict(attrs).get('href', '')
            self._a_text = ''
    def handle_endtag(self, tag):
        if tag == 'a' and self._a is not None:
            self.links.append((self.zone, norm(self._a_text), self._a))
            self._a = None
        if tag == 'footer': self._in_footer = False
        if self.stack: self.stack.pop()
        self.zone = self.stack[-1] if self.stack else 'outside'
    def handle_data(self, data):
        if self._a is not None: self._a_text += data
        if self._in_footer: self.footer_text += data

def main():
    pages, _ = parse_tabs(os.path.join(BASE, 'rebuild-doc-tabs.json'))
    by_slug = {p['slug']: p for p in pages}
    built = set(by_slug) | {'services', 'areas', 'guides'}
    report = {'pages': {}, 'template': {}, 'footer_text': {}}
    tot_doc = tot_ren = 0
    tot_missing = tot_extra = tot_wrong_order = 0
    for p in pages:
        slug = p['slug']
        hpath = os.path.join(OUT, 'index.html') if slug == '' else os.path.join(OUT, slug, 'index.html')
        h = open(hpath).read()
        lp = LinkParser()
        lp.feed(h)
        # content links: internal, in hero/content/faq zones (content = main default zone)
        content = [(a, href.strip('/')) for (z, a, href) in lp.links
                   if z in ('hero', 'faq', 'outside', 'content') and href.startswith('/') and not href.startswith('//')]
        # note: main body sections carry no zone class -> parser zone stays 'outside' after header;
        # hero/faq are zoned explicitly. cards/map/footer/header excluded by zone.
        doc_links = [(norm(l['anchor']), l['target']) for l in p['links'] if l['kind'] in ('paren', 'run', 'table-bare')]
        dc, rc = Counter(doc_links), Counter(content)
        missing = sorted((list((dc - rc).elements())))
        extra = sorted((list((rc - dc).elements())))
        doc_seq = [x for x in doc_links]
        ren_seq = [x for x in content]
        # FAQ-last structure: generator always renders the FAQ section after
        # all body sections, while most doc tabs have a closing section AFTER
        # their FAQ block. So exact doc order differs only by that block move:
        # rendered == body links (doc order) + FAQ links (doc order).
        faq_flags = [l['in_faq'] for l in p['links'] if l['kind'] in ('paren', 'run', 'table-bare')]
        hypo = [d for d, f in zip(doc_seq, faq_flags) if not f] + [d for d, f in zip(doc_seq, faq_flags) if f]
        order_ok = (doc_seq == ren_seq) or (hypo == ren_seq)
        order_note = 'exact' if doc_seq == ren_seq else ('faq-block-last' if hypo == ren_seq else 'REAL ORDER DIFF')
        self_links = [x for x in content if ('/' + x[1] + '/') == ('/' + slug + '/' if slug else '/') or (x[1] == '' and slug == '')]
        broken = [x for x in content if x[1] not in built]
        zones = Counter(z for (z, a, href) in lp.links)
        tel = sum(1 for (z, a, href) in lp.links if href.startswith('tel:'))
        report['pages'][slug or '/'] = {
            'doc_links': len(doc_links), 'rendered_content': len(content),
            'missing': missing, 'extra': extra, 'order_ok': order_ok, 'order_note': order_note,
            'self': self_links, 'broken': broken,
            'zones': dict(zones), 'tel_links': tel}
        tot_doc += len(doc_links); tot_ren += len(content)
        tot_missing += len(missing); tot_extra += len(extra)
        if not order_ok: tot_wrong_order += 1
        print(f"{slug or '/':32} doc={len(doc_links):3} ren={len(content):3} miss={len(missing)} extra={len(extra)} order_ok={order_ok} self={len(self_links)} broken={len(broken)} zones={dict(zones)} tel={tel}")
        if missing: print('   MISSING:', missing[:10])
        if extra: print('   EXTRA:', extra[:10])
    # hubs: template-only pages (no doc links); inventory their links by zone
    for hub in ('services', 'areas', 'guides'):
        h = open(os.path.join(OUT, hub, 'index.html')).read()
        lp = LinkParser(); lp.feed(h)
        zc = Counter(z for (z, a, href) in lp.links)
        cards = [(a, href) for (z, a, href) in lp.links if z == 'cards']
        hero = [(a, href) for (z, a, href) in lp.links if z == 'hero']
        report['template'][hub] = {'zones': dict(zc), 'cards': cards, 'hero_links': hero}
        print(f"HUB {hub}: zones={dict(zc)} cards={len(cards)} hero_links={hero}")
    # footer text audit: every footer sentence vs doc plain text
    doc_text = open(os.path.join(BASE, 'extracted.txt')).read().lower() if os.path.exists(os.path.join(BASE, 'extracted.txt')) else ''
    h0 = open(os.path.join(OUT, 'index.html')).read()
    lp0 = LinkParser(); lp0.feed(h0)
    ftxt = re.sub(r'\s+', ' ', lp0.footer_text).strip()
    report['footer_text']['home_footer_raw'] = ftxt
    print('FOOTER (home):', ftxt)
    # header/footer template link inventory (same on every page: layout.jsx)
    hdr = [(a, href) for (z, a, href) in lp0.links if z == 'header']
    ftr = [(a, href) for (z, a, href) in lp0.links if z == 'footer']
    report['template']['header_links'] = hdr
    report['template']['footer_links'] = ftr
    print(f"HEADER links ({len(hdr)}): {hdr}")
    print(f"FOOTER links ({len(ftr)}): {ftr}")
    print(f"TOTALS doc={tot_doc} rendered_content={tot_ren} missing={tot_missing} extra={tot_extra} pages_order_bad={tot_wrong_order}")
    json.dump(report, open(os.path.join(BASE, 'hero-fix-backlink-audit.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
