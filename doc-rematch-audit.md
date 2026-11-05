# Plano 3 — Doc Rematch Audit (READ-ONLY)

**Source doc:** Google Doc `plano 3` (43 tabs: homepage + 20 services + 10 areas + 10 guides + About + Contact).
**Site compared:** live GitHub Pages preview, all 46 URLs fetched 2026-11-05, every URL returned 200, plus `404.html`.
**This audit made zero edits.** No commits, no pushes, no Vercel, no DNS, no tokens. Fix pass only after the user sees this report.

## How links were detected (the blue-text rule)

- **Method A (authoritative):** Google Docs API `documents.get` with `includeTabsContent=true`, reading `textRun.textStyle.link.url` on every run.
- **Method B (visual):** runs styled underline + foreground `#1155cc` (rgb 0.0667 / 0.3333 / 0.8) — the blue the user sees in the doc.
- **Result: Method A and Method B agree 100%.** 609 blue/underline runs, 575 merged anchor phrases, **0 anomalies** (no blue text without a link, no link without blue styling).
- The earlier “0 link annotations” claim was wrong: it read a plain-text extraction, which drops link data (and an early scan of this audit read the wrong JSON field, `textRun.link` instead of `textRun.textStyle.link` — corrected and re-verified). **The doc DOES have real links, and they are the authority used below.**
- Doc link targets: exactly the 43 doc pages, every doc page targeted at least once, zero doc self-links, zero external targets, zero tel targets.

## How content was compared

- Doc body = all tab paragraphs except the header block (tab title, Meta Title/Description, URL, H1 — those are compared separately, exactly). Doc tables are tracked separately from regular paragraphs.
- Page text = visible text in `<main>` content + FAQ items only. Header, footer, sticky call bar, related cards, and image captions are excluded from the word-diff (they are template, listed separately).
- Tokenisation (identical both sides): em/en dash → space, curly apostrophe → straight, lowercase, split on non-alphanumerics (so “Plano’s” counts as `plano, s` on both sides — a link boundary inside a possessive cannot fake a diff).
- Bracket markers: `[Trust points]`, `Form fields:`, standalone `button` lines dropped (labels only, never visible); `[Call Now: …]` / `[Send Message]` inner text kept (they render as buttons); `Line under the button:` prefix stripped, sentence kept.
- Template tokens subtracted from page counts (disclosed, so the “0 added” claim is auditable): page H1 (compared separately), card-section headings, map-section headings (“Find Us in Plano, TX”), FAQ-heading prefixes (rendered “<ShortName> FAQs” minus the doc’s own “FAQs” word), and the hero CTA button — but ONLY when its text does not match a doc CTA line (when it matches, the hero button IS that line’s rendering).
- Link classes: MATCH = same anchor + same target in content/FAQ; PARTIAL ANCHOR = same target but the site link covers only part of the doc phrase (per the user’s rule this counts as missing); WRONG TARGET = same anchor, different target; MISSING = no content link at all; MATCH-HEADER-FOOTER = found only in nav/footer, not in content; EXTRA = site content link with no doc counterpart; SELF = page linking to itself in content (header/footer exempt).

## Headline findings (honest totals)

- **Doc links: 575** → MATCH 441, PARTIAL ANCHOR 24, MISSING 100, MATCH-HEADER-FOOTER 10, WRONG TARGET 0, SELF-LINK content 0, SELF-LINK cards 0.
- **EXTRA site content links (builder-added, no doc counterpart): 134.**
- **Content words: doc 52528 tokens** (regular 44809, table 7719) → **missing 7728** (directly table-attributed 2774, regular-paragraph residual 9), **added 0**.
- **Meta: title, description, and H1 match exactly on 43/43 pages.** Doc headers also match the earlier `tabs.json` extraction on 43/43.
- **Hubs (services / areas / guides) and 404 are clean:** every hub card target is a real doc page; 404 carries only header/footer/sticky links.

## The two root causes (everything else follows from these)

### 1. The builder never saw the doc’s blue links

The site was built from a plain-text extraction, which contains no link data. Internal links were instead produced from the builder’s own phrase map (textual references → slugs). That is why 441 of 575 doc links still match (the common phrases are in the map) while the long tail does not: list-item links the map lacks (“Water heater leaks”, “Sewage backups”, “wet attic insulation”), bold lead-ins rendered as plain `<strong>` (“Crawl space drying”, “Commercial water damage” on east-plano), ZIP-qualified anchors linked only on the short name (“Legacy West and Deerfield (75024)” → “Legacy West”), and all 12 in-table links (tables are not rendered at all). It is also why 134 EXTRA links exist: map phrases linked wherever the words appear, even where the doc has plain text (e.g. home’s “24/7 Emergency Water Damage Cleanup”, “Slab Leak Water Damage” title lines; area pages’ repeated “flood cleanup” / “sewage backup cleanup”).

### 2. Doc tables are not rendered

Every doc tab contains tables (7,719 table tokens sitewide). None of their cell text appears in the rendered pages — verified by direct grep (e.g. home’s “Custer Rd, Independence Pkwy, Coit Rd” and “Particleboard boxes swollen by dirty water” return 0 hits in the live HTML). What tables carry, per page group:

- **Home:** street lists (“Custer Rd, Independence Pkwy, Coit Rd”, “W Parker Rd, Coit Rd, Alma Dr”), save-vs-remove lists (“Particleboard boxes swollen by dirty water”, “Planks lifted, cleaned and relaid if click-locks hold”), area-group rows (ZIPs, neighborhoods, housing notes).
- **Service/guide pages:** “What Can Be Saved”-style save/remove rows and similar checklist tables.
- **Area pages:** at-a-glance rows (ZIPs, neighborhoods, streets, housing-era notes) — the largest per-page gaps (242–298 table tokens each).
- **Contact:** the “Areas We Cover” table (8 area links lost with it).

Regular (non-table) doc text, by contrast, renders **exactly**: 0 added words sitewide, and only 9 residual regular tokens (below). The “missing” headline is a table problem, not a prose problem.

## The 9 regular-paragraph residuals (everything else in prose is exact)

- **List-conjunction drops (3 tokens):** the builder’s list renderer turns “X and Y” into comma-separated linked items and drops the word “and”: water-extraction’s ZIP list loses 2 (“West Plano (75093) and Legacy West (75024)”, “Frisco and Richardson”), about’s “And nearby” list loses 1 (“Richardson, and Murphy, Parker & Wylie”). Wording change is real but confined to list punctuation.
- **About, one CTA button (6 tokens):** the doc has two `[Call 24/7: (972) 472-7917]` lines (early + tail); the page renders only one in main content. The identical “Call 24/7: (972) 472-7917” text still appears on the page in the header/footer template buttons, so a visitor loses nothing — but strictly, one doc CTA occurrence has no main-content rendering.

## Per-page table (43 doc pages)

| Tab | Page | Doc words (reg / tbl) | Missing total (reg / tbl-attr) | Added | Doc links | MATCH | PARTIAL | MISSING | HDR/FTR only | EXTRA | Meta |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | (home) | 2934 (2513 / 421) | 421 (0 / 118) | 0 | 26 | 26 | 0 | 0 | 0 | 9 | OK |
| 2 | emergency-water-damage | 1375 (1197 / 178) | 178 (0 / 70) | 0 | 14 | 14 | 0 | 0 | 0 | 3 | OK |
| 3 | water-extraction | 1201 (1049 / 152) | 154 (2 / 59) | 0 | 13 | 13 | 0 | 0 | 0 | 3 | OK |
| 4 | structural-drying | 1320 (1189 / 131) | 131 (0 / 47) | 0 | 10 | 10 | 0 | 0 | 0 | 0 | OK |
| 5 | burst-pipe-cleanup | 1209 (1077 / 132) | 132 (0 / 51) | 0 | 11 | 11 | 0 | 0 | 0 | 1 | OK |
| 6 | sewage-cleanup | 1188 (1063 / 125) | 125 (0 / 48) | 0 | 6 | 6 | 0 | 0 | 0 | 0 | OK |
| 7 | slab-leak | 1361 (1245 / 116) | 116 (0 / 45) | 0 | 10 | 10 | 0 | 0 | 0 | 4 | OK |
| 8 | water-heater-leak | 1346 (1225 / 121) | 121 (0 / 44) | 0 | 11 | 10 | 0 | 1 | 0 | 2 | OK |
| 9 | ceiling-leak | 1248 (1136 / 112) | 112 (0 / 32) | 0 | 11 | 10 | 0 | 1 | 0 | 2 | OK |
| 10 | flood-cleanup | 1215 (1104 / 111) | 111 (0 / 38) | 0 | 9 | 9 | 0 | 0 | 0 | 6 | OK |
| 11 | commercial-water-damage | 1187 (968 / 219) | 219 (0 / 88) | 0 | 7 | 7 | 0 | 0 | 0 | 4 | OK |
| 12 | hardwood-floor-drying | 1168 (1053 / 115) | 115 (0 / 35) | 0 | 8 | 8 | 0 | 0 | 0 | 1 | OK |
| 13 | ac-overflow | 1236 (1128 / 108) | 108 (0 / 37) | 0 | 8 | 8 | 0 | 0 | 0 | 0 | OK |
| 14 | cabinet-drying | 1164 (1040 / 124) | 124 (0 / 46) | 0 | 10 | 10 | 0 | 0 | 0 | 0 | OK |
| 15 | laundry-overflow | 1094 (942 / 152) | 152 (0 / 60) | 0 | 13 | 12 | 0 | 1 | 0 | 1 | OK |
| 16 | crawl-space-drying | 1067 (957 / 110) | 110 (0 / 42) | 0 | 9 | 9 | 0 | 0 | 0 | 2 | OK |
| 17 | appliance-leak | 1037 (926 / 111) | 111 (0 / 47) | 0 | 10 | 10 | 0 | 0 | 0 | 1 | OK |
| 18 | fire-sprinkler-cleanup | 966 (854 / 112) | 112 (0 / 48) | 0 | 7 | 7 | 0 | 0 | 0 | 0 | OK |
| 19 | moisture-mapping | 980 (856 / 124) | 124 (0 / 42) | 0 | 10 | 10 | 0 | 0 | 0 | 0 | OK |
| 20 | attic-insulation-drying | 1096 (991 / 105) | 105 (0 / 32) | 0 | 11 | 10 | 0 | 1 | 0 | 0 | OK |
| 21 | wall-drying | 1227 (1123 / 104) | 104 (0 / 31) | 0 | 9 | 9 | 0 | 0 | 0 | 2 | OK |
| 22 | west-plano | 1742 (1444 / 298) | 298 (0 / 101) | 0 | 23 | 16 | 3 | 3 | 1 | 7 | OK |
| 23 | legacy-west | 1560 (1265 / 295) | 295 (0 / 104) | 0 | 23 | 13 | 3 | 6 | 1 | 5 | OK |
| 24 | north-plano | 1482 (1208 / 274) | 274 (0 / 101) | 0 | 20 | 16 | 1 | 2 | 1 | 13 | OK |
| 25 | central-plano | 1487 (1208 / 279) | 279 (0 / 105) | 0 | 21 | 16 | 0 | 4 | 1 | 10 | OK |
| 26 | east-plano | 1452 (1156 / 296) | 296 (0 / 97) | 0 | 19 | 9 | 0 | 9 | 1 | 6 | OK |
| 27 | frisco | 1363 (1102 / 261) | 261 (0 / 105) | 0 | 22 | 17 | 1 | 3 | 1 | 6 | OK |
| 28 | allen | 1322 (1062 / 260) | 260 (0 / 109) | 0 | 22 | 14 | 1 | 6 | 1 | 11 | OK |
| 29 | mckinney | 1314 (1048 / 266) | 266 (0 / 108) | 0 | 19 | 11 | 1 | 6 | 1 | 8 | OK |
| 30 | richardson | 1286 (1044 / 242) | 242 (0 / 99) | 0 | 22 | 12 | 0 | 9 | 1 | 9 | OK |
| 31 | murphy | 1311 (1050 / 261) | 261 (0 / 113) | 0 | 20 | 13 | 1 | 5 | 1 | 6 | OK |
| 32 | shut-off-valve | 1053 (895 / 158) | 158 (0 / 58) | 0 | 7 | 7 | 0 | 0 | 0 | 2 | OK |
| 33 | warm-spot-on-floor | 1003 (824 / 179) | 179 (0 / 61) | 0 | 8 | 6 | 0 | 2 | 0 | 1 | OK |
| 34 | ceiling-dripping | 905 (721 / 184) | 184 (0 / 48) | 0 | 11 | 9 | 1 | 1 | 0 | 1 | OK |
| 35 | water-damage-cost | 1037 (870 / 167) | 167 (0 / 47) | 0 | 9 | 8 | 1 | 0 | 0 | 3 | OK |
| 36 | fans-wont-dry-walls | 953 (809 / 144) | 144 (0 / 50) | 0 | 6 | 5 | 0 | 1 | 0 | 0 | OK |
| 37 | storm-water-category-3 | 978 (746 / 232) | 232 (0 / 78) | 0 | 7 | 6 | 0 | 1 | 0 | 0 | OK |
| 38 | mold-after-water-damage | 878 (725 / 153) | 153 (0 / 43) | 0 | 7 | 4 | 2 | 1 | 0 | 0 | OK |
| 39 | copper-pinhole-leaks | 913 (732 / 181) | 181 (0 / 70) | 0 | 13 | 9 | 1 | 3 | 0 | 1 | OK |
| 40 | sagging-ceiling | 932 (762 / 170) | 170 (0 / 44) | 0 | 6 | 3 | 2 | 1 | 0 | 0 | OK |
| 41 | water-damage-insurance-texas | 923 (727 / 196) | 196 (0 / 61) | 0 | 5 | 2 | 1 | 2 | 0 | 0 | OK |
| 42 | about | 1155 (1031 / 124) | 131 (7 / 51) | 0 | 30 | 14 | 5 | 11 | 0 | 4 | OK |
| 43 | contact | 860 (744 / 116) | 116 (0 / 61) | 0 | 32 | 12 | 0 | 20 | 0 | 0 | OK |

Notes: “Missing total” is a token-Counter deficit; where a word appears in both regular and table text, the page count equals the regular count, so the table copies show up in the total but not in the split columns — the total is the honest number, the split shows direct attribution. “Added” is 0 on every page after the disclosed template subtractions.

## Full mismatch lists (per page)

Target slugs are bare (empty = home). “Heading” is the doc section the link sits under. “tbl” = link inside a doc table.

### Tab 1 — (home) (doc links 26)
- **EXTRA (9 — site content link, no doc counterpart):**
  - site anchor `24/7 Emergency Water Damage Cleanup` → target `emergency-water-damage` (main-content)
  - site anchor `Slab Leak Water Damage` → target `slab-leak` (main-content)
  - site anchor `water heater leak cleanup` → target `water-heater-leak` (main-content)
  - site anchor `sewage backup cleanup` → target `sewage-cleanup` (main-content)
  - site anchor `commercial water damage restoration` → target `commercial-water-damage` (main-content)
  - site anchor `Central Plano` → target `central-plano` (main-content)
  - site anchor `Legacy West` → target `legacy-west` (main-content)
  - site anchor `Legacy West` → target `legacy-west` (main-content)
  - site anchor `slab leak` → target `slab-leak` (faq)

### Tab 2 — emergency-water-damage (doc links 14)
- **EXTRA (3 — site content link, no doc counterpart):**
  - site anchor `Legacy West` → target `legacy-west` (main-content)
  - site anchor `Legacy West` → target `legacy-west` (main-content)
  - site anchor `water extraction` → target `water-extraction` (faq)

### Tab 3 — water-extraction (doc links 13)
- **EXTRA (3 — site content link, no doc counterpart):**
  - site anchor `East Plano` → target `east-plano` (main-content)
  - site anchor `Central Plano` → target `central-plano` (main-content)
  - site anchor `North Plano` → target `north-plano` (main-content)

### Tab 4 — structural-drying: CLEAN (all doc links match, no extras)

### Tab 5 — burst-pipe-cleanup (doc links 11)
- **EXTRA (1 — site content link, no doc counterpart):**
  - site anchor `Central Plano` → target `central-plano` (main-content)

### Tab 6 — sewage-cleanup: CLEAN (all doc links match, no extras)

### Tab 7 — slab-leak (doc links 10)
- **EXTRA (4 — site content link, no doc counterpart):**
  - site anchor `Central Plano` → target `central-plano` (main-content)
  - site anchor `North Plano` → target `north-plano` (main-content)
  - site anchor `West Plano` → target `west-plano` (main-content)
  - site anchor `East Plano` → target `east-plano` (main-content)

### Tab 8 — water-heater-leak (doc links 11)
- **MISSING (1):**
  - doc anchor `sagging ceiling safety steps` → target `sagging-ceiling` | heading `Water Heater Burst in Your Plano Home? Do These 5 Things Now` | tbl=False
- **EXTRA (2 — site content link, no doc counterpart):**
  - site anchor `Central Plano` → target `central-plano` (main-content)
  - site anchor `West Plano` → target `west-plano` (main-content)

### Tab 9 — ceiling-leak (doc links 11)
- **MISSING (1):**
  - doc anchor `sagging ceiling safety steps` → target `sagging-ceiling` | heading `Water Coming Through Your Plano Ceiling? Do These 5 Things` | tbl=False
- **EXTRA (2 — site content link, no doc counterpart):**
  - site anchor `Central Plano` → target `central-plano` (main-content)
  - site anchor `AC overflows` → target `ac-overflow` (main-content)

### Tab 10 — flood-cleanup (doc links 9)
- **EXTRA (6 — site content link, no doc counterpart):**
  - site anchor `Frisco` → target `frisco` (main-content)
  - site anchor `Allen` → target `allen` (main-content)
  - site anchor `East Plano` → target `east-plano` (main-content)
  - site anchor `Central Plano` → target `central-plano` (main-content)
  - site anchor `North Plano` → target `north-plano` (main-content)
  - site anchor `West Plano` → target `west-plano` (main-content)

### Tab 11 — commercial-water-damage (doc links 7)
- **EXTRA (4 — site content link, no doc counterpart):**
  - site anchor `Legacy West` → target `legacy-west` (main-content)
  - site anchor `Legacy West` → target `legacy-west` (main-content)
  - site anchor `Legacy West` → target `legacy-west` (main-content)
  - site anchor `East Plano` → target `east-plano` (main-content)

### Tab 12 — hardwood-floor-drying (doc links 8)
- **EXTRA (1 — site content link, no doc counterpart):**
  - site anchor `West Plano` → target `west-plano` (main-content)

### Tab 13 — ac-overflow: CLEAN (all doc links match, no extras)

### Tab 14 — cabinet-drying: CLEAN (all doc links match, no extras)

### Tab 15 — laundry-overflow (doc links 13)
- **MISSING (1):**
  - doc anchor `sagging ceiling safety steps` → target `sagging-ceiling` | heading `Upstairs Washer Flooded Your Plano Home? Do These 5 Things` | tbl=False
- **EXTRA (1 — site content link, no doc counterpart):**
  - site anchor `Allen` → target `allen` (main-content)

### Tab 16 — crawl-space-drying (doc links 9)
- **EXTRA (2 — site content link, no doc counterpart):**
  - site anchor `West Plano` → target `west-plano` (main-content)
  - site anchor `East Plano` → target `east-plano` (main-content)

### Tab 17 — appliance-leak (doc links 10)
- **EXTRA (1 — site content link, no doc counterpart):**
  - site anchor `hardwood floor drying` → target `hardwood-floor-drying` (faq)

### Tab 18 — fire-sprinkler-cleanup: CLEAN (all doc links match, no extras)

### Tab 19 — moisture-mapping: CLEAN (all doc links match, no extras)

### Tab 20 — attic-insulation-drying (doc links 11)
- **MISSING (1):**
  - doc anchor `sagging ceiling safety steps` → target `sagging-ceiling` | heading `Wet Insulation in Your Plano Attic? Do These 5 Things` | tbl=False

### Tab 21 — wall-drying (doc links 9)
- **EXTRA (2 — site content link, no doc counterpart):**
  - site anchor `West Plano` → target `west-plano` (main-content)
  - site anchor `North Plano` → target `north-plano` (main-content)

### Tab 22 — west-plano (doc links 23)
- **MISSING (3):**
  - doc anchor `where to find your shut-off valve` → target `shut-off-valve` | heading `Water Emergency in Your West Plano Home? Do These 5 Things` | tbl=False
  - doc anchor `moisture mapping` → target `moisture-mapping` | heading `What West Plano Homeowners Search When Water Hits` | tbl=False
  - doc anchor `Frisco` → target `frisco` | heading `What about nearby areas?` | tbl=False
- **PARTIAL ANCHOR (3 — link covers only part of the doc phrase):**
  - doc anchor `Kitchen cabinet drying` → target `cabinet-drying` | site anchor `cabinet drying` (main-content) | heading `Most Requested Services in West Plano`
  - doc anchor `Upstairs laundry overflow` → target `laundry-overflow` | site anchor `laundry overflow` (main-content) | heading `Most Requested Services in West Plano`
  - doc anchor `Legacy West and Deerfield (75024)` → target `legacy-west` | site anchor `Legacy West` (faq) | heading `What about nearby areas?`
- **HEADER/FOOTER ONLY (1 — not in content):**
  - doc anchor `24/7 emergency water damage cleanup` → target `emergency-water-damage` | site anchor `24/7 Emergency Water Damage Cleanup` (footer)
- **EXTRA (7 — site content link, no doc counterpart):**
  - site anchor `hardwood floor drying` → target `hardwood-floor-drying` (main-content)
  - site anchor `AC overflow cleanup` → target `ac-overflow` (main-content)
  - site anchor `slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `water heater leak` → target `water-heater-leak` (main-content)
  - site anchor `water heater leak cleanup` → target `water-heater-leak` (main-content)
  - site anchor `cabinet drying` → target `cabinet-drying` (main-content)
  - site anchor `slab leak` → target `slab-leak` (main-content)

### Tab 23 — legacy-west (doc links 23)
- **MISSING (6):**
  - doc anchor `where to find your shut-off valve` → target `shut-off-valve` | heading `Water Emergency in Your 75024 Home? Do These 5 Things` | tbl=False
  - doc anchor `fire sprinkler cleanup` → target `fire-sprinkler-cleanup` | heading `Stacked Living Around Legacy West` | tbl=False
  - doc anchor `Commercial water damage` → target `commercial-water-damage` | heading `Most Requested Services in 75024` | tbl=False
  - doc anchor `fire sprinkler cleanup` → target `fire-sprinkler-cleanup` | heading `Legacy West and The Shops at Legacy` | tbl=False
  - doc anchor `commercial water damage` → target `commercial-water-damage` | heading `Granite Park and the Headquarters Drive Corridor` | tbl=False
  - doc anchor `Frisco` → target `frisco` | heading `Do you cover nearby areas too?` | tbl=False
- **PARTIAL ANCHOR (3 — link covers only part of the doc phrase):**
  - doc anchor `Upstairs laundry overflow` → target `laundry-overflow` | site anchor `laundry overflow` (main-content) | heading `Most Requested Services in 75024`
  - doc anchor `West Plano and Willow Bend (75093)` → target `west-plano` | site anchor `West Plano` (faq) | heading `Do you cover nearby areas too?`
  - doc anchor `North Plano (75025)` → target `north-plano` | site anchor `North Plano` (faq) | heading `Do you cover nearby areas too?`
- **HEADER/FOOTER ONLY (1 — not in content):**
  - doc anchor `24/7 emergency water damage cleanup` → target `emergency-water-damage` | site anchor `24/7 Emergency Water Damage Cleanup` (footer)
- **EXTRA (5 — site content link, no doc counterpart):**
  - site anchor `laundry overflow cleanup` → target `laundry-overflow` (main-content)
  - site anchor `slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `AC overflow cleanup` → target `ac-overflow` (main-content)
  - site anchor `flood cleanup` → target `flood-cleanup` (main-content)
  - site anchor `AC overflow` → target `ac-overflow` (main-content)

### Tab 24 — north-plano (doc links 20)
- **MISSING (2):**
  - doc anchor `where to find your shut-off valve` → target `shut-off-valve` | heading `Water Emergency in Your North Plano Home? Do These 5 Things` | tbl=False
  - doc anchor `Allen` → target `allen` | heading `Do you cover nearby areas?` | tbl=False
- **PARTIAL ANCHOR (1 — link covers only part of the doc phrase):**
  - doc anchor `wet attic insulation removal` → target `attic-insulation-drying` | site anchor `attic insulation removal` (main-content) | heading `Most Requested Services in North Plano`
- **HEADER/FOOTER ONLY (1 — not in content):**
  - doc anchor `24/7 emergency water damage cleanup` → target `emergency-water-damage` | site anchor `24/7 Emergency Water Damage Cleanup` (footer)
- **EXTRA (13 — site content link, no doc counterpart):**
  - site anchor `slab leak` → target `slab-leak` (main-content)
  - site anchor `Slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `Water heater leak cleanup` → target `water-heater-leak` (main-content)
  - site anchor `water heater leak cleanup` → target `water-heater-leak` (main-content)
  - site anchor `flood cleanup` → target `flood-cleanup` (main-content)
  - site anchor `AC overflow cleanup` → target `ac-overflow` (main-content)
  - site anchor `slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `slab leak` → target `slab-leak` (main-content)
  - site anchor `slab leak` → target `slab-leak` (main-content)
  - site anchor `slab leak` → target `slab-leak` (main-content)
  - site anchor `attic insulation removal` → target `attic-insulation-drying` (main-content)
  - site anchor `attic insulation removal` → target `attic-insulation-drying` (main-content)
  - site anchor `Slab leak` → target `slab-leak` (main-content)

### Tab 25 — central-plano (doc links 21)
- **MISSING (4):**
  - doc anchor `where to find your shut-off valve` → target `shut-off-valve` | heading `Water Emergency in Your Central Plano Home? Do These 5 Things` | tbl=False
  - doc anchor `moisture mapping` → target `moisture-mapping` | heading `What Central Plano Homeowners Search When Water Hits` | tbl=False
  - doc anchor `West Plano` → target `west-plano` | heading `Do you cover nearby areas?` | tbl=False
  - doc anchor `Richardson` → target `richardson` | heading `Do you cover nearby areas?` | tbl=False
- **HEADER/FOOTER ONLY (1 — not in content):**
  - doc anchor `24/7 emergency water damage cleanup` → target `emergency-water-damage` | site anchor `24/7 Emergency Water Damage Cleanup` (footer)
- **EXTRA (10 — site content link, no doc counterpart):**
  - site anchor `Slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `Sewage backup cleanup` → target `sewage-cleanup` (main-content)
  - site anchor `Flood cleanup` → target `flood-cleanup` (main-content)
  - site anchor `sewage backup cleanup` → target `sewage-cleanup` (main-content)
  - site anchor `slab leak` → target `slab-leak` (main-content)
  - site anchor `slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `ceiling leak water damage` → target `ceiling-leak` (main-content)
  - site anchor `flood cleanup` → target `flood-cleanup` (main-content)
  - site anchor `sewage backup cleanup` → target `sewage-cleanup` (main-content)
  - site anchor `slab leak` → target `slab-leak` (main-content)

### Tab 26 — east-plano (doc links 19)
- **MISSING (9):**
  - doc anchor `where to find your shut-off valve` → target `shut-off-valve` | heading `Water Emergency in Your East Plano Home? Do These 5 Things` | tbl=False
  - doc anchor `crawl space drying` → target `crawl-space-drying` | heading `Historic Pier-and-Beam Homes` | tbl=False
  - doc anchor `Crawl space drying` → target `crawl-space-drying` | heading `Most Requested Services in East Plano` | tbl=False
  - doc anchor `Commercial water damage` → target `commercial-water-damage` | heading `Most Requested Services in East Plano` | tbl=False
  - doc anchor `crawl space drying` → target `crawl-space-drying` | heading `Haggard Park and Old Towne` | tbl=False
  - doc anchor `commercial water damage` → target `commercial-water-damage` | heading `Downtown Plano and the 15th Street Corridor` | tbl=False
  - doc anchor `fire sprinkler cleanup` → target `fire-sprinkler-cleanup` | heading `Downtown Plano and the 15th Street Corridor` | tbl=False
  - doc anchor `moisture mapping` → target `moisture-mapping` | heading `What East Plano Residents Search When Water Hits` | tbl=False
  - doc anchor `Murphy, Parker & Wylie` → target `murphy` | heading `Do you cover nearby areas?` | tbl=False
- **HEADER/FOOTER ONLY (1 — not in content):**
  - doc anchor `24/7 emergency water damage cleanup` → target `emergency-water-damage` | site anchor `24/7 Emergency Water Damage Cleanup` (footer)
- **EXTRA (6 — site content link, no doc counterpart):**
  - site anchor `West Plano` → target `west-plano` (main-content)
  - site anchor `Sewage backup cleanup` → target `sewage-cleanup` (main-content)
  - site anchor `Flood cleanup` → target `flood-cleanup` (main-content)
  - site anchor `flood cleanup` → target `flood-cleanup` (main-content)
  - site anchor `sewage backup cleanup` → target `sewage-cleanup` (main-content)
  - site anchor `flood cleanup` → target `flood-cleanup` (main-content)

### Tab 27 — frisco (doc links 22)
- **MISSING (3):**
  - doc anchor `Allen` → target `allen` | heading `Do you cover nearby areas?` | tbl=False
  - doc anchor `McKinney` → target `mckinney` | heading `Do you cover nearby areas?` | tbl=False
  - doc anchor `water damage restoration` → target `(home)` | heading `Water Damage in Frisco? Call (972) 472-7917.` | tbl=False
- **PARTIAL ANCHOR (1 — link covers only part of the doc phrase):**
  - doc anchor `Upstairs laundry overflow` → target `laundry-overflow` | site anchor `laundry overflow` (main-content) | heading `Most Requested Services in Frisco`
- **HEADER/FOOTER ONLY (1 — not in content):**
  - doc anchor `24/7 emergency water damage cleanup` → target `emergency-water-damage` | site anchor `24/7 Emergency Water Damage Cleanup` (footer)
- **EXTRA (6 — site content link, no doc counterpart):**
  - site anchor `water heater leak cleanup` → target `water-heater-leak` (main-content)
  - site anchor `slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `flood cleanup` → target `flood-cleanup` (main-content)
  - site anchor `hardwood floor drying` → target `hardwood-floor-drying` (main-content)
  - site anchor `AC overflow cleanup` → target `ac-overflow` (main-content)
  - site anchor `cabinet drying` → target `cabinet-drying` (main-content)

### Tab 28 — allen (doc links 22)
- **MISSING (6):**
  - doc anchor `where to find your shut-off valve` → target `shut-off-valve` | heading `Water Emergency in Your Allen Home? Do These 5 Things` | tbl=False
  - doc anchor `Commercial water damage` → target `commercial-water-damage` | heading `Most Requested Services in Allen` | tbl=False
  - doc anchor `commercial water damage` → target `commercial-water-damage` | heading `Watters Creek Area` | tbl=False
  - doc anchor `Frisco` → target `frisco` | heading `Do you cover nearby areas?` | tbl=False
  - doc anchor `Murphy, Parker & Wylie` → target `murphy` | heading `Do you cover nearby areas?` | tbl=False
  - doc anchor `water damage restoration` → target `(home)` | heading `Water Damage in Allen? Call (972) 472-7917.` | tbl=False
- **PARTIAL ANCHOR (1 — link covers only part of the doc phrase):**
  - doc anchor `wet attic insulation removal` → target `attic-insulation-drying` | site anchor `attic insulation removal` (main-content) | heading `Hail Alley Roofs and Attic Equipment`
- **HEADER/FOOTER ONLY (1 — not in content):**
  - doc anchor `24/7 emergency water damage cleanup` → target `emergency-water-damage` | site anchor `24/7 Emergency Water Damage Cleanup` (footer)
- **EXTRA (11 — site content link, no doc counterpart):**
  - site anchor `slab leak` → target `slab-leak` (main-content)
  - site anchor `slab leak` → target `slab-leak` (main-content)
  - site anchor `Slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `hardwood floor drying` → target `hardwood-floor-drying` (main-content)
  - site anchor `cabinet drying` → target `cabinet-drying` (main-content)
  - site anchor `slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `flood cleanup` → target `flood-cleanup` (main-content)
  - site anchor `slab leak` → target `slab-leak` (main-content)
  - site anchor `water heater leak` → target `water-heater-leak` (main-content)
  - site anchor `ceiling leak` → target `ceiling-leak` (main-content)
  - site anchor `attic insulation removal` → target `attic-insulation-drying` (main-content)

### Tab 29 — mckinney (doc links 19)
- **MISSING (6):**
  - doc anchor `where to find your shut-off valve` → target `shut-off-valve` | heading `Water Emergency in Your McKinney Home? Do These 5 Things` | tbl=False
  - doc anchor `crawl space drying` → target `crawl-space-drying` | heading `Historic Pier-and-Beam Homes Downtown` | tbl=False
  - doc anchor `Crawl space drying` → target `crawl-space-drying` | heading `Most Requested Services in McKinney` | tbl=False
  - doc anchor `crawl space drying` → target `crawl-space-drying` | heading `Historic Downtown McKinney (75069)` | tbl=False
  - doc anchor `North Plano` → target `north-plano` | heading `Do you cover nearby areas?` | tbl=False
  - doc anchor `water damage restoration` → target `(home)` | heading `Water Damage in McKinney? Call (972) 472-7917.` | tbl=False
- **PARTIAL ANCHOR (1 — link covers only part of the doc phrase):**
  - doc anchor `Upstairs laundry overflow` → target `laundry-overflow` | site anchor `laundry overflow` (main-content) | heading `Most Requested Services in McKinney`
- **HEADER/FOOTER ONLY (1 — not in content):**
  - doc anchor `24/7 emergency water damage cleanup` → target `emergency-water-damage` | site anchor `24/7 Emergency Water Damage Cleanup` (footer)
- **EXTRA (8 — site content link, no doc counterpart):**
  - site anchor `slab leak` → target `slab-leak` (main-content)
  - site anchor `Slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `AC overflows` → target `ac-overflow` (main-content)
  - site anchor `slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `flood cleanup` → target `flood-cleanup` (main-content)
  - site anchor `slab leak` → target `slab-leak` (main-content)
  - site anchor `flood cleanup` → target `flood-cleanup` (main-content)
  - site anchor `hardwood floor drying` → target `hardwood-floor-drying` (main-content)

### Tab 30 — richardson (doc links 22)
- **MISSING (9):**
  - doc anchor `where to find your shut-off valve` → target `shut-off-valve` | heading `Water Emergency in Your Richardson Home? Do These 5 Things` | tbl=False
  - doc anchor `commercial water damage` → target `commercial-water-damage` | heading `Offices Along the Telecom Corridor` | tbl=False
  - doc anchor `fire sprinkler cleanup` → target `fire-sprinkler-cleanup` | heading `Offices Along the Telecom Corridor` | tbl=False
  - doc anchor `Commercial water damage` → target `commercial-water-damage` | heading `Most Requested Services in Richardson` | tbl=False
  - doc anchor `commercial water damage` → target `commercial-water-damage` | heading `Telecom Corridor, CityLine and the UT Dallas Area` | tbl=False
  - doc anchor `fire sprinkler cleanup` → target `fire-sprinkler-cleanup` | heading `Telecom Corridor, CityLine and the UT Dallas Area` | tbl=False
  - doc anchor `moisture mapping` → target `moisture-mapping` | heading `What Richardson Residents Search When Water Hits` | tbl=False
  - doc anchor `Murphy, Parker & Wylie` → target `murphy` | heading `Do you cover nearby areas?` | tbl=False
  - doc anchor `water damage restoration` → target `(home)` | heading `Water Damage in Richardson? Call (972) 472-7917.` | tbl=False
- **HEADER/FOOTER ONLY (1 — not in content):**
  - doc anchor `24/7 emergency water damage cleanup` → target `emergency-water-damage` | site anchor `24/7 Emergency Water Damage Cleanup` (footer)
- **EXTRA (9 — site content link, no doc counterpart):**
  - site anchor `sewage backup cleanup` → target `sewage-cleanup` (main-content)
  - site anchor `Sewage backup cleanup` → target `sewage-cleanup` (main-content)
  - site anchor `Slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `sewage backup cleanup` → target `sewage-cleanup` (main-content)
  - site anchor `slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `AC overflows` → target `ac-overflow` (main-content)
  - site anchor `burst pipe cleanup` → target `burst-pipe-cleanup` (main-content)
  - site anchor `slab leak` → target `slab-leak` (main-content)
  - site anchor `flood cleanup` → target `flood-cleanup` (main-content)

### Tab 31 — murphy (doc links 20)
- **MISSING (5):**
  - doc anchor `where to find your shut-off valve` → target `shut-off-valve` | heading `Water Emergency in Your Murphy, Parker or Wylie Home? Do These 5 Things` | tbl=False
  - doc anchor `crawl space drying` → target `crawl-space-drying` | heading `Older Wylie Homes` | tbl=False
  - doc anchor `crawl space drying` → target `crawl-space-drying` | heading `Downtown Wylie and Older Homes` | tbl=False
  - doc anchor `Richardson` → target `richardson` | heading `Do you cover nearby areas?` | tbl=False
  - doc anchor `water damage restoration` → target `(home)` | heading `Water Damage East of Plano? Call (972) 472-7917.` | tbl=False
- **PARTIAL ANCHOR (1 — link covers only part of the doc phrase):**
  - doc anchor `Upstairs laundry overflow` → target `laundry-overflow` | site anchor `laundry overflow` (main-content) | heading `Most Requested Services East of Plano`
- **HEADER/FOOTER ONLY (1 — not in content):**
  - doc anchor `24/7 emergency water damage cleanup` → target `emergency-water-damage` | site anchor `24/7 Emergency Water Damage Cleanup` (footer)
- **EXTRA (6 — site content link, no doc counterpart):**
  - site anchor `Flood cleanup` → target `flood-cleanup` (main-content)
  - site anchor `AC overflows` → target `ac-overflow` (main-content)
  - site anchor `AC overflow cleanup` → target `ac-overflow` (main-content)
  - site anchor `flood cleanup` → target `flood-cleanup` (main-content)
  - site anchor `slab leak water damage` → target `slab-leak` (main-content)
  - site anchor `slab leak` → target `slab-leak` (main-content)

### Tab 32 — shut-off-valve (doc links 7)
- **EXTRA (2 — site content link, no doc counterpart):**
  - site anchor `Water Heater Leak` → target `water-heater-leak` (main-content)
  - site anchor `slab leak` → target `slab-leak` (main-content)

### Tab 33 — warm-spot-on-floor (doc links 8)
- **MISSING (2):**
  - doc anchor `why Plano copper pipes get pinhole leaks` → target `copper-pinhole-leaks` | heading `Expansive Clay Moves the Slab` | tbl=False
  - doc anchor `moisture mapping` → target `moisture-mapping` | heading `What Not to Do` | tbl=False
- **EXTRA (1 — site content link, no doc counterpart):**
  - site anchor `slab leak` → target `slab-leak` (main-content)

### Tab 34 — ceiling-dripping (doc links 11)
- **MISSING (1):**
  - doc anchor `sagging ceiling safety guide` → target `sagging-ceiling` | heading `` | tbl=False
- **PARTIAL ANCHOR (1 — link covers only part of the doc phrase):**
  - doc anchor `wet attic insulation removal` → target `attic-insulation-drying` | site anchor `attic insulation removal` (main-content) | heading `Why Fixing the Source Doesn't Fix the Ceiling`
- **EXTRA (1 — site content link, no doc counterpart):**
  - site anchor `ceiling leak water damage` → target `ceiling-leak` (main-content)

### Tab 35 — water-damage-cost (doc links 9)
- **PARTIAL ANCHOR (1 — link covers only part of the doc phrase):**
  - doc anchor `why fans won't dry walls` → target `fans-wont-dry-walls` | site anchor `fans won't dry walls` (main-content) | heading `How to Keep Your Cost Down`
- **EXTRA (3 — site content link, no doc counterpart):**
  - site anchor `AC overflow` → target `ac-overflow` (main-content)
  - site anchor `wall drying` → target `wall-drying` (main-content)
  - site anchor `water damage restoration in Plano` → target `(home)` (main-content)

### Tab 36 — fans-wont-dry-walls (doc links 6)
- **MISSING (1):**
  - doc anchor `moisture mapping` → target `moisture-mapping` | heading `` | tbl=False

### Tab 37 — storm-water-category-3 (doc links 7)
- **MISSING (1):**
  - doc anchor `ceiling leak water damage` → target `ceiling-leak` | heading `How the Water Got In Decides What Has to Happen` | tbl=True

### Tab 38 — mold-after-water-damage (doc links 7)
- **MISSING (1):**
  - doc anchor `moisture mapping` → target `moisture-mapping` | heading `` | tbl=False
- **PARTIAL ANCHOR (2 — link covers only part of the doc phrase):**
  - doc anchor `why fans won't dry walls` → target `fans-wont-dry-walls` | site anchor `fans won't dry walls` (main-content) | heading `Hidden Water`
  - doc anchor `Texas insurance guide` → target `water-damage-insurance-texas` | site anchor `insurance guide` (faq) | heading `Does insurance cover mold?`

### Tab 39 — copper-pinhole-leaks (doc links 13)
- **MISSING (3):**
  - doc anchor `warm spot guide` → target `warm-spot-on-floor` | heading `Where Pinhole Leaks Strike in Plano Homes` | tbl=True
  - doc anchor `attic insulation removal` → target `attic-insulation-drying` | heading `Where Pinhole Leaks Strike in Plano Homes` | tbl=True
  - doc anchor `wall cavity drying` → target `wall-drying` | heading `Where Pinhole Leaks Strike in Plano Homes` | tbl=True
- **PARTIAL ANCHOR (1 — link covers only part of the doc phrase):**
  - doc anchor `Texas insurance guide` → target `water-damage-insurance-texas` | site anchor `insurance guide` (faq) | heading `Does insurance cover pinhole leak damage?`
- **EXTRA (1 — site content link, no doc counterpart):**
  - site anchor `slab leak` → target `slab-leak` (main-content)

### Tab 40 — sagging-ceiling (doc links 6)
- **MISSING (1):**
  - doc anchor `ceiling dripping guide` → target `ceiling-dripping` | heading `Why Ceilings Sag in Plano Homes` | tbl=False
- **PARTIAL ANCHOR (2 — link covers only part of the doc phrase):**
  - doc anchor `wet attic insulation removal` → target `attic-insulation-drying` | site anchor `attic insulation removal` (main-content) | heading ``
  - doc anchor `Texas insurance guide` → target `water-damage-insurance-texas` | site anchor `insurance guide` (faq) | heading `Does insurance cover a collapsed ceiling?`

### Tab 41 — water-damage-insurance-texas (doc links 5)
- **MISSING (2):**
  - doc anchor `moisture mapping` → target `moisture-mapping` | heading `` | tbl=False
  - doc anchor `storm water guide` → target `storm-water-category-3` | heading `Is creek or storm flooding covered?` | tbl=False
- **PARTIAL ANCHOR (1 — link covers only part of the doc phrase):**
  - doc anchor `water damage cost guide` → target `water-damage-cost` | site anchor `water damage cost` (main-content) | heading `Understanding Your Deductible`

### Tab 42 — about (doc links 30)
- **MISSING (11):**
  - doc anchor `West Plano (75093)` → target `west-plano` | heading `Built for Plano Homes and Businesses` | tbl=False
  - doc anchor `East Plano (75074)` → target `east-plano` | heading `Built for Plano Homes and Businesses` | tbl=False
  - doc anchor `Water heater leaks` → target `water-heater-leak` | heading `What We Help With` | tbl=False
  - doc anchor `Ceiling and roof leaks` → target `ceiling-leak` | heading `What We Help With` | tbl=False
  - doc anchor `wet attic insulation` → target `attic-insulation-drying` | heading `What We Help With` | tbl=False
  - doc anchor `Sewage backups` → target `sewage-cleanup` | heading `What We Help With` | tbl=False
  - doc anchor `Hardwood floor` → target `hardwood-floor-drying` | heading `What We Help With` | tbl=False
  - doc anchor `cabinet` → target `cabinet-drying` | heading `What We Help With` | tbl=False
  - doc anchor `Commercial` → target `commercial-water-damage` | heading `What We Help With` | tbl=False
  - doc anchor `fire sprinkler` → target `fire-sprinkler-cleanup` | heading `What We Help With` | tbl=False
  - doc anchor `contact page` → target `contact` | heading `How do I reach you?` | tbl=False
- **PARTIAL ANCHOR (5 — link covers only part of the doc phrase):**
  - doc anchor `water damage cost guide` → target `water-damage-cost` | site anchor `water damage cost` (main-content) | heading `Honest About Costs`
  - doc anchor `Texas insurance guide` → target `water-damage-insurance-texas` | site anchor `insurance guide` (main-content) | heading `Honest About Insurance`
  - doc anchor `Legacy West and Deerfield (75024)` → target `legacy-west` | site anchor `Legacy West` (main-content) | heading `Built for Plano Homes and Businesses`
  - doc anchor `North Plano (75025)` → target `north-plano` | site anchor `North Plano` (main-content) | heading `Built for Plano Homes and Businesses`
  - doc anchor `Central Plano (75023, 75075)` → target `central-plano` | site anchor `Central Plano` (main-content) | heading `Built for Plano Homes and Businesses`
- **EXTRA (4 — site content link, no doc counterpart):**
  - site anchor `Water Damage Restoration Plano` → target `(home)` (main-content)
  - site anchor `Legacy West` → target `legacy-west` (main-content)
  - site anchor `Frisco` → target `frisco` (faq)
  - site anchor `Allen` → target `allen` (faq)

### Tab 43 — contact (doc links 32)
- **MISSING (20):**
  - doc anchor `Burst pipes` → target `burst-pipe-cleanup` | heading `What We Can Help With` | tbl=False
  - doc anchor `slab leaks` → target `slab-leak` | heading `What We Can Help With` | tbl=False
  - doc anchor `Water heater leaks` → target `water-heater-leak` | heading `What We Can Help With` | tbl=False
  - doc anchor `Ceiling leaks` → target `ceiling-leak` | heading `What We Can Help With` | tbl=False
  - doc anchor `wet attic insulation` → target `attic-insulation-drying` | heading `What We Can Help With` | tbl=False
  - doc anchor `Sewage backups` → target `sewage-cleanup` | heading `What We Can Help With` | tbl=False
  - doc anchor `storm flooding` → target `flood-cleanup` | heading `What We Can Help With` | tbl=False
  - doc anchor `Hardwood` → target `hardwood-floor-drying` | heading `What We Can Help With` | tbl=False
  - doc anchor `cabinets` → target `cabinet-drying` | heading `What We Can Help With` | tbl=False
  - doc anchor `walls` → target `wall-drying` | heading `What We Can Help With` | tbl=False
  - doc anchor `Hidden leaks and musty smells` → target `moisture-mapping` | heading `What We Can Help With` | tbl=False
  - doc anchor `Commercial properties` → target `commercial-water-damage` | heading `What We Can Help With` | tbl=False
  - doc anchor `West Plano` → target `west-plano` | heading `Areas We Cover` | tbl=True
  - doc anchor `Legacy West` → target `legacy-west` | heading `Areas We Cover` | tbl=True
  - doc anchor `North Plano` → target `north-plano` | heading `Areas We Cover` | tbl=True
  - doc anchor `Central Plano` → target `central-plano` | heading `Areas We Cover` | tbl=True
  - doc anchor `East Plano` → target `east-plano` | heading `Areas We Cover` | tbl=True
  - doc anchor `McKinney` → target `mckinney` | heading `Areas We Cover` | tbl=True
  - doc anchor `Richardson` → target `richardson` | heading `Areas We Cover` | tbl=True
  - doc anchor `Murphy, Parker & Wylie` → target `murphy` | heading `Areas We Cover` | tbl=True

## Related-card inventory (builder-generated, not counted as mismatches)

Every doc page carries related cards linking to other doc pages (home 30, services/areas/guides hubs 10–20 each, inner pages 1–6). No card links to its own page. Card anchors are page titles, not doc phrases, so they never match doc anchors — that is why MATCH-CARD is 0 everywhere and is not a defect. Full card lists are in the JSON companion.

## Hub + 404 notes (no doc tab — links listed, not scored)

- **services** (H1: Our Water Damage Services in Plano, TX) — links by region: {'header': 8, 'main-content': 1, 'related-card': 20, 'footer': 13, 'other': 1}; card targets not doc pages: none.
- **areas** (H1: Water Damage Restoration Areas Around Plano, TX) — links by region: {'header': 8, 'main-content': 1, 'related-card': 10, 'footer': 13, 'other': 1}; card targets not doc pages: none.
- **guides** (H1: Plano Water Damage Guides) — links by region: {'header': 8, 'main-content': 1, 'related-card': 10, 'footer': 13, 'other': 1}; card targets not doc pages: none.
- **404** (H1: 404) — links by region: {'header': 8, 'footer': 13, 'other': 1}; card targets not doc pages: none.

## What a fix pass would need to do (not done — read-only audit)

1. Rebuild from the Docs API model (with `textStyle.link` data), not from plain text — that alone resolves the 100 missing + 24 partial + most of the 134 extras.
2. Render doc tables (or get the user’s call on whether table content should be cut — never cut silently, per his content rule).
3. Preserve list conjunctions (“and”) in linked lists, and render both about CTA buttons in main content.
4. Re-run this exact rematch after the fix and require: MATCH = 575, MISSING = 0, PARTIAL = 0, EXTRA = 0, table missing = 0 (or an explicit user-approved table decision).

## Companion files

- Machine-readable companion: `doc-rematch-audit.json` (same directory) — per-page rows, full link rows, card inventories, hub inventories, method block.
- Working files (not deliverables): `doc-rematch/doc_api.json` (fresh Docs API fetch), `doc-rematch/doc_model.json`, `doc-rematch/site_model.json`, `doc-rematch/compare.json`, `doc-rematch/live/` (46 fetched live pages + 404).
