#!/usr/bin/env python3
"""Build the data for us-policy-eras.html (S75: US policy eras and their stability).

Every figure on the page comes from BetterToBest/compassionism-simulation files, read here
and written unchanged (rounded for display) to data/s75-us-eras.json and into the page's
inline data block:
  sources/s75_eras.json            the descriptive panel (part 1; results s75-panel-54e88bc)
  sources/s75_hx.json              each era's yearly path as the engine reads it
  dev/runs/s77-s75/tables.json     the engine readings (part 2, rerun with the release's settings in S77;
                                   results s75-eras-e5649ef; the first run, dev/runs/s75-eras/, is superseded)

Usage: python3 tools/build_s75_eras.py PATH/TO/compassionism-simulation
"""
import json
import os
import re
import subprocess
import sys

HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(HUB, "us-policy-eras.html")
OUT = os.path.join(HUB, "data", "s75-us-eras.json")


def r(x, n=2):
    return None if x is None else round(x, n)


def main(sim):
    panel = json.load(open(os.path.join(sim, "sources/s75_eras.json")))
    hx = json.load(open(os.path.join(sim, "sources/s75_hx.json")))
    tab = json.load(open(os.path.join(sim, "dev/runs/s77-s75/tables.json")))
    commit = subprocess.run(["git", "-C", sim, "rev-parse", "HEAD"], capture_output=True,
                            text=True).stdout.strip()

    # 1. The yearly path, 1946-2025, joined from the four eras (each era's year 0 is the
    #    previous era's last year; the joins agree, checked below).
    keys = {"cpi": "inflation", "un": "unemployment", "ff": "policy", "hR": "homes",
            "eR": "shares", "rm": "recession_months", "food": "food", "shel": "shelter",
            "med": "medical"}
    years, cols = [], {v: [] for v in keys.values()}
    for i, e in enumerate(["e1", "e2", "e3", "e4"]):
        s, y0 = hx[e]["series"], hx[e]["y0"]
        start = 0 if i == 0 else 1
        if i > 0:
            prev = hx[["e1", "e2", "e3"][i - 1]]["series"]
            for k in ("cpi", "un", "hR", "eR"):
                assert abs(prev[k][-1] - s[k][0]) < 1e-9, (e, k)
        for t in range(start, hx[e]["n"]):
            years.append(y0 + t)
            for k, v in keys.items():
                cols[v].append(r(s[k][t], 2))
    timeline = {"years": years, **cols}

    # 2. The panel: era statistics, the test of Duke's view, distribution, taxes, the rule.
    eras = ["E1", "E2", "E3", "E4", "W", "E0"]
    A = panel["A"]
    spread_keys = [("A1 inflation", "Inflation (CPI-U)"), ("A2 food", "Food prices"),
                   ("A2 shelter", "Shelter prices"), ("A2 medical", "Medical prices"),
                   ("A3 unemployment", "Unemployment rate"),
                   ("A4 growth per person", "Growth per person"),
                   ("A5 homes real change", "Real home prices"),
                   ("A5 shares real change", "Real share prices")]
    stats = {}
    for k, label in spread_keys:
        stats[k] = {"label": label, "eras": {}}
        for e in eras:
            v = A[e].get(k)
            if v and v.get("n"):
                stats[k]["eras"][e] = {"mean": r(v["mean"]), "sd": r(v["sd"]),
                                       "years": v["years"], "max": v.get("max")}
    draw = {}
    for e in eras:
        sh, ho = A[e]["A5 shares drawdown (monthly)"], A[e]["A5 homes drawdown (yearly)"]
        draw[e] = {"shares": sh and [r(sh["fall_pct"], 1), sh.get("months_to_recover")],
                   "homes": ho and [r(ho["fall_pct"], 1), ho.get("years_to_recover")],
                   "recession_months_pct": r(A[e]["A3 months in recession %"], 1)}

    comp = {}
    for key in ("W vs E1", "W vs E2", "W vs E3"):
        comp[key] = [{"measure": c["measure"], "earlier": c["earlier"], "later": c["later"],
                      "diff": c["diff"], "ci95": c["ci95"], "p_holm": c["p_holm"],
                      "verdict": c["verdict"]} for c in panel["comparisons"][key]]
    view = panel["dukes_view"]

    B = panel["B"]
    tax_groups = ["Bottom 50%", "Middle 40%", "Top 10%", "Top 1%", "Top 0.1%"]
    taxes = {g: {e: r(B[e]["B4 average tax rate, " + g]["mean"], 1)
                 for e in ("E1", "E2", "E3", "E4")
                 if B[e].get("B4 average tax rate, " + g)} for g in tax_groups}
    dist_keys = ["B1 top 1% income share", "B1 top 10% income share", "B1 top 1% wealth share",
                 "B2 official poverty %", "B2 anchored SPM poverty %",
                 "B3 health spending % of GDP", "B3 out-of-pocket % of health spending"]
    dist = {k: {e: {"years": B[e][k]["years"], "start": r(B[e][k]["start"], 1),
                    "end": r(B[e][k]["end"], 1)}
                for e in ("E1", "E2", "E3", "E4") if B[e].get(k)} for k in dist_keys}
    beds = {}
    for g, k in (("for-profit", "proprietary"), ("non-profit", "non-profit"),
                 ("government", "government")):
        key = "B3 all hospitals (HSUS): %s %% of beds" % k
        beds[g] = {e: {"years": B[e][key]["years"], "start": r(B[e][key]["start"], 1),
                       "end": r(B[e][key]["end"], 1)}
                   for e in ("E0", "E1", "E2", "E3") if B[e].get(key)}
    adm = panel["B3 community hospital admissions by ownership, % (Health, United States 2017, Table 82)"]
    admissions = {y: adm[y] for y in sorted(adm)}

    rule = {}
    for e, lab in (("E1", "1947-1972"), ("E1 from 1951Q2", "1951-1972 (after the Accord)"),
                   ("E2", "1973-1983"), ("E3", "1984-2007"), ("E4", "2008-2025")):
        v = panel["B5 estimated rule"][e]
        rule[lab] = {"phi": v["phi"], "phi_se": v["se"][1], "beta": v["beta"],
                     "beta_se": v["se"][2], "quarters": v["quarters"], "n": v["n"]}

    # 3. The engine readings.
    out_keys = ["P1", "P2", "P3", "P4", "P5"]

    def verdict(c):
        if c["hiH"] < 0:
            return "steadier"
        if c["loH"] > 0:
            return "less steady"
        return "no clear difference"

    q3 = {}
    for e in ("e1", "e2", "e3"):
        q3[e] = [{"k": out_keys[i], "m": r(c["m"], 3), "lo": r(c["loH"], 3),
                  "hi": r(c["hiH"], 3), "v": verdict(c)}
                 for i, c in enumerate(tab["q3"]["c22"]["P"][e])]
    lv = tab["levels"]
    level_names = ["P1", "P2", "P3", "P4", "P5", "P3_0_11", "basket_poverty",
                   "wealth_poverty_last", "wealth_poverty_avg"]
    levels = {}
    for e in ("e1", "e2", "e3", "e4"):
        levels[e] = {"none": dict(zip(level_names, [r(x, 3) for x in lv["c22"][e + " P 0"]])),
                     "c22": dict(zip(level_names, [r(x, 3) for x in lv["c22"][e + " P 1"]])),
                     "rel": dict(zip(level_names, [r(x, 3) for x in lv["rel"][e + " P 1"]]))}
        assert lv["c22"][e + " P 0"] == lv["rel"][e + " P 0"]
    q4 = {}
    for d in ("c22", "rel"):
        q4[d] = {}
        for e in ("e1", "e2", "e3", "e4"):
            q4[d][e] = [{"k": out_keys[i], "m": r(c["m"], 3), "lo": r(c["loH"], 3),
                         "hi": r(c["hiH"], 3)} for i, c in enumerate(tab["q4"][d][e + " P"])]
    tally = dict(tab["q4tally"])
    # S77: a reversal is favourable when the programme's effect is now in the steadier direction (lower is
    # steadier on all five outcomes), unfavourable otherwise. Counted over the tally's cells (six arms, P-A).
    s74dir = {"c22": [1, 1, -1, -1, -1], "rel": [1, 1, -1, 1, -1]}
    for d in ("c22", "rel"):
        fav = unf = 0
        for e in ("e1", "e2", "e3", "e4"):
            for a in ("P", "R", "S", "T", "H", "A"):
                for i, c in enumerate(tab["q4"][d][e + " " + a]):
                    sig = 1 if c["loH"] > 0 else (-1 if c["hiH"] < 0 else 0)
                    if sig and sig != s74dir[d][i]:
                        if sig < 0:
                            fav += 1
                        else:
                            unf += 1
        assert fav + unf == tally.get(d + " reversed", 0), (d, fav, unf, tally)
        tally[d + " reversed, favourable"] = fav
        tally[d + " reversed, unfavourable"] = unf
    tax_change = {hx[e]["era"]: {"groups": hx[e]["T"]["groups"],
                                 "d": [r(x, 2) for x in hx[e]["T"]["d"]],
                                 "years": hx[e]["T"]["years"]} for e in ("e1", "e2", "e3", "e4")}
    health = {hx[e]["era"]: r(hx[e]["H"]["hm"], 2) for e in ("e1", "e2", "e3", "e4")}
    stance = {e: {"era_rule": [r(x, 1) for x in tab["stance"][e + " c22 R"][:2]],
                  "todays_rule": [r(x, 1) for x in tab["stance"][e + " c22 S"][:2]]}
              for e in ("e1", "e2", "e3", "e4")}

    data = {
        "_about": "Built by research-hub tools/build_s75_eras.py from BetterToBest/compassionism-simulation "
                  "at %s (sources/s75_eras.json, sources/s75_hx.json, dev/runs/s77-s75/tables.json)." % commit,
        "sim_commit": commit,
        "engine_commit": tab["meta"]["e1"]["commit"],
        "seeds": tab["meta"]["e1"]["seeds"],
        "commands": {e: tab["meta"][e]["command"] for e in tab["meta"]},
        "eras": panel["eras"],
        "timeline": timeline,
        "stats": stats, "drawdowns": draw,
        "comparisons": comp, "dukes_view": view,
        "taxes": taxes, "distribution": dist, "beds": beds, "admissions": admissions,
        "rule": rule,
        "q3": q3, "levels": levels, "q4": q4, "q4tally": tally,
        "tax_change": tax_change, "health_real_growth": health, "stance": stance,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(data, f, indent=1)
        f.write("\n")

    # Inline copy in the page, so it works from a file and without a fetch.
    page = open(PAGE).read()
    blob = json.dumps(data, separators=(",", ":"))
    new, n = re.subn(r'(<script id="s75-data" type="application/json">).*?(</script>)',
                     lambda m: m.group(1) + blob + m.group(2), page, flags=re.S)
    assert n == 1, "data block not found in the page"
    open(PAGE, "w").write(new)
    print("wrote", OUT, "and the page's data block (%d bytes)" % len(blob))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
