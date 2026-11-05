#!/usr/bin/env python3
"""Publish-step subpath rewrite for the Plano 3 GitHub Pages PREVIEW.

The site is built root-relative (correct for the real apex domain
waterdamagerestorationplano.online). The github.io PREVIEW lives at the
subpath /waterdamagerestorationplano-online/, so every root-relative URL
in the built .html files must be prefixed with that subpath before the
tree is published to the gh-pages branch.

This step was done for the 12:44 and 14:20 pushes (their published HTML
has prefixed URLs) and was SKIPPED by the 20:09 push, which shipped
unprefixed HTML -> every CSS/JS/image/link 404'd on the preview and the
site rendered completely unstyled. NEVER publish gh-pages without this.

Usage:  python3 publish_prefix.py [src_dir] [dest_dir]
Default src = ~/workspace/plano3-water-damage/out
Default dest = ~/workspace/plano3-publish/pages-new

Rule: in *.html files only, rewrite a "/" that starts a site URL
(a slash NOT followed by another slash, preceded by a quote, paren,
comma or whitespace) to "/waterdamagerestorationplano-online/".
Untouched by design: absolute https:// URLs, tel: links, protocol-
relative // URLs, sitemap.xml / robots.txt (absolute already),
canonical + OG URLs (absolute already), CSS/JS/image file contents.
"""
import os
import re
import shutil
import sys

PREFIX = "/waterdamagerestorationplano-online"
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    "~/workspace/plano3-water-damage/out")
DEST = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser(
    "~/workspace/plano3-publish/pages-new")

# A site-URL slash: preceded by a quote (attribute value or JSON string
# start, e.g. href="/x, "/x) or by comma+space (srcset candidate, e.g.
# 400w, /images/x), and NOT followed by ">" or "/" — the lookahead is
# essential: a bare "/>" closes a self-closing tag (<meta .../>), and
# rewriting that slash corrupts the tag (lesson, 2026-11-05: the first
# version of this regex matched (["'\(,]\s*)/ and corrupted every />).
URL_SLASH = re.compile(r"""((?:["']|,\s*))/(?!>|/)""")


def rewrite_html(text):
    return URL_SLASH.sub(r"\1" + PREFIX + "/", text)


def main():
    if os.path.exists(DEST):
        shutil.rmtree(DEST)
    shutil.copytree(SRC, DEST)
    changed = 0
    for root, _dirs, files in os.walk(DEST):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as f:
                orig = f.read()
            new = rewrite_html(orig)
            if new != orig:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
                changed += 1
    print(f"rewrote {changed} html files: {SRC} -> {DEST}")


if __name__ == "__main__":
    main()
