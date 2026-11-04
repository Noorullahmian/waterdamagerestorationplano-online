#!/usr/bin/env python3
"""Doc-truth model for the Plano 3 doc-rematch FIX PASS.

Parses the Google Docs API JSON (doc-rematch/doc_api.json) with block
preservation, so the fix pass can render the doc's OWN links and tables
instead of the builder's phrase map (which invented 134 EXTRA links and
dropped 100 MISSING + 24 PARTIAL ones) and instead of dropping tables
(7,719 tokens) entirely.

Per tab (keyed by slug from tabs.json):
  - 'links': non-table doc links in document order. Each: anchor (exact doc
    text), target slug, heading (nearest preceding HEADING para, '' before
    the first heading), in_faq (after the FAQ heading para).
  - 'tables': tables in document order. Each: rows (list of rows; each row
    a list of cells; each cell a list of paras; each para a list of runs
    (text, url_or_None, bold)), heading at table position, prev block
    descriptor for placement: ('para', norm_text) | ('heading', norm_text)
    | ('table', previous_table_index).
  - 'section_headings': normalized headings seen (for orphan detection).

Header skipping mirrors the audit's doc_parse.py: first HEADING_1 is the tab
title, then Meta Title/Description/URL/H1 label paras, then body. The
'Nov ... @Noorullah' byline is skipped. Table cell paras are NOT flattened
into body paras here (unlike doc_parse) — tables keep row/cell structure.
"""
import json, os, re

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
DOC_API = os.path.join(BASE, 'doc-rematch', 'doc_api.json')
TABS_JSON = os.path.join(BASE, 'tabs.json')

def norm(s):
    s = (s or '').replace('\u2014', ' ').replace('\u2013', ' ')
    s = s.replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()

def norm_url(u):
    if not u:
        return None
    u = u.strip()
    u = re.sub(r'^https?://waterdamagerestorationplano\.online', '', u)
    return u.strip('/')

def _walk(elements, blocks):
    """Append ('para', style, runs) / ('table', rows) blocks in order."""
    for el in elements:
        if 'paragraph' in el:
            p = el['paragraph']
            runs = []
            for e in p.get('elements', []):
                tr = e.get('textRun')
                if not tr:
                    continue
                ts = tr.get('textStyle', {}) or {}
                runs.append((tr.get('content', ''),
                             (ts.get('link') or {}).get('url'),
                             bool(ts.get('bold'))))
            style = (p.get('paragraphStyle') or {}).get('namedStyleType', 'NORMAL_TEXT')
            blocks.append(('para', style, runs))
        elif 'table' in el:
            rows = []
            for row in el['table'].get('tableRows', []):
                cells = []
                for cell in row.get('tableCells', []):
                    sub = []
                    _walk(cell.get('content', []), sub)
                    cells.append([b for b in sub if b[0] == 'para'])
                rows.append(cells)
            blocks.append(('table', rows))

def load_truth():
    d = json.load(open(DOC_API))
    tabs_meta = json.load(open(TABS_JSON))
    meta_by_tab = {m['tab']: m for m in tabs_meta}
    doc_slugs = {m.get('slug', '') for m in tabs_meta}
    truth = {}
    for idx, t in enumerate(d['tabs']):
        tab_no = idx + 1
        slug = meta_by_tab.get(tab_no, {}).get('slug', '')
        dt = t['documentTab']
        blocks = []
        _walk(dt['body']['content'], blocks)
        # --- header phase: skip tab title H1 + Meta labels + byline ---
        body_blocks = []
        phase = 'pre'
        for b in blocks:
            if b[0] != 'para':
                if phase == 'body':
                    body_blocks.append(b)
                continue
            style, runs = b[1], b[2]
            text = ''.join(r[0] for r in runs)
            stripped = text.strip()
            if phase == 'pre' and style == 'HEADING_1':
                phase = 'meta'
                continue
            if phase == 'meta':
                m = re.match(r'^(Meta Title|Meta Description|URL|H1):\s*(.*)$', stripped, re.S)
                if m:
                    if m.group(1) == 'H1':
                        phase = 'body'
                    continue
                if stripped.startswith('Nov ') and '@Noorullah' in stripped:
                    continue
                phase = 'body'
            if phase == 'body':
                body_blocks.append(b)
        # --- walk body blocks: headings, faq split, links, tables ---
        links = []
        tables = []
        section_headings = set()
        cur_heading = ''
        faq_idx = None
        for bi, b in enumerate(body_blocks):
            if b[0] == 'para':
                style, runs = b[1], b[2]
                text = ''.join(r[0] for r in runs)
                stripped = text.strip()
                if style.startswith('HEADING'):
                    cur_heading = stripped
                    section_headings.add(norm(stripped))
                if faq_idx is None and re.search(r'FAQs?\s*$', stripped) and len(stripped) < 80:
                    faq_idx = bi
                # merge adjacent same-URL runs into anchor phrases
                cur_url = None
                cur_text = ''
                def flush():
                    nonlocal cur_url, cur_text
                    if cur_url is not None and cur_text.strip():
                        tgt = norm_url(cur_url)
                        if tgt is not None and tgt in doc_slugs:
                            links.append({
                                'anchor': cur_text.strip(),
                                'target': tgt,
                                'heading': norm(cur_heading),
                                'in_faq': faq_idx is not None and bi > faq_idx,
                                'in_table': False,
                            })
                    cur_url = None
                    cur_text = ''
                for (txt, link, _bold) in runs:
                    if link:
                        if cur_url is None:
                            cur_url, cur_text = link, txt
                        elif link == cur_url:
                            cur_text += txt
                        else:
                            flush()
                            cur_url, cur_text = link, txt
                    else:
                        flush()
                flush()
            else:
                # table: find previous non-empty block for placement
                prev = None
                for pb in reversed(body_blocks[:bi]):
                    if pb[0] == 'para':
                        ptxt = ''.join(r[0] for r in pb[2]).strip()
                        if ptxt:
                            if pb[1].startswith('HEADING'):
                                prev = ('heading', norm(ptxt))
                            else:
                                prev = ('para', norm(ptxt))
                            break
                    else:
                        prev = ('table', len(tables) - 1)
                        break
                tables.append({
                    'rows': b[1],
                    'heading': norm(cur_heading),
                    'prev': prev,
                })
        truth[slug] = {
            'links': links,
            'tables': tables,
            'section_headings': section_headings,
        }
    return truth

if __name__ == '__main__':
    tr = load_truth()
    tot_links = sum(len(v['links']) for v in tr.values())
    tot_tables = sum(len(v['tables']) for v in tr.values())
    print(f'tabs={len(tr)} doc_links={tot_links} tables={tot_tables}')
    for slug, v in tr.items():
        print(f'{slug or "(home)":28s} links={len(v["links"]):3d} tables={len(v["tables"])} '
              f'faq_links={sum(1 for l in v["links"] if l["in_faq"])}')
