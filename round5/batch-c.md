# PLANO 3 — ROUND 5 HUNT, BATCH C (read-only)

Pages (9, ONLY these): moisture-mapping, attic-insulation-drying, wall-drying,
west-plano, legacy-west, north-plano, central-plano, east-plano, frisco.

## Method

- Build hunted: `~/workspace/plano3-water-damage/out/` (final Round 4 fix-pass build).
  No rebuild, no edits to any build file, no push/deploy/domain/DNS/token.
- Served locally by the hunter: `python3 -m http.server 8913` from `out/`
  (server killed when the hunt finished).
- Browser: Playwright Chromium headless, executable
  `~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`,
  flags `--no-sandbox --disable-gpu --disable-dev-shm-usage`.
- Viewports: desktop 1440x900 + mobile 390x844 for screenshots; every page
  additionally re-loaded at 320, 390, 768 and 1440px for overflow
  (`documentElement.scrollWidth` vs viewport width).
- Settling: two slow-scroll passes per page (700–900px steps) before shooting,
  so lazy images and GSAP reveals settled before any screenshot.
- Evidence rule: every blunder line below has a TRUE viewport screenshot
  (image scrolled into view, then a viewport shot) in
  `~/workspace/plano3-water-damage/screenshots/round5/batch-c/`.
  No stitched full-page shot is used as evidence for any line.
  Pixel judgments were additionally confirmed against the source files in
  `out/images/` (identical pixels to the rendered shots).
- Static checks per page (from `out/<slug>/index.html`): H1 count, favicon link,
  iframe count (map rule), same-page image `src` duplicates, banned-file
  substrings, `•` bullets, empty H2/H3, `<li>` fragments (short/dangling "See"),
  figure captions vs pixels, and card-to-title mapping (card titles FOLLOW
  their images inside each `article.card` — preceding-heading mapping is wrong
  for cards and was corrected by parsing the card articles directly).

## DOM-checks table

Overflow columns are `scrollWidth` at that viewport width (equal = 0 overflow).
Map rule: iframe PRESENT on the 3 service pages, ABSENT on all 6 area pages.
Banned checked: R1–R3 set incl. `6436774`, plus R4 bans `28447774`, `9462163`,
`8082327`, `8961700`. NOTE: `moisture-meter-8961703` (moisture hero) is NOT the
banned `8961700` file, and `crawl-space-17181949` is NOT the banned `28447774`
file — both are different files and pass the banned check.

| Page | H1 | Ovf 320 | Ovf 390 | Ovf 768 | Ovf 1440 | Favicon | Map iframe | Same-page dup | Banned | Dot bullets | Empty H2/H3 | Broken imgs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| moisture-mapping | 1 | 320=0 | 390=0 | 768=0 | 1440=0 | yes | 1 (PRESENT, correct for service page) | 0 (5 imgs, 5 unique) | none | 0 | 0 | 0 |
| attic-insulation-drying | 1 | 320=0 | 390=0 | 768=0 | 1440=0 | yes | 1 (PRESENT, correct for service page) | 0 (8 imgs, 8 unique) | none | 0 | 0 | 0 |
| wall-drying | 1 | 320=0 | 390=0 | 768=0 | 1440=0 | yes | 1 (PRESENT, correct for service page) | 0 (9 imgs, 9 unique) | none | 0 | 0 | 0 |
| west-plano | 1 | 320=0 | 390=0 | 768=0 | 1440=0 | yes | 0 (ABSENT, correct for area page) | 0 (10 imgs, 10 unique) | none | 0 | 0 | 0 |
| legacy-west | 1 | 320=0 | 390=0 | 768=0 | 1440=0 | yes | 0 (ABSENT, correct for area page) | 0 (10 imgs, 10 unique) | none | 0 | 0 | 0 |
| north-plano | 1 | 320=0 | 390=0 | 768=0 | 1440=0 | yes | 0 (ABSENT, correct for area page) | 0 (10 imgs, 10 unique) | none | 0 | 0 | 0 |
| central-plano | 1 | 320=0 | 390=0 | 768=0 | 1440=0 | yes | 0 (ABSENT, correct for area page) | 0 (9 imgs, 9 unique) | none | 0 | 0 | 0 |
| east-plano | 1 | 320=0 | 390=0 | 768=0 | 1440=0 | yes | 0 (ABSENT, correct for area page) | 0 (6 imgs, 6 unique) | none | 0 | 0 | 0 |
| frisco | 1 | 320=0 | 390=0 | 768=0 | 1440=0 | yes | 0 (ABSENT, correct for area page) | 0 (10 imgs, 10 unique) | none | 0 | 0 | 0 |

List/heading hygiene (all 9 pages): no short (`<=3` char) list items, no
dangling "See" list items, no lone "." or "•" bullets, no heading promotion of
labels/tails/fragments, no empty H2/H3 shells, no post-hero lone-button bands.
All "See …" links inside body lists resolve to real linked phrases.
Displayed image sizes are sane everywhere (heroes 557x313, body figures
1198x674, related cards 386x217; east-plano's 2-card row renders 358x201 —
a wider 2-card grid, not a defect). All images natural size 1200x800, none
broken, none zero-display.

## Blunder lines (14)

- Page: moisture-mapping | Section: How Thermal Imaging Finds Hidden Water (body figure) | Blunder: Figure ceiling-stain-8624464 shows a dated, foreign-looking interior — striped wallpaper, lace-curtained French doors, framed landscape paintings, floral sofa — not a Plano/Texas home interior, and the stain is fully visible while the section is about hidden water found by thermal imaging (evidence: moisture-mapping-d-img02-ceiling-stain-8624464.png) | Fix: Swap to a Plano-style lived-in interior with a water stain, or to a thermal-camera/moisture-reading shot; keep the figure caption honest to the new pixels | How it was set: Pool rotation without a place-fit check — file reused for its "stain" keyword while its room reads as an old European flat | Re-view: NOT YET
- Page: moisture-mapping | Section: Common Hidden Leaks in Plano Homes (body figure) | Blunder: Figure ceiling-stain-14032089 shows a derelict, empty room — widespread peeling paint across the whole ceiling, stained walls, a rusty hanging lamp, warm/dark abandoned tone — contradicting the "Plano Homes" lived-in context; the copy never says abandoned or derelict (evidence: moisture-mapping-d-img03-ceiling-stain-14032089.png) | Fix: Swap to ceiling water damage in a lived-in Plano home (stain/drip, furniture present, daylight) | How it was set: Retained heavy-reuse watch file carried forward without a tone check — damage subject correct, derelict tone wrong | Re-view: NOT YET
- Page: attic-insulation-drying | Section: Wet Insulation in Your Plano Attic? Do These 5 Things (body figure) | Blunder: Same ceiling-stain-14032089 derelict-ceiling file as moisture-mapping, here under a safety-tips section (step on joists, clear the room below, turn off lights) — the photo illustrates none of the tips and repeats the abandoned-room tone (evidence: attic-insulation-drying-d-img01-ceiling-stain-14032089.png) | Fix: Swap to an attic-safety subject (joists/walkway, sagging ceiling from below with a room underneath) or drop the figure from the tips section | How it was set: Same retained watch file reused into a second, weaker context without a section-fit check | Re-view: NOT YET
- Page: attic-insulation-drying | Section: Attic Water Heaters (body figure) | Blunder: Figure crawl-space-4092030 shows a water-heater tank in an unfinished BASEMENT — block walls, basement stairs, basement windows, concrete floor — while the section copy is about a 40–50 gallon tank failing in the attic and spilling into insulation; the setting directly contradicts "attic" (evidence: attic-insulation-drying-d-img02-crawl-space-4092030.png; caption itself says "unfinished basement") | Fix: Swap to a tank actually photographed in an attic (roof slope, joists, insulation visible) | How it was set: Pool rotation matched the "water heater tank" keyword and ignored the room — filename prefix (crawl-space) already signalled the wrong setting | Re-view: NOT YET
- Page: attic-insulation-drying | Section: Attic AC and Frozen Pipes (body figure) | Blunder: Figure attic-insulation-4482829 shows an open skylight/roof window with blue sky and clouds and dry foil insulation — no AC unit, no AC pan, no pipe, no water — while the section copy is about overflowing AC pans and split attic pipes dumping dozens of gallons into insulation (evidence: attic-insulation-drying-d-img03-attic-insulation-4482829.png) | Fix: Swap to an attic AC air handler/pan or a split pipe in an attic with wet insulation | How it was set: Pool rotation matched the "attic" keyword only; the subject (sky) was never checked against the section's AC/pipe subject | Re-view: NOT YET
- Page: wall-drying | Section: Drywall Wicks Water Up (body figure) | Blunder: Figure mold-wall-9127236 shows a close-up of an EXTERIOR weathered masonry wall covered in green algae/moss with a large crack — not interior drywall — while the figure caption claims "Mold and moisture damage on drywall that wicks water upward" and the section copy is about paper-faced drywall wicking 1–2 inches an hour from the plate; pixels contradict both caption and section (evidence: wall-drying-d-img02-mold-wall-9127236.png) | Fix: Swap to interior drywall wicking/staining at the base of a wall and rewrite the caption to match the new pixels | How it was set: Caption was written to the section claim rather than the pixels; the file's "mold-wall" keyword masked that it is outdoor algae on masonry | Re-view: NOT YET
- Page: wall-drying | Section: Think Your Plano Walls Got Wet? Check These 5 Things (body figure) | Blunder: Figure moisture-meter-8293746 is the same shoot as moisture-mapping's moisture-meter-8293640 — same inspector in hi-vis vest and yellow hard hat, same kneeling pose at the same outlet/baseboard in the same light-wood-floor room, only a tighter crop and a different file number — so the two service pages show what reads as the same inspection twice; exact-file exclusion cannot catch it because the files differ (evidence: wall-drying-d-img01-moisture-meter-8293746.png vs moisture-mapping-d-img01-moisture-meter-8293640.png) | Fix: Swap one of the pair (wall-drying preferred — the moisture page is the inspection service's own page) to a different wall-check subject | How it was set: Same-shoot split across pages — two crops of one shoot entered the pool as separate files and were assigned to two pages without a same-shoot check | Re-view: NOT YET
- Page: west-plano | Section: Hero | Blunder: Hero suburban-home-7587470 shows a large brick estate behind an ornate iron gate and brick fence, steep dark tile roof, pine-forest backdrop and a second foreign-style house — reads as an Eastern-European suburban estate, not a Willow Bend / West Plano home; the copy sells high-value Willow Bend finishes and gated 75093 streets, and the photo's gate, roof and pines do not read as Texas (evidence: west-plano-d-top.png, west-plano-d-img00-suburban-home-7587470.png) | Fix: Swap the hero to a Willow Bend-style Texas brick home (shingle roof, driveway, lawn, no iron estate gate) | How it was set: Hero pool matched "elegant brick house" without a place-fit check against the Willow Bend context | Re-view: NOT YET
- Page: legacy-west | Section: Stacked Living Around Legacy West (body figure) | Blunder: Figure flooded-floor-7924140 shows a modern white staircase with glass balustrade standing in dark floodwater inside a commercial/public-looking space (velvet rope, a bird on the step) — it does not show stacked living, townhomes or condos, and it reuses the known pool-limited fire-hero flooded-stairs file in an unrelated housing-type section (evidence: legacy-west-d-img03-flooded-floor-7924140.png) | Fix: Swap to a Legacy West townhome/stacked-living exterior or interior stairwell without floodwater | How it was set: Flood-water keyword reuse — the file was pulled for "water" while its subject (commercial stairs) fits neither stacked living nor a home | Re-view: NOT YET
- Page: north-plano | Section: Hero | Blunder: Hero suburban-home-30707539 shows a brick house with a red tile roof, white-framed windows, brown winter hedges and flat overcast light, with a second tile-roof house behind — reads as a Northern-European brick house, not a North Plano / Whiffletree / Russell Creek home; the copy dates 75025 homes to the early 1980s–late 1990s, and the tile roof and hedge row do not read as Texas (evidence: north-plano-d-top.png, north-plano-d-img00-suburban-home-30707539.png) | Fix: Swap the hero to a North Plano brick suburb home (shingle roof, garage, lawn, Texas daylight) | How it was set: Hero pool matched "cozy red brick house" without a place-fit check | Re-view: NOT YET
- Page: central-plano | Section: Hero | Blunder: Hero suburban-home-32711440 shows a steep-gabled brick house with tall angled windows, overhead power lines and a metal chimney pot — reads as a Northern-European modern brick house, not a Central Plano home; the copy says Central Plano was mostly built early 1970s–1990 as ranch homes, and this steep modern gable contradicts that era as well as the place (evidence: central-plano-d-top.png, central-plano-d-img00-suburban-home-32711440.png) | Fix: Swap the hero to a Central Plano ranch/brick home (low profile, shingle roof, driveway) | How it was set: Hero pool matched "charming brick house" without a place- or era-fit check | Re-view: NOT YET
- Page: central-plano | Section: Related Services & Guides — Sewage Backup Cleanup card | Blunder: Card kitchen-leak-10961064 shows a close-up of a clean, wet stainless-steel sink with a wrench — a pristine fixture, no sewage, no drain backup, no toilet — as the image for "Sewage Backup Cleanup", a service whose whole identity is contaminated wastewater; the clean sink misleads about the service (evidence: central-plano-d-img04-kitchen-leak-10961064.png) | Fix: Swap the card image to a sewer/drain subject (floor drain, sewer cleanout, backup-affected bathroom) | How it was set: Card pool assigned a generic "wet plumbing" file to a specific contaminated-water service without a subject check | Re-view: NOT YET
- Page: east-plano | Section: Hero | Blunder: Hero suburban-home-25798114 shows a Mediterranean villa — bright red/orange tile roof, white stucco walls, wooden balcony brackets, olive trees — while the copy sells East Plano's oldest homes, historic pier-and-beam houses near Haggard Park and 1960s ranch slabs in Los Rios; the villa reads as Southern-European hillside, not East Plano (evidence: east-plano-d-top.png, east-plano-d-img00-suburban-home-25798114.png) | Fix: Swap the hero to an East Plano historic brick home, pier-and-beam house or 1960s ranch | How it was set: Hero pool matched "suburban home exterior" without a place-fit check against the historic/ranch copy | Re-view: NOT YET
- Page: east-plano | Section: Related Services & Guides — Sewage Backup Cleanup card | Blunder: Same kitchen-leak-10961064 clean wet sink + wrench file as central-plano, used again as the "Sewage Backup Cleanup" card image — same contradiction (pristine sink, no sewage or backup) in a second slot (evidence: east-plano-d-img05-kitchen-leak-10961064.png) | Fix: Swap the card image to a sewer/drain subject, ideally a different file from whatever replaces the central-plano card so the two cards do not repeat | How it was set: Same generic card file assigned to the same service on two area pages without a subject check | Re-view: NOT YET

## Per-page confirmations

- moisture-mapping: CONFIRMED except lines 1–2. Hero (8961703, worker touching
  a block wall with red PEX visible) is inspection-plausible — no meter/camera
  visible, but no on-page claim is contradicted, so it is a watch note, not a
  line. Inspector-at-outlet figure (8293640) is topic-exact. Related grid is a
  single centred Slab Leak card (17181949, clean garage concrete floor — the
  pool-limited slab file in a fitting card role, not worse). Map iframe present.
  No list/heading/overflow defects. Mobile footer clear of the call bar.
- attic-insulation-drying: CONFIRMED except lines 3–5. Hero (6124239, worker
  installing pink fiberglass batts) is topic-exact. All 4 related cards are
  topic-correct (solar tank → Water Heater card is the known pool-limited
  water-heater file, same file, not worse; stain detail → Ceiling card;
  warehouse AC units → AC card; dripping pipe → Burst card). Map iframe present.
  No list/heading/overflow defects. Mobile footer clear of the call bar.
- wall-drying: CONFIRMED except lines 6–7. Hero (9043415, attic brick room)
  is the known pool-limited wall hero, same file, not worse — not re-flagged.
  Retained 3935327 room figure PASSES: white baseboards are the visible subject
  along the wall in a clean Plano-style room (see watch verdicts). All 5 related
  cards topic-correct (fan → Structural, garage → Slab, pipe → Burst, washer →
  Laundry, kitchen → Appliance). Map iframe present. No list/heading/overflow
  defects. Mobile footer clear of the call bar.
- west-plano: CONFIRMED except line 8. Body figures 31602311 (red brick suburb
  home) and 186077 (US suburb at dusk) pass; 15303808 is a watch note only
  (Mediterranean arch/tile detailing that is common in Texas luxury builds).
  Related cards topic-correct (AC units → AC, solar tank → Water Heater,
  spraying pipe → Flood is generic water imagery consistent with the site's
  Flood-card pool, room → Hardwood, kitchen → Appliance, garage → Slab).
  No map iframe (correct). No list/heading/overflow defects. Mobile footer
  clear of the call bar.
- legacy-west: CONFIRMED except line 9. Hero (8278493, modern white house,
  metal roof, big glass window) passes for the Legacy West modern context.
  Body figures 3990589 (brick suburb home, basketball hoop) passes; 23930020
  is a watch note only (Tuscan stone/tile styling common in Texas luxury
  builds). Related cards topic-correct. No map iframe (correct).
  No list/heading/overflow defects. Mobile footer clear of the call bar.
- north-plano: CONFIRMED except line 10. Body figures 15303808 (watch note as
  west-plano), 8278493 (modern white house as generic area illustration) and
  186077 (US suburb) pass. Related cards topic-correct, including 9043415
  attic-brick room → Wall Cavity card (walls are the subject) and 31602311
  dry house → Flood card (generic pool fallback, consistent sitewide). No map
  iframe (correct). No list/heading/overflow defects. Mobile footer clear of
  the call bar.
- central-plano: CONFIRMED except lines 11–12. Body figures 31602311, 23930020
  (watch note), 186077 pass. Other related cards topic-correct (garage → Slab,
  spraying pipe → Flood generic, dripping pipe → Burst, stain detail →
  Ceiling). No map iframe (correct). No list/heading/overflow defects. Mobile
  footer clear of the call bar.
- east-plano: CONFIRMED except lines 13–14. Body figures 186077 (US suburb),
  26595553 (brick house, shingle roof, arched windows) and 29608837 (rusty
  pipe at an urban drain with vegetation — fits Old Sewer Lines and Mature
  Trees) pass. Flood card uses 31602311 dry house (generic pool fallback).
  No map iframe (correct). No list/heading/overflow defects. Mobile footer
  clear of the call bar.
- frisco: CONFIRMED, no lines. Hero (8278494, colourful US suburban street,
  garages, SUVs) passes as a Frisco street. Body figures 186077, 23930020
  (watch note) pass; 7924140 flooded stairs under "Creeks and Retention
  Lakes" is a watch note only — floodwater imagery is on-theme for a
  creek-flooding section, unlike legacy-west's housing-type section where it
  contradicts the subject. All 6 related cards topic-correct (garage → Slab,
  solar tank → Water Heater, AC units → AC, house → Flood generic, room →
  Hardwood, white cabinets → Kitchen Cabinet). No map iframe (correct).
  No list/heading/overflow defects. Mobile footer clear of the call bar.

## Watch-item verdicts (retained / heavy-reuse files, re-checked on viewed pixels)

- 9127236 (mold detail, wall-drying body figure): VERDICT WRONG — see line 6.
  Pixels are outdoor algae on masonry, not interior drywall; caption claims
  drywall wicking. This retained file fails on viewed pixels.
- 16243255 (fan, wall-drying Structural Drying card): VERDICT PASS — industrial
  air-mover fan close-up, topic-exact for structural drying.
- 14032089 (worn ceiling, moisture-mapping + attic-insulation-drying body
  figures): VERDICT WRONG — see lines 2–3. Derelict empty-room tone on both
  pages; damage subject correct, tone and (on attic) section fit wrong.
- 3708564 (stain detail, attic-insulation-drying Ceiling card +
  central-plano Ceiling card): VERDICT PASS — cracked, stained concrete
  ceiling corner, topic-exact for ceiling/roof leak in both card slots.
- 35290675 (about split): NOT PRESENT on any batch-C page — no verdict
  possible from this batch; the file was not found in these 9 pages' HTML.
- 3935327 (hardwood hero + slab/wall bodies; here wall-drying body figure +
  west/legacy/north/frisco related cards): VERDICT PASS in batch-C slots —
  bright empty room with visible white baseboards (wall body) and clean
  wood-floor room (hardwood cards); no slot contradicts its section.
- 29701042 (fans body only): NOT PRESENT on any batch-C page — no verdict
  possible from this batch (fans page is not in batch C).
- Pool-limited heroes, re-checked: wall hero attic brick room (9043415) same
  file, not worse — PASS, not re-flagged. Slab file 17181949 in card roles
  (moisture/west/legacy/north/central/frisco Slab cards) — clean garage
  concrete floor fits slab, not worse — PASS. Water-heater solar tank 34593293
  in card roles (attic/west/legacy/north/frisco Water Heater cards) — same
  file, not worse — PASS. Fire-hero flooded stairs 7924140: legacy-west body
  use is a WORSE context (line 9); frisco body use is on-theme for creek
  flooding (watch note, not a line). No other pool-limited hero appears as a
  hero on a batch-C page.

## R4 fix verification (holds in batch C)

- Hero/card chains: no same-page hero/card file collision on any batch-C page
  (same-page duplicates 0 on all 9 pages).
- Same-shoot pairs broken (R4 scope): no same-page same-shoot pair found on
  any batch-C page. NEW cross-page same-shoot pair found (line 7) — different
  files, same shoot, across moisture-mapping and wall-drying; exact-file
  exclusion cannot catch this class.
- Parser lists: no fragmented lists, no dangling "See", no lone "."/"•"
  bullets on any batch-C page (static + rendered checks agree).
- Caption purge: no stock-sales or listing-copy caption tails on any batch-C
  page; figure captions are alt-derived and (except line 6, where the caption
  itself is the false claim) match their pixels.
- Banned files: 0 occurrences of 6436774, 28447774, 9462163, 8082327, 8961700
  in all 9 pages' HTML.

## Artifacts NOT recorded (deliberately excluded)

- Map tiles: map iframe presence/absence was verified per the rule, but tile
  rendering inside the Google embed was NOT judged (pre-existing open item
  from earlier rounds; a blank tile frame in a screenshot is not recorded as
  a defect).
- Lazy-fill blanks that filled on re-scroll: none observed — all 77 page
  images rendered with natural size 1200x800 after the settling scrolls.
- Doc-structure sections: area at-a-glance / calendar / group-intro sections
  whose doc has no intro body are layout folds, not content omissions — no
  line demands invented body copy. No empty band or orphan heading stack was
  found on any batch-C page (group sections render as H2 + body copy).
- Centred thin grids: moisture-mapping's single-card related row, east-plano's
  2-card related row, and 3+1 card wraps on other pages are grid wraps, not
  defects — not recorded.
- Sticky-header clipping in scrolled screenshots: headings appearing cut
  under the sticky header in mid-page viewport shots are an artifact of the
  hunter's scroll offset; headings render fully at natural scroll positions
  (verified on every page-top shot) — not recorded.
- Sticky mobile call bar overlapping hero-image pixels on mobile top shots:
  the bar covers image area, never footer or body text (all 9 mobile footer
  shots show the full legal line above the bar) — not recorded.
- Cross-page reuse of generic pool files (31602311 dry brick house on 6
  pages, 34593293 solar tank on 5, 17181949 garage floor on 6, 186077 suburb
  on 5): same file across pages is the pool pattern, not a same-page
  duplicate, and none of those slots contradicts its section — noted here,
  not lined, except where a slot genuinely contradicts its label (lines 12
  and 14, which are about subject, not reuse).

## Screenshots

104 files in `~/workspace/plano3-water-damage/screenshots/round5/batch-c/`:
per page, `<slug>-d-top.png`, `<slug>-d-imgNN-<file>.png` (one true viewport
shot per image, scrolled into view), `<slug>-m-top.png`,
`<slug>-m-footer.png`. Evidence shots for each line are named in the line.
Total page images hunted: 77 (5 + 8 + 9 + 10 + 10 + 10 + 9 + 6 + 10).
