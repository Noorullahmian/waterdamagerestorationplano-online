# PLANO 3 — ROUND 4 HUNT, BATCH E (read-only, local only)

Hunted: 2026-11-04, from local `out/` served on port 8905 (server killed after the hunt).
Method: Playwright Chromium `~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`,
flags `--no-sandbox --disable-gpu --disable-dev-shm-usage`. Viewports desktop 1440x900 +
mobile 390x844, slow-scroll to settle lazy images/GSAP, then TRUE viewport shots per hero /
image element / section / footer (no stitched full-page shot used as evidence). Every line
below was seen in a viewed screenshot. 408 shots under
`screenshots/round4/batch-e/` (desktop element shots + mobile viewport shots, per page:
hero, every `main img`, every `main section`, group-intro H2s outside sections, footer).

## DOM CHECKS PER PAGE

All 10 pages: H1 present per template, favicon link present (`/favicon.svg` + apple-touch
`/favicon.png`), map `<iframe>` present (Find Us section on every page, including hubs
services/areas/guides and about/contact), dot bullets 0 (no `<li>.` / lone `•` / empty `<li>`),
same-page duplicate img src 0, banned files 0 in out HTML (no water-heater-6436774, no
workshop-technician 33388390, no drill 38749876), no stock-sales caption phrases found
(no "ideal for…", "perfect for real estate…", "showcasing modern architecture",
"Abstract background…"), no dangling "See" H2, no dangling "See" list item.
Overflow (scrollWidth − clientWidth, after slow-scroll): 0 at 320 / 390 / 768 / 1440 on all
10 pages. Map tiles render blank/grey in headless shots — the known artifact, NOT recorded
as a blunder. Lazy images that blanked on a first shot filled on re-scroll — not recorded.

| Page | imgs | Overflow 320/390/768/1440 | Favicon | Map iframe | Dot bullets | Same-page dup img | Banned files |
|---|---|---|---|---|---|---|---|
| shut-off-valve | 9 | 0/0/0/0 | yes | yes | 0 | 0 | 0 |
| storm-water-category-3 | 8 | 0/0/0/0 | yes | yes | 0 | 0 | 0 |
| sagging-ceiling | 6 | 0/0/0/0 | yes | yes | 0 | 0 | 0 |
| mold-after-water-damage | 7 | 0/0/0/0 | yes | yes | 0 | 0 | 0 |
| water-damage-insurance-texas | 5 | 0/0/0/0 | yes | yes | 0 | 0 | 0 |
| about | 10 | 0/0/0/0 | yes | yes | 0 | 0 | 0 |
| contact | 10 | 0/0/0/0 | yes | yes | 0 | 0 | 0 |
| services | 20 | 0/0/0/0 | yes | yes | 0 | 0 | 0 |
| areas | 10 | 0/0/0/0 | yes | yes | 0 | 0 | 0 |
| guides | 10 | 0/0/0/0 | yes | yes | 0 | 0 | 0 |

## BLUNDER LINES (11)

- Page: storm-water-category-3 | Section: "How the Water Got In Decides What Has to Happen" (group intro) | Blunder: REOPENED Round 3 line, only partly fixed — the cream band is gone, but the H2 plus its lone orange H3 ("Why Plano Homes Take On Storm Water") still stand alone with no body copy at all, immediately followed by the next H2 ("Creeks Run Through the City"); a reader expects content under the H3 and gets a different heading instead, on desktop and mobile | Fix: Fold the H3 line into the following section as its lead-in (existing words only, no invented copy), or give the group intro its own body paragraph; do not leave an H2+H3-only stack | How it was set: Round 3 fix pass converted the group-intro section to a plain div (band padding gone) but did not fold the H3 into the following content or add body copy | Re-view: NOT YET
- Page: mold-after-water-damage | Section: "Hour-by-Hour: What Happens Inside Wet Walls and Floors" (group intro) | Blunder: Same reopened Round 3 line — the H2 plus its lone orange H3 ("Why Plano Homes Are at Higher Risk") still stand alone with no body copy, immediately followed by the next H2 ("Warm Indoor Temperatures"); cream band gone, heading-only stack remains, on desktop and mobile | Fix: Fold the H3 line into the following section as its lead-in (existing words only), or give the group intro its own body paragraph; do not leave an H2+H3-only stack | How it was set: Round 3 fix pass converted the group-intro section to a plain div (band padding gone) but did not fold the H3 into the following content or add body copy | Re-view: NOT YET
- Page: storm-water-category-3 | Section: related grid — "Flood & Storm Water Cleanup" card | Blunder: Card photo (flooded-floor-28447774.webp) is still the Central-European-looking house — steep tiled roof with dormers, ornate red metal fence, muddy yard flood — not a Plano/North Texas brick suburban home. Round 3 fix swapped this file out of the split slot but left it in the related card, so the watch file still reads foreign on this page | Fix: Replace the card image with a North Texas-looking flooded residential street or brick home (no dormer/tile-roof European look) | How it was set: image pick for the flood-cleanup card; Round 3 fix-pass swap was split-scoped only and did not cover the card slot | Re-view: NOT YET
- Page: services | Section: services grid — "Flood & Storm Water Cleanup" card | Blunder: Same file (flooded-floor-28447774.webp), same read — steep tiled roof with dormers, red metal fence, muddy flood yard — on the services hub's flood card, visible even at grid-card size in the full-grid screenshot | Fix: Replace the card image with a North Texas-looking flooded residential street or brick home | How it was set: image pick for the flood-cleanup service card (same file as the storm related card and the shut-off related card) | Re-view: NOT YET
- Page: shut-off-valve | Section: related grid — "Emergency Water Damage Cleanup" card | Blunder: Same file (flooded-floor-28447774.webp), same read — steep tiled roof with dormers, red metal fence — as the first related card on the shut-off guide | Fix: Replace the card image with a North Texas-looking flooded residential street or brick home | How it was set: image pick for the emergency-cleanup related card (same file as the services-hub and storm related cards) | Re-view: NOT YET
- Page: shut-off-valve | Section: related grid — "Guide: Warm Spot on Floor" card | Blunder: Card photo (hardwood-floor-9462163.webp) is a person mopping a parquet floor barefoot with a flat mop — routine house cleaning, not a warm-spot/slab-leak visual; it contradicts the damage topic of the guide it links to | Fix: Replace with a warm-spot/slab visual (thermal image, warm floor, meter/wall reading) or a neutral wood-floor photo with no cleaning action | How it was set: image pick for the warm-spot guide card reusing the mopping file (watch item: heavy reuse of 9462163) | Re-view: NOT YET
- Page: guides | Section: guides grid — "Guide: Warm Spot on Floor" card | Blunder: Same file (hardwood-floor-9462163.webp), same read — barefoot mopping of a parquet floor, house cleaning, not a warm-spot/slab-leak visual, prominent in the second card of the guides grid | Fix: Replace with a warm-spot/slab visual (thermal image, warm floor, meter/wall reading) or a neutral wood-floor photo with no cleaning action | How it was set: image pick for the warm-spot guide card (same file as the shut-off related card) | Re-view: NOT YET
- Page: mold-after-water-damage | Section: "Hidden Water" split + related grid "Structural Drying" card | Blunder: Same-shoot near-duplicate pair on the same page — the wide split shot (moisture-meter-8293640.webp, inspector in hi-vis vest and yellow helmet kneeling at an outlet, full room) and the related card (moisture-meter-8293746.webp, tighter crop of the same man, same pose, same outlet, same vent). Different files, but a visitor scrolling the page sees the same inspector scene twice. Round 3 fix broke this pair on the insurance page only, not here | Fix: Replace one of the two with a different inspection/drying visual (different inspector scene, moisture meter close-up, drying equipment) | How it was set: image pick — split pool and card pool do not exclude same-shoot near-duplicates across split/card slots, only exact-file duplicates | Re-view: NOT YET
- Page: about | Section: "Save First, Remove Last" split + related grid "Structural Drying" card | Blunder: Same same-shoot pair on the same page — wide split shot (moisture-meter-8293640.webp, inspector kneeling at an outlet) and related card (moisture-meter-8293746.webp, tighter crop of the same man, same pose, same outlet, same vent); the same inspector scene appears twice on the about page | Fix: Replace one of the two with a different inspection/drying visual | How it was set: image pick — split pool and card pool do not exclude same-shoot near-duplicates across split/card slots | Re-view: NOT YET
- Page: contact | Section: no-heading block after "Whether it's clean water, gray water or sewage" (before "What We Can Help With") | Blunder: RESIDUAL of the Round 3 duplicate-heading line, only partly fixed — the duplicate H2 is gone, but the paragraph "Send Us a Message (Non-Emergency) Use this form for questions, scheduling an inspection or following up on a job. For active water, please call…" still sits here, two sections before the actual form, with no pointer down to it; a reader hitting this paragraph expects a form below and instead gets "What We Can Help With" and "Areas We Cover" first | Fix: Move this intro paragraph down to sit directly under the single "Send Us a Message (Non-Emergency)" H2 with the form, or delete the early mention and keep only the form-section intro; do not leave a form promise detached from the form | How it was set: Round 3 fix pass demoted the first "Send Us a Message" heading to plain paragraph text instead of moving the intro to the form | Re-view: NOT YET
- Page: areas | Section: area cards grid — "East Plano (75074) Area Page" card | Blunder: Card photo (suburban-home-25798114.webp) is a Mediterranean-looking house — full red tile roof, cream walls, olive trees in the foreground — not an East Plano brick suburban home. This replaces the Round 3 coastal/palm card, but the replacement still fails place fit for a city card | Fix: Replace with an East Plano-style brick suburban home/street photo (shingle roof, brick, no tile roof/olive trees) | How it was set: image pick for the areas-hub East Plano card (Round 3 replacement file, place fit not re-checked on viewed pixels) | Re-view: NOT YET

## PER-PAGE CONFIRMATIONS

- shut-off-valve: 2 lines (flood card 28447774, mopping card 9462163). Otherwise clean: hero meter/valve-box photo is an excellent topic fit; leaking-pipe split, wrench-on-sink split and running-faucet split all fit their sections; related flooded-stairs card fits; no post-hero lone CTA band; "See water heater leak cleanup" inline; FAQ and Find Us sections clean; mobile hero phone on one line.
- storm-water-category-3: 2 lines (group intro, flood card). Otherwise clean: Round 3 split fixes HOLD — Creeks split is now a downspout/drain pipe (not plumber hands) and Saturated Clay split is a US suburban home on a wet street; 60-Second flooded-stairs split fits; sewage-card rusty drain and insurance-card office skyline fit; related inspector card fits; no dot bullets; overflow 0.
- sagging-ceiling: CLEAN (0 lines). Round 3 fix HOLDS — "How Dangerous Is It?" now leads "The 6 Safety Steps" section with the full safety answer beneath it; stained-ceiling split, stained-bedroom split (8624464 retained use fits: water stain visible), brick-house split, insulation-worker split (6124239) and attic-room/moisture cards all fit; "What a Crew Does" list intact; related grid 2 cards centred.
- mold-after-water-damage: 2 lines (group intro, inspector same-shoot pair). Otherwise clean: hero green algae/mold wall fits; peeling-paint mold split fits; brick-home split is a textbook Plano brick home; Signs list intact; related meter/flooded-stairs cards fit; retained 9127236 hero use fits its slot.
- water-damage-insurance-texas: CLEAN (0 lines). Round 3 fix HOLDS — the same-shoot inspector pair is broken here: only 8293640 (wide inspector split) remains, 8293746 is gone from this page; office-skyline hero acceptable for a claims guide; brick-house and office-interior splits are generic but on-topic; Mistakes list intact (4 bullets); related grid 1 card (mold guide) centred; "Letting a slow drip continue" closing section reads as a closing section with body + CTA, not an empty tail.
- about: 1 line (inspector same-shoot pair). Otherwise clean: Round 3 fixes HOLD — double comma gone ("Frisco, Allen, McKinney, Richardson, Murphy, Parker & Wylie" single comma, verified in HTML and screenshot); "What We Help With" is 7 clean bullets; "We built this site…" proper H2 with body; "Honest About Insurance" ends with "See our Texas insurance guide" inline, no standalone H2; apartment-block split replaced by a brick suburban home with basketball hoop (3990589); pump-technician split (35290675 retained use fits crew work); related cards fit; no stock-sales captions.
- contact: 1 line (detached form intro paragraph). Otherwise clean: single "Send Us a Message (Non-Emergency)" H2 with the form directly under it; "What We Can Help With" is 8 clean bullets including folded tails; radio rows inline ("Is water still active? Yes / No"); form fields labelled; no post-hero lone CTA band; related cards fit; mobile hero phone on one line with sticky call bar. Weak-but-not-flagged: the "Service area" split (texas-home-23930020) is a stone villa with tile roof that leans Mediterranean; as a generic upscale stone home it does not clearly fail, so it is noted here, not listed.
- services: 1 line (flood card 28447774). Otherwise clean: 20-card grid renders 3-col, aligned, no overflow; remaining 19 cards fit their services (leaking pipe, flooded stairs, inspector, rusted pipe, drain pipe, cracked stained ceiling, solar water-heater tank, attic room, office night, empty wood room, stained bedroom, kitchen, washer, basement, kitchen, sprinkler ceiling, wall inspector, insulation worker, old wall); Find Us map section present in DOM (grey headless box is the known artifact).
- areas: 1 line (East Plano card 25798114). Otherwise clean: Round 3 fixes HOLD — coastal/palm East Plano card and apartment-block Legacy West card are both gone (Legacy West now a modern white house, fitting the area); remaining cards are Plano-appropriate brick/suburban/modern homes; grid renders 3-col; Find Us map section present in DOM.
- guides: 1 line (Warm Spot mopping card 9462163). Otherwise clean: 10-card grid renders 3-col, aligned; remaining 9 cards fit (meter box, attic room, brick house, peeling mold wall, caravan flood, mold wall, leaking garden pipe, stained ceiling, office skyline); Find Us map section present in DOM. Last-row single card (insurance guide) sits left in grid flow — normal 3-col flow for 10 cards, not a defect.

## ROUND 1–3 FIXES RE-VERIFIED ON BATCH-E PAGES (all hold unless listed above)

CTA bands suppressed (no lone-button post-hero strips); favicon link present on all 10;
banned R1+R2+R3 files absent from out HTML; no dot bullets; no dangling "See" headings or
list items (contact's earlier dangling-"See" H2 is now inline body copy "Extraction and
drying begin the same visit. See 24/7 emergency water damage cleanup."); no same-page
duplicate img src; contact radios inline; thin related grids centred (sagging 2, insurance
1); hub Find Us maps present (services, areas, guides); footer phone on one line; mobile
sticky call bar present; about double comma fixed; sagging Safety Steps tail fixed;
insurance same-shoot pair broken; about What We Help With 7 bullets; contact What We Can
Help With 8 bullets; contact single form H2 with form directly under it; storm/mold splits
replaced (drain pipe, suburban home); areas coastal + apartment cards replaced.
NOT fully closed (listed above): storm/mold group-intro H2+H3 stacks still have no body
copy (band gone only); inspector same-shoot pair survives on mold + about via split/card
slots; flood card 28447774 survives on 3 pages via card slots; contact form intro paragraph
still detached from the form.

## SCREENSHOTS VIEWED (408 files under screenshots/round4/batch-e/)

Desktop element shots + mobile viewport shots per page: hero, every main img, every main
section, group-intro H2s, footer. Per-page desktop/mobile counts: shut-off-valve 44,
storm 42 (incl. groupintro), sagging 32, mold 44 (incl. groupintro), insurance 34,
about 58, contact 50, services 48, areas 28, guides 28. All image lines above were judged
on viewed pixels, not file/alt claims. Files not individually re-opened in this round were
cross-checked as the identical file viewed on another batch-E page (e.g. about related
cards = areas/contact/mold files already viewed at full size).

## NOTES FOR THE FIX PASS (not lines)

- Pristine/generic room photos used as hub/related card thumbnails (kitchen, empty wood
  room, washer loading, office interiors) were NOT flagged: they match the card standard
  Round 3 accepted for hubs (room/service match, no cleaning action, no foreign scene).
  Only the mopping action photo was flagged, because it shows cleaning in progress.
- Retained watch files checked and passed in their slots: 35290675 (about pump
  technician, fits crew work), 8082327 (sagging related attic room + services ceiling
  card, fits), 3935327 (services hardwood empty room, generic card standard), 9127236
  (mold hero algae wall, fits), 8624464 (sagging stained bedroom, stain visible),
  6124239 (sagging insulation worker, fits), 3964564 (storm drain pipe, fits),
  29701042 (services old wall, fits). 8961700 was not present; the similar file on
  services is 8961703 (wall inspector, fits).
- No push, no deploy, no domain/DNS, no token used. Nothing outside
  screenshots/round4/batch-e/ and round4/batch-e.md was created or modified.
