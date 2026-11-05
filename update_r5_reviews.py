"""Update BLUNDER_HUNT.md Round 5 blunder lines with fix-pass verdicts.
Only touches lines between '## ROUND 5 BLUNDERS' and '## ROUND 5 — PER-PAGE'.
PASS = fixed + re-viewed on desktop+mobile screenshots in screenshots/review5sec/.
NOT YET (pool-limited) = no fitting file in the 161-file pool; kept file unchanged."""
import re

PATH = '/home/hatch/workspace/plano3-water-damage/BLUNDER_HUNT.md'
lines = open(PATH).read().split('\n')
start = next(i for i, l in enumerate(lines) if l.startswith('## ROUND 5 BLUNDERS'))
end = next(i for i, l in enumerate(lines) if l.startswith('## ROUND 5 — PER-PAGE'))

def P(fix, shots):
    return f'PASS — {fix} Re-view shots: screenshots/review5sec/{shots} (desktop+mobile viewed).'
def O(need, kept):
    return f'NOT YET — pool-limited: {need}; kept file {kept} unchanged (no fitting file in the 161-file pool; new sourcing required).'

# key: (page, section fragment) -> new Re-view text
V = {
('home', 'Commercial Water Damage Restoration card'): P('card now commercial-office-36631701.webp (open office, cubicles, plants); caveat: clean office, no damage visible', 'home-card-/commercial-water-damage/'),
('home', 'Fire Sprinkler Water Cleanup card'): P('card now fire-sprinkler-36631700.webp (open-plan office, drop-tile ceiling); caveat: commercial interior, no sprinkler head/discharge visible', 'home-card-/fire-sprinkler-cleanup/'),
('home', 'Sewage Backup Cleanup card'): P('card now sewage-drain-15242228.webp (frozen drain discharge into grate); caveat: frozen water, no true backup photo; east/central "different file" wish structurally impossible — all sewage cards share the single hero slot', 'home-card-/sewage-cleanup/'),
('home', 'Wall Cavity Drying & Flood Cuts card'): O('open wall cavity / flood cuts photo', 'attic-insulation-9043415.webp (attic bedroom); only open-cavity file 6124239 is consumed by the earlier home attic card'),
('water-extraction', 'Where the Water Hides'): P('split now moisture-meter-8961703.webp (indoor wall moisture check); caveat: meter check, not behind-wall evidence', 'water-extraction-fig-2'),
('water-extraction', 'Before Extraction Starts'): O('flooded residential home interior', 'flooded-floor-7924140.webp (commercial lobby stairs)'),
('sewage-cleanup', 'Hero'): P('hero now sewage-drain-15242228.webp (frozen drain discharge, brick wall); caveat: frozen water, no true backup photo in pool', 'sewage-cleanup-hero'),
('slab-leak', 'Blackland Prairie Clay'): O('cupped/damaged floor or slab-movement photo', 'hardwood-floor-3935327.webp (pristine empty room)'),
('water-heater-leak', 'Water Heater Burst'): O('attic-tank or ceiling-damage photo', 'attic-insulation-4482829.webp (attic skylight/blue sky, stock-pretty caption)'),
('ceiling-leak', 'The Attic Insulation Sponge'): P('split now attic-insulation-271743.webp (attic bedroom, wood ceiling, skylights); caveat: dry room, not wet/sagging insulation — true wet-insulation photo still owed', 'ceiling-leak-fig-1'),
('ceiling-leak', 'Attic AC and Water Heaters'): O('attic AC-pan or attic water-heater photo', 'attic-insulation-4482829.webp (skylight/blue sky)'),
('flood-cleanup', 'Storm Water Inside'): O('storm water entering a home (thresholds/weep holes)', 'burst-pipe-18274115.webp (spraying garden pipe = wrong mechanism)'),
('flood-cleanup', 'Six Creeks'): O('creek/street flood water at a Plano home exterior', 'flooded-floor-7924140.webp (commercial lobby stairs)'),
('flood-cleanup', 'Standing Water Extraction card'): P('card now moisture-meter-8961703.webp via water-extraction body[2] swap; caveat: meter check, not pumping', 'flood-cleanup-card-/water-extraction/'),
('commercial-water-damage', 'Water in Your Plano Office'): P('split now commercial-office-36631701.webp (open office, plants); caveat: clean office, no damage visible', 'commercial-water-damage-fig-0'),
('commercial-water-damage', 'Steel Studs'): P('split now commercial-office-9300768.webp (office interior, glass partition, desks); caveat: clean office, no studs/carpet visible', 'commercial-water-damage-fig-1'),
('hardwood-floor-drying', 'Wet Hardwood in Your Plano Home'): O('wet/cupped hardwood floor close-up', 'mold-wall-9127236.webp (exterior algae wall)'),
('hardwood-floor-drying', 'Buckling'): O('buckled/cupped hardwood boards pushing up', 'flooded-floor-7924140.webp (lobby stairs)'),
('ac-overflow', 'The Unit Sits in the Attic'): O('attic air handler / drain pan image', 'attic-insulation-6124239.webp (wall-cavity insulation worker)'),
('ac-overflow', 'Two Drains'): P('split now sewage-drain-3964564.webp (drain line with runoff); caveat: drain line, not attic pan', 'ac-overflow-fig-2'),
('laundry-overflow', 'Upstairs Washer Flooded'): O('washer overflow / wet laundry-floor image', 'laundry-room-7282378.webp (lifestyle loading shot); free washer file 4993073 has no water'),
('laundry-overflow', 'What Usually Fails'): P('split now sewage-drain-3964564.webp (drain pipe); caveat: drain pipe, not washer hose/box', 'laundry-overflow-fig-1'),
('laundry-overflow', 'Where the Water Goes'): O('water travelling between home floors / stained downstairs ceiling', 'flooded-floor-7924140.webp (lobby stairs)'),
('crawl-space-drying', 'Sewage Backup Cleanup card'): P('card now sewage-drain-15242228.webp via shared sewage hero slot; caveat: frozen water', 'crawl-space-drying-card-/sewage-cleanup/'),
('fire-sprinkler-cleanup', 'Where Sprinkler Water Goes'): P('split now fire-sprinkler-36631700.webp (open-plan office, drop-tile ceiling); caveat: commercial interior, no sprinkler head/discharge', 'fire-sprinkler-cleanup-fig-1'),
('fire-sprinkler-cleanup', 'Commercial Water Damage Restoration card'): P('card now commercial-office-36631701.webp via commercial body[0] (commercial hero is a fire body image); caveat: clean office', 'fire-sprinkler-cleanup-card-/commercial-water-damage/'),
('moisture-mapping', 'How Thermal Imaging'): O('lived-in Plano interior with a water stain, or thermal-camera/moisture-reading shot', 'ceiling-stain-8624464.webp (dated foreign flat)'),
('moisture-mapping', 'Common Hidden Leaks'): O('ceiling water damage in a lived-in Plano home (stain/drip, furniture, daylight)', 'ceiling-stain-14032089.webp (derelict room)'),
('attic-insulation-drying', 'Wet Insulation in Your Plano Attic'): P('split now attic-insulation-271743.webp (attic bedroom); caveat: attic room, not safety subject; true wet-insulation photo still owed', 'attic-insulation-drying-fig-0'),
('attic-insulation-drying', 'Attic Water Heaters'): O('tank actually photographed in an attic (roof slope, joists, insulation)', 'crawl-space-4092030.webp (basement tank)'),
('attic-insulation-drying', 'Attic AC and Frozen Pipes'): O('attic AC air handler/pan or split pipe in an attic with wet insulation', 'attic-insulation-4482829.webp (skylight/blue sky)'),
('wall-drying', 'Drywall Wicks Water Up'): O('interior drywall wicking/staining at the base of a wall; caption still mismatched until replaced', 'mold-wall-9127236.webp (exterior algae on masonry)'),
('wall-drying', 'Check These 5 Things'): P('split now moisture-meter-8482824.webp (engineer, spirit level on concrete wall) — different person/pose/tool from the moisture pair, same-shoot fixed; caveat: construction-site setting', 'wall-drying-fig-0'),
('west-plano', 'Hero'): P('hero now suburban-home-3990589.webp (brick home, garage, driveway, lawn); caveat: shares hero with richardson (score10x hero_unique)', 'west-plano-hero'),
('legacy-west', 'Stacked Living'): O('Legacy West townhome/stacked-living exterior or interior stairwell without floodwater', 'flooded-floor-7924140.webp (commercial stairs in floodwater)'),
('north-plano', 'Hero'): P('hero now suburban-home-26595553.webp (brick home, gable, shingle); caveat: shares hero with water-damage-cost (score10x hero_unique)', 'north-plano-hero'),
('central-plano', 'Hero'): P('hero now texas-home-8278494.webp (Texas street, 2-story homes, garages, driveways); caveat: tall 2-story, not low-profile ranch; shares hero with frisco (score10x hero_unique)', 'central-plano-hero'),
('central-plano', 'Sewage Backup Cleanup card'): P('card now sewage-drain-15242228.webp via shared sewage hero slot; caveat: frozen water', 'central-plano-card-/sewage-cleanup/'),
('east-plano', 'Hero'): O('East Plano historic brick home, pier-and-beam house or 1960s ranch', 'suburban-home-25798114.webp (Mediterranean villa); candidate 27852347 (European hillside) rejected on viewed pixels'),
('east-plano', 'Sewage Backup Cleanup card'): P('card now sewage-drain-15242228.webp via shared sewage hero slot; caveat: frozen water; per-card-different file structurally impossible (shared hero slot)', 'east-plano-card-/sewage-cleanup/'),
('fans-wont-dry-walls', 'Hero'): O('Plano home interior with a household fan / wet carpet or damp drywall baseboard', 'mold-wall-4597285.webp (derelict peeling wall)'),
('fans-wont-dry-walls', 'The 60-Second Answer'): P('split now moisture-meter-7937963.webp (man checking wall alignment in renovation room); caveat: wall check, not wet carpet edge/baseboard', 'fans-wont-dry-walls-fig-0'),
('fans-wont-dry-walls', 'Why Plano Humidity'): O('Plano home interior (window/AC vent condensation, hygrometer, or dehumidifier)', 'mold-wall-29701042.webp (foreign exterior stucco wall)'),
('murphy', 'Water Heater Leak Cleanup card'): O('attic/garage tank heater (or plumber at a tank)', 'water-heater-34593293.webp (rooftop solar tank)'),
('allen', 'Clay, Copper and Slab Leaks'): P('split now suburban-home-3990589.webp (brick home) + new topic caption "A brick Allen home, the kind affected by the clay and slab leaks in this section"; old listing string absent from allen HTML', 'allen-fig-1'),
('allen', 'Hail Alley'): O('attic/roof image (attic AC unit, wet insulation, roofline)', 'flooded-floor-7924140.webp (commercial stairs)'),
('water-damage-cost', 'The 4 Things That Set the Price'): P('all four factors now H3 (1. Square Footage and Room Size, 2. Water Category, 3. How Hard It Is to Dry, 4. How Many Days); factor-3 detail stays listhead+list between factors 2 and 3, hierarchy uniform at H3 level', 'water-damage-cost-h3-The-4-Things'),
('water-damage-cost', 'Sudden vs. Gradual'): O('home water-damage visual (stained ceiling/wall, wet floor, or plumber/drying shot)', 'commercial-office-5483188.webp (office desk, skyline); candidate 22711217 (generic office) = no improvement, rejected'),
('storm-water-category-3', 'Hero'): O('flooded Plano/Texas brick-home yard', 'storm-flood-11537987.webp (caravan/trailer flood); only storm-flood free file'),
('storm-water-category-3', 'The 60-Second Answer for Plano Homeowners'): O('standing water inside a home (floor/wall water line)', 'flooded-floor-7924140.webp (lobby stairs, reflective floor)'),
('storm-water-category-3', 'Saturated Clay'): O('wet yard / water pooling against a brick foundation', 'suburban-home-186077.webp (dry dusk house)'),
('storm-water-category-3', 'Sewage Backup Cleanup card'): P('card now sewage-drain-15242228.webp via shared sewage hero slot; caveat: frozen water', 'storm-water-category-3-card-/sewage-cleanup/'),
('storm-water-category-3', 'How the Water Got In Decides'): P('REOPENED fixed by kicker merge: section-kicker "How the Water Got In Decides What Has to Happen" + lead "Why Plano Homes Take On Storm Water." now open the "Creeks Run Through the City" section — no lone beige band, words preserved', 'storm-water-category-3-kicker-How-the-Water-Got-In'),
('mold-after-water-damage', 'Hero'): O('mold on an interior wall/baseboard in a home', 'mold-wall-9127236.webp (exterior algae); candidate 18351809 (derelict Russia) rejected'),
('mold-after-water-damage', 'The 60-Second Mold Clock'): O('visible mold on a home wall/baseboard with an honest caption', 'mold-wall-4597285.webp (peeling paint, no mold colonies)'),
('mold-after-water-damage', 'Warm Indoor Temperatures'): P('split now cabinet-kitchen-8146322.webp (empty kitchen, wooden cabinets, large windows); caveat: interior room only, no temperature/mold cue', 'mold-after-water-damage-fig-1'),
('mold-after-water-damage', 'Hidden Water'): O('hidden-water subject (under-floor, wall cavity, attic insulation) or genuine in-home air mover', 'drying-equipment-16243255.webp (industrial ventilator)'),
('mold-after-water-damage', 'Signs the Clock'): P('symptom line now 4th bullet of the Signs list; closing paragraph + Call button sit under the list, not in an H2 band', 'mold-after-water-damage-h2-Signs the Clock Has Already Run Out'),
('mold-after-water-damage', 'Hour-by-Hour'): P('REOPENED fixed by kicker merge: section-kicker "Hour-by-Hour: What Happens Inside Wet Walls and Floors" + lead "Why Plano Homes Are at Higher Risk." now open the "Warm Indoor Temperatures" section — no lone beige band, words preserved', 'mold-after-water-damage-kicker-Hour-by-Hour'),
('sagging-ceiling', 'Leave the room'): O('water stain on a current Texas-style bedroom wall/ceiling', 'ceiling-stain-8624464.webp (dated foreign flat)'),
('sagging-ceiling', 'The 6 Safety Steps'): O('sagging/bubbling ceiling interior', 'suburban-home-30707539.webp (tile-roof European exterior)'),
('water-damage-insurance-texas', 'Hero'): O('claim/documentation subject (adjuster, photos of damage, paperwork with home-damage context)', 'commercial-office-5483188.webp (office desk, skyline)'),
('water-damage-insurance-texas', 'Your Duty to Mitigate'): P('split now plumber-work-6419128.webp (plumber hands on steel pipes); caveat: pipe work, not drying', 'water-damage-insurance-texas-fig-1'),
('water-damage-insurance-texas', 'Understanding Your Deductible'): O('policy/claim subject with a plain caption', 'commercial-office-13068366.webp (sleek office, sales caption remains)'),
('water-damage-insurance-texas', 'Mistakes That Can Hurt a Claim'): P('drip line now 5th bullet of the Mistakes list; closing paragraph + Call button sit under the list, not in an H2 band', 'water-damage-insurance-texas-h2-Mistakes That Can Hurt a Claim'),
('contact', 'Post-hero band'): P('Tap-to-Call button moved to the head of the "Emergency in Your Plano Home? Call First, Then Do This" section; no lone strip between hero and Emergency', 'contact-h2-Emergency in Your Plano Home'),
('contact', 'Emergency in Your Plano Home'): P('split now plumber-work-35290675.webp (crew/work); caveat: crew/work subject, not an emergency scene', 'contact-h2-How to Reach Us'),
('contact', 'Service area: (split figure)'): P('split now suburban-home-26595553.webp (brick subdivision home); caveat: shares file with north/cost heroes (different pages, no same-page dup)', 'contact-h2-How to Reach Us'),
('contact', 'Service area: (heading)'): P('label now bold lead "Service area: Plano (75023, …) plus nearby Frisco, Allen, McKinney, Richardson, Murphy, Parker and Wylie." under "How to Reach Us"; Hours H3 untouched, ZIP/city words unchanged', 'contact-h2-How to Reach Us'),
('contact', "Whether it's clean water"): P('fragment lines restored as items 6–7 of the 7-item "What to Have Ready" list; "What Happens After You Call" restored as H2 with its paragraph', 'contact-h2-What to Have Ready When You Call + contact-h2-What Happens After You Call'),
('contact', 'Send Us a Message (Non-Emergency) (form intro)'): P('REOPENED fixed: intro now begins "Use this form for questions, scheduling an inspection or following up on a job. For active water, please call (972) 472-7917 instead." directly under the single form H2, immediately before <form>; duplicated heading echo stripped (duplicate removal, not user content)', 'contact-h2-Send Us a Message'),
('services', 'Sewage Backup Cleanup card'): P('card now sewage-drain-15242228.webp via shared sewage hero slot; caveat: frozen water', 'services-card-/sewage-cleanup/'),
('services', 'Fire Sprinkler Water Cleanup card'): O('sprinkler-head / sprinkler-water subject in a wet interior', 'flooded-floor-7924140.webp (lobby stairs) — services hub card shows the fire HERO, not fire body[1]; home card + fire split are fixed via body[1], hub card still shows the hero'),
}

changed, missed = 0, []
for i in range(start, end):
    l = lines[i]
    if not l.startswith('- Page:'):
        continue
    hit = None
    for (page, frag), txt in V.items():
        if l.startswith(f'- Page: {page} |') and f'Section: ' in l and frag in l.split('| Blunder:')[0]:
            hit = txt
            break
    if hit is None:
        missed.append(l[:110])
        continue
    if 'Re-view: NOT YET' not in l:
        continue  # already updated in a previous pass
    lines[i] = l.replace('Re-view: NOT YET', 'Re-view: ' + hit)
    changed += 1

open(PATH, 'w').write('\n'.join(lines))
print('changed:', changed, 'missed:', len(missed))
for m in missed:
    print('MISSED:', m)
npass = sum(1 for t in V.values() if t.startswith('PASS'))
print('PASS in map:', npass, 'OPEN in map:', len(V) - npass)
