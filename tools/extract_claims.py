#!/usr/bin/env python3
"""List every quantitative statement on the live Research Hub (step S23).

Usage: python3 tools/extract_claims.py [hub root] [--out figures.csv]   (prints counts by page)

Reads every HTML page, every Markdown page, every PDF in papers/pdfs (pdftotext)
and data/optimal-parameters.json. The frozen /v1/ archive, repository files
(CLAUDE.md, CONTRIBUTING.md, CITATION.cff), this step's own summary and the search-console
stub are skipped.

`context` is the sentence, or for a long sentence (PDF text often runs table
cells together) a window of 120 characters each side of the figure.

A "figure" is any number in prose or tables: a percentage, an amount of money,
a multiplier, a count, a ratio or rate, a duration or a year ahead. Not figures:
section, table, figure, equation and step numbers; past calendar years used as
dates (1900-2026); citation volume, page and issue numbers in reference lists
are kept but flagged (ref=1) so the classer can mark them corpus metadata.

One row per figure per sentence. `id` is stable across reruns as long as the
page, the sentence and the figure are unchanged (sha1 of the three).
Classing is done by tools/class_claims.py.
"""
import csv, hashlib, html, json, pathlib, re, subprocess, sys
from html.parser import HTMLParser

SKIP_DIRS = {".git", "v1", "tools"}
SKIP_FILES = {"CLAUDE.md", "CONTRIBUTING.md", "googlea418ef0496eb2fdc.html", "claims-summary.md"}

NUM = r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?|\.\d+"
SCALE = r"(?:\s?(?:trillion|billion|million|thousand|bn|[TBMK])\b)"
DASH = r"\s?(?:-|–|—|to)\s?"
FIG = re.compile(
    rf"""(?ix)
    (?:[~≈<>≤≥±]\s?|[+−-])?                     # bound, or a sign written against the number
    (?:(?:US)?\$|£|€|¥)?\s?(?:{NUM}){SCALE}?    # number, maybe money and scale
    (?:{DASH}(?:(?:US)?\$|£|€)?\s?(?:{NUM}){SCALE}?)?   # range
    (?:\s?(?:%|percent\b|per\s?cent\b|percentage\spoints?\b|pp\b|bps?\b|basis\spoints\b|-fold\b|fold\b|times\b)
       |(?:x\b|×|\+))?                         # unit (a multiplier sign or "+" only when attached)
    """)
LABEL = re.compile(r"(?i)(?:section|sec\.|table|figure|fig\.|eq\.|equation|appendix|phase|step|stage|tier|level|chapter|part|lemma|theorem|proposition|corollary|definition|assumption|hypothesis|page|p\.|pp\.|no\.|vol\.|issue|v|version|§|#|index)\s*$")
YEAR = re.compile(r"^(1[5-9]\d\d|20[0-2]\d)$")
REF_HEAD = re.compile(r"(?i)^\s*(?:p\.\d+\s+)?(\d+(\.\d+)*\.?\s*)?(references|bibliography|works cited|citations|further reading)\b")
STRONG_BIB = re.compile(r"\b\d+\s?\(\d+(?:[-–]\d+)?\),\s?[e\d]|\bdoi[:.]|\b(?:Journal|Review|Quarterly|Economics|Policy|Nature|Science)[A-Za-z :&]*,\s?\d+(?:\(\d+\))?,\s?\d+[-–]\d+")
BIB = re.compile(r"\(\d{4}[a-z]?\)\.|\b\d+\s?\(\d+\),\s?\d+|\bpp?\.\s?\d|\bdoi\b|https?://|\b(?:Press|University|Journal|Review|Quarterly|Proceedings|Working Paper)\b.{0,40}\b\d{4}\b|\b\d{4}\b.{0,80}\b(?:Press|Journal|Review|Quarterly)\b")

class Page(HTMLParser):
    BLOCK = {"p", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "div", "blockquote",
             "pre", "caption", "dt", "dd", "figcaption", "br", "section", "article", "summary", "title"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.buf, self.sec, self.hbuf, self.skip, self.inh = [], [], "", None, 0, None
    def flush(self):
        t = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if t:
            self.blocks.append((self.sec, t))
        self.buf = []
    def handle_starttag(self, tag, a):
        if tag in ("script", "style", "svg", "noscript"):
            self.skip += 1
        elif tag in self.BLOCK:
            self.flush()
        if re.fullmatch(r"h[1-4]", tag):
            self.inh, self.hbuf = tag, []
        if tag in ("td", "th"):
            self.buf.append(" | ")
    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg", "noscript"):
            self.skip = max(0, self.skip - 1)
        if tag == self.inh:
            self.sec = re.sub(r"\s+", " ", "".join(self.hbuf)).strip()[:90]
            self.inh = None
        if tag in self.BLOCK:
            self.flush()
    def handle_data(self, d):
        if self.skip:
            return
        self.buf.append(d)
        if self.inh:
            self.hbuf.append(d)

def html_blocks(text):
    p = Page(); p.feed(text); p.flush()
    return p.blocks

PDF_HEAD = re.compile(r"^(?:\d+(?:\.\d+)*\.?\s+[A-Z][^.]{2,80}|[A-Z][A-Za-z ,:&\-]{3,60}|Appendix [A-Z].{0,60}|Abstract|References)$")

def pdf_blocks(path):
    out = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True).stdout
    blocks, sec = [], ""
    for pno, page in enumerate(out.split("\f"), 1):
        for para in re.split(r"\n\s*\n", page):
            lines = [l.strip() for l in para.splitlines() if l.strip()]
            if not lines:
                continue
            if len(lines) == 1 and PDF_HEAD.match(lines[0]) and not re.fullmatch(r"\d+", lines[0]):
                sec = lines[0][:90]
                continue
            t = re.sub(r"-\n(?=[a-z])", "", "\n".join(lines))
            blocks.append((f"p.{pno} {sec}".strip(), re.sub(r"\s+", " ", t)))
    return blocks

def md_blocks(text):
    blocks, sec = [], ""
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        m = re.match(r"^#{1,4}\s+(.*)", para)
        if m:
            sec = m.group(1).strip()[:90]
            para = para[m.end():].strip()
        if para:
            blocks.append((sec, re.sub(r"\s+", " ", para)))
    return blocks

def json_blocks(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from json_blocks(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list) and all(not isinstance(x, (dict, list)) for x in obj):
        yield (path, f"{path} = {json.dumps(obj)}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from json_blocks(v, f"{path}[{i}]")
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        yield (path, f"{path} = {obj}")
    elif isinstance(obj, str) and re.search(r"\d", obj):
        yield (path, f"{path} = {obj}")

SENT = re.compile(r"(?<=[.!?])[\"”’)]?\s+(?=[A-Z(\"“$])")

def sentences(block):
    return [s.strip() for s in SENT.split(block) if s.strip()]

def figures(sent):
    out = []
    for m in FIG.finditer(sent):
        f = m.group(0).strip()
        if not re.search(r"\d", f):
            continue
        a = m.start() + len(m.group(0)) - len(m.group(0).lstrip())
        b = m.end()
        if a == 0 and re.match(r"(?:\d+\.)+\d*[a-z]?(?:\s|$)|\d+\)\s", sent):
            continue                                   # a numbered heading or list item: "1.1 The ...", "3. "
        if re.search(r"\[[\d,\s–-]*$", sent[:a]) and re.match(r"[\d,\s–-]*\]", sent[a:]):
            continue                                   # a citation marker: [18], [28,29]
        before, after = sent[max(0, a - 14):a], sent[b:b + 2]
        core = re.sub(r"[^\d.]", "", f)
        if LABEL.search(before) and not re.search(r"[%$£€×]|fold|times", f):
            continue                                   # Table 5.4, Section 3, Phase 2
        if a > 0 and (sent[a - 1].isalnum() or sent[a - 1] in "_^") and not f[0] in "$£€":
            continue                                   # part of a word or symbol: x2, B0, H2O
        if after[:1].isalpha():
            continue                                   # 3D, 2nd, 10am, CO2e
        if YEAR.match(core) and not re.search(r"[%$£€×]", f):
            continue                                   # a past calendar year used as a date
        if re.fullmatch(r"[0-9]", core) and not re.search(r"[%$£€×]|fold|times", f):
            nxt = sent[b:b + 30]
            if not re.match(r"\s?(?:years?|months?|weeks?|days?|hours?|million|billion|trillion|households?|people|participants|members|families|homes?|units?|percent|cents?|dollars?|times)\b", nxt, re.I):
                continue                               # bare single digits ("in 3 ways", list markers)
        out.append((f, a))
    return out

def collect(root):
    root = pathlib.Path(root)
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if not p.is_file() or any(x in SKIP_DIRS for x in rel.parts[:-1]) or p.name in SKIP_FILES:
            continue
        if p.suffix == ".html":
            yield str(rel), html_blocks(p.read_text(errors="ignore"))
        elif p.suffix == ".md":
            yield str(rel), md_blocks(p.read_text(errors="ignore"))
        elif p.suffix == ".pdf":
            yield str(rel), pdf_blocks(p)
        elif p.suffix == ".json":
            yield str(rel), list(json_blocks(json.loads(p.read_text())))

def rows_for(page, blocks):
    rows, seen = [], set()
    for sec, block in blocks:
        in_ref = bool(REF_HEAD.match(sec or ""))
        for s in sentences(block):
            for f, i in figures(s):
                key = (page, s, f)
                if key in seen:
                    continue
                seen.add(key)
                cid = hashlib.sha1("\x1f".join(key).encode()).hexdigest()[:10]
                ctx = s if len(s) <= 260 else ("…" + s[max(0, i - 120):i + len(f) + 120] + "…")
                ref = int(in_ref or bool(STRONG_BIB.search(ctx))
                          or bool(BIB.search(ctx) and re.search(r"\b(?:19|20)\d\d\b", ctx)))
                rows.append({"id": cid, "page": page, "section": sec, "figure": f, "ref": ref, "context": ctx})
    return rows

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = pathlib.Path(args[0] if args else pathlib.Path(__file__).resolve().parents[1])
    rows = [r for page, blocks in collect(root) for r in rows_for(page, blocks)]
    if "--out" in sys.argv:
        with open(sys.argv[sys.argv.index("--out") + 1], "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    by = {}
    for r in rows:
        by[r["page"]] = by.get(r["page"], 0) + 1
    print(f"{len(rows)} figures on {len(by)} pages")
    for k, v in sorted(by.items(), key=lambda kv: -kv[1]):
        print(f"{v:6d}  {k}")

if __name__ == "__main__":
    main()
