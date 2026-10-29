#!/usr/bin/env python3
"""Build v1/, the frozen archive of Research Hub v1, from a git commit (default: HEAD).

Usage: python3 tools/build_v1.py [commit]
Every HTML page gets the archive banner, a noindex robots meta and a canonical
link to the live page; absolute links to the hub stay inside /research-hub/v1/.
"""
import os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = "https://bettertobest.github.io/research-hub/"
SKIP_DIRS = {".git", ".github", "v1", "tools", "repec", "cco-ptf-simulation"}
SKIP_FILES = {"CLAUDE.md", "CONTRIBUTING.md", "README.md", "LICENSE", "CITATION.cff",
              "404.html", "googlea418ef0496eb2fdc.html"}
BANNER = ('<div id="v1-banner" role="note" style="background:#fff3cd;color:#533f03;'
          'border-bottom:2px solid #e0a800;padding:.75em 1em;text-align:center;font-size:.95em;">'
          'Archived: Research Hub version 1, frozen at s84. This is the text NEEC v1 cites. '
          'It is no longer updated and may contain errors since corrected. '
          '<a href="{live}" style="color:#533f03;font-weight:bold;">Read the current page</a>.</div>')

def main():
    commit = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    sha = subprocess.check_output(["git", "-C", ROOT, "rev-parse", commit], text=True).strip()
    out = os.path.join(ROOT, "v1")
    shutil.rmtree(out, ignore_errors=True)
    files = subprocess.check_output(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", sha],
                                    text=True).splitlines()
    n = 0
    for rel in files:
        top = rel.split("/")[0]
        if top in SKIP_DIRS or rel in SKIP_FILES:
            continue
        data = subprocess.check_output(["git", "-C", ROOT, "show", f"{sha}:{rel}"])
        dst = os.path.join(out, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if rel.endswith(".html"):
            data = transform(data.decode("utf-8"), rel).encode("utf-8")
            n += 1
        with open(dst, "wb") as f:
            f.write(data)
    print(f"built v1/ from {sha}: {n} html pages")

def transform(html, rel):
    live = LIVE + ("" if rel == "index.html" else rel[:-10] + "/" if rel.endswith("/index.html") else rel)
    # links stay inside /v1/
    html = re.sub(r'(href|src)="/research-hub/', r'\1="/research-hub/v1/', html)
    html = re.sub(r'(href|src)="https://bettertobest\.github\.io/research-hub/(?!v1/)', r'\1="/research-hub/v1/', html)
    # canonical -> the live page; robots noindex
    html = re.sub(r'\s*<link rel="canonical"[^>]*>', "", html)
    head = f'<meta name="robots" content="noindex">\n<link rel="canonical" href="{live}">\n'
    html, k = re.subn(r"(<head[^>]*>)", lambda m: m.group(1) + "\n" + head, html, count=1)
    assert k == 1, rel
    html, k = re.subn(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + BANNER.format(live=live), html, count=1)
    assert k == 1, rel
    return html

if __name__ == "__main__":
    main()
