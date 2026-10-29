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
then "section ¦ sentence", then optionally the figure itself). PDF text runs table cells
together, so on a PDF a rule sees only 70 characters either side of the figure, and a
PDF figure that also appears on the paper's HTML page takes the class reviewed there
before any page-wide fallback rule (a rule whose sentence pattern is ".") is tried.
The generic keyword rules below catch anything left; on the Oct 29, 2026 Hub they class
nothing, and the summary reports how many rows they class so a new page is noticed.
`rule` names the rule that classed each row, so every class can be traced. Rule numbers
change when rules are added; the rule text in claims_review.py is the record.
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
CITE = r"\[\d+(?:[,–-]\s?\d+)*\]|\b[A-Z][a-zA-Z'’-]+(?: (?:et al\.|and|&) [A-Z][a-zA-Z'’-]+)*,? \(?(?:19|20)\d\d[a-z]?\)?"
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

def slug(page):
    return re.sub(r"^papers/pdfs/|^papers/|\.(html|pdf|md)$", "", page)

def words(t):
    return set(re.findall(r"[a-z]{4,}", t.lower()))

def classify(rows, triage):
    review = [(rx(t[0]), rx(t[1]), *t[2:8], rx(t[8]) if len(t) > 8 else None, f"R{i:03d}")
              for i, t in enumerate(REVIEW, 1)]
    keys = ["class", "claimed", "action", "source", "checked", "note", "rule"]
    # 1. reference lists and reviewed rules
    for r in rows:
        r["hit"] = None
        if str(r["ref"]) == "1":
            r["hit"] = ("corpus metadata", "reference-list entry", "keep", "reference list", "", "", "ref")
            continue
        text = f"{r['section']} ¦ {r['context']}"
        pdf = r["page"].endswith(".pdf")
        if pdf:                                  # PDF text runs neighbouring cells together: match near the figure only
            i = max(0, r["context"].find(r["figure"]))
            text = f"{r['section']} ¦ " + r["context"][max(0, i - 70):i + len(r["figure"]) + 70]
        for prx, crx, cls, claimed, action, src, chk, note, frx, name in review:
            if pdf and crx.pattern == ".":       # a page-wide fallback waits until the HTML class has been tried
                continue
            if prx.search(r["page"]) and crx.search(text) and (frx is None or frx.search(r["figure"])):
                r["hit"] = (cls, claimed, action, src, chk, note, name); break
    # 2. a PDF figure that is also on the paper's HTML page takes the class reviewed there
    html = collections.defaultdict(list)
    for r in rows:
        if r["page"].endswith(".html") and r["hit"] and r["hit"][6].startswith("R"):
            html[(slug(r["page"]), r["figure"])].append(r)
    for r in rows:
        if r["hit"] or not r["page"].endswith(".pdf"):
            continue
        cands = html.get((slug(r["page"]), r["figure"]))
        if cands:
            w = words(r["context"])
            best = max(cands, key=lambda c: len(w & words(c["context"])))
            h = best["hit"]
            r["hit"] = (*h[:5], ("as on the HTML page; " + h[5]).rstrip("; "), "html:" + h[6])
    # 3. page-wide fallback rules for the PDF rows still unclassed, then generic keyword rules, then the paper default
    for r in rows:
        if not r["hit"] and r["page"].endswith(".pdf"):
            for prx, crx, cls, claimed, action, src, chk, note, frx, name in review:
                if crx.pattern == "." and prx.search(r["page"]) and (frx is None or frx.search(r["figure"])):
                    r["hit"] = (cls, claimed, action, src, chk, note, name); break
        if not r["hit"]:
            for name, test, cls, claimed, action, src, chk in GENERIC:
                if test(r, r["context"]):
                    r["hit"] = (cls, claimed, action, src, chk, "", "g:" + name); break
        if not r["hit"]:
            d = PAPER_DEFAULTS.get(slug(r["page"]), ("no basis found", "fact", "remove", "", "", ""))
            r["hit"] = (*d, "default")
        r.update(zip(keys, r.pop("hit")))
        if r["page"].endswith(".pdf") and not r["rule"].startswith("html:") and r["rule"] != "ref":
            r["note"] = ("PDF only (not on the HTML page); " + r["note"]).rstrip("; ")
        ids = [tid for tid, files, loc, hub, verdict, sev in triage
               if r["page"] in files and loc.search(f"{r['section']} ¦ {r['context']}") and hub != "gone"]
        r["s29_id"] = " ".join(ids)
        live = [t for t in triage if t[0] in ids and t[4] in ("valid", "partly valid") and t[5] in ("headline", "derivation")]
        if live and r["action"] == "keep" and r["class"] != "corpus metadata":
            r["action"] = "correct"
    return rows

HEADLINE = re.compile(r"^(index|research-summary|papers/index)\.html$|^wiki/|^data/")

def summary(rows, triage):
    n = collections.Counter(r["class"] for r in rows)
    a = collections.Counter((r["class"], r["action"]) for r in rows)
    pages = collections.defaultdict(collections.Counter)
    for r in rows:
        pages[r["page"]][r["class"]] += 1
    head = [r for r in rows if HEADLINE.search(r["page"])]
    nh = collections.Counter(r["class"] for r in head)
    pdf_only = sum(1 for r in rows if r["note"].startswith("PDF only"))
    by_rule = collections.Counter(("reviewed" if re.match(r"R|ref|html:R", r["rule"]) else "generic") for r in rows)
    ext = collections.Counter(("opened" if r["checked"].startswith("opened") else "cited, not opened" if r["checked"].startswith("cited")
                               else "a standard fact or definition, not cited" if r["checked"].startswith("standard")
                               else "named in the text, not opened") for r in rows if r["class"] == "external source")
    opened = sorted({(r["source"], r["checked"]) for r in rows if r["checked"].startswith("opened")})
    linked = collections.Counter(i for r in rows for i in r["s29_id"].split())
    unlinked = [t for t in triage if t[3] != "gone" and t[0] not in linked and t[4] in ("valid", "partly valid") and t[5] in ("headline", "derivation")]
    prior = collections.Counter(i for r in rows for i in r["prior_id"].split())
    L = ["# Claims ledger summary (S23)", "",
         "Generated by `tools/class_claims.py`; do not edit by hand. The ledger itself is `data/claims.csv`: one row per figure per sentence, on every live page, Markdown page, PDF and `data/optimal-parameters.json` (the `/v1/` archive is not included).", "",
         "## What this is", "",
         "Every number the Hub states (percentages, money, multipliers, counts, durations, years ahead) was extracted by `tools/extract_claims.py` and given one basis class from research rule 5, and an action for the corrections step (S24) and the rewrite (S25):", "",
         "- **keep**: the figure has the basis its class names;",
         "- **correct**: the figure or its arithmetic is wrong, or its source must be added (the note says what);",
         "- **relabel**: keep the number but say what it is, usually an illustrative projection, a design parameter or a target;",
         "- **remove**: nothing supports it and nothing honest can be said in its place. Most removals are model results that no published run produced: S30 looks for the code that may have made them, and S25 replaces them with results from the preregistered studies.", "",
         "Each class was set by a rule in `tools/claims_review.py` written after reading the passage (the `rule` column names it), or by the reference list (`ref`), or, for a PDF figure that also appears on the paper's HTML page, by the class reviewed there (`html:R…`). "
         + f"Reviewed or reference-list classes: {by_rule['reviewed']} of {len(rows)}; keyword fallbacks: {by_rule['generic']}.", "",
         "How to read the classes: a value the framework chooses is a **design parameter**; arithmetic that follows from figures printed beside it is **derived** (`checked` says whether it was recomputed); a real-world figure is an **external source** only when the text cites one (`checked` says whether it was opened); a figure stated as a fact or a result with no source, run or derivation is **no basis found** (`claimed` says what it is presented as). This is Claude's reading of rule 5, taking the cautious reading where a page is unclear.", "",
         f"Figures: **{len(rows)}** on {len(pages)} pages and PDFs. {pdf_only} of them are in a PDF only (the PDF is an older or longer version of its HTML page; S24 rebuilds the PDFs).", "",
         "| Class | Figures | keep | correct | relabel | remove |", "|---|---|---|---|---|---|"]
    for c in CLASSES:
        L.append(f"| {c} | {n[c]} | " + " | ".join(str(a[(c, x)]) for x in ("keep", "correct", "relabel", "remove")) + " |")
    L.append(f"| **all** | {len(rows)} | " + " | ".join(str(sum(a[(c, x)] for c in CLASSES)) for x in ("keep", "correct", "relabel", "remove")) + " |")
    L += ["", f"On the front page, research summary, paper index, wiki and parameters file ({len(head)} figures): "
          + ", ".join(f"{c} {nh[c]}" for c in CLASSES if nh[c]) + ".", "",
          "Simulation: only the BLEI paper cites a simulation release for its figures (v4.4, Full Integration, N = 5,000), and it gives no command, seeds or results file, so those rows are marked to be rerun on a release with a recorded command (S40).", "",
          "External sources: " + ", ".join(f"{k} {v}" for k, v in ext.most_common()) + ". Opening the rest is left to S24/S25, figure by figure, before any is kept in a rewritten paper. Sources opened this step:", ""]
    for src, chk in opened:
        L.append(f"- {src}: {chk}")
    L += ["", f"Earlier records merged: the session-5 claims records ({', '.join(sorted(prior))}) are carried in `prior_id` (the original claims-ledger draft was not brought over). "
          f"S29 refine.ink ids are in `s29_id`: {len(linked)} ids are linked to figure rows."]
    if unlinked:
        L[-1] += (f" Valid headline or derivation items with no figure row to attach to (they concern formulas or wording; see the S29 triage): {', '.join(t[0] for t in unlinked)}.")
    L += ["", "## By page", "", "| Page | " + " | ".join(CLASSES) + " |", "|---|" + "---|" * len(CLASSES)]
    for p in sorted(pages):
        L.append(f"| {p} | " + " | ".join(str(pages[p][c]) for c in CLASSES) + " |")
    L += ["", "## No basis found (full list)", "",
          "Grouped by page; the same figure and sentence appearing twice on one page is listed once. Ids are `data/claims.csv` ids.", ""]
    for p in sorted(pages):
        seen, items = set(), []
        for r in rows:
            if r["page"] != p or r["class"] != "no basis found":
                continue
            k = (r["figure"], r["sentence"][:120])
            if k in seen:
                continue
            seen.add(k)
            i = max(0, r["sentence"].find(r["figure"]))
            s_ = re.sub(r"\s+", " ", r["sentence"][max(0, i - 70):i + len(r["figure"]) + 70]).replace("|", "/").strip("… ")
            tag = f" [{r['s29_id']}]" if r["s29_id"] else ""
            items.append(f"- `{r['id']}` **{r['figure']}**: {r['claimed']}, {r['action']}{tag}. …{s_}…")
        if items:
            L += [f"### {p} ({len(items)})", ""] + items + [""]
    return "\n".join(L) + "\n"

def main():
    tri = sys.argv[sys.argv.index("--triage") + 1] if "--triage" in sys.argv else ROOT.parent / "research-update/audits/refine/triage.csv"
    rows = []
    for page, blocks in ex.collect(ROOT):
        rows += ex.rows_for(page, blocks)
    triage = load_triage(tri)
    rows = classify(rows, triage)
    cols = ["id", "page", "section", "sentence", "figure", "class", "claimed", "source", "checked",
            "action", "s29_id", "prior_id", "note", "rule"]
    for r in rows:
        r["sentence"] = r.pop("context")
        ids = re.findall(r"\[?(S5-\d\d)\]?", r["note"])
        r["prior_id"] = " ".join(dict.fromkeys(ids))
        r["note"] = re.sub(r"\[(S5-\d\d)\]\s*", r"\1: ", r["note"])
    with open(ROOT / "data/claims.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    (ROOT / "data/claims-summary.md").write_text(summary(rows, triage))
    n = collections.Counter(r["class"] for r in rows)
    print(f"{len(rows)} figures: " + ", ".join(f"{c} {n[c]}" for c in CLASSES))

if __name__ == "__main__":
    main()
