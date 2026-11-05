#!/usr/bin/env python3
"""QA gates for the Plano 3 rebuild (gen4): word-diff, links, tables, meta,
FAQ==schema, H1, images, sitemap, forbidden strings, image weights.
Reads out/*.html + gen4.parse_tabs (fresh doc). Writes qa4.json."""
import re, os, json, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen4 import parse_tabs, words_of, segs_plain

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'out')

def clean_html_text(h):
    h = re.sub(r'<script.*?</script>', ' ', h, flags=re.S)
    h = re.sub(r'<style.*?</style>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return html.unescape(h)

def norm_anchor(s):
    s = (s or '').replace('\u2014', ' ').replace('\u2013', ' ')
    s = s.replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    s = re.sub(r'\s+', ' ', s).strip().lower()
    s = re.sub(r'\s+([,.;:?!])', r'\1', s)
    return s

def doc_words(page):
    ws = set()
    def add(t):
        ws.update(words_of(t))
    add(page['h1'])
    for b in page['intro']:
        if b['type'] == 'para':
            add(segs_plain(b['segs']))
        elif b['type'] == 'trust':
            for x in b['items']:
                add(x)
        elif b['type'] == 'cta':
            add(b['label'])
        elif b['type'] == 'list':
            for it in b['items']:
                add(it)
    for sec in page['sections']:
        if sec.get('heading'):
            add(sec['heading'])
        for b in sec['blocks']:
            if b['type'] == 'para':
                add(segs_plain(b['segs']))
            elif b['type'] == 'subhead':
                add(b['text'])
            elif b['type'] == 'trust':
                for x in b['items']:
                    add(x)
            elif b['type'] == 'cta':
                add(b['label'])
            elif b['type'] == 'list':
                for it in b['items']:
                    add(it)
            elif b['type'] == 'table':
                for row in b['rows']:
                    for cell in row:
                        for csegs in cell:
                            add(segs_plain(csegs))
            elif b['type'] == 'form':
                for f in b['fields']:
                    add(f)
                add(b['note'])
                add('Send Message')
    if page['faq_heading']:
        add(page['faq_heading'])
    for f in page['faqs']:
        add(f['q'])
        add(f['a'])
    return ws

def main():
    pages, _ = parse_tabs(os.path.join(BASE, 'rebuild-doc-tabs.json'))
    by_slug = {p['slug']: p for p in pages}
    built_slugs = set(by_slug) | {'services', 'areas', 'guides'}
    results = []
    for p in pages:
        slug = p['slug']
        hpath = os.path.join(OUT, 'index.html') if slug == '' else os.path.join(OUT, slug, 'index.html')
        h = open(hpath).read()
        main = re.search(r'<main>(.*?)</main>', h, re.S).group(1)
        # strip template sections from the rendered side
        stripped = re.sub(r'<section class="block cards-sec">.*?</section>', ' ', main, flags=re.S)
        stripped = re.sub(r'<section class="block map-sec">.*?</section>', ' ', stripped, flags=re.S)
        vis = clean_html_text(stripped)
        ren_words = set(words_of(vis))
        dw = doc_words(p)
        miss = sorted(w for w in dw if w not in ren_words)
        h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', main, re.S)
        h1_text = [norm_anchor(clean_html_text(x)) for x in h1s]
        # meta
        title_m = re.search(r'<title>(.*?)</title>', h, re.S)
        desc_m = re.search(r'<meta name="description" content="([^"]*)"', h)
        canon_m = re.search(r'<link rel="canonical" href="([^"]*)"', h)
        meta_ok = (bool(title_m) and html.unescape(title_m.group(1)) == p['meta_title']
                   and bool(desc_m) and html.unescape(desc_m.group(1)) == p['meta_desc'])
        # FAQ visible vs schema
        faq_items = re.findall(r'<div class="faq-item"><h3>(.*?)</h3><p>(.*?)</p></div>', main, re.S)
        faq_vis = [(norm_anchor(clean_html_text(q)), norm_anchor(clean_html_text(a))) for q, a in faq_items]
        schema_faq = []
        for sm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try:
                obj = json.loads(sm.group(1))
            except Exception:
                continue
            if obj.get('@type') == 'FAQPage':
                schema_faq = [(norm_anchor(q['name']), norm_anchor(q['acceptedAnswer']['text'])) for q in obj['mainEntity']]
        faq_match = (len(faq_vis) == len(schema_faq) and faq_vis == schema_faq)
        faq_doc = [(norm_anchor(f['q']), norm_anchor(f['a'])) for f in p['faqs']]
        faq_doc_match = (faq_vis == faq_doc)
        # links: internal content links in stripped main
        link_pairs = []
        for href, inner in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', stripped, re.S):
            if href.startswith('/') and not href.startswith('//'):
                link_pairs.append((norm_anchor(clean_html_text(inner)), href.strip('/')))
        doc_links = [(norm_anchor(l['anchor']), l['target']) for l in p['links']
                     if l['kind'] in ('paren', 'run', 'table-bare')]
        doc_set = {}
        for a, t in doc_links:
            doc_set.setdefault(a, set()).add(t)
        ren_set = {}
        for a, t in link_pairs:
            ren_set.setdefault(a, set()).add(t)
        missing = [(a, sorted(ts)) for a, ts in doc_set.items() if a not in ren_set]
        extra = [(a, sorted(ts)) for a, ts in ren_set.items() if a not in doc_set]
        wrong = [(a, sorted(doc_set[a]), sorted(ren_set[a])) for a in doc_set if a in ren_set and doc_set[a] != ren_set[a]]
        own = '/' + slug + '/' if slug else '/'
        self_links = [x for x in link_pairs if ('/' + x[1] + '/') == own or (x[1] == '' and slug == '')]
        broken = [x for x in link_pairs if x[1] not in built_slugs]
        # tables
        doc_tables = []
        for sec in p['sections']:
            for b in sec['blocks']:
                if b['type'] == 'table':
                    doc_tables.append([(len(row), [len(cell) for cell in row]) for row in b['rows']])
        ren_tables = []
        for tm in re.finditer(r'<table[^>]*>(.*?)</table>', stripped, re.S):
            rows = []
            for rm in re.finditer(r'<tr>(.*?)</tr>', tm.group(1), re.S):
                cells = len(re.findall(r'<t[hd][ >]', rm.group(1)))
                rows.append(cells)
            ren_tables.append(rows)
        doc_table_shapes = [[r[0] for r in t] for t in doc_tables]
        tables_ok = (len(doc_tables) == len(ren_tables) and doc_table_shapes == ren_tables)
        # images
        imgs = re.findall(r'<img[^>]+>', main)
        split_imgs = re.findall(r'<figure class="split-fig">(<img[^>]+>)', main)
        hero_imgs = re.findall(r'<div class="hero[^"]*">.*?(<img[^>]+>)', main, re.S)
        bad_alt = [i for i in imgs if not re.search(r'alt="[^"]+"', i)]
        files = [re.search(r'src="([^"]+)"', i).group(1) for i in imgs if re.search(r'src="([^"]+)"', i)]
        dup_files = sorted({f for f in files if files.count(f) > 1})
        missing_files = [f for f in files if not os.path.exists(os.path.join(OUT, f.lstrip('/')))]
        forb = [f for f in ['claude.ai', '945-2118', 'waterdamagerestorationplano.org', 'Tulsa'] if f in h]
        row = {'slug': slug, 'h1_count': len(h1s), 'h1_match': h1_text == [norm_anchor(p['h1'])],
               'miss': miss, 'meta_ok': meta_ok, 'faq_vis': len(faq_vis), 'faq_doc': len(p['faqs']),
               'faq_match': faq_match, 'faq_doc_match': faq_doc_match,
               'links_doc': len(doc_links), 'links_ren': len(link_pairs),
               'links_missing': missing, 'links_extra': extra, 'links_wrong': wrong,
               'self': self_links, 'broken': broken,
               'tables_doc': len(doc_tables), 'tables_ren': len(ren_tables), 'tables_ok': tables_ok,
               'imgs': len(imgs), 'splits': len(split_imgs), 'hero_imgs': len(hero_imgs),
               'bad_alt': len(bad_alt), 'dup_files': dup_files, 'missing_files': missing_files,
               'forb': forb}
        results.append(row)
        print(f"{slug or '/':32} H1={row['h1_count']} match={row['h1_match']} miss={len(miss)} {miss[:8]} "
              f"meta={meta_ok} FAQ={len(faq_vis)}/{len(p['faqs'])} schema={faq_match} doc={faq_doc_match} "
              f"links={len(link_pairs)}/{len(doc_links)} missL={len(missing)} extraL={len(extra)} wrongL={len(wrong)} self={len(self_links)} broken={broken} "
              f"tables={len(ren_tables)}/{len(doc_tables)} ok={tables_ok} imgs={len(imgs)} splits={len(split_imgs)} dup={dup_files} forb={forb}")
    # sitemap
    sm = open(os.path.join(OUT, 'sitemap.xml')).read()
    locs = re.findall(r'<loc>([^<]+)</loc>', sm)
    expected = {'https://waterdamagerestorationplano.online/'} | \
               {f'https://waterdamagerestorationplano.online/{s}/' for s in built_slugs if s}
    print(f"sitemap urls={len(locs)} expected={len(expected)} match={set(locs) == expected} image_entries={sm.count('<image:')}")
    # weights
    idx = {}
    imgdir = os.path.join(BASE, 'public', 'images')
    for f in os.listdir(imgdir):
        idx[f] = os.path.getsize(os.path.join(imgdir, f))
    def served(f, kind):
        stem = f[:-5] if f.endswith('.webp') else f
        if kind == 'hero':
            return idx.get(f'{stem}-800.webp', idx.get(f, 0))
        return idx.get(f'{stem}-400.webp', idx.get(f, 0))
    summ = json.load(open(os.path.join(BASE, 'rebuild-summary.json')))
    wrows = []
    for s in summ:
        hero_b = served(s['hero'], 'hero') if s['hero'] else 0
        split_b = sum(served(e[1], 'split') for e in s['splits'])
        wrows.append({'slug': s['slug'], 'hero_bytes': hero_b, 'splits_bytes': split_b,
                      'content_total': hero_b + split_b})
    json.dump({'pages': results, 'sitemap': {'urls': len(locs), 'match': set(locs) == expected,
                                             'image_entries': sm.count('<image:')},
               'weights': wrows}, open(os.path.join(BASE, 'qa4.json'), 'w'), indent=1)
    tot = sum(w['content_total'] for w in wrows)
    print(f"image weights: total content bytes all pages={tot} avg/page={tot // max(1, len(wrows))}")
    for w in wrows:
        if w['slug'] in ('', 'emergency-water-damage', 'west-plano', 'shut-off-valve', 'about', 'contact'):
            print(f"  weight {w['slug'] or '/':28} hero={w['hero_bytes']} splits={w['splits_bytes']} total={w['content_total']}")

if __name__ == '__main__':
    main()
