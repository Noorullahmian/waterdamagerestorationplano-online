#!/usr/bin/env python3
"""Plano 3 generator — fresh code, v2 skeleton only. Parses extracted.txt, renders Next.js app.
Phone/domain ONLY from plano3 doc: (972) 472-7917, waterdamagerestorationplano.online
Never the old .org phone/domain. No Tulsa files/text/phone/images/colours copied.
"""
import re, os, json, html, sys
BASE = os.path.expanduser('~/workspace/plano3-water-damage')
PHONE = '(972) 472-7917'
TEL = 'tel:+19724727917'
DOMAIN = 'https://waterdamagerestorationplano.online'
BRAND = 'Water Damage Restoration Plano'

# ---------- link map: phrase (lower) -> slug ('' = home) ----------
LINK_PHRASES = [
    ('24/7 emergency water damage cleanup in plano', 'emergency-water-damage'),
    ('24/7 emergency water damage cleanup', 'emergency-water-damage'),
    ('standing water extraction in plano', 'water-extraction'),
    ('water extraction in plano', 'water-extraction'),
    ('water extraction', 'water-extraction'),
    ('structural drying in plano', 'structural-drying'),
    ('structural drying', 'structural-drying'),
    ('burst pipe water damage cleanup', 'burst-pipe-cleanup'),
    ('burst pipe cleanup', 'burst-pipe-cleanup'),
    ('sewage backup cleanup', 'sewage-cleanup'),
    ('sewage cleanup', 'sewage-cleanup'),
    ('slab leak water damage in plano', 'slab-leak'),
    ('slab leak water damage', 'slab-leak'),
    ('slab leak', 'slab-leak'),
    ('water heater leak cleanup', 'water-heater-leak'),
    ('water heater leak', 'water-heater-leak'),
    ('ac overflow water damage cleanup', 'ac-overflow'),
    ('ac overflows', 'ac-overflow'),
    ('ac overflow cleanup', 'ac-overflow'),
    ('ac overflow', 'ac-overflow'),
    ('ceiling leak water damage', 'ceiling-leak'),
    ('ceiling leak', 'ceiling-leak'),
    ('flood cleanup in plano', 'flood-cleanup'),
    ('flood cleanup', 'flood-cleanup'),
    ('hardwood floor drying', 'hardwood-floor-drying'),
    ('commercial water damage restoration', 'commercial-water-damage'),
    ('wall cavity drying', 'wall-drying'),
    ('wall drying', 'wall-drying'),
    ('plano main water shut-off valve guide', 'shut-off-valve'),
    ('where to find the main shut-off in a plano home', 'shut-off-valve'),
    ('where your plano shut-off valve is', 'shut-off-valve'),
    ('where to find your plano shut-off valve', 'shut-off-valve'),
    ('shut-off valve guide', 'shut-off-valve'),
    ('safety steps for a sagging wet ceiling', 'sagging-ceiling'),
    ('sagging ceiling guide', 'sagging-ceiling'),
    ('why household fans won\'t dry wet walls and carpet', 'fans-wont-dry-walls'),
    ('fans won\'t dry walls', 'fans-wont-dry-walls'),
    ('water damage restoration in east plano', 'east-plano'),
    ('east plano water damage', 'east-plano'),
    ('east plano', 'east-plano'),
    ('central plano water damage', 'central-plano'),
    ('central plano', 'central-plano'),
    ('north plano water damage', 'north-plano'),
    ('north plano', 'north-plano'),
    ('west plano', 'west-plano'),
    ('legacy west area', 'legacy-west'),
    ('legacy west', 'legacy-west'),
    ('murphy, parker & wylie', 'murphy'),
    ('water damage restoration in plano', ''),
    ('water damage restoration plano', ''),
    ('appliance leak cleanup', 'appliance-leak'),
    ('warm spot on floor guide', 'warm-spot-on-floor'),
    ('cost guide', 'water-damage-cost'),
    ('insurance guide', 'water-damage-insurance-texas'),
    ('about us', 'about'),
    ('water damage cost', 'water-damage-cost'),
    ('cabinet drying', 'cabinet-drying'),
    ('laundry overflow cleanup', 'laundry-overflow'),
    ('laundry overflow', 'laundry-overflow'),
    ('frisco', 'frisco'),
    ('allen', 'allen'),
    ('mckinney', 'mckinney'),
    ('richardson', 'richardson'),
    ('murphy', 'murphy'),
    ('texas water damage insurance guide', 'water-damage-insurance-texas'),
    ('mold clock guide', 'mold-after-water-damage'),
    ('mold clock', 'mold-after-water-damage'),
    ('fans won\'t dry walls', 'fans-wont-dry-walls'),
    ('attic insulation removal', 'attic-insulation-drying'),  # Round 3 re-view: moisture hidden-leaks bullet 5 "See attic insulation removal." rendered unlinked; self-suppressed on the attic page itself by render_seg_text
]
LINK_PHRASES.sort(key=lambda x: -len(x[0]))

def clean_text(s):
    s = s.replace('\u2014', ' ').replace('\u2013', ' ').replace('\u2019', "'")
    s = re.sub(r'\s+([,.;:?!%)])', r'\1', s)
    s = re.sub(r'([(])\s+', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()

def is_phone(s):
    return bool(re.fullmatch(r'\(?\d{3}\)?\s*\d{3}[- ]\d{4}', s.strip()))

def is_bracket_cta(s):
    return bool(re.match(r'^\[(Call|Tap to Call).*?\]$', s.strip()))

def cta_label(s):
    m = re.match(r'^\[(.*?):\s*\(?\d', s.strip())
    return m.group(1) if m else 'Call Now'

def phrase_target(line):
    """If a whole line is a link phrase/title, return slug or None."""
    t = line.strip().lower().rstrip('.')
    # exact title match first via LINK_PHRASES
    for phrase, slug in LINK_PHRASES:
        if t == phrase:
            return slug
    return None

def parse_tabs():
    raw = open(os.path.join(BASE, 'extracted.txt')).read()
    parts = re.split(r'===== TAB (\d+) =====', raw)
    tabs = []
    for i in range(1, len(parts), 2):
        num = int(parts[i]); c = parts[i+1]
        lines = [l.rstrip() for l in c.splitlines()]
        # header block
        title = ''
        meta_title = ''; meta_desc = ''; slug = ''; h1 = ''
        idx = 0
        for j, l in enumerate(lines):
            s = l.strip()
            if s and not title:
                title = s
            if s == 'Meta Title:':
                meta_title = lines[j+1].strip() if j+1 < len(lines) else ''
            if s == 'Meta Description:':
                meta_desc = lines[j+1].strip() if j+1 < len(lines) else ''
            if s == 'URL:':
                u = lines[j+1].strip() if j+1 < len(lines) else ''
                slug = u.replace('waterdamagerestorationplano.online', '').strip('/').strip()
            if s == 'H1:':
                h1 = lines[j+1].strip() if j+1 < len(lines) else ''
                idx = j + 2
                break
        body = [l for l in lines[idx:] if l.strip() != '']
        tabs.append({'tab': num, 'title': title, 'meta_title': meta_title,
                     'meta_desc': meta_desc, 'slug': slug, 'h1': h1, 'lines': body})
    return tabs

def classify_and_build(tab):
    """Turn raw lines into blocks, preserving every content word in order.
    Block types: para, heading2, heading3, cta, trust, list, faq (handled separately), form (contact only)
    Returns (intro_blocks, sections, faqs, raw_words)
    """
    lines = tab['lines']
    slug = tab['slug']
    # --- special: contact form section ---
    # We keep form field names as form UI labels; the instruction lines
    # 'Form fields:' / ' button' / 'Line under the button:' are NOT rendered as text.
    filtered = []
    i = 0
    form_fields = []
    form_note = ''
    while i < len(lines):
        s = lines[i].strip()
        if s == 'Form fields:':
            j = i + 1
            while j < len(lines) and lines[j].strip() not in ('[Send Message]',) and not lines[j].strip().endswith('button'):
                # field names may span 2 lines (e.g. 'Type of property: house, ...' is one line)
                form_fields.append(lines[j].strip())
                j += 1
            # skip the '[Send Message]' + ' button' lines; form will render its own button
            i = j
            while i < len(lines) and (lines[i].strip() == '[Send Message]' or lines[i].strip() == 'button'):
                i += 1
            continue
        if s == 'Line under the button:':
            form_note = lines[i+1].strip() if i+1 < len(lines) else ''
            # form_note is content (the sentence after), keep it as a para later via form block
            i += 2
            continue
        filtered.append(lines[i])
        i += 1
    lines = filtered

    # --- split FAQ section ---
    faq_start = None
    for k, l in enumerate(lines):
        if re.search(r'FAQs?\s*$', l.strip()) and len(l.strip()) < 80:
            faq_start = k
            break
    faq_heading = None
    faqs = []
    main_lines = lines
    if faq_start is not None:
        faq_heading = lines[faq_start].strip()
        main_lines = lines[:faq_start]
        rest = lines[faq_start+1:]
        # FAQ pairs: Q ends with ?, answer = following lines until next Q.
        # Final CTA block: last bracket CTA + preceding para/heading are NOT faq;
        # detect: find last bracket line in rest; the block before it that is a
        # paragraph (not Q) is CTA — but if that paragraph is an answer to last Q,
        # keeping it in the answer is still schema-exact, so we simply stop FAQ
        # pairing when we hit a line that looks like a final CTA heading:
        # a line containing 'Call (972)' and not ending with '?'.
        cur_q = None; cur_a = []
        post_faq = False
        for ri, l in enumerate(rest):
            s = l.strip()
            nxt_r = rest[ri+1].strip() if ri+1 < len(rest) else None
            if post_faq:
                main_lines.append(s)
                continue
            # Final CTA heading after the last FAQ answer: a short heading-like
            # line followed by a paragraph (not a question) ends the FAQ section.
            # Also: any line containing the call phone that follows an answer and
            # is itself followed by a paragraph is the final CTA heading, even
            # if it ends with a period (e.g. 'Get the Water Out... Call (972)...').
            if cur_q is not None and 'Call (972)' in s and nxt_r and len(nxt_r) > 30 and not nxt_r.endswith('?'):
                faqs.append({'q': cur_q, 'a': clean_text(' '.join(cur_a))})
                cur_q = None; cur_a = []
                post_faq = True
                main_lines.append(s)
                continue
            if cur_q is not None and len(s) < 90 and not s.endswith('?') and not s.endswith('.') \
               and nxt_r and len(nxt_r) > 50 and not nxt_r.endswith('?') and s[0].isupper():
                faqs.append({'q': cur_q, 'a': clean_text(' '.join(cur_a))})
                cur_q = None; cur_a = []
                post_faq = True
                main_lines.append(s)
                continue
            if is_bracket_cta(s):
                if cur_q:
                    faqs.append({'q': cur_q, 'a': clean_text(' '.join(cur_a))})
                    cur_q = None; cur_a = []
                # bracket CTA after FAQ: treat as trailing CTA block in main flow
                main_lines.append(s)
                continue
            if s.endswith('?') and len(s) < 140 and cur_q is None:
                cur_q = s; cur_a = []
                continue
            if s.endswith('?') and len(s) < 140 and cur_q is not None:
                faqs.append({'q': cur_q, 'a': clean_text(' '.join(cur_a))})
                cur_q = s; cur_a = []
                continue
            if cur_q is not None:
                # phone/link fragments join the answer
                cur_a.append(s)
            else:
                # post-FAQ non-Q text (final CTA heading/para) -> main flow
                main_lines.append(s)
        if cur_q:
            faqs.append({'q': cur_q, 'a': clean_text(' '.join(cur_a))})

    # --- build blocks from main_lines ---
    blocks = []  # each: dict
    cur_para = []  # list of (text, link_slug_or_None) segments
    def flush_para():
        nonlocal cur_para
        if cur_para:
            blocks.append({'type': 'para', 'segs': cur_para})
            cur_para = []
    def is_heading_candidate(s, next_s):
        if len(s) > 85: return False
        if s.endswith('.') or s.endswith('!') or s.endswith('?'): return False
        if is_phone(s) or is_bracket_cta(s): return False
        if phrase_target(s) is not None: return False
        if s.lower().startswith(('call ', 'done?', 'back to', 'see ')): return False
        if s.lower() in ('call', 'see'): return False
        # Sentence fragment ending ". Call" followed by the phone number is
        # the sentence itself ("...counts. Call" + "(972)..."), not a heading.
        # (A plain imperative like "Leave the room and call" stays a heading.)
        if re.search(r'\.\s+Call$', s) and next_s and is_phone(next_s): return False
        if not s[0].isupper(): return False
        # Sentence fragment: next line starts lowercase -> this line continues it.
        if next_s and next_s[0].islower(): return False
        # Continuation starting with a comma (", through clear, local guides...")
        # belongs to this line's sentence, so this line is NOT a heading.
        if next_s and next_s[0] == ',': return False
        # a heading is followed by a paragraph, a lead-in (ends .), a list, or another heading
        if next_s is None: return True
        if len(next_s) < 85 and not next_s.endswith('.'):
            return True  # another heading-like line follows
        return True
    def list_like_para(segs):
        # A para made only of short phrases + 'and'/',' joiners (the about/
        # contact service lists) is a list, not a sentence para. A heading
        # may follow it only when the next line is a real sentence.
        content = [t for t, _ in segs if t not in ('and', ',', ', ')]
        return len(content) >= 3 and all(len(t) < 45 and not t.endswith('.') for t in content)
    k = 0
    pending_lead = None
    while k < len(main_lines):
        s = main_lines[k].strip()
        nxt = main_lines[k+1].strip() if k+1 < len(main_lines) else None
        # A lone ':' line is a separator left when a "Name: description" line
        # was split into a heading + body — it carries no words, drop it so
        # no section body ever starts with a stray colon.
        if s == ':':
            k += 1; continue
        if is_bracket_cta(s):
            flush_para()
            blocks.append({'type': 'cta', 'label': cta_label(s)})
            k += 1; continue
        if '·' in s and len(s) < 200 and s.count('·') >= 3:
            flush_para()
            parts = [p.strip() for p in s.split('·') if p.strip()]
            blocks.append({'type': 'trust', 'items': parts})
            k += 1; continue
        # link-phrase line: attach to current para (or start a para that is just the link)
        tgt = phrase_target(s)
        if tgt is not None:
            if cur_para:
                cur_para.append((s, tgt))
            else:
                # standalone link line after a heading/para break: treat as link para
                cur_para.append((s, tgt))
            k += 1; continue
        if s == '.':
            if cur_para:
                cur_para.append(('.', None))
            k += 1; continue
        if is_phone(s):
            if cur_para:
                cur_para.append((s, None))
            else:
                cur_para.append((s, None))
            k += 1; continue
        # colon-introduced list: line ends with ':' and following lines are short items
        if s.endswith(':') and nxt and len(nxt) < 100 and not nxt.endswith('.'):
            flush_para()
            items = []
            j = k + 1
            while j < len(main_lines):
                it = main_lines[j].strip()
                # An indented line in the doc is a CONTINUATION of the
                # previous item (e.g. " a ladder, moving box..." belongs to
                # "Accidental impact:"), never a new item and never a reason
                # to end the list — the old code broke the list here whenever
                # the continuation ran past 100 chars (fire-sprinkler list).
                if items and (main_lines[j].startswith(' ') or main_lines[j].startswith('\t')):
                    items[-1] = items[-1] + ' ' + it
                    j += 1
                    continue
                if len(it) >= 100 or it.endswith('.') and len(it) > 90:
                    break
                if is_heading_candidate(it, main_lines[j+1].strip() if j+1 < len(main_lines) else None) and len(it) < 85 and not it.startswith(',') and not it.startswith('and '):
                    # A new section heading ends the list — unless the next line
                    # is a list continuation (starts with ',' / 'and ' / 'plus ').
                    nxt2 = main_lines[j+1].strip() if j+1 < len(main_lines) else ''
                    if nxt2 and not nxt2.startswith((',', 'and ', 'plus ')):
                        break
                items.append(it)
                j += 1
                # continuation lines starting with ',' or 'and ' or 'plus ' join previous item
                while j < len(main_lines) and (main_lines[j].strip().startswith(',') or main_lines[j].strip().startswith('and ') or main_lines[j].strip().startswith('plus ')):
                    items[-1] = items[-1] + ' ' + main_lines[j].strip()
                    j += 1
            if items:
                blocks.append({'type': 'listhead', 'text': s})
                blocks.append({'type': 'list', 'items': items})
                k = j; continue
        # Contact: the "Send Us a Message" intro heading duplicates the form
        # section's heading (appended at the end). Demote the intro instance
        # to paragraph copy so the page has a single form heading, with the
        # form directly under it. No words change.
        if slug == 'contact' and s == 'Send Us a Message (Non-Emergency)':
            # Round 5 (AUTHORIZED duplicate strip): the old code appended
            # the heading string itself as the intro para's first seg, so
            # the paragraph under the form H2 repeated the H2 verbatim.
            # Do NOT append it — the para now begins 'Use this form…'
            # and the string survives once, as the form H2. (i7) below
            # also strips a leading heading seg if one ever appears.
            flush_para()
            k += 1; continue
        # Heading triggers only after a completed sentence/heading (never mid-sentence).
        last_ended = False
        if cur_para:
            last_txt = cur_para[-1][0]
            last_ended = last_txt.endswith(('.', '?', '!', ':'))
        # A line followed by a lone ':' line is a "Name: description" split
        # (area "Most Requested" lists), NOT a section heading — the ':' line
        # itself is dropped, so heading-ising the name would orphan it as a
        # false H2 section (allen "Commercial water damage" did exactly this).
        if nxt != ':' and is_heading_candidate(s, nxt) and (not cur_para or last_ended or (list_like_para(cur_para) and nxt and (len(nxt) > 50 or nxt.endswith('.')))):
            flush_para()
            blocks.append({'type': 'heading', 'text': s})
            k += 1; continue
        # Bare-phrase lead + indented continuation pairs form a list, not a
        # run-on paragraph (laundry "What Usually Fails": "Rubber supply
        # hoses" / " that crack after 5+ years", ...). Narrow rule so normal
        # bold-lead paragraphs are untouched: lead has no trailing
        # punctuation and no colon, is short, and its continuation starts
        # lowercase; 2+ such pairs are required, else normal para behaviour.
        _raw_next = main_lines[k+1] if k+1 < len(main_lines) else ''
        if (not cur_para and s and s[0].isupper() and len(s) < 60
                and not s.endswith(('.', ':', '!', '?')) and ':' not in s
                and _raw_next.startswith(' ') and nxt and nxt[0].islower()):
            _pairs = []
            _j = k
            while _j < len(main_lines):
                _lead = main_lines[_j].strip()
                _rn = main_lines[_j+1] if _j+1 < len(main_lines) else ''
                _nn = main_lines[_j+1].strip() if _j+1 < len(main_lines) else ''
                if (not _lead or not _lead[0].isupper() or len(_lead) >= 60
                        or _lead.endswith(('.', ':', '!', '?')) or ':' in _lead
                        or not _rn.startswith(' ') or not _nn or not _nn[0].islower()):
                    break
                _item = _lead
                _j += 1
                while _j < len(main_lines) and main_lines[_j].startswith(' '):
                    _item += ' ' + main_lines[_j].strip()
                    _j += 1
                _pairs.append(_item)
            if len(_pairs) >= 2:
                blocks.append({'type': 'list', 'items': _pairs})
                k = _j; continue
        # ordinary paragraph line (may be lead-in or continuation).
        # An indented line is a CONTINUATION of the previous segment (doc
        # line " water damage" completes "fire sprinkler"), not a new
        # segment — join it, unless it is a joiner ('and'/','), which must
        # stay its own segment for list grouping, or the previous segment
        # is a link (never extend a link anchor).
        _raw = main_lines[k]
        if (cur_para and (_raw.startswith(' ') or _raw.startswith('\t'))
                and s not in ('and',) and not s.startswith('and ') and not s.startswith(',')
                and cur_para[-1][1] is None):
            _pt, _tg = cur_para[-1]
            cur_para[-1] = (_pt.rstrip() + ' ' + s, _tg)
        else:
            cur_para.append((s, None))
        k += 1
    flush_para()

    # group blocks into sections: heading starts a new section
    sections = []
    cur = {'heading': None, 'blocks': []}
    for b in blocks:
        if b['type'] == 'heading':
            if cur['blocks'] or cur['heading'] is not None:
                sections.append(cur)
            cur = {'heading': b['text'], 'blocks': []}
        else:
            cur['blocks'].append(b)
    sections.append(cur)
    # Post-process: empty sections are either a parent heading (single empty
    # section before a content section) or a bullet list (run of empty sections).
    merged = []
    i = 0
    while i < len(sections):
        if sections[i]['blocks'] or sections[i]['heading'] is None:
            merged.append(sections[i]); i += 1; continue
        # run of empty sections
        j = i
        while j < len(sections) and not sections[j]['blocks'] and sections[j]['heading'] is not None:
            j += 1
        run = sections[i:j]
        if len(run) == 2 and j < len(sections):
            # A run of exactly 2 empty headings is a heading + subheading,
            # not a one-bullet list (that rendered as a truncated section).
            merged.append({'heading': run[0]['heading'],
                           'blocks': [{'type': 'subhead', 'text': run[1]['heading']}]})
            i = j; continue
        if len(run) >= 2 and j < len(sections):
            merged.append({'heading': run[0]['heading'],
                           'blocks': [{'type': 'list', 'items': [r['heading'] for r in run[1:]]}]})
            i = j; continue
        if len(run) == 1 and j < len(sections):
            nxt = dict(sections[j]); nxt['parent'] = run[0]['heading']
            merged.append(nxt); i = j + 1; continue
        merged.extend(run); i = j
    sections = merged
    # City/area enumerations (short items after a ':' listhead) read as a
    # sentence, not bullets: convert to a paragraph with link segments.
    for sec in sections:
        new_blocks = []
        for b in sec['blocks']:
            if b['type'] == 'list' and len(b['items']) >= 3 and all(len(it) < 45 for it in b['items']) \
               and sum(1 for it in b['items'] if phrase_target(it.rstrip(',').strip()) is not None) >= 2:
                segs = []
                para_after = None
                for it in b['items']:
                    t = it.strip()
                    if t.startswith('.'):
                        para_after = t.lstrip('. ').strip()
                        continue
                    t2 = t.rstrip(',').strip()
                    # 'Richardson, and' / 'West Plano (75093) and' -> the 'and'
                    # belongs before the next city and is a DOC WORD: keep it
                    # as its own segment (DOC-REMATCH FIX: the old code
                    # dropped it and always inserted a comma). Emit ', '
                    # only when the original item had a comma before 'and'.
                    if t2.endswith(' and'):
                        base = t2[:-4].strip()
                        had_comma = base.endswith(',')
                        base = base.rstrip(',').strip()
                        segs.append((base, phrase_target(base)))
                        if had_comma:
                            segs.append((', ', None))
                        segs.append(('and', None))
                        continue
                    tgt = phrase_target(t2)
                    segs.append((t2, tgt))
                    segs.append((', ', None))
                if segs:
                    # replace trailing comma segment with a period
                    if segs and segs[-1][0] == ', ':
                        segs[-1] = ('.', None)
                    new_blocks.append({'type': 'para', 'segs': segs})
                    if para_after:
                        new_blocks.append({'type': 'para', 'segs': [(para_after, None)]})
                    continue
            new_blocks.append(b)
        sec['blocks'] = new_blocks
    # --- post-process: rejoin fragments the doc split across lines ---
    # The doc itself breaks sentences at links ("See" / link phrase / "."),
    # at conjunctions ("and"), and at commas/colons. Rejoining them is a
    # layout/markup fix only: no word is added, removed, or reordered.
    def join_items(items):
        out = []
        idx = 0
        while idx < len(items):
            t = items[idx].strip()
            # Stray leading dot on a trailing sentence (home cities list:
            # ". If your address is in Plano...") — the dot is punctuation
            # debris, not a bullet; keep the sentence, drop the dot.
            if t.startswith('. '):
                t = t[2:].strip()
            # Orphan "see" item (ceiling-dripping source list): the 'see'
            # belongs to the following item ("see AC overflow cleanup.").
            if t.lower() == 'see' and idx + 1 < len(items):
                nxt_it = items[idx + 1].strip()
                if nxt_it.startswith('. '):
                    nxt_it = nxt_it[2:].strip()
                out.append(clean_text('see ' + nxt_it))
                idx += 2
                continue
            if t in ('', '.', '•', '·'):
                if out:
                    out[-1] = out[-1].rstrip() + '.'
                idx += 1
                continue
            if out and t == 'and':
                out[-1] = out[-1].rstrip() + ' and'
                idx += 1
                continue
            if out and t.startswith('and '):
                out[-1] = out[-1].rstrip() + ' ' + t
                idx += 1
                continue
            if out and t.startswith(','):
                out[-1] = out[-1].rstrip() + t
                idx += 1
                continue
            if out and out[-1].rstrip().endswith('See'):
                out[-1] = out[-1].rstrip() + ' ' + t
                idx += 1
                continue
            if out and t and t[0].islower() and not out[-1].rstrip().endswith(('.', '?', '!')):
                # Continuation line ("with timestamps, ...", "photographed ...")
                # belonging to the previous list item's sentence.
                out[-1] = out[-1].rstrip() + ' ' + t
                idx += 1
                continue
            out.append(t)
            idx += 1
        return [clean_text(x) for x in out if x.strip()]
    for sec in sections:
        new_blocks = []
        for b in sec['blocks']:
            if b['type'] == 'list':
                b = dict(b, items=join_items(b['items']))
                if not b['items']:
                    continue
                new_blocks.append(b)
                continue
            if b['type'] == 'para' and b['segs']:
                first = b['segs'][0][0]
                if first.startswith(',') and new_blocks:
                    # Fragment belonging to the previous list item / para.
                    frag = ' '.join(t for t, _ in b['segs'])
                    prev = new_blocks[-1]
                    if prev['type'] == 'list' and prev['items']:
                        prev = dict(prev, items=prev['items'][:-1] + [prev['items'][-1].rstrip() + frag])
                        new_blocks[-1] = prev
                    elif prev['type'] == 'para':
                        prev = dict(prev, segs=prev['segs'] + b['segs'])
                        new_blocks[-1] = prev
                    continue
                if first.startswith(',') and sec.get('heading'):
                    # Only a SHORT comma fragment may join its heading (a
                    # split heading phrase). A long fragment is body copy
                    # (about "Understand exactly..." was 78 chars and became
                    # a giant H2) — keep it as a paragraph instead.
                    frag = ' '.join(t for t, _ in b['segs'])
                    if len(frag) < 60:
                        sec['heading'] = sec['heading'].rstrip() + frag
                        continue
                    new_blocks.append(b)
                    continue
                if first.startswith(':'):
                    # Stray leading colon left by a heading/body split.
                    segs = [(first.lstrip(':').strip(), b['segs'][0][1])] + b['segs'][1:]
                    segs = [sg for sg in segs if sg[0]]
                    if segs:
                        new_blocks.append(dict(b, segs=segs))
                    continue
                if first.startswith(','):
                    segs = [(first.lstrip(',').strip().capitalize(), b['segs'][0][1])] + b['segs'][1:]
                    new_blocks.append(dict(b, segs=[sg for sg in segs if sg[0]]))
                    continue
            new_blocks.append(b)
        sec['blocks'] = new_blocks
    # Detached "See <link>" at a list end: the doc breaks "See <link phrase>"
    # across lines, so the link phrase lands as its own paragraph after the
    # list (ceiling-dripping crew/source lists, copper repair list). Rejoin
    # it into the final bullet; the renderer links the phrase there.
    for sec in sections:
        merged_blocks = []
        bi = 0
        blks = sec['blocks']
        while bi < len(blks):
            b = blks[bi]
            if (b['type'] == 'list' and bi + 1 < len(blks) and blks[bi + 1]['type'] == 'para'
                    and b['items'] and b['items'][-1].rstrip().endswith(('See', 'see'))
                    and blks[bi + 1]['segs'] and blks[bi + 1]['segs'][0][1] is not None):
                link_text = blks[bi + 1]['segs'][0][0]
                b = dict(b, items=b['items'][:-1] + [b['items'][-1].rstrip() + ' ' + link_text])
                rest = blks[bi + 1]['segs'][1:]
                if rest and rest[0][0] == '.':
                    rest = rest[1:]
                merged_blocks.append(b)
                if rest:
                    merged_blocks.append(dict(blks[bi + 1], segs=rest))
                bi += 2
                continue
            merged_blocks.append(b)
            bi += 1
        sec['blocks'] = merged_blocks
    # --- Round 3 post-processing: rejoin parser fragments without
    # touching any word (layout/markup only). Each fix is verified per
    # instance after rebuild; the gates (word-diff 0) must stay green.
    def _join_segs(segs):
        out = ''
        for t, _tg in segs:
            if t in ('.', ',', ', '):
                out += t
            elif out:
                out += ' ' + t
            else:
                out = t
        return re.sub(r'\s+([,.;:?!])', r'\1', out).strip()
    # (a) Fragmented neighborhood area lists (slab-leak, flood-cleanup):
    # the doc breaks each neighborhood across lines (label / description /
    # "See" / link) and the parser promoted descriptions to H2s with
    # detached links. Re-chunk the region's text at area labels into one
    # bullet per neighborhood.
    _AREA_LABEL = re.compile(r'(East|Central|North|West) Plano \(\d{5}(?:, \d{5})?\):')
    _si = 0
    while _si < len(sections):
        _sec = sections[_si]
        _has_area_list = False
        for _b in _sec['blocks']:
            if _b['type'] == 'list' and _b['items'] and any('Neighborhood' in _it or 'Storm Water' in _it for _it in _b['items']):
                _has_area_list = True
                break
        if not _has_area_list:
            _si += 1
            continue
        _region = [_sec]
        _j = _si + 1
        while _j < len(sections):
            _ns = sections[_j]
            _h = _ns['heading'] or ''
            if 'Cost' in _h:
                break
            if _h.endswith(' See') or _h.endswith(':') or (_ns.get('parent') or '').endswith(':') or any(_b['type'] == 'listhead' for _b in _ns['blocks']):
                _region.append(_ns)
                _j += 1
                continue
            break
        if len(_region) < 2:
            _si += 1
            continue
        _parts = []
        for _ri, _rs in enumerate(_region):
            if _rs.get('parent'):
                _parts.append(_rs['parent'])
            # The first region section's heading is the section title
            # itself (kept as the section heading); later sections'
            # headings are list content (labels / descriptions).
            if _ri > 0 and _rs['heading']:
                _parts.append(_rs['heading'])
            for _b in _rs['blocks']:
                if _b['type'] == 'listhead':
                    _parts.append(_b['text'])
                elif _b['type'] == 'list':
                    _parts.extend(_b['items'])
                elif _b['type'] == 'para':
                    _parts.append(_join_segs(_b['segs']))
        _joined = re.sub(r'\s+', ' ', re.sub(r'\s+([,.;:?!])', r'\1', ' '.join(_parts))).strip()
        _labels = list(_AREA_LABEL.finditer(_joined))
        if not _labels:
            _si += 1
            continue
        _title = _joined[:_labels[0].start()].strip()
        _bullets = []
        for _li, _lm in enumerate(_labels):
            _end = _labels[_li + 1].start() if _li + 1 < len(_labels) else len(_joined)
            _bullets.append(_joined[_lm.start():_end].strip())
        sections[_si:_j] = [{'heading': _sec['heading'],
                             'blocks': [{'type': 'listhead', 'text': _title},
                                        {'type': 'list', 'items': _bullets}]}]
        _si += 1
    # (b) A heading ending in " See" whose only block is a link paragraph
    # is a split sentence, not a section (contact "Extraction and drying
    # begin the same visit. See" + link). Merge into one paragraph.
    for _sec in sections:
        if (_sec['heading'] and _sec['heading'].rstrip().endswith(' See')
                and _sec['blocks'] and _sec['blocks'][0]['type'] == 'para'
                and _sec['blocks'][0]['segs'] and _sec['blocks'][0]['segs'][0][1] is not None):
            _sec['blocks'] = [{'type': 'para', 'segs': [(_sec['heading'], None)] + _sec['blocks'][0]['segs']}] + _sec['blocks'][1:]
            _sec['heading'] = None
    # (c) List whose last item dangles at "and" with the link paragraph
    # detached after it (moisture-mapping hidden leaks). Rejoin the link
    # into the last item, then re-chunk the remaining paragraph segments
    # into list items at sentence ends.
    for _sec in sections:
        _blks = _sec['blocks']
        for _bi in range(len(_blks) - 1):
            _lb, _pb = _blks[_bi], _blks[_bi + 1]
            if (_lb['type'] == 'list' and _pb['type'] == 'para' and _lb['items']
                    and _lb['items'][-1].rstrip().endswith(' and')
                    and _pb['segs'] and _pb['segs'][0][1] is not None):
                _items = _lb['items'][:-1] + [_lb['items'][-1].rstrip() + ' ' + _pb['segs'][0][0] + '.']
                _cur = []
                for _t, _tg in _pb['segs'][1:]:
                    if _t == '.':
                        if _cur:
                            _items.append(_join_segs(_cur) + '.')
                            _cur = []
                        continue
                    _cur.append((_t, _tg))
                if _cur:
                    _items.append(_join_segs(_cur))
                _sec['blocks'] = _blks[:_bi] + [{'type': 'list', 'items': _items}] + _blks[_bi + 2:]
                break
    # (d) Numbered factor swallowed into a preceding bullet list
    # (water-damage-cost factor 3). Lift it out as a subheading and split
    # the following paragraph at the next numbered factor.
    for _sec in sections:
        _blks = _sec['blocks']
        for _bi in range(len(_blks) - 1):
            _lb, _pb = _blks[_bi], _blks[_bi + 1]
            if (_lb['type'] == 'list' and _pb['type'] == 'para'
                    and any(re.match(r'^\d+\. ', _it) for _it in _lb['items'])):
                _idx = next(_i for _i, _it in enumerate(_lb['items']) if re.match(r'^\d+\. ', _it))
                _num_at = next((_k for _k, (_t, _tg) in enumerate(_pb['segs']) if re.match(r'^\d+\. ', _t)), None)
                if _num_at is None:
                    continue
                _factor = _lb['items'][_idx]
                _new_blks = _blks[:_bi]
                if _lb['items'][:_idx] + _lb['items'][_idx + 1:]:
                    _new_blks.append({'type': 'list', 'items': _lb['items'][:_idx] + _lb['items'][_idx + 1:]})
                _new_blks.append({'type': 'subhead', 'text': _factor})
                _new_blks.append({'type': 'para', 'segs': _pb['segs'][:_num_at]})
                _new_blks.append({'type': 'subhead', 'text': _pb['segs'][_num_at][0]})
                if _pb['segs'][_num_at + 1:]:
                    _new_blks.append({'type': 'para', 'segs': _pb['segs'][_num_at + 1:]})
                _new_blks.extend(_blks[_bi + 2:])
                _sec['blocks'] = _new_blks
                break
    # (e) List-tail items promoted to headings (cabinet-drying bullet 5,
    # fans-wont-dry-walls 6th sign). Fold the heading back into the
    # previous list; the fans closing sentence stays a paragraph.
    _TAIL = {'Fridge ice-maker lines behind the island': 'item',
             'Allergy symptoms that seem worse in one room': 'closing',
             # Round 5: list tails promoted to H2 with a closing para + a
             # trailing Call button (mold symptom, insurance drip). Same
             # 'closing' semantics: heading becomes a list item, the
             # closing para and button stay after the list, in order.
             'Allergy-like symptoms in one area of the house': 'closing',
             'Letting a slow drip continue after you notice it': 'closing'}
    _si = 0
    while _si < len(sections) - 1:
        _cur_s, _nxt_s = sections[_si], sections[_si + 1]
        _nxt_blks = _nxt_s['blocks']
        _tail_ok = (_cur_s['blocks'] and _cur_s['blocks'][-1]['type'] == 'list'
                and _nxt_s['heading'] in _TAIL
                and _nxt_blks and _nxt_blks[0]['type'] == 'para'
                and all(_b['type'] == 'cta' for _b in _nxt_blks[1:]))
        if _tail_ok and (_TAIL[_nxt_s['heading']] == 'closing' or len(_nxt_blks) == 1):
            _lst = dict(_cur_s['blocks'][-1])
            _lst['items'] = _lst['items'] + [_nxt_s['heading']]
            if _TAIL[_nxt_s['heading']] == 'closing':
                _cur_s['blocks'] = _cur_s['blocks'][:-1] + [_lst] + _nxt_blks
            else:
                _lst['items'] = _lst['items'] + [_join_segs(_nxt_blks[0]['segs'])]
                _cur_s['blocks'] = _cur_s['blocks'][:-1] + [_lst]
            del sections[_si + 1]
            continue
        _si += 1
    # (f) Split-sentence headings demoted to paragraph leads.
    for _sec in sections:
        _h = _sec['heading']
        if _h == 'Typical drying time:' and len(_sec['blocks']) == 1 and _sec['blocks'][0]['type'] == 'para':
            _sec['blocks'] = [{'type': 'para', 'segs': [(_h, None)] + _sec['blocks'][0]['segs']}]
            _sec['heading'] = None
        elif _h == 'Leave the thermostat at 72 to 75°F' and len(_sec['blocks']) == 1 and _sec['blocks'][0]['type'] == 'para':
            _segs = _sec['blocks'][0]['segs']
            if _segs and _segs[0][0].startswith('('):
                _merged = (_h + ' ' + _segs[0][0], _segs[0][1])
                _sec['blocks'] = [{'type': 'para', 'segs': [_merged]}] + [{'type': 'para', 'segs': [_sg]} for _sg in _segs[1:]]
                _sec['heading'] = None
    # (g) Orphan question lead-in at a section tail (sagging-ceiling
    # "How Dangerous Is It?") moves to the head of the next section.
    for _si in range(len(sections) - 1):
        _cur_s, _nxt_s = sections[_si], sections[_si + 1]
        if (_cur_s['blocks'] and any(_b['type'] == 'list' for _b in _cur_s['blocks'])
                and _cur_s['blocks'][-1]['type'] == 'para'
                and len(_cur_s['blocks'][-1]['segs']) == 1
                and _cur_s['blocks'][-1]['segs'][0][0] == 'How Dangerous Is It?'):
            _para = _cur_s['blocks'].pop()
            _nxt_s['blocks'] = [_para] + _nxt_s['blocks']
    # (h) Link-phrase promoted to a section parent, splitting a sentence
    # (fire-sprinkler "See also commercial water damage restoration and
    # our" + parent "Legacy West area page"). If a section's parent maps
    # to a link target and the previous section's last paragraph dangles
    # at "and our", rejoin parent + period into that paragraph and drop
    # the parent. The dangling guard keeps real parents (area calendars)
    # untouched: their previous paragraphs never end this way.
    for _si in range(1, len(sections)):
        _prev_s, _sec = sections[_si - 1], sections[_si]
        _par = _sec.get('parent')
        if not _par:
            continue
        # 'Legacy West area page' is the link phrase 'legacy west area'
        # plus a trailing ' page' word, so try with that suffix stripped.
        _tgt = phrase_target(_par) or phrase_target(_par.rstrip().removesuffix(' page'))
        if _tgt is None:
            continue
        if not _prev_s['blocks'] or _prev_s['blocks'][-1]['type'] != 'para':
            continue
        _segs = _prev_s['blocks'][-1]['segs']
        if _segs and _segs[-1][0].rstrip().endswith('and our'):
            _prev_s['blocks'][-1]['segs'] = _segs + [(_par, _tgt), ('.', None)]
            _sec['parent'] = None
    # (i) Round 4 post-processing: parser fragments flagged in Round 4.
    # All fixes are layout/markup only: no word is added, removed, or
    # reordered, except the contact intro paragraph, which MOVES (words
    # preserved; qa1 word-diff is a set comparison, so a move stays green).
    # (i1) Copper 60-second list: "From the inside:" was promoted to a
    # standalone H2 section; fold it back as bullet 2 of the list.
    if slug == 'copper-pinhole-leaks':
        for _si in range(len(sections) - 1):
            _cur, _nxt = sections[_si], sections[_si + 1]
            if (_cur['heading'] == 'The 60-Second Answer for Plano Homeowners'
                    and _nxt['heading'] == 'From the inside:'
                    and _cur['blocks'] and _cur['blocks'][-1]['type'] == 'list'
                    and _nxt['blocks'] and _nxt['blocks'][0]['type'] == 'para'):
                _lst = dict(_cur['blocks'][-1])
                _lst['items'] = _lst['items'] + ['From the inside: ' + _join_segs(_nxt['blocks'][0]['segs'])]
                _cur['blocks'] = _cur['blocks'][:-1] + [_lst] + _nxt['blocks'][1:]
                del sections[_si + 1]
                break
    # (i2) Copper area listheads: West/East items trapped as sub-items
    # of the North Plano list; split each area lead into its own
    # listhead + single-item list.
    if slug == 'copper-pinhole-leaks':
        for _sec in sections:
            if _sec['heading'] != 'Which Plano Homes Are Most at Risk':
                continue
            _out = []
            for _b in _sec['blocks']:
                if _b['type'] != 'list':
                    _out.append(_b)
                    continue
                _cur_items = []
                for _it in _b['items']:
                    _m = re.match(r'^((?:West|East|North|Central) Plano \(\d{5}(?:, \d{5})?\):)\s+(.+)$', _it)
                    if _m and _cur_items:
                        _out.append({'type': 'list', 'items': _cur_items})
                        _out.append({'type': 'listhead', 'text': _m.group(1)})
                        _cur_items = [_m.group(2)]
                    else:
                        _cur_items.append(_it)
                if _cur_items:
                    _out.append({'type': 'list', 'items': _cur_items})
            _sec['blocks'] = _out
    # (i3) Uniform para + listhead + list sections (allen/mckinney/
    # richardson search queries, warm-spot methods): the trailing
    # listhead + bullets are the same kind of items as the paragraph
    # sentences, so render ALL of them as one uniform bullet list.
    # List rendering re-linkifies phrases, so no link is lost.
    _UNIFORM = {
        ('allen', 'What Allen Homeowners Search When Water Hits'),
        ('mckinney', 'What McKinney Homeowners Search When Water Hits'),
        ('richardson', 'What Richardson Residents Search When Water Hits'),
        ('warm-spot-on-floor', 'How Under-Floor Drying Works'),
    }
    for _sec in sections:
        if (slug, _sec['heading']) not in _UNIFORM:
            continue
        _blks = _sec['blocks']
        if (len(_blks) == 3 and _blks[0]['type'] == 'para'
                and _blks[1]['type'] == 'listhead' and _blks[2]['type'] == 'list'):
            _items = [t for t, _ in _blks[0]['segs'] if t.strip() not in ('', '.', ',')]
            _items.append(_blks[1]['text'] + ' ' + _blks[2]['items'][0])
            _items.extend(_blks[2]['items'][1:])
            _sec['blocks'] = [{'type': 'list', 'items': _items}]
    # (i4) Ceiling-dripping safety fragment: "Get out from under it and
    # call" was promoted to an H2 over a one-line phone body. Demote it
    # to a bold lead paragraph (colon added for the bold-lead render;
    # words unchanged).
    if slug == 'ceiling-dripping':
        for _sec in sections:
            if (_sec['heading'] == 'Get out from under it and call'
                    and _sec['blocks'] and _sec['blocks'][0]['type'] == 'para'):
                _p = _sec['blocks'][0]
                _sec['blocks'] = [{'type': 'para', 'segs': [('Get out from under it and call:', None)] + _p['segs']}] + _sec['blocks'][1:]
                _sec['heading'] = None
    # (i5) Ceiling-leak area fragment: the sentence "We see hail-season
    # roof leaks in Hunters Glen and Preston Meadow (" was promoted to
    # an H3, splitting the sentence at the parenthesis. Restore the
    # real heading ("Ceiling Leaks Across Plano") and rejoin the
    # fragment as the paragraph's lead (render joins " (" with no space
    # before the area link, so the parenthesis closes correctly).
    if slug == 'ceiling-leak':
        for _sec in sections:
            if (_sec.get('parent') == 'Ceiling Leaks Across Plano'
                    and _sec['heading'] and _sec['heading'].startswith('We see hail-season')):
                _frag = _sec['heading']
                _sec['heading'] = _sec['parent']
                _sec['parent'] = None
                if _sec['blocks'] and _sec['blocks'][0]['type'] == 'para':
                    _sec['blocks'] = [{'type': 'para', 'segs': [(_frag, None)] + _sec['blocks'][0]['segs']}] + _sec['blocks'][1:]
    # (i6) Storm/mold group intros (REOPENED Round 3): the H2 + lone H3
    # stack still stands with no body copy. Give it body copy by
    # rendering the H3 text as a lead paragraph under the H2 — existing
    # words only, no invented copy, section count unchanged (so split
    # image placement does not shift).
    _GROUP_INTRO = {
        ('storm-water-category-3', 'How the Water Got In Decides What Has to Happen'),
        ('mold-after-water-damage', 'Hour-by-Hour: What Happens Inside Wet Walls and Floors'),
    }
    for _sec in sections:
        if ((slug, _sec['heading']) in _GROUP_INTRO and len(_sec['blocks']) == 1
                and _sec['blocks'][0]['type'] == 'subhead'):
            _sec['blocks'] = [{'type': 'para', 'segs': [(_sec['blocks'][0]['text'] + '.', None)]}]
    # contact form
    if tab['slug'] == 'contact' and form_fields:
        sections.append({'heading': 'Send Us a Message (Non-Emergency)', 'blocks': [
            {'type': 'form', 'fields': form_fields, 'note': form_note}]})
    # (i7) Contact form intro (REOPENED Round 3): the "Send Us a Message"
    # intro paragraph sits two sections before the actual form. MOVE it
    # to sit directly under the single form H2 (words preserved, order
    # within the page changes only for this paragraph). Runs AFTER the
    # form section is appended above, so the target exists.
    if slug == 'contact':
        _form_sec = next((s for s in sections if s['heading'] == 'Send Us a Message (Non-Emergency)'
                          and any(b['type'] == 'form' for b in s['blocks'])), None)
        if _form_sec is not None:
            for _sec in sections:
                if _sec is _form_sec:
                    continue
                for _bi, _b in enumerate(_sec['blocks']):
                    # Round 5: the intro para now begins 'Use this form…'
                    # (source fix above); belt-and-braces: if a leading
                    # heading seg ever appears, drop ONLY that seg.
                    if (_b['type'] == 'para' and _b['segs']
                            and (_b['segs'][0][0] == 'Send Us a Message (Non-Emergency)'
                                 or _b['segs'][0][0].startswith('Use this form for questions'))):
                        _moved = _sec['blocks'].pop(_bi)
                        if _moved['segs'][0][0] == 'Send Us a Message (Non-Emergency)':
                            _moved = dict(_moved, segs=_moved['segs'][1:])
                        _form_sec['blocks'] = [_moved] + _form_sec['blocks']
                        break
                else:
                    continue
                break
    # (j) Round 5 post-processing: parser fragments flagged in Round 5.
    # All fixes are layout/markup only, except the contact form-intro
    # echo strip above (authorized duplicate removal). Each fix is
    # slug- and exact-string-scoped; no shared predicate changes.
    # (j1) Contact 'Service area:' bare label H2 -> bold-lead paragraph.
    # The colon-list branch misses (ZIP line is ~140 chars, ends '.'),
    # so the label became an H2. Demote in place (section count and
    # split placement unchanged): one para whose text starts with the
    # label, so render's bold-lead rule bolds it. Hours H3 untouched.
    if slug == 'contact':
        for _sec in sections:
            if (_sec['heading'] == 'Service area:' and len(_sec['blocks']) == 1
                    and _sec['blocks'][0]['type'] == 'para'):
                _txt = ' '.join(t for t, _ in _sec['blocks'][0]['segs']).strip()
                _sec['blocks'] = [{'type': 'para',
                                   'segs': [('Service area: ' + _txt, None)]}]
                _sec['heading'] = None
                break
    # (j2) Contact 'Whether it's clean water…' fragment H2: doc lines
    # show this AND 'Your insurance company, if you plan to file a
    # claim' are items 6-7 of the 'What to Have Ready' list, and
    # 'What Happens After You Call' is the next section heading.
    # Restore both items to the previous list and promote the heading.
    if slug == 'contact':
        for _si in range(1, len(sections)):
            _sec = sections[_si]
            if (_sec['heading'] != "Whether it's clean water, gray water or sewage"
                    or len(_sec['blocks']) != 1 or _sec['blocks'][0]['type'] != 'para'):
                continue
            _segs = _sec['blocks'][0]['segs']
            _wha = next((_k for _k, (_t, _tg) in enumerate(_segs)
                         if _t == 'What Happens After You Call'), None)
            if (_wha is None or len(_segs) < 3 or _segs[0][0] != 'Your insurance company'
                    or not _segs[1][0].startswith(',')):
                continue
            _prev = sections[_si - 1]
            if not _prev['blocks'] or _prev['blocks'][-1]['type'] != 'list':
                continue
            _lst = dict(_prev['blocks'][-1])
            _lst['items'] = _lst['items'] + [
                "Whether it's clean water, gray water or sewage",
                'Your insurance company' + _segs[1][0]]
            _prev['blocks'] = _prev['blocks'][:-1] + [_lst]
            sections[_si] = {'heading': 'What Happens After You Call',
                             'blocks': [{'type': 'para', 'segs': _segs[_wha + 1:]}]}
            break
    # (j3) Contact lone 'Tap to Call' strip: move the button block to
    # the head of the Emergency section (render then takes the intro
    # para as hero_para and the empty section 0 is skipped). The word
    # 'tap' stays on the page in the same button label. The render
    # exception for contact section 0 is deleted in gen3_render.py.
    if slug == 'contact' and len(sections) >= 2:
        _s0, _s1 = sections[0], sections[1]
        if (_s0['heading'] is None and len(_s0['blocks']) == 2
                and _s0['blocks'][0]['type'] == 'para'
                and _s0['blocks'][1]['type'] == 'cta'
                and _s1['heading'] == 'Emergency in Your Plano Home? Call First, Then Do This'):
            _s1['blocks'] = [_s0['blocks'][1]] + _s1['blocks']
            _s0['blocks'] = [_s0['blocks'][0]]
    # (j4) Cost 'The 4 Things That Set the Price': items 1-2 run inline
    # in the opening para (digit-initial lines fail is_heading_candidate)
    # while items 3-4 are subheads (lifted by step (d)). Split the
    # opening para at ^\d+\. segs so all four items are subheads; the
    # Category 3 listhead/list stays in place between factors 2 and 3.
    if slug == 'water-damage-cost':
        for _sec in sections:
            if _sec['heading'] != 'The 4 Things That Set the Price':
                continue
            _new = []
            _done = False
            for _b in _sec['blocks']:
                if (_b['type'] == 'para' and not _done
                        and any(re.match(r'^\d+\. ', _t) for _t, _ in _b['segs'])):
                    _segs = _b['segs']
                    _first = next(_k for _k, (_t, _tg) in enumerate(_segs)
                                  if re.match(r'^\d+\. ', _t))
                    if _segs[:_first]:
                        _new.append({'type': 'para', 'segs': _segs[:_first]})
                    _k = _first
                    while _k < len(_segs):
                        _nxt = next((_m for _m in range(_k + 1, len(_segs))
                                     if re.match(r'^\d+\. ', _segs[_m][0])), len(_segs))
                        _new.append({'type': 'subhead', 'text': _segs[_k][0]})
                        if _segs[_k + 1:_nxt]:
                            _new.append({'type': 'para', 'segs': _segs[_k + 1:_nxt]})
                        _k = _nxt
                    _done = True
                else:
                    _new.append(_b)
            _sec['blocks'] = _new
            break
    raw_words = ' '.join(lines)
    return sections, faqs, faq_heading, raw_words

if __name__ == '__main__':
    tabs = parse_tabs()
    print(f"tabs={len(tabs)}")
    for t in tabs:
        secs, faqs, fh, _ = classify_and_build(t)
        print(t['tab'], t['slug'], 'sections=', len(secs), 'faqs=', len(faqs), 'h1=', t['h1'][:50])
    json.dump([{'tab': t['tab'], 'title': t['title'], 'meta_title': t['meta_title'],
                'meta_desc': t['meta_desc'], 'slug': t['slug'], 'h1': t['h1']}
               for t in tabs], open(os.path.join(BASE, 'tabs.json'), 'w'), indent=1)
