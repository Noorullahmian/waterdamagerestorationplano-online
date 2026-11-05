# PLANO 3 ROUND 4 — BATCH D HUNT REPORT (read-only, local only)

Pages (9): allen, mckinney, richardson, murphy, warm-spot-on-floor,
fans-wont-dry-walls, water-damage-cost, ceiling-dripping, copper-pinhole-leaks.
No generator/build file edited, no rebuild, BLUNDER_HUNT.md untouched,
no push/deploy/domain/DNS/token. Server killed after the hunt.

## Method

- Served `~/workspace/plano3-water-damage/out/` with
  `python3 -m http.server 8904` (killed when done).
- Playwright Chromium at
  `~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`,
  flags `--no-sandbox --disable-gpu --disable-dev-shm-usage`.
- Viewports desktop 1440x900 + mobile 390x844, plus overflow sweeps at
  320 and 768. Every page slow-scrolled to settle lazy images/GSAP reveals
  before shooting.
- TRUE viewport shots per image, per H2, hero, related grid and footer —
  no stitched full-page shot used as evidence for any line.
  296 shots under `screenshots/round4/batch-d/`.
- Every shot below was viewed by eye; every unique image file (41) was also
  viewed as source pixels. File/alt claims alone were never treated as evidence
  (two alt claims were wrong on pixels: 3708564 "Abstract image" is in fact a
  real stained ceiling corner; 9462163's alt does not warn that the photo is
  a mopping/cleaning shot).

## DOM checks per page (built out/ HTML + browser overflow)

Banned set checked = full `gen3_render.py` BANNED set (R1+R2+R3, incl.
water-heater-6436774) — not just the 5-file R3 DOM subset.

- allen: imgs 10, same-page dups [], banned [], favicon link yes,
  iframe NO (map ABSENT, correct for area page), dot bullets no,
  empty li no, dangling See H2 no, H2 17, lists 1x[2 bullets]
- mckinney: imgs 9, dups [], banned [], favicon yes, iframe NO (map ABSENT,
  correct), dot bullets no, H2 18, lists 1x[1]
- richardson: imgs 8, dups [], banned [], favicon yes, iframe NO (map ABSENT,
  correct), dot bullets no, H2 17, lists 1x[1]
- murphy: imgs 10, dups [], banned [], favicon yes, iframe NO (map ABSENT,
  correct), dot bullets no, H2 18, lists 0
- warm-spot-on-floor: imgs 7, dups [], banned [], favicon yes, iframe YES
  (map PRESENT, correct for guide page), dot bullets no, H2 11, lists 1x[2]
- fans-wont-dry-walls: imgs 8, dups [], banned [], favicon yes, iframe YES
  (map PRESENT, correct), dot bullets no, H2 11, lists 1x[6]
- water-damage-cost: imgs 8, dups [], banned [], favicon yes, iframe YES
  (map PRESENT, correct), dot bullets no, H2 8, lists 2x[3,1]
- ceiling-dripping: imgs 5, dups [], banned [], favicon yes, iframe YES
  (map PRESENT, correct), dot bullets no, H2 8, lists 2x[4,7]
- copper-pinhole-leaks: imgs 6, dups [], banned [], favicon yes, iframe YES
  (map PRESENT, correct), dot bullets no, H2 10, lists 4x[1,1,3,5]
- Overflow: 0 at 320 / 390 / 768 / 1440 on all 9 pages (scrollWidth ==
  innerWidth at every width).
- No same-page duplicate image on any page; no same-shoot near-duplicate
  pair on any single page (warm-spot's two outdoor pipe photos and copper's
  three pipe photos are different pipes/framings, not one shoot).
- No visible stock-sales figcaption on any page. (3708564's alt says
  "Abstract image of..." but related cards carry no visible figcaption, so
  no visible stock wording; the alt text itself is misleading, see notes.)

## Blunder lines

- Page: warm-spot-on-floor | Section: Hero | Blunder: Hero photo is a person mopping a wood floor with a Swiffer-style mop, bare feet prominent, floor dominant — it reads as house-cleaning, not slab-leak detection or drying, and bare feet on the floor contradicts the page's own barefoot-warm-patch safety framing | Fix: Swap the hero to a slab-leak/drying photo (warm-spot test, thermal scan, or under-floor drying work); do not reuse any cleaning-activity photo | How it was set: Hero picked from the hardwood-floor pool without a cleaning-activity exclusion; 9462163 was flagged as a watch item and fails on viewed pixels | Re-view: NOT YET
- Page: ceiling-dripping | Section: Hero | Blunder: Hero is a dry, pristine finished attic room (brick walls, clean wood floor, windows, no water, no stain, no drip) on a page titled "Water Dripping From the Ceiling" — first impression is a real-estate attic conversion, not water damage | Fix: Swap the hero to a drip/stain photo (the worn-ceiling split photo already on this page shows a stained ceiling and would fit) | How it was set: Hero picked from the attic-insulation pool as a location shot with no damage-visible check | Re-view: NOT YET
- Page: water-damage-cost | Section: Estimated Cost by Situation (split image) | Blunder: Split photo suburban-home-25798114 is a Mediterranean villa — red tile roof, white stucco, timber balcony brackets, olive trees in the foreground — not a Plano/North Texas home, captioned only "Suburban home exterior in a residential neighborhood" | Fix: Swap to a North Texas brick/stone suburban home photo (same language as the page's brick hero) | How it was set: Split rotation picked a suburban-home pool file with no place-architecture check | Re-view: NOT YET
- Page: allen | Section: Related Services & Guides (Flood & Storm Water Cleanup card) | Blunder: Card photo flooded-floor-28447774 is a European village flood scene — white stucco house with three gabled dormers, tiled roof, red ornamental metal fence, muddy street — no North Texas cues, on an Allen area page | Fix: Swap the flood card to a North Texas flood/storm photo (brick home, creek or street flooding) | How it was set: Card rotation picked the flooded-floor pool file with no place-architecture check; same file on all 4 area pages | Re-view: NOT YET
- Page: mckinney | Section: Wilson Creek and the East Fork (split image) | Blunder: Split photo flooded-floor-28447774 is the same European village flood scene — white stucco dormered house, red metal fence, muddy street — used as the creek/flood illustration for McKinney | Fix: Swap to a North Texas creek/storm-runoff photo | How it was set: Split rotation picked the flooded-floor pool file with no place-architecture check | Re-view: NOT YET
- Page: murphy | Section: Related Services & Guides (Flood & Storm Water Cleanup card) | Blunder: Card photo flooded-floor-28447774 is the same European village flood scene — white stucco dormered house, red metal fence, muddy street — on a Murphy/Parker/Wylie area page | Fix: Swap the flood card to a North Texas flood/storm photo | How it was set: Card rotation picked the flooded-floor pool file with no place-architecture check | Re-view: NOT YET
- Page: richardson | Section: Related Services & Guides (Flood & Storm Water Cleanup card) | Blunder: Card photo flooded-floor-28447774 is the same European village flood scene — white stucco dormered house, red metal fence, muddy street — on a Richardson area page | Fix: Swap the flood card to a North Texas flood/storm photo | How it was set: Card rotation picked the flooded-floor pool file with no place-architecture check | Re-view: NOT YET
- Page: allen | Section: Related Services & Guides (Slab Leak Water Damage card) | Blunder: Card photo ceiling-stain-3708564 is a cracked, stained concrete ceiling — a ceiling image on a card linking to slab-leak (under-floor) damage; the linked service's subject (floor/slab) is nowhere in the photo | Fix: Swap the slab-leak card to a floor/slab photo (warm floor, under-floor drying, slab work) | How it was set: Related-card image assigned from rotation with no service-topic match check for the linked service | Re-view: NOT YET
- Page: mckinney | Section: Related Services & Guides (Slab Leak Water Damage card) | Blunder: Same ceiling-stain-3708564 card photo on the slab-leak link — cracked stained ceiling, not a floor/slab subject | Fix: Swap the slab-leak card to a floor/slab photo | How it was set: Related-card image assigned from rotation with no service-topic match check | Re-view: NOT YET
- Page: richardson | Section: Related Services & Guides (Slab Leak Water Damage card) | Blunder: Same ceiling-stain-3708564 card photo on the slab-leak link — cracked stained ceiling, not a floor/slab subject | Fix: Swap the slab-leak card to a floor/slab photo | How it was set: Related-card image assigned from rotation with no service-topic match check | Re-view: NOT YET
- Page: murphy | Section: Related Services & Guides (Slab Leak Water Damage card) | Blunder: Same ceiling-stain-3708564 card photo on the slab-leak link — cracked stained ceiling, not a floor/slab subject | Fix: Swap the slab-leak card to a floor/slab photo | How it was set: Related-card image assigned from rotation with no service-topic match check | Re-view: NOT YET
- Page: warm-spot-on-floor | Section: Related Services & Guides (Slab Leak Water Damage card) | Blunder: Same ceiling-stain-3708564 card photo on the slab-leak link — cracked stained ceiling, not a floor/slab subject, on the very page about under-floor slab leaks | Fix: Swap the slab-leak card to a floor/slab photo | How it was set: Related-card image assigned from rotation with no service-topic match check | Re-view: NOT YET
- Page: copper-pinhole-leaks | Section: Related Services & Guides (Slab Leak Water Damage card) | Blunder: Same ceiling-stain-3708564 card photo on the slab-leak link — cracked stained ceiling, not a floor/slab subject | Fix: Swap the slab-leak card to a floor/slab photo | How it was set: Related-card image assigned from rotation with no service-topic match check | Re-view: NOT YET
- Page: copper-pinhole-leaks | Section: The 60-Second Answer for Plano Homeowners + From the inside: | Blunder: The 60-second list promises pressure "from two directions" but renders only ONE bullet ("From the outside: ..."); the second direction was promoted to a standalone full H2 band "From the inside:" with a single paragraph that then duplicates the later "Why the Water Matters Too" section (same hard-water/chloramine pitting point) | Fix: Demote "From the inside:" to the second bullet of the 60-second list (bold lead, same wording) and delete the standalone H2 band; keep "Why the Water Matters Too" as the full water-chemistry section | How it was set: List parser promoted the second bullet's lead to H2 instead of keeping it as bullet 2 | Re-view: NOT YET
- Page: copper-pinhole-leaks | Section: Which Plano Homes Are Most at Risk | Blunder: Under the listhead "North Plano (75025):" the bullets run North Plano, then "West Plano (75093): larger homes..." then "East Plano (75074): older homes..." — West and East Plano presented as sub-items of North Plano, which is geographically wrong | Fix: Give West Plano and East Plano their own listheads (same pattern as Central/North) or move them out of the North Plano list | How it was set: Parser kept trailing area bullets under the first area's listhead instead of splitting on each "Area (ZIP):" lead | Re-view: NOT YET
- Page: ceiling-dripping | Section: Get out from under it and call | Blunder: H2 is a sentence fragment — "Get out from under it and call" — and the whole section body is a single line, "(972) 472-7917. See ceiling leak water damage and our sagging ceiling safety guide." The heading is half a sentence whose object (the phone number) sits in the body | Fix: Demote to a bold lead paragraph ("Get out from under it and call (972) 472-7917...") or complete the heading; do not leave a fragment H2 over a one-line section | How it was set: Parser split the opening safety sentence into H2 + body line | Re-view: NOT YET
- Page: ceiling-dripping | Section: Quick Diagnosis Table | Blunder: H2 promises a table ("Quick Diagnosis Table") but no table renders — the section body is an H3 essay ("Why Fixing the Source Doesn't Fix the Ceiling") plus prose about wet insulation; there are no diagnosis rows anywhere in the section | Fix: Either render the diagnosis rows as a real table/list under this H2 or rename the H2 to match the essay body (e.g. fold it under the "Why Fixing..." H3) | How it was set: Doc heading carried over while its table rows were rendered as prose under the following H3 | Re-view: NOT YET
- Page: allen | Section: What Allen Homeowners Search When Water Hits | Blunder: Fragmented list — five search queries render inline as one dense paragraph, then the last query breaks out as a bold listhead ("ceiling leak after hail Allen":) plus 2 bullets ("attic drying and insulation removal", "creek water in house Allen"), so the section ends in a dangling mini-list that looks like leftovers, not a designed list | Fix: Render all seven queries uniformly — either all as bullets or all inline — with the link-carrying queries keeping their links | How it was set: Parser converted only the link-carrying trailing queries into listhead+bullets and left the rest inline | Re-view: NOT YET
- Page: mckinney | Section: What McKinney Homeowners Search When Water Hits | Blunder: Same fragmentation — six queries inline as one paragraph, then the last query breaks out as a bold listhead ("hardwood floor water damage McKinney":) plus a single bullet ("mat drying. See hardwood floor drying."), a lone dangling bullet after a full paragraph | Fix: Render all queries uniformly (all bullets or all inline) | How it was set: Parser converted only the link-carrying trailing query into listhead+bullet | Re-view: NOT YET
- Page: richardson | Section: What Richardson Residents Search When Water Hits | Blunder: Same fragmentation — six queries inline as one paragraph, then the last query breaks out as a bold listhead ("musty smell old house Richardson":) plus a single bullet ("a thermal scan finds hidden moisture. See moisture mapping.") | Fix: Render all queries uniformly (all bullets or all inline) | How it was set: Parser converted only the link-carrying trailing query into listhead+bullet | Re-view: NOT YET
- Page: warm-spot-on-floor | Section: How Under-Floor Drying Works | Blunder: Same fragmentation inside a method section — the first two methods ("Thermal mapping:", "Floor-by-floor method:") render as inline prose, then "Walls and cabinets:" appears as a bold listhead with the last two methods as bullets below it, so one 4-method section uses two treatments | Fix: Render all four methods uniformly (one 4-bullet list, or all as bold-lead prose) | How it was set: Parser converted only the link-carrying trailing methods into listhead+bullets | Re-view: NOT YET

## Per-page confirmations

- allen (3 lines): Passed — hero is a US suburban house with car/lawn (fits
  Allen); splits 26595553 (modern white house), 8278493 (modern white home),
  7924140 (flooded modern stairs, water dominant) all fit; cabinet card
  (white kitchen) and appliance card (fridge/ice-maker kitchen) match their
  links; hardwood card 3935327 shows the service subject (hardwood floor);
  at-a-glance + calendar folds render as H2+H3 shells per doc structure;
  footer clean, no map (correct), no overflow, no banned/dup/dot-bullet.
  Borderline passed, not flagged: 8624464 AC card is a dated bedroom but the
  water stain on the wall is prominent and on-topic.
- mckinney (3 lines): Passed — H1 "McKinney, TX" does NOT orphan TX (both on
  one line in the hero shot); hero is a stone Texas home; splits 7587470
  (brick two-story), 33404353 (wood-frame new build, fits new-construction
  McKinney) fit; flood card 29608837 (storm drain + downpipe) fits;
  laundry card (washer) and inspector card (8293746, kneeling at baseboard)
  fit their links; no overflow, no banned/dup/dot-bullet, map absent (correct).
- richardson (3 lines): Passed — hero is a classic brick North Texas house
  with lawn; splits 3990589 (brick house), 8278494 (Texas street row houses),
  35188667 (night office tower, fits Telecom Corridor) fit; sewage card
  3964564 (drain pipe on concrete wall) fits the drains slot; burst card
  4406597 (rusted tube dripping over lawn) fits; no overflow, no banned/
  dup/dot-bullet, map absent (correct).
- murphy (2 lines): Passed — hero is a brick/stucco two-story (fits newer
  subdivisions); splits 32711440 (brick house), 23928963 (stone luxury street
  scene with car/driveway — Texas luxury-suburb plausible), 7924140 (flooded
  stairs) fit; water-heater card 34593293 is a real heater tank (R3-noted
  pool-limited solar unit, not a new defect); search section is uniformly
  inline (all queries as sentences, no trailing fragment) — dense but
  consistent, so no fragmentation line here; no overflow, no banned/dup/
  dot-bullet, map absent (correct).
- warm-spot-on-floor (3 lines): Passed — splits 15206136 (leaking plastic
  pipe, rag-wrapped joint) and 36571568 (rusty elbow dripping) are different
  pipes, not a same-shoot pair; brick-house split 3990589 fits; mold card
  9127236 (algae wall) fits; mobile stacks cleanly, no overflow at any
  width; map present (correct); no banned/dup/dot-bullet.
- fans-wont-dry-walls (0 lines, CLEAN): Passed — R1-3 fix HOLDS: Signs list
  is 6 bullets incl. "Allergy symptoms that seem worse in one room", tail
  NOT promoted to H2, closing para "If you see any of these, the hidden
  moisture is still there. See our mold clock guide." joined with its link;
  hero is a genuinely peeling/damaged wall (fits hidden wall moisture);
  splits 9127236 (algae wall), 8293746 (inspector at baseboard),
  29701042 (peeling wall + downpipe + grass) all fit; related cards
  (inspector, worn ceiling, brick house, flooded stairs) match their links;
  no overflow, no banned/dup/dot-bullet, map present (correct).
- water-damage-cost (1 line): Passed — R1-3 fix HOLDS: factor sequence 1-4
  intact (1 Square Footage + 2 Water Category inline in the intro paragraph,
  Category 3 as listhead+bullet, 3 How Hard It Is to Dry + 4 How Many Days
  as H3s); hero is a brick Plano-style house; inspector split 8293746,
  plumber-hands split 6419128, inspector card 8961700, algae-wall card
  9127236, office card 5483188, valve-panel card 11658940 all fit their
  slots/links; no overflow, no banned/dup/dot-bullet, map present (correct).
- ceiling-dripping (3 lines): Passed — R1-3 fix HOLDS: lists rejoined
  (Crew Arrives 4 bullets in one list; Specific Help 7 bullets in one list,
  first source as listhead + link bullet, rest as labelled bullets);
  splits 14032089 (worn stained ceiling + lamp) and 3708564 (cracked stained
  ceiling corner — real ceiling on pixels despite its "Abstract image" alt)
  fit; attic split 8082327 (retained use) passes as attic-location context
  inside the attic-sources section; related grid is a single card but
  CENTRED (known artifact, not a defect); footer map grey in headless is
  the known tile-render artifact, not a defect; no overflow, no banned/dup/
  dot-bullet, map present (correct).
- copper-pinhole-leaks (3 lines): Passed — R1-3 fix HOLDS in part: Repair
  Options reads as one joined paragraph (Spot repair / Reroute / Whole-home
  repipe, no dangling See link, no fragment); After the Repair is a clean
  5-bullet list with links joined inline; hero is a spraying burst pipe
  (perfect topic fit); splits 4406597 (rusted tube dripping over lawn),
  3990589 (brick house), 6419128 (plumber hands, no face) fit; burst card
  36571568 (dripping elbow) fits; no overflow, no banned/dup/dot-bullet,
  map present (correct). Minor observation, not a line: in Repair Options
  only "Spot repair:" is bold while "Reroute:"/"Whole-home repipe:" are not.

## Watch-item / retained-use re-checks (all viewed on pixels)

- hardwood-floor-9462163 (warm-spot hero): FAILS — mopping/cleaning activity,
  bare feet dominant. Line recorded above.
- flooded-floor-28447774 (all 4 area pages): FAILS — European dormered
  house + fence + street. Lines recorded above.
- Heavy reuse, still fitting per slot (no line): ceiling-stain-3708564 x7 in
  batch (6 slab cards flagged for topic mismatch, but the ceiling-dripping
  split use itself fits); hardwood-floor-3935327 x4 (all hardwood-drying
  cards — floor is the service subject); moisture-meter-8293746 x4
  (inspector shots, fit); flooded-floor-7924140 x3 (flood water dominant,
  fits); ceiling-stain-8624464 x3 (wall stain prominent, fits);
  sewage-drain-3964564 x1 (drain pipe, fits); plumber-work-6419128 x2
  (plumber hands, fits); mold-wall-29701042 x1 (peeling wall + downpipe, fits).
- Retained uses deliberately NOT globally banned, each re-checked and
  STILL FITTING its slot: moisture-meter-8961700 x2 (fans structural card,
  cost structural card — worker inspecting a wall, reads as professional
  inspection; no meter visible but context fits); attic-insulation-8082327
  x1 (ceiling Specific Help split — attic location for attic sources);
  hardwood-floor-3935327 x4 (see above); mold-wall-9127236 x3 (fans 60-sec
  split, cost mold card, warm mold card — algae/cracked wall, fits);
  plumber-work-35290675: 0 occurrences in batch D.
- Files with 0 occurrences in batch D (not re-checkable here): 6124239,
  35290675.

## Known artifacts NOT recorded as blunders

- Headless Google Map tiles render blank/grey (guide footers) — embed
  present, live render owed, not a defect.
- Ceiling single-card related grid is centred (R1 fix) — thin but centred.
- Doc-structure single-sentence / H2+H3-only sections (area at-a-glance,
  calendar folds) — no invented copy, not defects.
- Uniform dense paragraphs (area "Do These 5 Things", ceiling "3 Clues",
  cost factors 1-2 inline) — doc paragraph style, readable, bold leads
  present; only MIXED paragraph+trailing-bullet fragmentation was flagged.
