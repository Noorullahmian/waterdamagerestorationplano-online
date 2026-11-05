# PLANO 3 — ROUND 4 HUNT, BATCH A (read-only, local only)

Hunter: Batch A. No generator/build file edited, no rebuild, BLUNDER_HUNT.md untouched,
no push/deploy/domain/DNS/token. Content issues are recorded only, never edited.

## Method / server / browser / viewports

- Served `~/workspace/plano3-water-damage/out/` with `python3 -m http.server 8901`
  (killed when done; a second short run on port 8902 was used only for the home
  final-CTA re-check, also killed; no listeners remain).
- Playwright Chromium at `~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`,
  flags `--no-sandbox --disable-gpu --disable-dev-shm-usage`.
- Viewports: desktop 1440x900 + mobile 390x844. Each page slow-scrolled to settle
  lazy images/GSAP reveals before shooting.
- Shots are TRUE viewport shots (never a stitched full-page shot as evidence):
  per-image desktop viewport shots (scroll element into view, then viewport shot),
  hero + footer desktop viewport shots, mobile sequential viewport steps, plus a
  dedicated home final-CTA desktop viewport shot.
- Saved under `~/workspace/plano3-water-damage/screenshots/round4/batch-a/`
  (304 files: per-image desktop shots, hero/footer shots, mobile steps, DOM dump
  `../batch-a-dom.json`).
- Every split/hero image listed below was viewed as a screenshot before recording.
  Related-card images that reuse a hero/split file already viewed in another slot
  were judged on that viewed file (no file/alt-only claims).
- Extra overflow check: each page re-loaded at 320 and 768px widths.

## DOM checks per page

Overflow = document scrollWidth at that viewport width. Favicon = head icon link.
Map = footer/hub iframe present (src `https://www.google.com/maps?q=Plano,%20TX&output=embed`
on all 9). Same-page duplicate img = exact same file twice on the same page.
Banned = R1+R2+R3 banned set from gen3_render.py (incl. water-heater-6436774.webp).
Dot bullets = li text exactly "." / "•" / empty.

| Page | Imgs | Overflow 320/390/768/1440 | Favicon | Map iframe | Same-page dup | Banned files | Dot bullets | Empty H2/H3 |
|---|---|---|---|---|---|---|---|---|
| home | 34 | 320/390/768/1440 | yes | yes | none | none | none | none |
| emergency-water-damage | 10 | 320/390/768/1440 | yes | yes | none | none | none | none |
| water-extraction | 9 | 320/390/768/1440 | yes | yes | none | none | none | none |
| structural-drying | 9 | 320/390/768/1440 | yes | yes | none | none | none | none |
| burst-pipe-cleanup | 10 | 320/390/768/1440 | yes | yes | none | none | none | none |
| sewage-cleanup | 8 | 320/390/768/1440 | yes | yes | none | none | none | none |
| slab-leak | 8 | 320/390/768/1440 | yes | yes | none | none | none | none |
| water-heater-leak | 7 | 320/390/768/1440 | yes | yes | none | none | none | none |
| ceiling-leak | 10 | 320/390/768/1440 | yes | yes | none | none | none | none |

Notes on the DOM snapshot: several below-fold card images showed naturalWidth 0 in
the first DOM snapshot (lazy, not yet scrolled to). All of them filled in their
per-image scroll-into-view viewport shots and were judged there — this is the
known lazy-fill case, NOT recorded as broken images. Headless Google Map tiles
render blank/grey in every footer/map shot (known artifact); the iframe src is
correct on all 9 pages, so no map line is recorded.

## Blunder lines

- Page: home | Section: split image 1 | Blunder: Large split photo flooded-floor-28447774.webp is a European-looking house — steep tiled roof with dormer windows, white render walls and a red wrought-iron fence — not a Plano brick home, despite the floodwater topic fitting | Fix: Swap split 1 for a brick/suburban Texas home in floodwater, or a Plano-style exterior; keep the flood topic, change the house | How it was set: R3 body override / rotation pick, retained as the flood visual | Re-view: NOT YET
- Page: home | Section: split images 2 and 3 | Blunder: Two consecutive large splits are both outdoor pipe close-ups — burst-pipe-36571568.webp (dripping elbow) followed by burst-pipe-18274115.webp (burst garden pipe spraying) — same subject back-to-back, so the page reads as one pipe photo repeated | Fix: Change one of the two splits to a non-pipe visual (extraction equipment, wet interior, drying) | How it was set: R3 body overrides for home splits 2/3, both drawn from the burst-pipe pool | Re-view: NOT YET
- Page: home | Section: services card — Standing Water Extraction | Blunder: Card photo flooded-floor-7924140.webp is a sleek modern white staircase with glass balustrade, reflective floor and a velvet-rope barrier — a commercial/public lobby, not a Plano home interior with standing water to extract | Fix: Swap the extraction card (and its hero on the extraction page) for a home interior with standing water on a residential floor | How it was set: R3 hero swap (emergency ↔ extraction); the extraction card takes the target hero file | Re-view: NOT YET
- Page: home | Section: services card — Upstairs Laundry Overflow Cleanup | Blunder: Card photo laundry-room-7282378.webp shows a hand loading dirty clothes into a washing machine — ordinary housework, no overflow, no water, no wet floor or ceiling below | Fix: Swap the card for a home laundry-room flood visual (wet laundry floor, washer hose, water running) | How it was set: R3 hero/file pick for laundry-overflow, reused as the home card image | Re-view: NOT YET
- Page: emergency-water-damage | Section: split image 1 | Blunder: Same European-dormer flood house as home split 1 (flooded-floor-28447774.webp) — tiled roof, dormers, red fence — reused as a large split on a second page, still not a Plano home | Fix: Swap for a Plano-style brick home in floodwater; do not reuse the dormer file as a large split elsewhere | How it was set: R3 body override for emergency split 1, same file as home split 1 | Re-view: NOT YET
- Page: emergency-water-damage | Section: hero + split images 2 and 3 | Blunder: Three dripping-pipe photos on one page — hero burst-pipe-15206136.webp (leaking pipe with rag), split 2 burst-pipe-36571568.webp (dripping elbow), split 3 burst-pipe-4406597.webp (rusted tube dripping over grass) — the emergency page is pipe-drip, pipe-drip, pipe-drip with only the flood-house split breaking the pattern | Fix: Change at least one large split (preferably split 2) to crew work, extraction, or a wet interior; keep at most one dripping-pipe large image per page | How it was set: R3 hero swap + body overrides, all drawn from the burst-pipe pool | Re-view: NOT YET
- Page: emergency-water-damage | Section: related card — Standing Water Extraction | Blunder: Card photo flooded-floor-7924140.webp is the same commercial-lobby white staircase with velvet rope as on home — not a home extraction scene | Fix: Same fix as the extraction hero/card swap above; the card must change with the hero file | How it was set: related-card image takes the extraction target hero | Re-view: NOT YET
- Page: water-extraction | Section: hero | Blunder: Hero flooded-floor-7924140.webp is a modern white staircase with glass balustrade and a velvet-rope barrier in a bright commercial-looking space — no Plano home, no residential floor being extracted, and the copy promises truck-mounted home extraction | Fix: Swap the hero for a residential interior with standing water (living room / hallway / stairs inside a house, no rope barrier) | How it was set: R3 hero swap with emergency-water-damage (was the leaking outdoor pipe) | Re-view: NOT YET
- Page: water-extraction | Section: split image 2 | Blunder: Visible caption claims "a metal drainage pipe on a concrete wall with visible water runoff", but on viewed pixels the pipe in sewage-drain-3964564.webp is dry — no water stream or runoff is visible, only a dark pipe mouth | Fix: Correct the caption to what is actually shown, or swap for a pipe photo with visible water running | How it was set: caption carried from images.json alt text, not checked against viewed pixels | Re-view: NOT YET
- Page: water-extraction | Section: split image 3 (Where Water Hides) | Blunder: Photo mold-wall-29701042.webp is an exterior Mediterranean wall — cracked cream/yellow render, arched yellow niche, downpipe, grass at the base — an outdoor foreign wall, not water hiding inside a Plano home (under carpet, behind drywall, under cabinets) | Fix: Swap for an interior hidden-water visual (wet baseboard, lifted flooring edge, damp wall interior) | How it was set: R3 body override for water-extraction split 3; heavy-reuse file across the site | Re-view: NOT YET
- Page: structural-drying | Section: split image 1 | Blunder: Retained file moisture-meter-8961700.webp shows a man in a hard hat touching a dry cinderblock/brick construction wall — no moisture meter is visible in the shot, no wet wall, no drying equipment, so the retained use fails its own topic (the file name promises a meter the pixels do not show) | Fix: Swap split 1 for a photo with an actual meter on a wall, or wet-wall drying work; do not keep a no-meter shot in a moisture-meter slot | How it was set: retained R2/R3 use, deliberately not globally banned — this retained slot is the one that does not hold up on viewed pixels | Re-view: NOT YET
- Page: burst-pipe-cleanup | Section: hero + split image 1 | Blunder: Hero burst-pipe-4406597.webp (rusted tube dripping over grass) and the first split burst-pipe-36571568.webp (dripping pipe elbow) are the same subject at the top of the page — two dripping outdoor pipes in a row before any indoor damage or crew work appears | Fix: Change split 1 to an indoor burst consequence (wet ceiling/floor, crew extracting, opened wall) | How it was set: hero file + R3 body override, both from the burst-pipe pool | Re-view: NOT YET
- Page: burst-pipe-cleanup | Section: split image 3 | Blunder: Photo crawl-space-40440114.webp is a clean, dry, finished-looking basement (painted floor, furnace + water heater, laundry sink, stairs) with the visible caption "Explore this spacious unfinished basement" — real-estate sales wording, and a basement is the wrong geography for slab-built Plano homes, with no water damage visible at all | Fix: Swap for a wet garage / under-house / opened-wall burst visual and drop the "Explore this spacious…" sales caption; do not use a basement photo for Plano | How it was set: R3 body override (was a clean dry garage; pool has no wet-garage photo, recorded pool-limited) | Re-view: NOT YET
- Page: sewage-cleanup | Section: hero | Blunder: Hero sewage-drain-3964564.webp at hero crop is only a tight grey drain-pipe segment on a concrete wall — no sewage, no water, no home, no backup cue; at hero size it reads as an abstract plumbing close-up, not a Category 3 backup page hero | Fix: Swap the hero for a home drain/backup-context visual (lowest drain, wet bathroom floor, crew in PPE/containment if the pool has one) | How it was set: sewage hero file carried from rotation; same file is also the water-extraction split 2 | Re-view: NOT YET
- Page: sewage-cleanup | Section: split image 1 | Blunder: Visible caption for sewage-drain-29608837.webp ends "depicting resilience" — abstract stock-sales phrasing on a sewage page, attached to a rusty pipe + drain grate with leaves | Fix: Rewrite the caption to plain service wording (rusty drain pipe / drain grate, no "resilience" stock phrase) | How it was set: caption carried from images.json alt text, not purged by the stock-caption purge | Re-view: NOT YET
- Page: sewage-cleanup | Section: split image 3 | Blunder: Photo mold-wall-29701042.webp is again the Mediterranean exterior wall (yellow arch, cracked render), and its caption claims "Storm water and sewage residue on a wall after heavy rain" — on viewed pixels there is no residue line or sewage mark, only peeling paint and a downpipe | Fix: Swap for a lower-wall waterline/residue visual, or at minimum correct the caption to peeling exterior paint with no residue claim | How it was set: R3 body override for sewage split 3; heavy-reuse file, caption not matched to pixels | Re-view: NOT YET
- Page: slab-leak | Section: hero | Blunder: Hero ceiling-stain-3708564.webp is a brown stained-concrete texture / ceiling corner — no floor, no tile, no warm spot, no cupped hardwood — so the slab-leak hero shows neither a slab nor a floor, only an abstract stain texture, while the copy opens on "a warm spot on the tile" | Fix: Swap the hero for a floor-damage visual (cupped hardwood, dark grout, warm-spot/tile context) | How it was set: R3 hero lock (was a generic pipe drip; pool has no thermal-scan/cupped-floor photo, recorded pool-limited) | Re-view: NOT YET
- Page: slab-leak | Section: split image 2 | Blunder: Photo mold-wall-29701042.webp is the same Mediterranean exterior wall used on water-extraction and sewage — cracked render, yellow arch, grass — an outdoor foreign wall on an under-floor slab page, with no slab/floor content | Fix: Swap for an interior floor/wall-base damage visual; stop reusing this exterior file as a generic damage filler | How it was set: R3 body override for slab split 2; heavy-reuse file | Re-view: NOT YET
- Page: slab-leak | Section: split image 3 (Signs You Have a Slab Leak) | Blunder: Photo ceiling-stain-8624464.webp shows a water stain on a wallpapered WALL above a bed in a dated room (lace curtains, striped wallpaper, eclectic bed) — the stain is not on a ceiling and not on a floor, and the room does not read as a Plano bedroom; it is off-topic for slab-leak signs | Fix: Swap for a slab-sign visual (warm floor spot, cupped boards, dark grout, high meter reading) | How it was set: R3 body override for slab split 3; heavy-reuse file | Re-view: NOT YET
- Page: water-heater-leak | Section: hero | Blunder: Hero water-heater-34593293.webp is a rooftop solar water-heater unit against a white sky — not the "50-gallon tank in your Plano attic" the hero copy describes, and not a garage tank either; a reader comparing copy to photo sees a different kind of heater in a different place | Fix: Swap the hero for an attic/garage tank photo if the pool gains one; otherwise accept explicitly as pool-limited, not as a match | How it was set: R3 re-view fix (was the face-cropped pipe man 35290675; solar tank is a real heater tank, but rooftop solar, recorded pool-limited) | Re-view: NOT YET
- Page: water-heater-leak | Section: split image 1 | Blunder: Photo burst-pipe-4406597.webp is a rusted garden pipe dripping over grass — no water heater, no attic, no garage, no tank — off-topic as the first split on a water-heater page | Fix: Swap split 1 for a tank/attic/garage-adjacent visual (tank, pan, attic hatch, wet ceiling below a tank) | How it was set: R3 body override for water-heater split 1 | Re-view: NOT YET
- Page: water-heater-leak | Section: split image 3 | Blunder: Photo ceiling-stain-14032089.webp is a worn ceiling with a hanging lamp in a deserted, dimly lit room — the caption itself says "deserted" — an abandoned/derelict tone, not a Plano home ceiling after an attic-tank flood | Fix: Swap for a lived-in home ceiling with a fresh water stain / sag, not a derelict room | How it was set: body rotation pick for water-heater split 3; caption accurately admits the derelict tone | Re-view: NOT YET
- Page: ceiling-leak | Section: hero | Blunder: Hero attic-insulation-8082327.webp is a pristine finished attic room — skylights, brick pillar, wooden ladder, clean floor, no stain, no water, no insulation damage — a dry room as the hero of a page whose copy says "20 to 50 square feet of attic insulation above it is usually already soaked" | Fix: Swap the hero for a stained ceiling or soaked-insulation visual; a dry attic room contradicts the page's own opening claim | How it was set: R3 rotation-churn lock (pool has no free stained-ceiling photo; all others are heroes elsewhere, recorded pool-limited); retained-use check: this retained use does NOT hold up as a damage-page hero | Re-view: NOT YET
- Page: ceiling-leak | Section: split image 1 | Blunder: Photo ceiling-stain-8624464.webp shows the stain on a wallpapered WALL, not on a ceiling, and its caption claims "a unique ceiling design, featuring water stains" — caption/pixel mismatch, in a dated room that does not read as a Plano bedroom | Fix: Swap for a genuine ceiling stain/sag photo, or correct the caption to a wall stain and move the file off the ceiling page | How it was set: R3 body override for ceiling split 1; heavy-reuse file | Re-view: NOT YET
- Page: ceiling-leak | Section: split image 2 (The Attic Insulation Sponge) | Blunder: Photo attic-insulation-6124239.webp shows a worker installing dry, new pink insulation — the opposite of the section's subject, soaked attic insulation acting as a sponge; the insulation in the shot is clean and dry | Fix: Swap for soaked/discoloured insulation, removed wet batts, or a wet attic cavity; a dry-install photo must not illustrate a soaked-insulation section | How it was set: R3 body override for ceiling split 2; heavy-reuse file across structural/water-heater/ceiling | Re-view: NOT YET
- Page: ceiling-leak | Section: split image 3 (Attic AC and Water Heaters) | Blunder: Photo drying-fan-28726413.webp is a warehouse exterior wall with industrial AC units — a commercial warehouse, not a Plano home attic AC unit or water heater | Fix: Swap for a home attic/residential AC visual (attic air handler, condensate pan, residential condenser) | How it was set: R3 body override for ceiling split 3; same warehouse file is also the structural-drying split 2 | Re-view: NOT YET
- Page: ceiling-leak | Section: Ceiling Leaks Across Plano (H3 fragment) | Blunder: A sentence fragment is promoted to an orange H3 — "We see hail-season roof leaks in Hunters Glen and Preston Meadow (" — with a dangling open parenthesis, and the following paragraph starts mid-sentence with "Central Plano), upstairs bath leaks in Deerfield and Kings Ridge (Legacy West), …" — confirmed in the mobile viewport shot, not a stitch artifact | Fix: Demote the fragment to body text (or give the subsection a real heading) and rejoin the sentence so the parenthesis closes around the area link; no word changes beyond the heading/body split | How it was set: section/subsection classifier promoting a lead sentence to H3 before its parenthetical area links | Re-view: NOT YET

## Per-page confirmations

- home — 4 lines. Passed: H1=1, hero copy/CTA readable, trust band, no post-hero lone-button band, footer phone number unwrapped, overflow 0 at 320/390/768/1440, favicon present, map iframe present, no banned files, no dot bullets, no dangling See (the "See 24/7 emergency…" sentence is a complete link sentence). Final CTA re-verified in a dedicated desktop viewport shot: navy background rgb(14,58,92), white text, orange Call button — R1–R3 final-CTA fix HOLDS. Home hero itself (dry two-story house, wet driveway at dusk) is NOT recorded as a line: it is a generic exterior, not a pristine interior, and was the R3-locked home hero.
- emergency-water-damage — 3 lines. Passed: H1=1, hero copy/CTA readable, checklist section readable, "See AC overflow cleanup." / "See sewage backup cleanup and flood cleanup." are complete link sentences (not dangling See), no lone-button band, overflow 0 at all widths, favicon, map, no banned/dot/dup.
- water-extraction — 3 lines. Passed: H1=1, hero copy readable, related-cards grid readable (Allen brick home, Frisco pastel homes, Richardson brick home cards all render), no lone-button band, overflow 0 at all widths, favicon, map, no banned/dot/dup.
- structural-drying — 1 line. Passed: hero worker inspecting a wall vent reads as inspection context (dry wall is the point of the hero copy: "your floor feels dry…"), warehouse AC split fits the Fans/AC section topic, insulation split is crew work; no lone-button band, overflow 0 at all widths, favicon, map, no banned/dot/dup. Closest to clean in this batch.
- burst-pipe-cleanup — 2 lines. Passed: hero copy readable, plumber-hands split (6419128, retained heavy-reuse file) genuinely fits — close-up hands installing steel pipes indoors, no face crop, no defect; no lone-button band, overflow 0 at all widths, favicon, map, no banned/dot/dup.
- sewage-cleanup — 3 lines. Passed: drain-grate split (13961561) genuinely fits the drain topic; hero copy readable; no lone-button band, overflow 0 at all widths, favicon, map, no banned/dot/dup.
- slab-leak — 3 lines. Passed: water-meter split (11658940) genuinely fits slab detection — meter box in a concrete wall, valves readable; hero copy readable; no lone-button band, overflow 0 at all widths, favicon, map, no banned/dot/dup.
- water-heater-leak — 3 lines. Passed: attic-insulation split (6124239) fits the "Plano Attics Hit 135 to 150°F" attic-activity section (worker in attic, not an empty loft); hero copy readable; no lone-button band, overflow 0 at all widths, favicon, map, no banned/dot/dup.
- ceiling-leak — 5 lines. Passed: aside from the lines above, page structure is sound — H1=1, FAQ questions readable, related-cards grid readable, no lone-button band, overflow 0 at all widths, favicon, map, no banned/dot/dup. The H3 fragment is the only heading defect found in this batch.

## Watch-item verdicts (flagged only where genuinely wrong on viewed pixels)

- hardwood-floor-9462163 (mopping activity): NOT on any Batch A page — no verdict, no line.
- flooded-floor-28447774 (European-dormer reading): CONFIRMED wrong — flagged on home split 1 and emergency split 1 (tiled roof, dormers, red fence).
- Heavy reuse 3964564: flagged on sewage hero (dry abstract pipe) and water-extraction split 2 (caption claims runoff the pixels do not show); the file itself is a drain pipe, but both slots over-claim it.
- Heavy reuse 6124239: flagged on ceiling split 2 (dry install vs soaked-insulation section); passes on water-heater attic-activity split and structural 5-step split.
- Heavy reuse 8624464: flagged on slab split 3 and ceiling split 1 (stain is on a wall, not a ceiling/floor, in a dated room).
- Heavy reuse 29701042: flagged on water-extraction split 3, sewage split 3, slab split 2 (same foreign exterior wall, three different claimed subjects).
- Heavy reuse 6419128: PASSES — plumber-hands close-up on burst split 2 genuinely fits; no line.
- Retained 35290675: NOT on any Batch A page — no verdict, no line.
- Retained 8961700: FLAGGED — structural split 1 shows no meter and no wet wall (see line above).
- Retained 8082327: FLAGGED — ceiling hero is a pristine dry attic room (see line above).
- Retained 3935327: PASSES as a topic card — bright empty hardwood room on home/structural cards is wood-floor context, not claimed as damage; no line (weaker than the flagged cards, and the file's slot is a floor-topic card, not a damage photo).
- Retained 9127236: NOT on any Batch A page — no verdict, no line.

## Known artifacts — NOT recorded as blunders

- Headless Google Map tiles blank/grey in every map shot (iframe src verified correct).
- Lazy card images blank in the first DOM snapshot but filled on scroll-into-view shots.
- Doc-structure single-sentence sections (e.g. short "See …" link sentences, area-label H2s with body following) — not orphan shells.
- Centred thin related grids — template behaviour, not a defect.
- Sticky mobile call bar sitting below the hero button on mobile — template behaviour, not a lone-button band.

## Caveats for the coordinator

- Home mobile steps in the first run stopped at step 25 (loop cap) before the FAQ/final-CTA/map tail; the home final CTA was therefore re-verified separately (desktop viewport shot + computed navy/white colours, see above) and the footer/map were verified on desktop + mobile footer shots.
- Several lines are pool-limited by the R3 record (no thermal-scan/cupped-floor photo, no attic-tank photo, no wet-garage photo, no soaked-batts photo, no free stained-ceiling photo). They are recorded as genuine viewed-pixel mismatches; whether the fix pass accepts them as pool-limited or sources new photos is the coordinator's call, not this hunter's.
- No invented-copy check was possible against the doc in this read-only hunt (no doc access in this batch); folded/empty-looking sections were not recorded as content omissions.
- Server killed at end of hunt; no listeners on 8901/8902 remain.
