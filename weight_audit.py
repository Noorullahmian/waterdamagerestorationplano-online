#!/usr/bin/env python3
"""Per-page weight audit for Plano 3 out/ build.
For each of the 46 routes: HTML KB, hero file KB (mobile 400w / desktop 800w
variant from srcset), all-images KB (sum of every <img> src file on the page),
CSS KB, JS KB (chunks the page actually loads). Prints a summary + per-page
table. Usage: python3 weight_audit.py [out_dir]"""
import os, re, sys, json

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/workspace/plano3-water-damage/out")

def fsize(p):
    try:
        return os.path.getsize(p)
    except OSError:
        return 0

# CSS: the single stylesheet
css_files = []
for root, _, files in os.walk(os.path.join(OUT, "_next", "static", "css")):
    for f in files:
        css_files.append(os.path.join(root, f))
css_kb = sum(fsize(p) for p in css_files) / 1024

# JS chunks
js_total = 0
js_files = {}
for root, _, files in os.walk(os.path.join(OUT, "_next", "static", "chunks")):
    for f in files:
        if f.endswith(".js"):
            p = os.path.join(root, f)
            js_files["/_next/static/chunks/" + os.path.relpath(p, os.path.join(OUT, "_next", "static", "chunks"))] = fsize(p)
            js_total += fsize(p)
js_total_kb = js_total / 1024

pages = []
for root, _, files in os.walk(OUT):
    for f in files:
        if f == "index.html":
            pages.append(os.path.join(root, f))
pages.sort(key=lambda p: os.path.relpath(p, OUT))

rows = []
for p in pages:
    html = open(p, encoding="utf-8").read()
    rel = "/" + os.path.relpath(p, OUT).replace(os.sep, "/").replace("/index.html", "/")
    if rel == "/index.html":
        rel = "/"
    # all img srcs
    srcs = re.findall(r'<img[^>]*\ssrc="([^"]+)"', html)
    all_img_kb = sum(fsize(os.path.join(OUT, s.lstrip("/"))) for s in srcs) / 1024
    # hero srcset variants
    hero_m = re.search(r'class="hero-img"[^>]*srcset="([^"]+)"', html)
    hero_400 = hero_800 = 0.0
    if hero_m:
        for cand in hero_m.group(1).split(","):
            cand = cand.strip().split()
            if len(cand) == 2:
                url, w = cand
                if w == "400w":
                    hero_400 = fsize(os.path.join(OUT, url.lstrip("/"))) / 1024
                elif w == "800w":
                    hero_800 = fsize(os.path.join(OUT, url.lstrip("/"))) / 1024
    # JS this page loads (script srcs)
    scripts = re.findall(r'<script[^>]*\ssrc="([^"]+)"', html)
    page_js_kb = sum(js_files.get(s, fsize(os.path.join(OUT, s.lstrip("/")))) for s in scripts) / 1024
    html_kb = fsize(p) / 1024
    rows.append({
        "page": rel,
        "html_kb": round(html_kb, 1),
        "css_kb": round(css_kb, 1),
        "js_kb": round(page_js_kb, 1),
        "hero_400w_kb": round(hero_400, 1),
        "hero_800w_kb": round(hero_800, 1),
        "all_images_kb": round(all_img_kb, 1),
        "above_fold_mobile_kb": round(html_kb + css_kb + page_js_kb + hero_400, 1),
        "above_fold_desktop_kb": round(html_kb + css_kb + page_js_kb + hero_800, 1),
        "full_page_kb": round(html_kb + css_kb + page_js_kb + all_img_kb, 1),
        "n_imgs": len(srcs),
    })

def avg(k):
    return round(sum(r[k] for r in rows) / len(rows), 1)

print(json.dumps({
    "n_pages": len(rows),
    "css_kb": round(css_kb, 1),
    "js_total_all_chunks_kb": round(js_total_kb, 1),
    "avg_html_kb": avg("html_kb"),
    "avg_js_per_page_kb": avg("js_kb"),
    "avg_hero_400w_kb": avg("hero_400w_kb"),
    "avg_hero_800w_kb": avg("hero_800w_kb"),
    "avg_all_images_kb": avg("all_images_kb"),
    "avg_above_fold_mobile_kb": avg("above_fold_mobile_kb"),
    "avg_above_fold_desktop_kb": avg("above_fold_desktop_kb"),
    "avg_full_page_kb": avg("full_page_kb"),
    "max_full_page_kb": max(r["full_page_kb"] for r in rows),
    "max_above_fold_mobile_kb": max(r["above_fold_mobile_kb"] for r in rows),
    "rows": rows,
}, indent=1))
