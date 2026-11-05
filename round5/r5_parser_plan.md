# Round 5 parser/layout fix plan — READ-ONLY analysis, NO edits made

Source of truth for this plan: `gen3.py` (`parse_tabs` + `classify_and_build`,
lines ~143–958) feeding `gen3_render.py` (`write_page`, `block_html`), and the
Round 5 lines in `BLUNDER_HUNT.md` (Round 5 section). Section structures below
were verified by running `classify_and_build()` in memory on the current
`extracted.txt` (no build, no rebuild, no file edits except this plan).

Standing constraint for every fix below: **heading/list markup only — no doc
word is cut, reordered, or paraphrased.** The single exception is fix (6),
which is explicitly authorized duplicate removal (the same string remains
once, as the form H2). `qa1.py` word-diff is a **set** comparison, so moves,
demotions, promotions, and duplicate removals stay green as long as the word
set is unchanged; visible order/count still has to be re-screenshotted.

## Shared mechanism the fix pass must understand first

### How a "run of short lines" becomes a list — and why its last item escapes

In `classify_and_build`, `is_heading_candidate()` (gen3.py:256) returns True
for essentially any short (<85-char), non-terminal-punctuation, uppercase-
initial line that is not a phone number, bracket CTA, or link phrase — it
returns True in both branches at the end, so the "followed by" tests only
exclude lowercase- / comma-continuations. Each such line therefore starts a
new section in the section-grouping loop (~430). The post-process merge
(~440–460) then repairs runs of **empty** sections:

- run length exactly 2 → heading + `subhead` block;
- run length ≥ 2 → heading + `list` of `run[1:]`;
- run length 1 → next section gets `parent = run[0]`.

The trap: the run's **terminator** section — the first section that actually
has blocks — is *not* part of `run`, so if the terminator's heading is
itself the last list item, that item is excluded from the list and rendered
as its own H2. That is exactly fixes (1) and (2). The Round 3/4 precedent
for this trap is the `_TAIL` post-process (gen3.py:757, step (e)), which
folds a promoted tail heading back into the previous list for two exact
strings. Fixes (1)(2) extend that precedent rather than inventing a new
generic rule (see "Cross-page risk" below).

### How render treats the resulting sections (gen3_render.py)

- `block_html`: `subhead` → `<h3>`, `list` → `<ul>`, `cta` →
  `<p class="cta-row"><a class="btn-call">…</a></p>`, `para` → `<p>` (with
  bold-lead handling in `para_html`).
- `write_page` lone-CTA suppression (~766): a heading-less section whose
  blocks are all `cta` is dropped — **except** contact section 0 (see fix 5).
- Parent rendering (~786–801): `parent` → `<h2>`, section heading → `<h3>`;
  the `Calendar` / `Quick Diagnosis Table` parents instead render as
  `<p class="section-kicker">` (CSS `.section-kicker` already exists, :679).
- `_subhead_only` (~815): a section whose blocks are **all** `subhead` is
  rendered as a plain `<div class="wrap">` with **no** `<section>` band.
  This path is the key to fixes (8)(9): it no longer fires for the group
  intros, because step (i6) already converted their subhead to a `para`.

---

## Fix 1 — mold-after-water-damage: symptom line promoted to H2

- **Hunt line:** "Signs the Clock Has Already Run Out" list ends at 3 bullets;
  "Allergy-like symptoms in one area of the house" is its own H2 band,
  followed by the closing paragraph and a lone "Call 24/7" button.
- **Verified parser state:** section [9] heading
  `Signs the Clock Has Already Run Out`, `list` = 3 items (musty smell;
  dark spots; swollen drywall). Section [10] heading =
  `Allergy-like symptoms in one area of the house`, blocks = [`para`
  ("If you see these, drying alone may not be enough…" + the flattened
  final-CTA lines), `cta` ("Call 24/7")].
- **Root cause:** doc lines (extracted.txt tab 38, lines 62–67) are 4 short,
  non-terminal lines followed by a paragraph. Lines 1–3 become empty
  sections; line 4 becomes the terminator section because the closing
  paragraph lands in its blocks. The run merge (`run[1:]`) therefore yields
  only 3 bullets and leaves line 4 as an H2. The existing `_TAIL` step (e)
  does **not** fire here because it requires `len(next blocks) == 1` and a
  single `para`; this section has `[para, cta]`.
- **Proposed change (gen3.py, step (e), ~757):**
  1. Extend `_TAIL` with `'Allergy-like symptoms in one area of the house':
     'closing'` (same `'closing'` semantics as the existing fans entry:
     heading becomes a list item; the following paragraph stays a paragraph,
     it is **not** merged into the item text).
  2. Widen the (e) guard from `len(blocks) == 1 and blocks[0] is para` to
     `blocks[0] is para` with all remaining blocks being `cta` only
     (i.e. `[para]` or `[para, cta]`). On a match: append the heading to
     the previous section's last list, then append **all** of the next
     section's blocks (para, then cta) after that list, and delete the
     next section.
- **Result:** Signs list = 4 bullets; closing paragraph sits under the
  list; the "Call 24/7" button follows the paragraph in the same band
  (it was already there — no CTA is added or removed). Section count
  11 → 10 on this page only.
- **Affects:** `mold-after-water-damage` only (guarded by exact string +
  structure; see "Cross-page risk").

## Fix 2 — water-damage-insurance-texas: drip line promoted to H2

- **Hunt line:** "Mistakes That Can Hurt a Claim" list ends at 4 bullets;
  "Letting a slow drip continue after you notice it" is its own H2 band,
  followed by the "Protect Your Claim From Day One" paragraph and a lone
  "Call 24/7" button.
- **Verified parser state:** section [6] heading
  `Mistakes That Can Hurt a Claim`, `list` = 4 items. Section [7] heading =
  `Letting a slow drip continue after you notice it`, blocks = [`para`
  ("Protect Your Claim From Day One. Call (972) 472-7917. …" + back-to
  lines), `cta` ("Call 24/7")]. (The FAQ split removes the FAQ heading
  that follows in the doc, so the drip line is the last main-flow section
  and its "closing" paragraph is the final-CTA text absorbed as para segs.)
- **Root cause:** identical to fix 1 — doc lines (tab 41, lines 61–66) are
  5 short lines; lines 1–4 form the run, line 5 is the terminator section
  (its blocks are the final-CTA paragraph + bracket CTA), so the run merge
  yields 4 bullets and line 5 becomes an H2.
- **Proposed change (gen3.py, step (e), same edit as fix 1):** extend
  `_TAIL` with `'Letting a slow drip continue after you notice it':
  'closing'` and apply the same `[para]` / `[para, cta]` widening.
- **Result:** Mistakes list = 5 bullets; "Protect Your Claim…" paragraph
  and its button sit under the list in the same band. Section count
  8 → 7 on this page only.
- **Affects:** `water-damage-insurance-texas` only.
- **Do NOT do:** do not split the "Protect Your Claim…" para seg into a
  separate H2 in this fix — the hunt fix for this line is only "demote
  the drip line back to a fifth bullet and keep the closing CTA paragraph
  under that list". The flattened final-CTA heading inside that paragraph
  is a separate, unflagged pattern (it also occurs in the mold closing
  paragraph); leave it untouched.

## Fix 3 — contact: bare label "Service area:" promoted to H2

- **Hunt line:** section heading is the bare label `Service area:` (colon
  included), followed by a single line of ZIP codes and city names.
- **Verified parser state:** section [3] heading = `Service area:`,
  blocks = [single `para` (Plano ZIPs + nearby cities)]. Section [2] is
  the parent case: `parent = 'How to Reach Us'`, heading = `Hours:`,
  para = hours sentence.
- **Root cause (two missed gates, gen3.py):**
  1. The colon-introduced-list branch (~322) requires the following line
     to be short (`len < 100`) **and** non-terminal (`not endswith('.')`).
     The ZIP/city line is ~140 chars and ends with `.`, so the branch
     never fires.
  2. `is_heading_candidate()` (gen3.py:256) has **no** exclusion for a
     line ending in `:` — so the label falls through to the heading
     trigger and becomes an H2. (Same reason `Hours:` became a heading,
     but there the run-length-1 parent rule gave it the "How to Reach Us"
     H2 context, so it was not flagged. Do not "fix" Hours in this pass.)
- **Proposed change (gen3.py, new contact-scoped post-process, placed
  after section grouping / before the form append):** if
  `slug == 'contact'` and a section has `heading == 'Service area:'` and
  exactly one `para` block, replace it with a heading-less section whose
  single para's segs are `[(heading + ' ' + para_text, None)]` — i.e.
  `Service area: Plano (75023, …) plus nearby … .` as one paragraph.
  Render then applies the existing `para_html` bold-lead rule (first
  phrase ≤65 chars ending in `:` + rest ≥80 chars → `<strong>`), so the
  page shows a **bold lead-in line, not an H2**, exactly as the hunt fix
  asks ("demote the label to a lead-in line … keeping the ZIP/city words
  unchanged"). No words are added, removed, or reordered; only the `:` 
  line's markup level changes.
- **Why scoped, not a global `is_heading_candidate` colon exclusion:**
  a global "lines ending in `:` are never headings" rule would also
  demote `Hours:` (changing its parent rendering) and every other
  colon-terminated heading-like line on other pages. The exact-label +
  single-para guard limits the blast radius to this one section.
- **Affects:** `contact` only. Re-verify the "How to Reach Us" area
  visually: the Hours parent section and the new bold-lead paragraph
  must read as one contact-details group, not as two competing headings.

## Fix 4 — contact: "Whether it's clean water…" fragment H2 + flattened next heading

- **Hunt line:** H2 is the clause fragment
  `Whether it's clean water, gray water or sewage`; its body runs
  "Your insurance company, if you plan to file a claim What Happens After
  You Call We answer and listen." — a What-to-Have-Ready list item became
  body text and the next section title was flattened into paragraph text
  with no sentence break.
- **Verified parser state:** section [4] heading
  `What to Have Ready When You Call`, `listhead` + `list` = 5 items
  (ends at "What kind of floors: carpet, hardwood, LVP or tile").
  Section [5] heading = `Whether it's clean water, gray water or sewage`,
  blocks = [one `para` whose segs are, in order: `Your insurance company`,
  `, if you plan to file a claim`, `What Happens After You Call`,
  `We answer and listen. …`, `A local crew is dispatched. …`, etc.].
  Doc source is tab 43, lines 34–50.
- **Root cause (chain, gen3.py colon-list loop ~322 + heading trigger
  ~370):**
  1. In the colon-list collection loop, the heading-break test for each
     candidate item `it` looks at `nxt2` = the line **after** `it`. For
     `it = "Whether it's clean water, gray water or sewage"`,
     `is_heading_candidate(it, "Your insurance company")` is True and
     `nxt2 = "Your insurance company"` does **not** start with `,`,
     `and `, or `plus `, so the loop **breaks** — the list ends at 5.
     The existing `nxt2` comma guard only protects the case where the
     candidate's *own* continuation starts with a comma; it does not
     recognise that the candidate is itself followed by another short,
     non-terminal list item.
  2. Back in the main loop, "Whether…" (cur_para empty after the list
     flush) passes `is_heading_candidate` and becomes an H2 section.
  3. "Your insurance company" fails `is_heading_candidate` (its next line
     starts with `,`) so it falls into the para; ", if you plan to file
     a claim" joins it as a seg.
  4. "What Happens After You Call" then fails the heading trigger because
     `last_ended` is False (the para's last seg does not end in `.`/`?`/
     `!`/`:`) and `list_like_para(cur_para)` is False (only 2 content
     segs) — so it is appended as just another para seg, with no period
     or break before it. Every following "We answer…" / "A local crew…"
     sentence line then accumulates into the same para.
  (Note: the tail of this chain, "Extraction and drying begin the same
  visit. See" + link, is already handled by step (b) in gen3.py, which
  converts that heading back to a heading-less para — section [6] in the
  dump. Do not touch step (b).)
- **Proposed change — primary (gen3.py, colon-list loop ~322):** narrow
  the heading-break test so it breaks **only** when the candidate is
  followed by paragraph-like content. Concretely, in the
  `is_heading_candidate(it, …)` branch, do **not** break when `nxt2`
  is short (<85 chars) **and** non-terminal (does not end in `.`) —
  i.e. when `nxt2` itself looks like another list item rather than a
  heading's body paragraph. With this guard:
  - "Whether…" is appended as list item 6 (its `nxt2` is the short,
    non-terminal "Your insurance company");
  - "Your insurance company" is appended as item 7 and its `, if you…`
    continuation joins it (existing continuation-while loop), giving
    item 7 = "Your insurance company, if you plan to file a claim";
  - "What Happens After You Call" then **does** break the list (its
    `nxt2`, "We answer and listen.", ends in `.`), and in the main loop
    it passes the heading trigger (cur_para empty) and becomes an H2,
    with the "We answer…" sentences as its own paragraph.
  - No period needs inventing: the list items in this list carry no
    trailing periods in the existing rendering, and the H2 markup itself
    is the sentence break the hunt fix allows ("add only the missing
    sentence break/heading markup, cut nothing").
- **Fallback if the full-tab diff gate (below) shows any other page
  changing:** revert the loop change and implement a contact-scoped
  post-process repair instead, using the exact strings
  `Whether it's clean water, gray water or sewage` (fold heading + first
  two para segs back into the previous section's list as items 6–7) and
  `What Happens After You Call` (promote that para seg to the next
  section's heading, splitting the para's segs at that point). Same
  visible result, zero other-page risk.
- **Affects:** `contact` only (primary change is diff-gated; fallback is
  slug-scoped). Re-verify the whole "What to Have Ready" → "What Happens
  After You Call" run visually, plus every other colon-introduced list
  that the diff gate touches.

## Fix 5 — contact: lone orange "Tap to Call" button in a bare white strip

- **Hunt line:** a lone orange "Tap to Call: (972) 472-7917" button sits
  by itself in a bare white strip between the hero and the Emergency
  section; no other page has this strip.
- **Verified parser/render state:** doc tab 43, line 13 is the bracket CTA
  `[Tap to Call: (972) 472-7917]`. `is_bracket_cta` / `cta_label`
  (gen3.py:96–102) turn it into a `cta` block with label `Tap to Call`,
  in heading-less section [0] alongside the intro paragraph. In
  `gen3_render.py write_page`, the hero-para extraction removes that
  intro paragraph into the hero, leaving section [0] as `[cta]` only.
  The lone-CTA suppression branch (~766) would normally drop such a
  section — but its Round 3 exception (`if not (slug == 'contact' and
  si == 0)`) deliberately renders this one button row, because the word
  **'tap' appears nowhere else on the page** and suppressing the block
  would make `qa1` report `miss=['tap']` (see the comment at :771–775).
- **Why the current strip is NOT required — and what to do instead:**
  the strip is not required for phone access (the hero already has a
  "Call Now" button, and header/footer/sticky bar carry the phone — the
  suppression comment itself says this). It is required **only** as the
  carrier of the word 'tap'. So the fix is to **move the carrier, not
  delete it**:
  - **Primary (gen3.py post-process, after section grouping):** if
    `slug == 'contact'` and `sections[0]` blocks are `[para, cta]`,
    move the `cta` block to the **head** of `sections[1]` (heading
    `Emergency in Your Plano Home? Call First, Then Do This`). Render
    then: hero-para extraction still takes the intro para from
    section [0]; section [0] is left empty and skipped by the
    `heading is None and not blocks: continue` guard; the Emergency
    section renders its H2, then the `cta-row` button
    ("Tap to Call: (972) 472-7917"), then its existing paragraphs —
    a button inside a full copy section, not a bare strip. The word
    'tap' stays on the page verbatim, in the same button label.
  - Then **delete the render exception** (`slug == 'contact' and
    si == 0`, gen3_render.py:776) so a future lone CTA can never re-open
    a bare strip. The exception becomes dead code once the move exists;
    deleting it is safe **only** together with the move — deleting it
    alone would suppress the button and lose 'tap' (qa1 miss). That is
    the trap this fix must not fall into.
  - **Alternative (not recommended):** change the contact hero CTA label
    from "Call Now:" to "Tap to Call:" in the hero template. It also
    preserves 'tap' with a single button, but it special-cases the shared
    hero template and loses the "Call Now" wording; the body move keeps
    the button next to the Emergency copy it belongs to.
- **Affects:** `contact` only. Gate: after the fix, `qa1` for contact
  must still show no `tap` miss, and the post-hero strip must be gone
  in both desktop and mobile screenshots.

## Fix 6 — contact: form intro repeats the heading verbatim — AUTHORIZED duplicate strip

- **Hunt line:** the intro paragraph directly under the single form H2
  reads "Send Us a Message (Non-Emergency) Use this form for questions,
  scheduling an inspection or following up on a job." — the heading
  text appears twice in a row.
- **Verified parser state:** section [9] heading =
  `Send Us a Message (Non-Emergency)`, blocks = [`para` with segs
  [`Send Us a Message (Non-Emergency)`, `Use this form for questions, …`,
  `(972) 472-7917 instead.`], `form`]. This is a **duplicate, not a
  content cut**, and it is the one explicitly authorized word removal:
  the string remains on the page once, as the form section's H2.
- **Where the heading gets copied into the lead paragraph (two steps
  in gen3.py):**
  1. The contact special case (~356): when the main loop meets the doc
     line `Send Us a Message (Non-Emergency)` (tab 43, line 64), it
     flushes the current para and appends **the heading string itself**
     as the first seg of a new `cur_para` — intended as "demote the
     intro instance to paragraph copy so the page has a single form
     heading", but it keeps the heading text inside the paragraph.
     The following lines ("Use this form…", the phone line) then join
     the same para.
  2. Step (i7) (~926): the form section is appended at the end with
     heading `Send Us a Message (Non-Emergency)` + `form` block, and
     (i7) then **moves** that whole intro para to the head of the form
     section (words preserved, order within the page changes only for
     this paragraph). Result on screen: H2, then a paragraph that
     starts with the same H2 text.
- **Proposed change (both steps, idempotent):**
  1. **Primary, at the source (~360):** do not append the heading seg —
     on `slug == 'contact' and s == 'Send Us a Message (Non-Emergency)'`,
     `flush_para()` and advance `k` **without** `cur_para.append((s,
     None))`, so the para that (i7) later moves begins with
     `Use this form for questions…`.
  2. **Belt-and-braces, in (i7) (~940):** when moving a para whose
     `segs[0][0] == 'Send Us a Message (Non-Emergency)'`, drop that
     first seg (keep the rest) before prepending it to the form section.
     This is a no-op if step 1 already applied, and it protects the fix
     if the para is ever built by another path.
  - Guard on both: strip **only** a first seg exactly equal to the form
    heading, and only when remaining segs are non-empty (they are:
    "Use this form…" + phone seg). Never strip any other seg.
- **Result:** intro begins exactly "Use this form for questions,
  scheduling an inspection or following up on a job." The H2 above it
  is unchanged. `qa1` word set is unchanged (set comparison; the string
  was present twice, now once).
- **Affects:** `contact` only.

## Fix 7 — water-damage-cost: "The 4 Things That Set the Price" split across two levels

- **Hunt line:** items 1 (Square Footage) and 2 (Water Category) run
  inline inside a paragraph, while items 3 (How Hard It Is to Dry) and 4
  (How Many Days) are promoted to H3 — one numbered set at two levels.
- **Verified parser state:** section [2], `parent =
  'Estimated Cost by Situation'`, heading = `The 4 Things That Set the
  Price`, blocks in order: [`para` (intro + `1. Square Footage and Room
  Size` + its body + `2. Water Category` + Category 1/2 segs),
  `listhead` (`Category 3 (black):`), `list` (1 sewage item),
  `subhead` (`3. How Hard It Is to Dry`), `para` (carpet/drywall body +
  structural-drying link), `subhead` (`4. How Many Days`), `para`
  (equipment-per-day body)]. Doc source is tab 35, lines 28–46.
- **Root cause (chain, gen3.py):**
  1. Items 1–2 never become headings: `is_heading_candidate` (:256)
     rejects them because their first character is a digit
     (`'1'.isupper()` is False), so they fall into ordinary paragraph
     segs and accumulate into the intro para.
  2. Item 3 **does** become a subhead, but only by accident of the
     colon-list loop: `Category 3 (black):` opens a colon list (its next
     line ends in `See`, not `.`, and is <100 chars), and the loop's
     heading-break test does not fire for `3. How Hard It Is to Dry`
     (digit-initial → `is_heading_candidate` False), so item 3 is
     swallowed as a **list item** of the Category 3 list.
  3. Step (d) (~730, "numbered factor swallowed into a preceding bullet
     list") then fires on that list + following-para pair: it lifts the
     first `^\d+\. ` list item out as a `subhead` (item 3) and splits
     the following para at the next `^\d+\. ` seg, making item 4 a
     second `subhead`. Step (d) runs once per section (`break`), and
     items 1–2 were never in a list, so they are never lifted. Hence
     1–2 inline, 3–4 as H3.
- **Proposed change (gen3.py, new post-process step placed AFTER step
  (d), so it sees the final 3/4 subheads):** in the section with
  `slug == 'water-damage-cost'` and heading
  `The 4 Things That Set the Price`, walk its blocks; when a `para`
  contains segs matching `^\d+\. `, split that para at each numbered
  seg into: intro para (segs before the first number, if any),
  then per number: `subhead` (the numbered seg text) + `para` (the
  segs up to the next numbered seg). Applied to the opening para this
  yields: intro para, `subhead 1` + body para, `subhead 2` + body para
  (including the Category 1/2 segs, which are item 2's body), followed
  **unchanged and in place** by the existing Category 3 `listhead` +
  `list`, `subhead 3`, body para, `subhead 4`, body para. No block
  moves across another block; only the markup level of items 1–2
  changes (inline seg → subhead), matching items 3–4.
  - Render note: `subhead` renders as `<h3>` (gen3_render.py
    `block_html`). The section heading itself renders as `<h3>` too
    under its `Estimated Cost by Situation` parent H2 — so this fix
    makes all four factors the **same level as each other** (H3), which
    is the hunt fix's "all H3" option. The fix pass should confirm the
    rendered outline reads H2 parent → H3 section title → H3 factors
    and accept that as "same level" per the hunt wording; if the outline
    gate instead demands factors strictly below the section title, the
    fallback is the hunt's other option (all bold inline): reverse step
    (d) for this section only, demoting subheads 3–4 back to bold-lead
    paragraph starts — do **not** attempt the fallback unless the
    outline gate actually fails, because it undoes a deliberate R3 fix
    and re-merging item 3 into the Category list is fiddly.
- **Affects:** `water-damage-cost` only (slug + heading scoped; see
  guard below).

## Fix 8 — storm-water-category-3 group-intro band: merge into next section

- **Hunt line (REOPENED Round 4):** the R4 fold "is structurally present
  but renders as a lone one-line beige band containing only the label
  sentence 'Why Plano Homes Take On Storm Water.' between two full H2
  sections."
- **Verified parser state:** section [2] heading =
  `How the Water Got In Decides What Has to Happen`, blocks = [single
  `para` (`Why Plano Homes Take On Storm Water.`)]. Next section [3] =
  `Creeks Run Through the City` + body para. Doc source is tab 37,
  lines 26–28: group H2, label line, then the four child headings
  (Creeks / Slabs / Saturated Clay / Brick Weep Holes).
- **How it got here (gen3.py + gen3_render.py):**
  1. Pre-merge, the group H2 and the label line are two consecutive
     empty sections (the label's following line is another heading, so
     it gets no blocks). The run-length-2 merge (~447) turns them into
     heading + `subhead` block.
  2. Step (i6) (~914, `_GROUP_INTRO`, Round 4) then converts that single
     `subhead` block into a `para` (`subhead text + '.'`) "to give it
     body copy … section count unchanged (so split image placement does
     not shift)".
  3. Render then misses the band-less path: `_subhead_only`
     (gen3_render.py:815) requires **all** blocks to be `subhead`; after
     (i6) the blocks are `[para]`, so the section renders as a normal
     `<section class="block reveal">` beige band containing an H2 and a
     one-line paragraph. Reverting (i6) would restore the plain
     `<div class="wrap">` H2+H3 pair — still a dangling label, just
     without the band — which is why the hunt fix says **merge, not
     another demotion**.
- **Proposed change — primary, in `gen3_render.py write_page` (render
  carry-over, so section indices and split placement do not shift):**
  in the section loop, before emitting, detect a group-intro lone
  section: `heading in {'How the Water Got In Decides What Has to
  Happen', 'Hour-by-Hour: What Happens Inside Wet Walls and Floors'}`
  (or, more generally, a section whose blocks are a single `para` and
  whose heading is in the `_GROUP_INTRO` set) **and** a following
  section exists. Instead of appending its own `out_section`, stash
  `pending_group = (heading, para_text)` and `continue` **without**
  consuming a split (this section's index, 2, is not a split index —
  splits fire after indices 1, 3, 5 — so no split is lost and later
  splits stay attached to the same sections as today). When the next
  section is emitted, prepend to its `inner`: a kicker line carrying
  the group heading text and the label line as its lead paragraph —
  concretely, reuse the existing parent/kicker machinery: render the
  stashed heading as `<p class="section-kicker">` (the same class used
  for Calendar / Quick Diagnosis parents, :790/:797) followed by the
  label paragraph, then the next section's own H2 + blocks. Every word
  is preserved (group H2 text + label text both appear, now inside the
  first child section's full band); the lone band disappears.
  - Keep (i6) as-is: it already produces the label `para` (with its
    `.`) that the carry-over consumes. Do **not** strip the `.` —
    the rendered label text must stay exactly
    `Why Plano Homes Take On Storm Water.` as R4 left it.
- **Parser-side alternative (only if the fix pass prefers parser
  changes):** replace (i6) with: delete the group section, set the
  following section's `parent` to the group H2, and prepend the label
  `para` to the following section's blocks — the existing parent branch
  (H2 parent + H3 heading + blocks) then renders it inside a full band.
  Cost of this variant: deleting a section shifts later section indices
  by −1, so splits that today follow sections 1/3/5 would follow
  different content (verified: storm splits today follow indices
  1/3/5 = 60-Second / Creeks / Saturated; after deletion they would
  follow 60-Second / Slabs / Brick). If this variant is chosen, every
  split image on the page must be re-screenshotted against its new
  neighbour section. The render carry-over avoids this entirely, which
  is why it is primary.
- **Affects:** `storm-water-category-3` only for this line (same pattern
  on mold, fix 9). Merge target section: `Creeks Run Through the City`.

## Fix 9 — mold-after-water-damage group-intro band: same merge

- **Hunt line (REOPENED Round 4):** same defect as fix 8 — a lone
  one-line beige band containing only
  `Why Plano Homes Are at Higher Risk.` between two full H2 sections.
- **Verified parser state:** section [2] heading =
  `Hour-by-Hour: What Happens Inside Wet Walls and Floors`, blocks =
  [single `para` (`Why Plano Homes Are at Higher Risk.`)]. Next
  section [3] = `Warm Indoor Temperatures` + body para. Doc source is
  tab 38, lines 26–28.
- **Root cause:** identical to fix 8 (run-length-2 merge → `subhead`,
  then (i6) `_GROUP_INTRO` conversion to `para`, then the
  `_subhead_only` band-less path no longer firing).
- **Proposed change:** same render carry-over as fix 8, with this
  page's strings: stash heading
  `Hour-by-Hour: What Happens Inside Wet Walls and Floors` + label
  para `Why Plano Homes Are at Higher Risk.`, and prepend them
  (kicker + lead paragraph) to the `Warm Indoor Temperatures` section's
  band. Keep the `.` on the label text as R4 left it. Parser-side
  alternative and its split-shift cost are the same as fix 8.
- **Affects:** `mold-after-water-damage` only for this line. Merge
  target section: `Warm Indoor Temperatures`.
- **Note on the other (i6) behaviour:** (i6) also covers the area
  at-a-glance shells via the `_subhead_only` path in render — this fix
  must be scoped to the two `_GROUP_INTRO` headings only, not to
  `_subhead_only` sections generally, or the area shells' band-less
  rendering changes too.

---

## Cross-page risk: do fixes (1), (2), (7) change other pages' lists?

**Fixes (1)(2) — no, by construction.** The change is an exact-string
allowlist (`_TAIL`) plus a structural guard, the same pattern as the
existing cabinet/fans `_TAIL` entries, which have never fired on another
page:

- guard conjunction: previous section's last block is a `list` **and**
  next section's heading is exactly one of the two new strings **and**
  next section's blocks are `[para]` or `[para, cta]` **and** heading is
  <85 chars with no terminal punctuation.
- A generic version of this rule ("any H2 after a list with a single
  para is a list item") was considered and **rejected**: genuine H2
  sections routinely follow a list with a single paragraph, and such a
  rule would swallow real sections sitewide. The allowlist is the guard.

**Fix (7) — no, by construction.** The change is scoped to
`slug == 'water-damage-cost'` **and** heading ==
`The 4 Things That Set the Price`, and it only splits a `para` at
`^\d+\. ` segs inside that one section. The only other numbered-para
splitting in the codebase is step (d), which is untouched. A generic
"split every para at numbered segs" rule was considered and rejected:
numbered segs appear inside ordinary paragraphs on other pages (e.g.
"Day one:" / "Day two or three:" style bodies) where splitting would
manufacture false subheads.

**Fix (4) is the one with real cross-page risk.** Its primary loop-guard
change touches the shared colon-list break test, so it is the only fix
in this plan that **must** pass the full-tab diff gate below; the
contact-scoped fallback exists precisely so the fix pass can abandon
the loop change if the gate fails, with no loss of the contact result.

**Fixes (3)(5)(6)(8)(9) — no.** Each is scoped by slug (`contact`,
`storm-water-category-3`, `mold-after-water-damage`) and, where
applicable, by exact heading string. None touches a shared predicate
(`is_heading_candidate`, `list_like_para`, `join_items`, `_join_segs`
are all **unchanged** by this plan).

## Verification gates for the fix pass (no gate skipped)

1. **Classify diff (before any rebuild):** dump `classify_and_build()`
   section structures for all 43 tabs before and after the gen3.py
   edits; assert the only tabs whose structures change are
   `mold-after-water-damage`, `water-damage-insurance-texas`,
   `contact`, `water-damage-cost`, `storm-water-category-3` — and, for
   the render-only fixes (5, 8, 9), that the parser dump is unchanged
   except where the parser fix itself applies. Any other tab changing
   = stop, fall back (fix 4) or re-scope.
2. **Section-count expectations after parser fixes:** mold 11 → 10
   (fix 1 + fix 9 is render-only, so parser count moves only for fix 1:
   11 → 10); insurance 8 → 7; contact sections unchanged in count for
   fixes 3/4/5/6 (3 demotes a heading to a para inside a heading-less
   section, 4 keeps section count, 5 moves a block, 6 strips a seg);
   cost section count unchanged, block count inside section [2] grows
   by the 1→subhead+para splits; storm/mold parser counts unchanged
   for fixes 8/9 (render carry-over).
3. **Word-diff green:** `qa1` must stay at miss = 0 (set comparison)
   on all 46 pages after rebuild — including contact `tap` still
   present (fix 5) and no group-heading words lost (fixes 8/9 carry
   both the group H2 text and the label text into the next section).
4. **Visual re-view (desktop + mobile) of every changed band:**
   mold Signs list (4 bullets, closing para under it); insurance
   Mistakes list (5 bullets, closing para under it); contact Hours /
   Service-area bold lead, What-to-Have-Ready list (7 items) →
   What Happens After You Call H2, Emergency section with the
   Tap-to-Call button inside it and **no** post-hero strip, form intro
   starting "Use this form for questions…"; cost 4 Things (all four
   at H3, Category 3 listhead/list still sitting between factors 2
   and 3 in place); storm Creeks and mold Warm Indoor Temperatures
   sections opening with the group kicker + label lead and **no**
   lone beige band before them.
5. **Split-image re-check:** fixes 8/9 (render carry-over) must leave
   split attachment unchanged — confirm by screenshot; if the
   parser-side alternative is used instead, re-screenshot every split
   on storm and mold (attachment shifts by one section, see fix 8).
6. **Explicit non-regressions:** Hours H3 under "How to Reach Us"
   unchanged (fix 3 must not touch it); step (b) "See"-heading handling
   unchanged (fix 4 tail); step (d) items 3–4 subheads unchanged in
   wording and order (fix 7 builds on them); area at-a-glance shells'
   `_subhead_only` rendering unchanged (fixes 8/9 scoped to
   `_GROUP_INTRO` headings only).

## What this plan deliberately does NOT propose

- No deletion, reordering, or paraphrasing of doc words (except fix 6's
  authorized duplicate-heading strip, where the string survives as the
  form H2).
- No change to `is_heading_candidate`, `list_like_para`, `join_items`,
  or `_join_segs` — the shared predicates stay untouched; every fix is
  scoped by slug, exact string, or a diff-gated narrow guard.
- No new generic "heading after a list = list item" or "split every
  numbered para" rule (both rejected above with reasons).
- No build, push, deploy, domain, DNS, or token action — this plan is
  for the local fix pass only, to be verified by the gates above
  before any rebuild is claimed complete.
