"""QA1 for Plano 3: checks built out/ HTML per page.
- H1 count, doc-vs-rendered missing words (via gen3 pipeline text),
- FAQ visible count vs FAQPage schema exact match (unescape + whitespace/punct normalisation),
- internal links (count, broken, body self-links), images (count, missing/empty alt),
- forbidden strings (old Plano phone/domain, Tulsa).
Writes qa1.json (list of per-page dicts) and prints one line per page.
Reconstructed 2026-11-04 after /tmp cleanup removed the original script; logic matches
the documented behaviour of the original (same checks, same normalisation).
"""
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen3 import parse_tabs, classify_and_build

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'out')
FORB = ['945-2118', 'waterdamagerestorationplano.org', 'Tulsa', '918)']

def words(t):
    return re.findall(r"[A-Za-z0-9'’\-]+", t.lower())

def clean(x):
    t = re.sub(r'<[^>]+>', ' ', html.unescape(x)).strip()
    return re.sub(r'\s+([,.;:?!])', r'\1', t)

def page_text(sections, faqs):
    parts = []
    for s in sections:
        if s.get('heading'): parts.append(s['heading'])
        for b in s['blocks']:
            if b['type'] == 'para': parts.append(' '.join(t for t, _ in b['segs']))
            elif b['type'] == 'list': parts.extend(b['items'])
            elif b['type'] == 'trust': parts.extend(b['items'])
            elif b['type'] == 'cta': parts.append(b['label'])
            elif b['type'] in ('heading', 'listhead'): parts.append(b['text'])
            elif b['type'] == 'form':
                parts.extend(b.get('fields', []))
                if b.get('note'): parts.append(b['note'])
    for f in faqs:
        parts.append(f['q']); parts.append(f['a'])
    return ' '.join(parts)

tabs = parse_tabs()
# build slug -> rendered html path map
results = []
for tab in tabs:
    slug = tab['slug']
    sections, faqs, _fh, _ = classify_and_build(tab)
    hpath = os.path.join(OUT, slug, 'index.html') if slug else os.path.join(OUT, 'index.html')
    h = open(hpath).read()
    main = re.search(r'<main>(.*?)</main>', h, re.S).group(1)
    visible = re.sub(r'<script.*?</script>', ' ', main, flags=re.S)
    visible_text = html.unescape(re.sub(r'<[^>]+>', ' ', visible))
    doc_words = set(words(page_text(sections, faqs)))
    ren_words = set(words(visible_text))
    miss = sorted(w for w in doc_words if w not in ren_words)
    h1 = len(re.findall(r'<h1[ >]', main))
    faq_items = re.findall(r'<div class="faq-item"><h3>(.*?)</h3><p>(.*?)</p></div>', main, re.S)
    faq_vis = [(clean(q), clean(a)) for q, a in faq_items]
    schema_faq = []
    for sm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: obj = json.loads(sm.group(1))
        except Exception: continue
        if obj.get('@type') == 'FAQPage':
            schema_faq = [(html.unescape(q['name']), html.unescape(q['acceptedAnswer']['text'])) for q in obj['mainEntity']]
    match = (len(faq_vis) == len(schema_faq) and
             all(re.sub(r'\s+', ' ', clean(a)) == re.sub(r'\s+', ' ', sa) and clean(q) == sq
                 for (q, a), (sq, sa) in zip(faq_vis, schema_faq)))
    # links in main
    hrefs = re.findall(r'href="([^"]+)"', main)
    internal = [x for x in hrefs if x.startswith('/') and not x.startswith('//')]
    def route_exists(href):
        p = href.split('#')[0].split('?')[0].strip('/')
        if p == '': return os.path.exists(os.path.join(OUT, 'index.html'))
        return os.path.exists(os.path.join(OUT, p, 'index.html'))
    broken = [x for x in internal if not route_exists(x)]
    # body self-links: link to own slug from body (header/footer exempt: main only here)
    own = '/' + slug + '/' if slug else '/'
    self_links = [x for x in internal if x.rstrip('/') + '/' == own or x == own]
    imgs = re.findall(r'<img[^>]+>', main)
    bad = [i for i in imgs if not re.search(r'alt="[^"]+"', i)]
    forb = [f for f in FORB if f in h]
    row = {'slug': slug, 'h1': h1, 'miss': len(miss), 'miss_words': miss,
           'faqs_vis': len(faq_vis), 'faqs_doc': len(faqs), 'match': match,
           'links': len(internal), 'broken': broken, 'self': self_links,
           'imgs': len(imgs), 'bad': bad, 'forb': forb}
    results.append(row)
    print(f"{slug or '/':32} H1={h1} miss={len(miss)} {miss[:5]} FAQ={len(faq_vis)}/{len(faqs)} match={match} links={len(internal)} broken={broken} self={self_links} imgs={len(imgs)} bad={bad} forb={forb}")
sitemap = open(os.path.join(OUT, 'sitemap.xml')).read()
print('sitemap urls:', len(re.findall(r'<loc>', sitemap)), 'image entries:', sitemap.count('<image:'))
json.dump(results, open(os.path.join(BASE, 'qa1.json'), 'w'), indent=1)
