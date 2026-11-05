# PLANO 3 — ROUND 5 HUNT, BATCH A (read-only)

Pages hunted (9 ONLY): home, emergency-water-damage, water-extraction,
structural-drying, burst-pipe-cleanup, sewage-cleanup, slab-leak,
water-heater-leak, ceiling-leak. No other page was hunted. Nothing was
edited, rebuilt, pushed, or deployed. No build file was touched.

## Method / server / browser / viewports

- Build: `~/workspace/plano3-water-damage/out/` (final Round 4 fix-pass
  build), served locally only with `python3 -m http.server 8911` and
  killed when done (server confirmed stopped, port 8911 dead).
- Browser: Playwright Chromium headless
  `~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`, flags
  `--no-sandbox --disable-gpu --disable-dev-shm-usage`.
- Viewports: desktop 1440x900, mobile 390x844, plus re-loads at 320px and
  768px for overflow (scrollWidth vs viewport width).
- Settling: slow scroll (600px steps) + waits before shooting, so lazy
  images and GSAP reveals settled before every shot.
- Evidence rule kept: every blunder line below has a TRUE viewport
  screenshot (image scrolled into view, then viewport shot). No stitched
  full-page shot is used as evidence. Screenshots:
  `~/workspace/plano3-water-damage/screenshots/round5/batch-a/` (132 files:
  one viewport shot per image slot + desktop/mobile top + mobile footer
  per page).
- Note on one artifact name: `home-desktop-top.png` was shot after the
  per-image scroll pass, so it actually shows the home area-cards region,
  not the page top. It is still a true viewport shot; the genuine home
  top is in `home-mobile-top.png` and `home-img00.png` (hero).
- Card-mapping caution (found during this hunt): on this build a card's
  `<img>` comes BEFORE its `<h3>` title in the DOM. Judging an image by
  the heading above it mis-assigns every card by one slot. All card
  verdicts below use the FOLLOWING heading (image -> its own card title),
  verified against the raw card HTML.

## DOM-checks table per page

H1 = count of `<h1>` in the page. Overflow = scrollWidth at that viewport
width (equal = 0 overflow). Favicon = `<link rel="icon">` present. Map =
`<iframe>` present (non-area pages; all 9 batch-A pages are non-area).
Same-page dup = exact duplicate image files within that page's `<main>`.
Banned = any of the 55-file BANNED set from `gen3_render.py`, which
includes water-heater-6436774 and the R4 bans flooded-floor-28447774,
hardwood-floor-9462163, attic-insulation-8082327, moisture-meter-8961700.
Dot bullets = literal `•` in main text (none on any page; an early regex
hit for a lone `.` turned out to be sentence punctuation between links,
e.g. `</a>. <a`, not a bullet — not recorded). Empty H2/H3 = heading
with no text (none; the `Find Us in Plano, TX` section holds the map
iframe, so it is not an empty shell). Broken images = browser check,
naturalWidth 0 (none on any page). R4 caption-purge strings = 0 hits on
all 9 pages. No same-shoot near-duplicate pair was found within any
single batch-A page (the R4 moisture-meter and crawl-space pairs are
absent).

| Page | H1 | Overflow 320/390/768/1440 | Favicon | Map iframe | Same-page dup | Banned | Dot bullets | Empty H2/H3 | Broken imgs |
|---|---|---|---|---|---|---|---|---|---|
| home | 1 | 320/390/768/1440 (0) | yes | yes | 0 (34 imgs) | 0 | none | none | 0 |
| emergency-water-damage | 1 | 320/390/768/1440 (0) | yes | yes | 0 (10 imgs) | 0 | none | none | 0 |
| water-extraction | 1 | 320/390/768/1440 (0) | yes | yes | 0 (9 imgs) | 0 | none | none | 0 |
| structural-drying | 1 | 320/390/768/1440 (0) | yes | yes | 0 (9 imgs) | 0 | none | none | 0 |
| burst-pipe-cleanup | 1 | 320/390/768/1440 (0) | yes | yes | 0 (10 imgs) | 0 | none | none | 0 |
| sewage-cleanup | 1 | 320/390/768/1440 (0) | yes | yes | 0 (8 imgs) | 0 | none | none | 0 |
| slab-leak | 1 | 320/390/768/1440 (0) | yes | yes | 0 (8 imgs) | 0 | none | none | 0 |
| water-heater-leak | 1 | 320/390/768/1440 (0) | yes | yes | 0 (7 imgs) | 0 | none | none | 0 |
| ceiling-leak | 1 | 320/390/768/1440 (0) | yes | yes | 0 (10 imgs) | 0 | none | none | 0 |

Image display sizes (desktop, measured): heroes 557x313, splits
1198x674, cards 386x217; all source files 1200x800, so no upscaling and
no squashed aspect anywhere in this batch. Mobile heroes stack the image
below the copy with readable text (home-mobile-top, ceiling-leak-mobile-top
viewed); the sticky mobile call bar (58px, bottom) sits below the footer
text and covers no footer copy (home-mobile-footer viewed).

Home final CTA holds: the `Stop the Damage Before It Spreads` section is
`class="block dark"`, built CSS `section.block.dark{background:#0e3a5c;
color:#fff}` — navy background + white text confirmed.

List/heading scan: no dangling "See" bullets, no lone "." or "•" bullets,
no list tails promoted to H2/H3, no empty H2/H3 shells on any batch-A
page. Emergency area H2s ending in colons (e.g. `East Plano (75074,
75094):`) each carry body copy underneath and are label subheads, not
empty shells — not flagged. No post-hero lone-button band on any page
(hero is followed by a checklist/content section, not a bare button).

## Blunder lines (11)

- Page: home | Section: Our Services in Plano, TX — Commercial Water Damage Restoration card | Blunder: card photo ceiling-stain-14032089.webp is a worn residential ceiling with peeling paint and a hanging pendant lamp in a bare room — no office, retail, or commercial interior of any kind, under a Commercial heading (home-img11.png) | Fix: swap this card slot only to a commercial interior/office photo | How it was set: pool reuse — the worn-ceiling file is also the burst/ceiling damage file, and it was placed in the commercial slot where its damage subject does not match the service | Re-view: NOT YET
- Page: home | Section: Our Services in Plano, TX — Fire Sprinkler Water Cleanup card | Blunder: card photo mold-wall-9127236.webp is a close-up of a cracked wall covered in green algae/mold — no sprinkler head, no ceiling, no commercial interior, nothing sprinkler-related (home-img18.png) | Fix: swap this card slot only to a sprinkler-head/ceiling or commercial-interior photo | How it was set: pool reuse — the heavy-reuse mold-detail file was dropped into a slot whose service it does not depict | Re-view: NOT YET
- Page: home | Section: Our Services in Plano, TX — Sewage Backup Cleanup card | Blunder: card photo kitchen-leak-10961064.webp is a clean wet stainless-steel kitchen sink with water droplets only — no drain backup, no sewage, no grime, reads as an ordinary kitchen leak (home-img06.png) | Fix: swap this card slot only to a drain/sewage-backup photo | How it was set: pool reuse — the sink file fits kitchen leaks and was reused for sewage, where its cleanliness contradicts the service | Re-view: NOT YET
- Page: home | Section: Our Services in Plano, TX — Wall Cavity Drying & Flood Cuts card | Blunder: card photo attic-insulation-9043415.webp is an empty finished attic/loft room with brick walls and a wood floor — no open wall cavity, no flood cut, no exposed framing being dried (home-img21.png) | Fix: swap this card slot only to an open wall-cavity/flood-cut photo | How it was set: pool reuse — an attic-room file was placed in a wall-cavity slot on a loose "interior" match | Re-view: NOT YET
- Page: water-extraction | Section: Where the Water Hides (split figure) | Blunder: split photo mold-wall-9127236.webp is an exterior weathered wall covered in surface green algae — it shows surface weathering, not water hidden inside a Plano home (no interior, no hidden moisture) (water-extraction-img03.png) | Fix: swap this split slot only to an interior hidden-moisture photo (behind-wall/under-floor evidence) | How it was set: pool reuse — the heavy-reuse algae-wall file was used as generic "water damage" in a section whose point is hidden water | Re-view: NOT YET
- Page: water-extraction | Section: Before Extraction Starts: 5 Things to Do Right Now (split figure) | Blunder: split photo flooded-floor-7924140.webp is a flooded modern white lobby staircase with a velvet-rope stanchion — a commercial/public interior, not a Plano home, in a section about standing water in Plano homes (water-extraction-img01.png) | Fix: swap this split slot only to a flooded residential home interior | How it was set: pool reuse — the flooded-stairs file reads "flood" at thumbnail size and its commercial setting was not checked against the section's "Plano Homes" framing | Re-view: NOT YET
- Page: sewage-cleanup | Section: Hero | Blunder: hero photo kitchen-leak-10961064.webp is a clean wet stainless-steel sink with droplets only — no sewage rising, no drain backup, no contamination visible — directly under hero copy about sewage rising through a shower drain carrying bacteria and viruses (sewage-cleanup-img00.png) | Fix: swap the hero slot only to a sewage-backup/drain photo | How it was set: same sink file as the home sewage card; a clean-fixture photo was used as the hero for a Category 3 service | Re-view: NOT YET
- Page: slab-leak | Section: Blackland Prairie Clay Moves Your Slab (split figure) | Blunder: split photo hardwood-floor-3935327.webp is a bright, pristine, empty hardwood room — no cupping, no cracks, no damage of any kind, so it shows nothing clay movement does to a slab or floor (slab-leak-img02.png) | Fix: swap this split slot only to a cupped/damaged floor or slab-movement photo | How it was set: pool reuse — the retained hardwood-room file was used as a generic floor illustration in a damage-cause section | Re-view: NOT YET
- Page: water-heater-leak | Section: Water Heater Burst in Your Plano Home? Do These 5 Things Now (split figure) | Blunder: split photo attic-insulation-4482829.webp is an attic skylight framing a pretty blue sky with fluffy white clouds — no water heater, no water, no damage — and its caption is stock-pretty ("clear blue sky and fluffy white clouds") in an emergency checklist section (water-heater-leak-img01.png) | Fix: swap this split slot only to an attic-tank or ceiling-damage photo | How it was set: pool reuse — an attic-window file was used for loose "attic" context without checking subject or caption tone | Re-view: NOT YET
- Page: ceiling-leak | Section: The Attic Insulation Sponge (split figure) | Blunder: split photo mold-wall-9127236.webp is an exterior algae-covered wall — no attic, no insulation, no sponge effect, nothing the section describes (ceiling-leak-img02.png) | Fix: swap this split slot only to a wet/sagging attic-insulation photo | How it was set: pool reuse — the heavy-reuse algae-wall file was used as generic damage in an insulation-specific section | Re-view: NOT YET
- Page: ceiling-leak | Section: Attic AC and Water Heaters (split figure) | Blunder: split photo attic-insulation-4482829.webp is the same pretty attic-skylight/blue-sky photo as the water-heater split — no AC unit, no water heater, no leak, no ceiling damage (ceiling-leak-img03.png) | Fix: swap this split slot only to an attic AC-pan or attic water-heater photo | How it was set: pool reuse — the attic-window file was reused for loose "attic" context in a second, unrelated section | Re-view: NOT YET

## Per-page confirmations

- home: CONFIRMED except the 4 card lines above. Hero (suburban-home-186077, wet driveway at dusk) holds; trust chips, checklist, service-grid layout, area/city cards (brick/suburban homes, viewed in home-img06/11/18/21 and the area-cards viewport) hold; final CTA navy+white holds; overflow 0 at all widths; mobile hero readable, sticky bar covers no footer text.
- emergency-water-damage: CONFIRMED, no new lines. Hero leaking pipe holds; plumber-hands split (crew section) and water-stained bedroom wall split (frozen-pipe section) hold as damage/crew evidence; the colorful-townhome split is American townhomes, not European/foreign, and its "Texas neighborhood" caption is not contradicted by the pixels; related cards (meter/valve guide, pipe, worker, solar heater, warehouse AC) all match their titles.
- water-extraction: CONFIRMED except the 2 split lines above. Hero leaking garden pipe holds; drain-pipe split (shop-vac section) is water-plumbing generic and acceptable; related cards (hardwood room, worker, area homes) match.
- structural-drying: CONFIRMED, no new lines. Hero inspection worker holds; industrial-fan split (fans/AC section) and warehouse-AC split (4-rules section, caption honestly says warehouse) both illustrate the section's fan/AC point; insulation-worker split (drying-process section) shows a drying-relevant material; related cards match.
- burst-pipe-cleanup: CONFIRMED, no new lines. Hero rusty dripping pipe holds; stained-bedroom-wall split (checklist section) and plumber-hands split (repipe section) hold; worn-ceiling split under "Garage Water Heaters and Hose Bibs" is loose (interior ceiling damage in a garage-source section) but remains burst-damage evidence on a burst page, so it is a watch note, not a line; related cards match.
- sewage-cleanup: CONFIRMED except the hero line above. Drain-pipe/vegetation split and rusty drain-grate split both fit drains/roots; the algae-wall split under "Heavy Storms" is loose but reads as storm-contamination consequence and is not recorded as a line; area cards match.
- slab-leak: CONFIRMED except the hardwood-room split line above. Hero dry garage floor is a KNOWN pool-limited item, unchanged, not re-flagged; meter-manifold split (checklist section) is plumbing-plausible; algae-wall split under "Signs You Have a Slab Leak" reads as a leak-sign (mold growth) and is not recorded as a line; related cards match.
- water-heater-leak: CONFIRMED except the attic-window split line above. Hero rooftop solar tank is a KNOWN pool-limited item, unchanged, not re-flagged; insulation-worker split under "Plano Attics Hit 135 to 150°F" shows attic labor and is acceptable in that section (it is NOT the sediment section — that attribution was checked and corrected); ceiling-stain split (drain-pans section) holds; related cards match.
- ceiling-leak: CONFIRMED except the 2 split lines above. Hero stained concrete ceiling (3708564) is a KNOWN pool-limited item, unchanged, and its brown stain matches the hero copy ("brown ring") — holds; worn-ceiling split (checklist section) holds as ceiling-damage evidence; related cards (warehouse AC, solar heater, worker, attic room, area homes) match.

## Watch-item verdicts (re-checked, per brief)

- Heavy reuse 9127236 (mold/algae detail): GENUINELY WRONG in 3 batch-A slots — home Fire Sprinkler card, water-extraction "Where the Water Hides" split, ceiling-leak "Attic Insulation Sponge" split (lines above). ACCEPTABLE as generic damage consequence in sewage "Heavy Storms" and slab "Signs" slots (not recorded as lines). Fix = per-slot swaps only, not a global ban (it still holds some slots).
- Heavy reuse 16243255 (industrial fan): HOLDS. Structural "5 Rules" split and home "Burst & Frozen Pipe Cleanup" split both show drying equipment in drying/cleanup context; caption "Industrial air mover fan" matches pixels.
- Heavy reuse 14032089 (worn ceiling): GENUINELY WRONG in 1 batch-A slot — home Commercial card (line above). HOLDS as damage evidence on burst-pipe ("Garage Water Heaters") and ceiling-leak (checklist) splits. Fix = home card slot only.
- Heavy reuse 3708564 (stain detail): HOLDS. Ceiling hero (brown stain ring = copy) and water-heater drain-pans split both show genuine ceiling-stain evidence; caption matches pixels.
- Retained 35290675 (about split): not a batch-A page slot; not applicable here, no verdict.
- Retained 3935327 (hardwood hero + slab/wall bodies): GENUINELY WRONG in 1 batch-A slot — slab "Blackland Prairie Clay" split (pristine room, line above). HOLDS as the home Hardwood Floor card and as related-card room illustration elsewhere; fix = slab split slot only.
- Retained 29701042 (fans body only): no batch-A page uses this file; not applicable here, no verdict.
- Known pool-limited heroes, all unchanged files, NOT re-flagged: home flood split dry brick home (31602311, viewed — dry lawn, brick house, caption accurate), water-heater rooftop solar tank (34593293, viewed), slab dry garage floor (17181949), ceiling concrete stain detail (3708564, viewed). The other named pool-limited heroes (commercial fan, fire flooded stairs, wall attic brick room, warm kitchen, ac warehouse AC, ceiling-dripping wall-stain room, crawl under-floor area) do not appear as heroes on batch-A pages except as cards/splits already judged above; none got worse (no file change, no worse mismatch, no regression).

## R4 fixes verified holding

- Hero/card chains: no chain break found in batch A; cards point at their own service's image (verified by following-heading mapping).
- Same-shoot pairs broken: R4 moisture-meter pair and crawl-space pair are absent from all 9 pages; no new same-shoot pair within any page.
- Parser lists: no fragmented lists, no dangling "See", no split bullets on any batch-A page (li counts: home 13, water-extraction 3, structural-drying 2, slab-leak 10, water-heater-leak 5, others 0 — all clean).
- Caption purge: 0 R4 purge strings on all 9 pages. Remaining stock-flavored captions are accurate to their pixels except the attic-window "clear blue sky and fluffy white clouds" caption, which is recorded via the water-heater/ceiling lines above (caption tone is part of those lines, not a separate purge hit).
- Banned files: 0 of the 55-file set on all 9 pages, including all four R4 bans and water-heater-6436774.

## Artifacts NOT recorded (per brief)

- Headless map tiles blank/grey in the map iframe (known artifact — iframe presence, not tile rendering, is the check, and it passes on all 9 pages).
- Any lazy-fill blank that filled on re-scroll (none persisted; all 115 image slots rendered with naturalWidth 1200).
- Doc-structure sections (e.g. emergency colon-label area subheads with body copy; "Find Us" map sections) — layout folds from the source doc, not blunders.
- Centred thin grids (home final service rows with 2 cards) — design pattern, not a defect.
- The worn-ceiling file's shabby-room tone on burst/ceiling damage splits, the stained-bedroom-wall file's dated-room tone on emergency/burst splits, and the colorful-townhome split on emergency — all viewed and judged acceptable damage/neighbourhood evidence, not derelict/foreign failures.
- The home `desktop-top` screenshot filename (see Method note) — a naming artifact of this hunt's shot order, not a site defect.
