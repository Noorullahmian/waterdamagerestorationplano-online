# PLANO 3 — ROUND 5 HUNT, BATCH E (read-only)

Batch pages (10 ONLY): storm-water-category-3, mold-after-water-damage, sagging-ceiling,
water-damage-insurance-texas, shut-off-valve, about, contact, services, areas, guides.
No other page was hunted. Nothing was edited, rebuilt, pushed, deployed, or touched for
domain/DNS/token. All content issues below are recorded only, never edited.

## Method / server / browser / viewports

- Build hunted: `~/workspace/plano3-water-damage/out/` (final Round 4 fix-pass build, local only).
- Served by the hunter with `python3 -m http.server` on port 8915 from `out/`, killed when
  done (verified connection-refused afterwards). No rebuild was run.
- Browser: Playwright Chromium headless (chromium-1243, default Playwright launch),
  flags `--no-sandbox --disable-gpu --disable-dev-shm-usage`.
  NOTE: the first launch attempt with an explicit `chrome-linux64` executable crashed the
  page; the default Playwright Chromium launch worked and was used for all evidence.
- Viewports: desktop 1440x900 + mobile 390x844 for every page; overflow re-loads at
  320 / 390 / 768 / 1440 px measuring `documentElement.scrollWidth` vs viewport width.
- Settling: slow scroll through the full page height, wait, back to top, then TRUE viewport
  shots only — each hero / split / card image scrolled into view before its shot. No
  stitched full-page shot is used as evidence for any line below.
- First-pass hub card shots (services/areas/guides) came out as repeated top-of-grid
  frames because of smooth-scroll timing; they were DISCARDED as evidence and every hub
  card was re-shot with instant JS scroll (`window.scrollTo` to the image offset, scrollY
  verified in the log, e.g. services card04 target 665 -> scrollY 545). The `-check.png`
  shots are the hub-card evidence. This was a hunter tooling artifact, not a page defect,
  and is not recorded as a blunder.
- Judgement standard applied: large hero/split images are judged strictly (topic AND
  Plano/Texas place fit for the section they sit in); small related/grid cards are judged
  on subject class only. That is why the same file can be lined as a large split and
  accepted as a small card (see Watch-item verdicts). A line is recorded only where a
  screenshot in `screenshots/round5/batch-e/` shows the defect.

## DOM checks (from `out/<slug>/index.html` main content + headless render)

Banned check covers the R1–R3 set (incl. water-heater-6436774) plus the R4 bans
flooded-floor-28447774, hardwood-floor-9462163, attic-insulation-8082327,
moisture-meter-8961700. "Dot bullets" = literal `•` in visible text. "Empty H2/H3" =
heading with no text. Broken images = headless `naturalWidth == 0`.

| Page | H1 | Overflow 320/390/768/1440 | Favicon link | Map iframe | Same-page img dup | Banned file | Dot bullets | Empty H2/H3 | Broken imgs |
|---|---|---|---|---|---|---|---|---|---|
| storm-water-category-3 | 1 | 0 / 0 / 0 / 0 | yes | yes | 0 | 0 | 0 | 0 | 0 |
| mold-after-water-damage | 1 | 0 / 0 / 0 / 0 | yes | yes | 0 | 0 | 0 | 0 | 0 |
| sagging-ceiling | 1 | 0 / 0 / 0 / 0 | yes | yes | 0 | 0 | 0 | 0 | 0 |
| water-damage-insurance-texas | 1 | 0 / 0 / 0 / 0 | yes | yes | 0 | 0 | 0 | 0 | 0 |
| shut-off-valve | 1 | 0 / 0 / 0 / 0 | yes | yes | 0 | 0 | 0 | 0 | 0 |
| about | 1 | 0 / 0 / 0 / 0 | yes | yes | 0 | 0 | 0 | 0 | 0 |
| contact | 1 | 0 / 0 / 0 / 0 | yes | yes | 0 | 0 | 0 | 0 | 0 |
| services | 1 | 0 / 0 / 0 / 0 | yes | yes | 0 | 0 | 0 | 0 | 0 |
| areas | 1 | 0 / 0 / 0 / 0 | yes | yes | 0 | 0 | 0 | 0 | 0 |
| guides | 1 | 0 / 0 / 0 / 0 | yes | yes | 0 | 0 | 0 | 0 | 0 |

Overflow numbers are `scrollWidth - viewport width` (0 = no horizontal overflow at that
width). No bare `<li>` / `<p>` containing only `.`, `•` or `See` was found on any of the
10 pages, and no H2 ends with `See`. No R4 caption-purge string occurs in any of the 10
pages' HTML. No same-page same-shoot pair was found: the inspector pair
(moisture-meter-8293640 + moisture-meter-8293746) never co-occurs on one page in this
batch (insurance carries 8293640 only; all other pages carrying one carry 8293746 only),
and the crawl pair (crawl-space-4092026 + crawl-space-4092030) never co-occurs
(services carries 4092026 only).
Favicon tab-chrome rendering itself was NOT visually verified (headless has no tab
chrome); only the `<link rel="icon">` / apple-touch-icon presence was checked.

## Blunder lines (25) — all Re-view: NOT YET

Screenshot names below are files in
`~/workspace/plano3-water-damage/screenshots/round5/batch-e/`.

- Page: storm-water-category-3 | Section: Hero | Blunder: hero photo (storm-flood-11537987) shows a flooded yard with a caravan/trailer, a red shed and leafless trees — flood topic fits, but the subject is not a Plano brick home and reads as a rural caravan-park flood, not a Plano house taking on storm water (storm-water-category-3-hero-desktop.png) | Fix: swap the hero to a flooded Plano/Texas brick-home yard; keep the caravan file out of this hero slot | How it was set: pool hero assigned on flood topic alone, place fit not checked against the hero | Re-view: NOT YET
- Page: storm-water-category-3 | Section: The 60-Second Answer for Plano Homeowners (split figure) | Blunder: split photo (flooded-floor-7924140) is a glossy modern white staircase in a commercial-style lobby with a velvet-rope stanchion and a reflective floor — not flood damage inside a home, and the caption "Flooded area with stairs reflecting on water surface" describes a polished floor, not standing flood water (storm-water-category-3-img01-flooded-floor-7924140.png) | Fix: swap the split to standing water inside a home (floor/wall water line); do not reuse this lobby file as a home-flood image | How it was set: file name ("flooded-floor") trusted over viewed pixels; the reflective floor was mistaken for flood water | Re-view: NOT YET
- Page: storm-water-category-3 | Section: Saturated Clay Can't Absorb Any More (split figure) | Blunder: split photo (suburban-home-186077) is a dry, dusk listing-style house with a dry lawn; the only wet cue is a reflective driveway, and there is no saturated yard, pooling water or water against the house to carry the section's point (storm-water-category-3-img03-suburban-home-186077.png) | Fix: swap the split to a wet yard / water pooling against a brick foundation | How it was set: generic suburban-home file slotted into a water-specific section on subject class alone | Re-view: NOT YET
- Page: storm-water-category-3 | Section: Related Services & Guides — Sewage Backup Cleanup card | Blunder: card photo (kitchen-leak-10961064) is a clean, wet stainless-steel kitchen sink — no sewage, no backup, no drain overflow — as the face of "Sewage Backup Cleanup" (storm-water-category-3-img04-suburban-home-31602311.png, related grid row) | Fix: swap the sewage card image to a drain/sewage-backup subject; the clean sink belongs on a kitchen-leak slot, not a sewage slot | How it was set: wet-sink file reused as a generic "water" card image for a sewage service | Re-view: NOT YET
- Page: storm-water-category-3 | Section: How the Water Got In Decides What Has to Happen (group-intro band) | Blunder: the R4 fold is structurally present (no empty H2+H3 stack, no invented copy) but renders as a lone one-line beige band containing only the label sentence "Why Plano Homes Take On Storm Water." — it reads as a dangling label, not a lead paragraph, between two full H2 sections (storm-water-category-3-group-intro.png) | Fix: merge the label line into the following section as a kicker/lead line (words preserved) or fold the band away; do not leave a one-sentence label as its own section | How it was set: R4 fold demoted the group heading to a paragraph but left it isolated in its own section block | Re-view: NOT YET
- Page: mold-after-water-damage | Section: Hero | Blunder: hero photo (mold-wall-9127236) is an exterior weathered wall covered in green algae with long cracks — outdoor algae on an outside wall, not mold inside a Plano home after a leak; algae is not indoor drywall mold and there is no home context in frame (mold-after-water-damage-hero-desktop.png) | Fix: swap the hero to mold on an interior wall/baseboard in a home; keep this algae texture out of the hero slot | How it was set: heavy-reuse mold-texture file assigned to the hero on "mold-like" texture alone, interior/exterior not checked | Re-view: NOT YET
- Page: mold-after-water-damage | Section: The 60-Second Mold Clock for Plano Homes (split figure) | Blunder: split photo (mold-wall-4597285) shows peeling multi-colour paint / torn poster layers and a bolt on a derelict-looking wall — no mold colonies are visible — while its caption claims "old cement wall with blots and mold on dirty surface"; the pixels contradict the caption and the tone is abandoned/derelict, which the copy does not describe (mold-after-water-damage-img01-mold-wall-4597285.png) | Fix: swap the split to visible mold on a home wall/baseboard and correct the caption to what the replacement shows | How it was set: caption text trusted over viewed pixels; peeling paint mistaken for mold | Re-view: NOT YET
- Page: mold-after-water-damage | Section: Warm Indoor Temperatures (split figure) | Blunder: split photo (suburban-home-31602311) is a dry, well-kept red-brick home with a manicured lawn under a blue sky — no interior, no temperature cue, no mold or water cue — under a section about indoor temperatures (68–85°F) inside wet walls (mold-after-water-damage-img02-suburban-home-31602311.png) | Fix: swap the split to an interior wall/room subject; the dry brick exterior does not carry this section | How it was set: brick-home file reused as a generic "Plano home" illustration inside an interior-topic section | Re-view: NOT YET
- Page: mold-after-water-damage | Section: Hidden Water (split figure) | Blunder: split photo (drying-equipment-16243255) is a giant dusty industrial exhaust ventilator, with a yard/vehicles blurred behind it — not a restoration air mover inside a home, and not a hidden-water location (under LVP, inside walls, attic insulation) as the section describes (mold-after-water-damage-img03-drying-equipment-16243255.png) | Fix: swap the split to a hidden-water subject (under-floor, wall cavity, attic insulation) or to a genuine in-home air mover | How it was set: heavy-reuse "fan" file slotted by keyword, fan type and section topic not checked on viewed pixels | Re-view: NOT YET
- Page: mold-after-water-damage | Section: Signs the Clock Has Already Run Out (list tail) | Blunder: the list item "Allergy-like symptoms in one area of the house" is promoted to its own H2 band, followed by the section's closing paragraph and a lone "Call 24/7" button, while the parent Signs list ends at three bullets above it — a list item orphaned as a heading (mold-after-water-damage-mold-symptom.png) | Fix: demote the symptom line back to a fourth bullet of the Signs list and keep the closing paragraph under that list (words preserved, no cut) | How it was set: parser promoted a list item to H2 and the closing paragraph + CTA followed it into the new band | Re-view: NOT YET
- Page: mold-after-water-damage | Section: Hour-by-Hour: What Happens Inside Wet Walls and Floors (group-intro band) | Blunder: same defect as the storm page — the R4 fold is structurally present but renders as a lone one-line beige band containing only "Why Plano Homes Are at Higher Risk." between two full H2 sections (mold-after-water-damage-group-intro.png) | Fix: merge the label line into the following section as a kicker/lead line (words preserved) or fold the band away | How it was set: R4 fold demoted the group heading to a paragraph but left it isolated in its own section block | Re-view: NOT YET
- Page: sagging-ceiling | Section: Leave the room and call / 60-Second Check (split figure) | Blunder: split photo (ceiling-stain-8624464) shows a water stain running down striped wallpaper in a dated room with lace curtains, old landscape paintings and old bedding — the stain subject is correct, but the interior reads as an old foreign flat, not a Plano home (sagging-ceiling-img01-ceiling-stain-8624464.png) | Fix: swap the split to a water stain on a current Texas-style bedroom wall/ceiling | How it was set: stain subject accepted without a place-fit check on the room itself | Re-view: NOT YET
- Page: sagging-ceiling | Section: The 6 Safety Steps (split figure) | Blunder: split photo (suburban-home-30707539) is a dry red-brick house with a clay-tile roof, an orange-tiled neighbouring roof and dense trimmed hedges — European-style roofing/planting, not a Plano brick subdivision home — and it shows a dry exterior under a section about ceiling-collapse safety, with no ceiling subject at all (sagging-ceiling-img02-suburban-home-30707539.png) | Fix: swap the split to a sagging/bubbling ceiling interior; do not use this tile-roof exterior as a Plano safety-section illustration | How it was set: brick-house file slotted by "house" keyword into a ceiling-safety section, roof style and section topic not checked | Re-view: NOT YET
- Page: water-damage-insurance-texas | Section: Hero | Blunder: hero photo (commercial-office-5483188) is a generic office desk with a laptop and a city skyline through the window — no water, no claim, no adjuster, no documentation subject — as the hero of an insurance-claim guide (water-damage-insurance-texas-hero-desktop.png) | Fix: swap the hero to a claim/documentation subject (adjuster, photos of damage, paperwork with a home-damage context) | How it was set: office file assigned as a generic "professional" hero, guide topic not matched to pixels | Re-view: NOT YET
- Page: water-damage-insurance-texas | Section: Your Duty to Mitigate (split figure) | Blunder: split photo (suburban-home-15303808) is a dry Mediterranean-style house — arched white-stucco gable, louvered shutters, clay-tile roof accents — not a Plano brick home, and it carries no mitigation subject (no shut-off, no water removal, no drying) (water-damage-insurance-texas-img02-suburban-home-15303808.png) | Fix: swap the split to a mitigation subject in/around a Plano brick home (shut-off, extraction, drying in progress) | How it was set: brick-house file accepted on "brick" alone, Mediterranean styling and section topic not checked | Re-view: NOT YET
- Page: water-damage-insurance-texas | Section: Understanding Your Deductible (split figure) | Blunder: split photo (commercial-office-13068366) is an empty sleek modern office with a desk lamp and black furniture, and its own caption is sales copy — "A sleek modern office interior featuring elegant black furniture and pendant lights" — with no deductible, policy or claim subject (water-damage-insurance-texas-img03-commercial-office-13068366.png) | Fix: swap the split to a policy/claim subject and replace the sales-style caption with a plain description of the replacement | How it was set: office file reused as a generic section illustration; caption kept as stock-library sales wording | Re-view: NOT YET
- Page: water-damage-insurance-texas | Section: Mistakes That Can Hurt a Claim (list tail) | Blunder: the list item "Letting a slow drip continue after you notice it" is promoted to its own H2 band, followed by the "Protect Your Claim From Day One" paragraph and a lone "Call 24/7" button, while the parent Mistakes list ends at four bullets above it — a list item orphaned as a heading + CTA band (water-damage-insurance-texas-insurance-cta.png) | Fix: demote the drip line back to a fifth bullet of the Mistakes list and keep the closing CTA paragraph under that list (words preserved, no cut) | How it was set: parser promoted a list item to H2 and the closing paragraph + CTA followed it into the new band | Re-view: NOT YET
- Page: contact | Section: Post-hero band (between hero and Emergency section) | Blunder: a lone orange "Tap to Call: (972) 472-7917" button sits by itself in a bare white strip with no surrounding copy — a post-hero lone-button band; no other batch page has this strip (contact-hero-desktop.png) | Fix: fold the button into the hero block or into the Emergency section's copy; do not leave a button as its own section | How it was set: a doc CTA rendered as its own section block instead of being attached to adjacent copy | Re-view: NOT YET
- Page: contact | Section: Emergency in Your Plano Home? Call First, Then Do This (split figure) | Blunder: split photo (suburban-home-15303808) is the same dry Mediterranean-style house (arched stucco gable, louvered shutters, clay-tile roof) already lined on the insurance page — here it sits under emergency steps, with no emergency, water or crew subject (contact-img01-suburban-home-15303808.png) | Fix: swap the split to an emergency subject (crew, shut-off, water in progress) in a Plano-style home | How it was set: same Mediterranean file reused across pages as a generic home illustration, section topic not checked | Re-view: NOT YET
- Page: contact | Section: Service area: (split figure) | Blunder: split photo (texas-home-23930020) is a stone Mediterranean-style villa — terracotta tile roofs, a curved balcony with string lights — presented directly under the Plano ZIP service-area line, not a Plano brick-subdivision home (contact-img02-texas-home-23930020.png; also visible at the foot of contact-service-area.png) | Fix: swap the split to a Plano brick-subdivision home exterior | How it was set: file caption ("Stone suburban home in Texas") trusted over viewed pixels; Mediterranean villa styling not checked | Re-view: NOT YET
- Page: contact | Section: Service area: (heading) | Blunder: the section heading is the bare label "Service area:" (colon included) followed by a single line of ZIP codes and city names — a label promoted to H2, not a heading (contact-service-area.png) | Fix: demote the label to a lead-in line (bold lead or plain paragraph lead) under the "How to Reach Us" section, keeping the ZIP/city words unchanged | How it was set: parser promoted a doc label ("Service area:") to H2 | Re-view: NOT YET
- Page: contact | Section: Whether it's clean water, gray water or sewage (list fragmentation) | Blunder: the H2 is a clause fragment with no conclusion, and its body runs two unrelated pieces together with no break — "Your insurance company, if you plan to file a claim What Happens After You Call We answer and listen." — i.e. a "What to Have Ready" list item became the body, and the next section title ("What Happens After You Call") was flattened into paragraph text with no heading and no sentence break (contact-what-to-have.png) | Fix: restore the "Your insurance company…" line to the "What to Have Ready" list, promote "What Happens After You Call" back to an H2, and keep every word (add only the missing sentence break/heading markup, cut nothing) | How it was set: parser split a list across a section boundary, promoting one fragment to H2 and flattening the next heading into body text | Re-view: NOT YET
- Page: contact | Section: Send Us a Message (Non-Emergency) (form intro) | Blunder: the intro paragraph directly under the single form H2 repeats the heading verbatim at its start — "Send Us a Message (Non-Emergency) Use this form for questions, scheduling an inspection or following up on a job." — so the heading text appears twice in a row on screen; the R4 structural check (intro directly under H2, before the form, count 1 in main text) passes, but the duplicated echo is a visible defect (contact-contact-form.png) | Fix: strip the duplicated heading echo from the start of the intro paragraph so it begins "Use this form for questions…"; this removes a duplicate, not user content | How it was set: parser copied the section heading into the start of its lead paragraph | Re-view: NOT YET
- Page: services | Section: Services grid — Sewage Backup Cleanup card | Blunder: card photo (kitchen-leak-10961064) is a clean, wet stainless-steel kitchen sink — no sewage, no backup, no drain overflow — as the face of "Sewage Backup Cleanup" (services-card04-check.png, middle card of the second row) | Fix: swap the sewage card image to a drain/sewage-backup subject sitewide in this card slot (same fix also closes the storm-page related-card line for this file) | How it was set: wet-sink file reused as a generic "water" card image for a sewage service | Re-view: NOT YET
- Page: services | Section: Services grid — Fire Sprinkler Water Cleanup card | Blunder: card photo (flooded-floor-7924140) is the same glossy modern staircase lobby with a velvet-rope stanchion and reflective floor already lined on the storm page — a commercial lobby, not a home fire-sprinkler scene (services-card16-check.png, middle card of the sixth row) | Fix: swap the card to a sprinkler-head / sprinkler-water subject in a home or commercial interior that is actually wet | How it was set: "flooded-floor" file reused by name across card slots without a viewed-pixels check | Re-view: NOT YET

## Per-page confirmations

- storm-water-category-3: DOM clean (H1 1, overflow 0 at all widths, favicon + map present,
  no dup/banned/dot/empty). Related grid holds: Flood card = brick hero 31602311,
  Structural card = inspector 8293746. Creeks/Slabs/Clay/Weep Holes sections read clean;
  drain-pipe split (sewage-drain-3964564) accepted (downspout/drain subject fits the
  street-drain point; caption matches pixels). Lines: 5 (above).
- mold-after-water-damage: DOM clean. Related grid holds (Structural / Shut-Off /
  Extraction cards, all on-topic). Hour-by-Hour, Warm/Humidity/Hidden/Slow-Leak, Where
  Mold Shows Up, How to Stop the Clock sections read clean apart from the lined items.
  Lines: 6 (above).
- sagging-ceiling: DOM clean. Hero (ceiling-stain-14032089, worn ceiling with peeling
  paint and hanging lamp) accepted — ceiling damage is the legible subject. Attic
  insulation split (attic-insulation-6124239, worker installing pink insulation) accepted.
  Related cards accepted (ceiling-stain-3708564 stain detail; meter-box 11658940).
  Lines: 2 (above).
- water-damage-insurance-texas: DOM clean. Inspector split (moisture-meter-8293640,
  hi-vis worker examining an outlet in a modern room) accepted for "What Adjusters Look
  For". Related grid is PRESENT but holds a single card (Guide: The Mold Clock) — see
  "Artifacts NOT recorded" (centred thin grid), not lined. Lines: 4 (above).
- shut-off-valve: DOM clean. CLEAN PAGE — no lines. Hero meter/valve box (11658940) is
  an exact topic match; leaking-pipe split (15206136), wet sink (10961064), running
  faucet (34295401) all fit their sections; related grid holds (Texas homes, rooftop
  solar tank — pool-limited, see below — warm kitchen, fridge kitchen, garden pipe).
- about: DOM clean. CLEAN PAGE — no lines. Hero plumber hands (6419128) fits; retained
  split 35290675 judged ACCEPTED (see Watch verdicts); brick home with garage and
  basketball hoop (3990589) fits a Plano suburb; "We built this site so a Plano
  homeowner can do two things fast:" H2 is a complete-sentence lead, not a bare label,
  and is accepted as a doc-structure heading (see "Artifacts NOT recorded").
- contact: DOM clean. Form structure holds: single "Send Us a Message (Non-Emergency)"
  H2, intro paragraph directly under it before the `<form>`, intro sentence count 1 in
  main text — the lined defect is only the duplicated heading echo inside that
  paragraph. Mobile footer text is fully visible above the sticky call bar (see below).
  Lines: 6 (above).
- services: DOM clean. 20/20 cards present, no dup/banned file; thermal card file is
  moisture-meter-8961703, which is a DIFFERENT file from banned moisture-meter-8961700
  and is not banned (worker checking a brick wall — accepted for Thermal Imaging).
  Slab card uses crawl-space-17181949 (pool-limited slab hero file, not re-flagged).
  Find Us map section present. Lines: 2 (above).
- areas: DOM clean. CLEAN PAGE — no lines. 10/10 area/city cards present; West Plano
  brick home, Legacy West modern white house, Central brick gable, East dusk house,
  Frisco colourful homes, Allen suburban home, Richardson brick home all accepted at
  card size (see Watch note on McKinney/Murphy/North reuses). Find Us map present.
- guides: DOM clean. CLEAN PAGE — no lines. 10/10 guide cards present; card reuses of
  the storm flood, mold algae wall, sagging worn ceiling and insurance office files are
  accepted at card size under the card-size standard (subject class fits the guide
  title) and are NOT double-lined — the large-slot lines for those files are on their
  home pages. Find Us map present.

## R4-fix verification (holds, except where a line says otherwise)

- Storm + mold group intros: structural fold HOLDS (group label is a paragraph under an
  H2, no empty H2+H3 stack, no invented copy) — but the rendered one-line label band is
  itself lined above on both pages, because the fix left the label isolated as its own
  section.
- Contact form intro: HOLDS structurally (single form H2, intro directly under it before
  the form, count 1) — the duplicated heading echo inside the paragraph is lined above.
- About split 35290675 retained use: HOLDS, judged ACCEPTED (see Watch verdicts).
- Insurance related grid: PRESENT (single Mold Clock card) — not lined; single-card
  centred grid is an excluded artifact (see below).
- Hub Find Us map sections: PRESENT on services, areas and guides, and on all 7 other
  pages (map iframe in main content, 10/10).
- Hero/card chains: services Flood card = suburban-home-31602311 (brick hero) confirmed
  in services-card06-check.png. Same-shoot pairs broken (see DOM section).
- Caption purge: HOLDS — 0 R4 purge strings in any of the 10 pages.
- Banned files: HOLDS — 0 banned files in any of the 10 pages.

## Watch-item verdicts

- KNOWN pool-limited heroes — NOT re-flagged (same files, same slots, no regression):
  flood hero dry brick home, commercial hero fan, fire hero flooded stairs, wall hero
  attic brick room, warm hero kitchen, ac hero warehouse AC, ceiling hero concrete stain
  detail, ceiling-dripping hero wall-stain room, slab hero dry garage floor, water-heater
  hero rooftop solar tank, crawl hero unfinished under-floor area. None of these files
  appears in a worse slot in this batch; the water-heater solar tank (34593293) on the
  shut-off related grid and the services Water Heater card is the same known pool-limited
  use, not a new mismatch.
- Heavy reuse 9127236 (mold detail): FLAGGED at the mold hero (large slot, exterior
  algae — line above). Its small-card uses (insurance Mold Clock card, about split,
  guides Mold Clock card) are NOT separately lined: at card size the texture reads as a
  mold wall and the subject class fits the card title.
- Heavy reuse 16243255 (fan): FLAGGED on the mold Hidden Water split (wrong section and
  wrong fan type — line above). Its services Commercial card use is ACCEPTED at card
  size (fan = commercial drying equipment class), with the fan-type caveat noted.
- Heavy reuse 14032089 (worn ceiling): ACCEPTED — sagging hero and its contact/guides
  card uses all show a damaged ceiling as the legible subject; the room is old/empty but
  the subject is correct, so this is not counted as a new blunder.
- Heavy reuse 3708564 (stain detail): ACCEPTED as a card (sagging related card, services
  Ceiling card) — a stained concrete ceiling corner reads as ceiling stain at card size.
- Retained 35290675 (about split, "Who We Are in Plano"): ACCEPTED — viewed pixels show
  a technician concentrating on adjusting a water pump/pipe indoors; tight face crop is
  a stock-crop quirk, not a topic or place mismatch; the crew/work subject fits the
  section. Do not swap on Round 5 evidence.
- Retained 3935327 (hardwood): ACCEPTED — services Hardwood Floor card shows a bright
  empty room with wood floors and large windows; subject fits exactly.
- Retained 29701042 (fans body): NOT FOUND on any of the 10 Batch E pages (checked all
  DOM image lists) — no verdict possible for this batch, nothing to line.
- 15303808 (Mediterranean brick) and 23930020 (stone villa): lined at large-split size
  (insurance, contact) but ACCEPTED at area-card size (Murphy and McKinney cards), where
  a brick/stone home is the expected subject class — card-size standard, not a
  contradiction.
- 30707539 (tile-roof brick): lined as a sagging safety split, ACCEPTED as the North
  Plano area card for the same card-size reason.

## Layout / text / mobile checks

- Alignment, line width, text size: no defect observed at 1440x900 or 390x844 on any of
  the 10 pages. Body text is readable, section headings carry the orange left bar
  consistently, cards align in 3-column (desktop) grids, and no text block runs
  edge-to-edge or overflows (overflow 0 at 320/390/768/1440 on every page).
- Sticky mobile call bar: does NOT cover footer text on any page. At full bottom scroll
  (390x844) the footer-bottom text sits fully above the bar (contact-footer-mobile.png
  shows both footer lines complete, bar below them); the measured ~7px geometric overlap
  falls inside footer padding, not over any glyph. Identical bar geometry on all 10 pages.
- Post-hero lone-button bands: found on ONE page only — contact (lined above). No other
  batch page has a lone-button strip between hero and first section.
- Hub H1/H2 title repeat (services, areas, guides: the grid H2 repeats the hero H1 text)
  is the site's hub pattern, present on all three hubs, and is NOT lined.
- Text-size/line-width: no page needed a text-size line; nothing was recorded on font
  size grounds.

## Artifacts NOT recorded (per brief, deliberately excluded)

- Headless map tiles rendering blank/grey inside the Google Maps iframes (known artifact;
  iframe presence, not tile rendering, was verified — 10/10 present).
- Lazy-fill blanks that filled on re-scroll (none observed as a page defect; the
  first-pass hub-card framing issue was hunter smooth-scroll timing, re-shot and
  verified — see Method).
- Doc-structure sections: about "We built this site…" complete-sentence H2; sagging
  "Leave the room and call" CTA strip (heading + phone + links, reads as a call strip);
  hub H1/H2 title repeats.
- Centred thin grids: insurance related grid (1 card), areas final grid row (1 Murphy
  card), services final grid row (2 cards) — grid population follows the doc's related
  links, not a layout break.
- Stock-style captions that accurately describe their pixels (e.g. "A close-up image
  of a metal drainage pipe on a concrete wall", "Crop unrecognizable worker in gloves…"):
  accurate wording, not listing-copy tails, and none matches the R4 purge list — not lined.

## Screenshots

186 files in `~/workspace/plano3-water-damage/screenshots/round5/batch-e/`:
desktop hero + mobile hero + mobile footer + map + per-image viewport shots for every
page, plus section shots (storm/mold group-intro, mold symptom, insurance CTA, contact
form / service-area / what-to-have / areas-we-cover, about built) and re-shot hub-card
checks (`services-cardNN-check.png`, `areas-cardNN-check.png`, `guides-cardNN-check.png`,
40 files). Every blunder line above names its evidence file in that directory.

## Totals

- Pages hunted: 10/10. Lines: 25 (storm 5, mold 6, sagging 2, insurance 4, contact 6,
  services 2; shut-off, about, areas, guides clean).
- DOM gates all pass on all 10 pages (H1 1, overflow 0 at 4 widths, favicon + map present,
  no dup/banned/dot/empty/broken).
- Read-only compliance: no build file, generator, stylesheet or hunt file was edited;
  no rebuild, push, deploy, domain, DNS or token action was taken. Server on port 8915
  started for this hunt only and killed afterwards.
