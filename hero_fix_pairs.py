#!/usr/bin/env python3
"""Build BEFORE/AFTER side-by-side pairs for the 6 replaced + 3 hub heroes.
before = screenshots/hero-audit/, after = screenshots/hero-fix/.
Output: screenshots/hero-fix/pairs/{slug}-hero-{w}-pair.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.expanduser('~/workspace/plano3-water-damage')
BEFORE = os.path.join(BASE, 'screenshots', 'hero-audit')
AFTER = os.path.join(BASE, 'screenshots', 'hero-fix')
OUT = os.path.join(AFTER, 'pairs')
os.makedirs(OUT, exist_ok=True)
SLUGS = ['burst-pipe-cleanup', 'sewage-cleanup', 'slab-leak', 'water-heater-leak',
         'ac-overflow', 'copper-pinhole-leaks', 'services', 'areas', 'guides']
LABEL = 34

def label_bar(img, text, bg):
    bar = Image.new('RGB', (img.width, LABEL), bg)
    d = ImageDraw.Draw(bar)
    try:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
    except Exception:
        f = ImageFont.load_default()
    d.text((12, 6), text, fill='white', font=f)
    out = Image.new('RGB', (img.width, img.height + LABEL))
    out.paste(bar, (0, 0))
    out.paste(img, (0, LABEL))
    return out

for slug in SLUGS:
    for w in (1440, 390):
        b = os.path.join(BEFORE, f'{slug}-hero-{w}.png')
        a = os.path.join(AFTER, f'{slug}-hero-{w}.png')
        if not (os.path.exists(b) and os.path.exists(a)):
            print('MISSING', slug, w, os.path.exists(b), os.path.exists(a))
            continue
        bi, ai = Image.open(b).convert('RGB'), Image.open(a).convert('RGB')
        bi, ai = label_bar(bi, 'BEFORE (live, rejected)', (150, 30, 30)), label_bar(ai, 'AFTER (local fix)', (20, 90, 60))
        h = max(bi.height, ai.height)
        canvas = Image.new('RGB', (bi.width + ai.width, h), 'white')
        canvas.paste(bi, (0, 0))
        canvas.paste(ai, (bi.width, 0))
        p = os.path.join(OUT, f'{slug}-hero-{w}-pair.png')
        canvas.save(p)
        print('pair', p, canvas.size)
