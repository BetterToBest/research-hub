#!/usr/bin/env python3
"""Class every Hub figure by its basis (step S23, research rule 5).

Usage: python3 tools/class_claims.py [--triage ../research-update/audits/refine/triage.csv]

Runs tools/extract_claims.py, then gives each figure one basis class:

  simulation             a simulation release is cited for it (`source` says whether a command is given)
  derived                arithmetic from other stated figures (`source` names the file or section)
  external source        a cited outside source (`checked` says whether it was opened)
  design parameter       a value the framework chooses: an amount, rate, cap, threshold or target
  illustrative projection  a worked example, scenario or projection the text presents as one
  corpus metadata        dates, versions, counts of papers, reference-list details
  no basis found         stated as a fact, finding or result with no source, run or derivation

and an action: keep, correct (the figure or its derivation is wrong), relabel (keep the
number but say what it is: usually "illustrative projection" or "design parameter"), or
remove (no basis and nothing honest to relabel it as). `claimed` records what the text
presents the figure as (simulation result, finding, projection, fact ...).

Order: reference-list entries first, then the reviewed rules in tools/claims_review.py
(first match wins; each was written after reading the passage; a rule matches the page,
then "section ¦ sentence", then optionally the figure itself), then the generic rules
below. `rule` names the rule that classed the row, so every class can be traced.
The S29 refine.ink triage (research-update audits/refine/triage.csv) adds its id and,
for live valid critiques, turns a "keep" into "correct".

Writes data/claims.csv and data/claims-summary.md.
"""
import collections, csv, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import extract_claims as ex
from claims_review import REVIEW, PAPER_DEFAULTS

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLASSES = ["simulation", "derived", "external source", "design parameter",
           "illustrative projection", "corpus metadata", "no basis found"]

def rx(p):
    return re.compile(p, re.I)

# Generic rules: (name, test(row, ctx) -> bool, class, claimed, action, source, checked)
SOURCES = (r"\b(?:BLS|Bureau of Labor|Census|OECD|World Bank|IMF|Federal Reserve|Fed\b|CBO|GAO|USDA|HUD|"
           r"Gallup|Pew|UN\b|United Nations|WHO\b|EMCDDA|CDC|NIH|NBER|Brookings|Urban Institute|"
           r"Pew|Eurostat|Statistics|Survey|Mondragon|Alaska Permanent Fund|Grounded Solutions|Estonia|X-Road|"
           r"according to|reported by|data from|source:|study|studies)\b")
CITE = r"\b[A-Z][a-zA-Z'’-]+(?: (?:et al\.|and|&) [A-Z][a-zA-Z'’-]+)*,? \(?(?:19|20)\d\d[a-z]?\)?"
GENERIC = [
    ("meta", lambda r, c: bool(rx(r"\b(?:last updated|published|updated|version|v\d|min(?:ute)? read|pages?|papers?|"
                                   r"documents?|word count|copyright|©|ISBN|ISSN|SSRN|Zenodo|month\s?=|year\s?=|"
                                   r"volume|edition|session|commit)\b").search(c)) and not rx(r"[%$£€]").search(r["figure"]),
     "corpus metadata", "metadata", "keep", "the page itself", ""),
    ("formula", lambda r, c: bool(re.search(r"[=×÷]|\d\s?[*/]\s?\d", c)) and not rx(r"\bvalue = |\bmonth = |\byear = ").search(c),
     "derived", "calculation", "keep", "printed on the page", "not recomputed"),
    ("cited", lambda r, c: bool(re.search(CITE, c)) or bool(re.search(SOURCES, c)),
     "external source", "fact", "keep", "cited on the page", "cited, not opened"),
    ("example", lambda r, c: bool(rx(r"\b(?:example|e\.g\.|for instance|illustrat\w*|hypothetical|suppose|consider an?|worked|sample household|"
                                      r"scenario|case study|imagine)\b").search(c)),
     "illustrative projection", "example", "keep", "the page presents it as an example", ""),
    ("target", lambda r, c: bool(rx(r"\b(?:target|goal|aim|KPI|success metric|benchmark|milestone|objective)s?\b").search(c)),
     "design parameter", "target", "relabel", "a target set by the design", ""),
    ("param", lambda r, c: bool(rx(r"\b(?:parameter|set (?:at|to)|capped|cap(?: of)?|fee|allocation|allocated|BU\b|Basic Units?|"
                                    r"per month|monthly|threshold|multiplier|tier|octave|phi|Φ|φ|conversion rate|rate of|"
                                    r"budget|fund(?:ed|ing)?|cost(?:s)?|expire|vesting|credits?|weight(?:ed|s)?|ratio|share of|"
                                    r"members?|households?|board|quorum|supermajority|vote|term|seats?)\b").search(c)),
     "design parameter", "specification", "keep", "the framework's design", ""),
    ("projection", lambda r, c: bool(rx(r"\b(?:project(?:ed|ion|s)?|expect(?:ed)?|will|would|could|can|estimat\w+|potential|forecast|"
                                         r"anticipated?|likely|within \d+|over \d+ years|by 20[3-9]\d|reduc\w+|increas\w+|improv\w+|"
                                         r"growth|sav(?:e|es|ings))\b").search(c)),
     "no basis found", "projection", "relabel", "", ""),
    ("sim", lambda r, c: bool(rx(r"\b(?:simulat\w+|Monte Carlo|iterations|agent-based|ABM|model(?:led|ed|ing)?|results?|"
                                  r"analysis (?:reveals|shows)|our analysis|we find|findings?|demonstrat\w+)\b").search(c)),
     "no basis found", "simulation result", "remove", "", ""),
]

def load_triage(path):
    out = []
    if not path or not pathlib.Path(path).exists():
        print(f"note: S29 triage not found at {path}; s29_id left blank")
        return out
    for t in csv.DictReader(open(path)):
        out.append((t["id"], set(t["files"].split()), re.compile(t["locator"], re.I), t["hub"], t["verdict"], t["severity"]))
    return out

def classify(rows, triage):
    review = [(rx(t[0]), rx(t[1]), *t[2:8], rx(t[8]) if len(t) > 8 else None, f"R{i:03d}")
              for i, t in enumerate(REVIEW, 1)]
    for r in rows:
        ctx, page = r["context"], r["page"]
        hit = None
        if r["ref"] == "1" or r["ref"] == 1:
            hit = ("corpus metadata", "reference-list entry", "keep", "reference list", "", "", "ref")
        if not hit:
            text = f"{r['section']} ¦ {ctx}"
            for prx, crx, cls, claimed, action, src, chk, note, frx, name in review:
                if prx.search(page) and crx.search(text) and (frx is None or frx.search(r["figure"])):
                    hit = (cls, claimed, action, src, chk, note, name); break
        if not hit:
            for name, test, cls, claimed, action, src, chk in GENERIC:
                if test(r, ctx):
                    hit = (cls, claimed, action, src, chk, "", "g:" + name); break
        if not hit:
            slug = re.sub(r"^papers/pdfs/|^papers/|\.(html|pdf|md)$", "", page)
            d = PAPER_DEFAULTS.get(slug, ("no basis found", "fact", "remove", "", "", ""))
            hit = (*d, "default")
        r.update(zip(["class", "claimed", "action", "source", "checked", "note", "rule"], hit))
        ids = [tid for tid, files, loc, hub, verdict, sev in triage
               if page in files and loc.search(ctx) and hub != "gone"]
        r["s29_id"] = " ".join(ids)
        live = [t for t in triage if t[0] in ids and t[4] in ("valid", "partly valid") and t[5] in ("headline", "derivation")]
        if live and r["action"] == "keep" and r["class"] != "corpus metadata":
            r["action"] = "correct"
    return rows

def summary(rows):
    n = collections.Counter(r["class"] for r in rows)
    a = collections.Counter((r["class"], r["action"]) for r in rows)
    pages = collections.defaultdict(collections.Counter)
    for r in rows:
        pages[r["page"]][r["class"]] += 1
    L = ["# Claims ledger summary (S23)", "",
         "Generated by `tools/class_claims.py`; do not edit by hand. One row per figure per sentence in `data/claims.csv`.",
         "Basis classes are research rule 5's. `rule` in the CSV names how each row was classed: `ref` (reference list),",
         "`R…` (a rule in `tools/claims_review.py`, written after reading the passage), `g:…` (a generic keyword rule) or `default` (the paper's default).", "",
         f"Figures: **{len(rows)}** on {len(pages)} pages and PDFs.", "",
         "| Class | Figures | keep | correct | relabel | remove |", "|---|---|---|---|---|---|"]
    for c in CLASSES:
        L.append(f"| {c} | {n[c]} | " + " | ".join(str(a[(c, x)]) for x in ("keep", "correct", "relabel", "remove")) + " |")
    by_rule = collections.Counter(("reviewed" if r["rule"].startswith("R") or r["rule"] == "ref" else "generic") for r in rows)
    L += ["", f"Classed by a reviewed rule or the reference list: {by_rule['reviewed']}; by a generic rule or a paper default: {by_rule['generic']}.", "",
          "## By page", "", "| Page | " + " | ".join(CLASSES) + " |", "|---|" + "---|" * len(CLASSES)]
    for p in sorted(pages):
        L.append(f"| {p} | " + " | ".join(str(pages[p][c]) for c in CLASSES) + " |")
    L += ["", "## No basis found (full list)", "", "| id | page | figure | claimed | action | S29 | sentence |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        if r["class"] == "no basis found":
            s = r["sentence"].replace("|", "/")[:220]
            L.append(f"| {r['id']} | {r['page']} | {r['figure']} | {r['claimed']} | {r['action']} | {r['s29_id']} | {s} |")
    return "\n".join(L) + "\n"

def main():
    tri = sys.argv[sys.argv.index("--triage") + 1] if "--triage" in sys.argv else ROOT.parent / "research-update/audits/refine/triage.csv"
    rows = []
    for page, blocks in ex.collect(ROOT):
        rows += ex.rows_for(page, blocks)
    rows = classify(rows, load_triage(tri))
    cols = ["id", "page", "section", "sentence", "figure", "class", "claimed", "source", "checked",
            "action", "s29_id", "prior_id", "note", "rule"]
    for r in rows:
        r["sentence"] = r.pop("context")
        r.setdefault("prior_id", "")
        m = re.match(r"\[(S5-\d\d)\]\s*", r["note"])
        if m:
            r["prior_id"], r["note"] = m.group(1), r["note"][m.end():]
    with open(ROOT / "data/claims.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    (ROOT / "data/claims-summary.md").write_text(summary(rows))
    n = collections.Counter(r["class"] for r in rows)
    print(f"{len(rows)} figures: " + ", ".join(f"{c} {n[c]}" for c in CLASSES))

if __name__ == "__main__":
    main()
