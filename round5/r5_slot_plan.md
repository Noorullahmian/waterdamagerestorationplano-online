# Round 5 slot plan — read-only analysis (no build files touched, no rebuild)

File: `~/workspace/plano3-water-damage/round5/r5_slot_plan.json` (a JSON list, 64 objects, one per Round 5 image line).

## Counts

- 73 Round 5 lines total = 64 image lines mapped here + 9 non-image lines NOT in this file
  (cost heading hierarchy; storm + mold group-intro bands; mold symptom H2; insurance drip H2;
  contact post-hero lone button, service-area H2, list fragmentation, form-intro echo).
- 64 image lines collapse to **53 distinct controlling slots**: 12 hero slots, 41 body slots.
  Card lines are mapped to the slot that actually renders them (target hero, or target body
  fallback), proven from the built `app/<page>/page.jsx` files in card order, not assumed.
- **24 lines have a pool replacement** (16 slots).
- **40 lines are pool-limited** (37 slots): no fitting file exists in `images.json` once banned
  files (55 in `gen3_render.py`) and Round 5-flagged files (29 distinct) are excluded, and no
  wrong-topic file was relabelled to fill them. These need new photo sourcing before the fix pass.

## How card slots were proven (the two non-obvious ones)

- Home fire-sprinkler card = `BODY_FILE['fire-sprinkler-cleanup'][1]`, not the fire hero:
  the flood card takes `flooded-floor-7924140` first (flood body[1], because flood body[0]
  was already chosen by the water-extraction card), so the fire hero is already chosen and the
  fire card falls to body[1] `mold-wall-9127236`.
- Every east-plano card uses the card-hero override in `gen3_render.py`
  (`card_hero_by_slug['east-plano'] = east body[0]`), never the east hero. Changing
  `HERO_FILE['east-plano']` therefore changes no card; the home/areas east cards keep showing
  east body files and are not Round 5 lines.

## Shared slots (one change fixes several lines)

- `HERO_FILE['sewage-cleanup']` — 7 lines: sewage hero + home, crawl-space, central-plano,
  east-plano, storm, services cards. Replacement: `sewage-drain-15242228` (drain subject,
  frozen-water caveat; a true backup photo is absent from the pool).
- `BODY_FILE['commercial-water-damage'][0]` — 3 lines: commercial split + home commercial
  card + fire-sprinkler commercial card. Replacement: `commercial-office-36631701` (clean
  office; no damaged commercial interior exists in the pool).
- `BODY_FILE['water-extraction'][2]` — 2 lines: water-extraction split + flood-cleanup
  extraction card. Pool-limited.
- `BODY_FILE['fire-sprinkler-cleanup'][1]` — 2 lines: fire split + home fire card.
  Pool-limited (no sprinkler-discharge photo in the pool).
- `HERO_FILE['water-damage-insurance-texas']` — 2 lines: insurance hero + cost guide card.
  Pool-limited (no claim/documentation photo in the pool).

## Replacements with a caveat the fix pass must respect

- East hero `suburban-home-27852347`: PROVISIONAL — alt is generic and does not evidence
  brick/ranch/shingle. Pixel-verify before applying; if it fails, east hero is pool-limited.
- Central hero `texas-home-8278494`: Texas-neighborhood alt, but brick/ranch profile not
  evidenced — pixel-verify a low-profile ranch/brick look before applying.
- Commercial slots (`36631701`, `9300768`), attic body[0] (`271743`), fans body[0]
  (`7937963`), mold body[1] (`8146322`), insurance body[1] (`6419128`), laundry body[1]
  (`3964564`): subject family fits, one dimension is short (clean office, attic room not
  joists, inspection not wet carpet, interior room not temperature, pipe work not drying,
  drain pipe not washer hose). Each caveat is written in that entry's `notes`.
- Caption rewrites required with the swap (do not carry stock captions over): allen body[1]
  (listing copy), wall-drying body[1] + mold body[0] (captions claim what pixels contradict),
  insurance body[2] (sales copy) — the last three only once a sourced photo exists.

## Proposed R5 BANNED set (8 files)

Each is flagged in 2+ Round 5 slots AND has no clean use left — every remaining use shows the
same rejected pixels (the same algae wall, lobby stairs, derelict room, sky skylight,
Mediterranean house, foreign flat, peeling wall, or tile-roof house):

- `mold-wall-9127236.webp` — 8 slots (exterior algae wall everywhere it appears)
- `flooded-floor-7924140.webp` — 8 slots incl. the fire hero via the services card
  (commercial lobby stairs; banning the fire hero still needs a new sprinkler photo)
- `ceiling-stain-14032089.webp` — 3 slots (derelict empty room)
- `attic-insulation-4482829.webp` — 4 slots (blue-sky skylight, no subject)
- `suburban-home-15303808.webp` — 2 slots (Mediterranean house; murphy hero + west/north
  bodies share the same defect and would also need replacements)
- `ceiling-stain-8624464.webp` — 2 slots (dated foreign flat; ceiling-dripping hero is the
  same file)
- `mold-wall-4597285.webp` — 2 slots (derelict peeling wall; guides-hub fans card is the
  same file via the hero)
- `suburban-home-30707539.webp` — 2 slots (tile-roof house; hub/home north cards are the
  same file via the hero)

NOT globally banned, deliberately: `kitchen-leak-10961064.webp` is flagged in 2 slots
(sewage hero, laundry body) but keeps a plausible clean use on kitchen pages
(cabinet/appliance/shut-off bodies, where a wet sink fits). Fix it per-slot only; a global
ban would churn three unflagged kitchen slots. All other flagged files appear in only one
flagged slot and are per-slot overrides, not bans.

## Known pool-limited heroes — status after this plan

Untouched, as instructed, except where a Round 5 line flags the slot itself: the fire hero
(flagged via the services card) and the water-heater hero (flagged via the murphy card) are
both pool-limited even after flagging — the pool still has no sprinkler-discharge or
attic/garage-tank photo. All other pool-limited heroes (flood dry brick, commercial fan,
wall attic brick, warm kitchen, ac warehouse, ceiling stain detail, ceiling-dripping
wall-stain, slab garage floor, crawl under-floor) have no Round 5 line and were not touched.

## Verification done (no edits)

- Built `app/*/page.jsx` split order matches `BODY_FILE` + `pages-summary.json` on all 43
  doc pages; card images re-derived in card order for home, flood, crawl, fire, central,
  east, storm, murphy, cost, services, areas, guides, west, north.
- Every replacement checked: not in the 55-file banned set, not among the 29 Round 5-flagged
  files, not already on its viewing page (hero + bodies + cards), and different per page
  where the same flagged file was shared across slots.
