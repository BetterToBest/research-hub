#!/usr/bin/env python3
"""Check every page under v1/: banner, noindex, canonical to the live page, no link out of /v1/."""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bad = 0
pages = glob.glob(os.path.join(ROOT, "v1", "**", "*.html"), recursive=True)
for p in pages:
    t = open(p, encoding="utf-8").read()
    rel = os.path.relpath(p, ROOT)
    errs = []
    if 'id="v1-banner"' not in t: errs.append("banner")
    if '<meta name="robots" content="noindex">' not in t: errs.append("noindex")
    if len(re.findall(r'<link rel="canonical" href="https://bettertobest\.github\.io/research-hub/(?!v1/)[^"]*">', t)) != 1: errs.append("canonical")
    body = re.sub(r'<div id="v1-banner".*?</div>|<link rel="canonical"[^>]*>', "", t, flags=re.S)
    if re.search(r'(?:href|src)="(?:/research-hub/(?!v1/)|https://bettertobest\.github\.io/research-hub/)', body): errs.append("link leaves v1")
    if errs: bad += 1; print(rel, "FAIL:", ", ".join(errs))
print(f"{len(pages)} pages, {bad} failing")
sys.exit(1 if bad else 0)
