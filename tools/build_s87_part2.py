#!/usr/bin/env python3
"""Build the data for part 2 of us-money-history.html (S87 items 4-8): crypto, offshore money and
corporate tax, college costs and student debt, and other changes since the 1960s.

Descriptive history only: no simulation run and no model figure. Every number is an external
source, opened (data/s87/SOURCES.md, part 2), or a derived calculation from those sources (this
file). Text sources (news reports, court opinions, statutes, reports) are cited on the page; this
file computes only the series and tables below.

  fred_CBBTCUSD.csv        Coinbase Bitcoin price, US dollars, daily (FRED series CBBTCUSD), from Dec 2014
  fred_NASDAQCOM.csv       NASDAQ Composite index, daily (FRED series NASDAQCOM)
  fred_DTWEXBGS.csv        Nominal Broad US Dollar Index, Federal Reserve Board, daily (FRED DTWEXBGS)
  wb_CMO-Historical-Data-Monthly.xlsx  World Bank Pink Sheet, monthly prices: Gold ($/troy oz)
  omb_hist02z1_fy2027.xlsx OMB Historical Tables, Table 2.1, receipts by source ($ millions), FY 1934-
  omb_hist02z2_fy2027.xlsx OMB Historical Tables, Table 2.2, percentage composition of receipts, FY 1934-
  fred_A053RC1A027NBEA.csv BEA, corporate profits before tax (without IVA and CCAdj), annual, $ billions
  hhd_2026q3.xlsx          Federal Reserve Bank of New York, Household Debt and Credit Report, 2026 Q3,
                           page 3 data: debt balance by type, $ trillions, 2003 Q1 - 2026 Q3
  fred_MSPUS.csv           Census and HUD, median sales price of houses sold, quarterly (FRED MSPUS)
  fred_MEHOINUSA646N.csv   Census, median household income, current dollars (FRED MEHOINUSA646N)
  fred_OPHNFB.csv          BLS, nonfarm business sector: labor productivity (output per hour), index
  fred_COMPRNFB.csv        BLS, nonfarm business sector: real hourly compensation, index
  fred_TDSP.csv            Federal Reserve Board, household debt service payments, % of disposable income
  irs_histab23.xls         IRS Statistics of Income, Historical Table 23: highest bracket tax rate
  ../s87/items.csv         part 1 of this page: a year of college (NCES Table 330.10) in 2025 dollars
  ../s75-us-eras.json      the policy eras page: health spending % of GDP (CMS national health expenditure)

Usage: python3 tools/build_s87_part2.py RAWDIR      (RAWDIR from tools/fetch_s87_part2.sh)
Writes data/s87/part2-*.csv, data/s87-part2.json and the page's second inline data block.
"""
import csv
import hashlib
import json
import math
import os
import re
import sys

HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(HUB, "us-money-history.html")
OUTDIR = os.path.join(HUB, "data", "s87")
OUT = os.path.join(HUB, "data", "s87-part2.json")
Y0, Y1 = 2015, 2025          # full calendar years covered by every market series used in section 4
MIN_WAGE = 7.25              # federal minimum wage from July 24, 2009 (DOL; part 1's table)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def fred(raw, sid):
    out = []
    with open(os.path.join(raw, "fred_%s.csv" % sid)) as f:
        r = csv.reader(f)
        next(r)
        for d, v in r:
            if v not in ("", "."):
                out.append((d, float(v)))
    return out


def monthly_mean(rows):
    acc = {}
    for d, v in rows:
        acc.setdefault(d[:7], []).append(v)
    return {k: sum(v) / len(v) for k, v in acc.items()}


def annual_mean(rows):
    acc = {}
    for d, v in rows:
        acc.setdefault(int(d[:4]), []).append(v)
    return {k: sum(v) / len(v) for k, v in acc.items()}


def wb_gold(raw):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(raw, "wb_CMO-Historical-Data-Monthly.xlsx"), read_only=True, data_only=True)
    rows = list(wb["Monthly Prices"].iter_rows(values_only=True))
    h = next(i for i, r in enumerate(rows) if r and any(x is not None and str(x).strip() == "Gold" for x in r))
    gi = [i for i, x in enumerate(rows[h]) if x is not None and str(x).strip() == "Gold"][0]
    assert "troy oz" in str(rows[h + 1][gi])
    out = {}
    for r in rows[h + 2:]:
        if r[0] and re.match(r"^\d{4}M\d\d$", str(r[0])) and isinstance(r[gi], (int, float)):
            out["%s-%s" % (r[0][:4], r[0][5:])] = float(r[gi])
    return out


def months(y0, y1):
    return ["%d-%02d" % (y, m) for y in range(y0, y1 + 1) for m in range(1, 13)]


def vol(series, keys):
    """Annualised standard deviation of monthly log changes in the monthly average, percent."""
    ch = [math.log(series[b] / series[a]) for a, b in zip(keys, keys[1:])]
    mu = sum(ch) / len(ch)
    sd = math.sqrt(sum((c - mu) ** 2 for c in ch) / (len(ch) - 1))
    return 100 * sd * math.sqrt(12)


def worst_fall(series, keys):
    """Largest fall from a previous peak, on monthly averages: (percent, peak month, trough month)."""
    best = (0.0, None, None)
    pk = keys[0]
    for k in keys:
        if series[k] > series[pk]:
            pk = k
        f = 100 * (series[k] / series[pk] - 1)
        if f < best[0]:
            best = (f, pk, k)
    return best


def omb(raw, name, col):
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(raw, name), data_only=True).active
    out = {}
    for r in ws.iter_rows(values_only=True):
        if r[0] is not None and re.match(r"^\d{4}$", str(r[0]).strip()) and isinstance(r[col], (int, float)):
            out[int(r[0])] = float(r[col])
    return out


def nyfed(raw):
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(raw, "hhd_2026q3.xlsx"), read_only=True, data_only=True)["Page 3 Data"]
    rows = list(ws.iter_rows(values_only=True))
    h = next(i for i, r in enumerate(rows) if r and r[1] == "Mortgage")
    hdr = list(rows[h])
    si, ti = hdr.index("Student Loan"), hdr.index("Total")
    out = []
    for r in rows[h + 1:]:
        if r[0] and re.match(r"^\d\d:Q\d$", str(r[0])):
            out.append({"q": "20%s Q%s" % (r[0][:2], r[0][4]), "student": round(r[si], 4), "total": round(r[ti], 4)})
    return out


def irs_top(raw):
    import pandas as pd
    d = pd.read_excel(os.path.join(raw, "irs_histab23.xls"), header=None)
    out = {}
    for i in range(d.shape[0]):
        r = d.iloc[i].tolist()
        try:
            y = int(r[0])
        except (TypeError, ValueError):
            continue
        if not 1913 <= y <= 2030:
            continue
        cells = [str(x) for x in r[1:] if str(x) != "nan"]
        # highest bracket rate is the 6th non-empty cell after the year (exemptions x3, lowest rate,
        # lowest bracket, highest rate); strip footnote markers such as "[12] 94.0"
        try:
            out[y] = float(re.sub(r"\[[^\]]*\]", "", cells[5]).strip())
        except (IndexError, ValueError):
            pass
    return out


def main(raw):
    os.makedirs(OUTDIR, exist_ok=True)
    data = {"_about": "Built by research-hub tools/build_s87_part2.py from external sources (data/s87/SOURCES.md, part 2). Descriptive history; no simulation figure."}

    # ---- 4. Crypto: Bitcoin against gold, shares and the dollar, 2015-2025 ----
    btc_d = fred(raw, "CBBTCUSD")
    nas_d = fred(raw, "NASDAQCOM")
    usd_d = fred(raw, "DTWEXBGS")
    btc_m, nas_m, usd_m = monthly_mean(btc_d), monthly_mean(nas_d), monthly_mean(usd_d)
    gold_m = wb_gold(raw)
    keys = months(Y0, Y1)
    assets = [("btc", "Bitcoin (Coinbase price)", btc_m), ("gold", "Gold (World Bank, per troy ounce)", gold_m),
              ("nasdaq", "Shares (NASDAQ Composite index)", nas_m), ("usd", "The dollar (Fed broad dollar index)", usd_m)]
    for _, _, s in assets:
        missing = [k for k in keys if k not in s]
        assert not missing, missing[:3]
    years = list(range(Y0, Y1 + 1))
    ann = {}
    for code, label, s in assets:
        ann[code] = [sum(s["%d-%02d" % (y, m)] for m in range(1, 13)) / 12 for y in years]
    stats = []
    for code, label, s in assets:
        f, pk, tr = worst_fall(s, keys)
        stats.append({"code": code, "label": label, "vol": round(vol(s, keys), 1),
                      "fall": round(f, 1), "peak": pk, "trough": tr,
                      "change": round(100 * (ann[code][-1] / ann[code][0] - 1), 0)})
    # Bitcoin's highest daily price to the end of 2025, and its deepest fall on daily prices
    upto = [(d, v) for d, v in btc_d if d <= "%d-12-31" % Y1]
    pk = max(upto, key=lambda x: x[1])
    best, run_pk = (0.0, None, None), upto[0]
    for d, v in upto:
        if v > run_pk[1]:
            run_pk = (d, v)
        f = v / run_pk[1] - 1
        if f < best[0]:
            best = (f, run_pk, (d, v))
    on_day = dict(btc_d)
    data["crypto"] = {
        "years": years,
        "annual": {c: [round(v, 2) for v in ann[c]] for c in ann},
        "index": {c: [round(100 * v / ann[c][0], 1) for v in ann[c]] for c in ann},
        "btc_gold_oz": [round(b / g, 2) for b, g in zip(ann["btc"], ann["gold"])],
        "btc_minwage_hours": [round(b / MIN_WAGE, 0) for b in ann["btc"]],
        "stats": stats,
        "btc_first": btc_d[0],
        "btc_peak_daily": pk,
        "btc_daily_fall": {"pct": round(100 * best[0], 1), "peak": best[1], "trough": best[2]},
        "btc_2022_11_11": on_day.get("2022-11-11"),
        "window": "%d-01 to %d-12, monthly averages of daily prices (gold: World Bank monthly average)" % (Y0, Y1),
    }
    with open(os.path.join(OUTDIR, "part2-crypto.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "bitcoin_usd", "gold_usd_oz", "nasdaq_composite", "broad_dollar_index", "bitcoin_in_gold_oz", "bitcoin_in_minwage_hours"])
        for i, y in enumerate(years):
            w.writerow([y] + [round(ann[c][i], 2) for c in ("btc", "gold", "nasdaq", "usd")] +
                       [data["crypto"]["btc_gold_oz"][i], data["crypto"]["btc_minwage_hours"][i]])

    # ---- 5. Corporate income tax: share of federal receipts and of pre-tax profits ----
    share = omb(raw, "omb_hist02z2_fy2027.xlsx", 2)        # % of total receipts, fiscal years
    corp = omb(raw, "omb_hist02z1_fy2027.xlsx", 2)         # $ millions, fiscal years
    prof = {int(d[:4]): v for d, v in fred(raw, "A053RC1A027NBEA")}   # $ billions, calendar years
    ty = [y for y in range(1934, 2026) if y in share and y in corp and y in prof]
    assert ty[0] == 1934 and ty[-1] == 2025, (ty[0], ty[-1])
    data["corptax"] = {
        "years": ty,
        "share_of_receipts": [share[y] for y in ty],
        "share_of_profits": [round(100 * corp[y] / (1000 * prof[y]), 1) for y in ty],
    }
    with open(os.path.join(OUTDIR, "part2-corporate-tax.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "corporate_income_tax_pct_of_federal_receipts_FY", "corporate_income_tax_usd_millions_FY",
                    "corporate_profits_before_tax_usd_billions_CY", "tax_pct_of_profits"])
        for i, y in enumerate(ty):
            w.writerow([y, share[y], corp[y], prof[y], data["corptax"]["share_of_profits"][i]])

    # ---- 6. College and student debt ----
    col = {}
    with open(os.path.join(OUTDIR, "items.csv")) as f:
        for r in csv.DictReader(f):
            if r["item"] == "college":
                col[int(r["year"])] = (float(r["usd"]), float(r["usd_2025"]), float(r["minwage_hours"]))
    cy = [y for y in (1963, 1970, 1980, 1990, 2000, 2010, 2020) if y in col] + [max(col)]
    debt = nyfed(raw)
    data["college"] = {"rows": [[y] + [round(x, 0) for x in col[y]] for y in cy]}
    data["debt"] = {"first": debt[0], "last": debt[-1], "quarters": [d["q"] for d in debt],
                    "student": [d["student"] for d in debt], "total": [d["total"] for d in debt]}
    with open(os.path.join(OUTDIR, "part2-household-debt.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["quarter", "student_loans_usd_trillions", "total_household_debt_usd_trillions"])
        for d in debt:
            w.writerow([d["q"], d["student"], d["total"]])

    # ---- 8. Other changes ----
    hp = annual_mean(fred(raw, "MSPUS"))
    inc = {int(d[:4]): v for d, v in fred(raw, "MEHOINUSA646N")}
    prd, cmp_ = annual_mean(fred(raw, "OPHNFB")), annual_mean(fred(raw, "COMPRNFB"))
    tdsp = fred(raw, "TDSP")
    top = irs_top(raw)
    eras = json.load(open(os.path.join(HUB, "data", "s75-us-eras.json")))
    h = eras["distribution"]["B3 health spending % of GDP"]

    def g(a, y0, y1):
        return round(100 * (a[y1] / a[y0] - 1), 0)
    yi0, yi1 = min(inc), max(y for y in inc if y in hp)
    data["other"] = {
        "home_to_income": {"y0": yi0, "v0": round(hp[yi0] / inc[yi0], 1), "y1": yi1, "v1": round(hp[yi1] / inc[yi1], 1)},
        "health_gdp": {"y0": 1960, "v0": h["E1"]["start"], "y1": 2024, "v1": h["E4"]["end"]},
        "productivity_vs_pay": {"p_48_73": g(prd, 1948, 1973), "c_48_73": g(cmp_, 1948, 1973),
                                "p_73_25": g(prd, 1973, 2025), "c_73_25": g(cmp_, 1973, 2025)},
        "debt_service": {"q0": tdsp[0][0], "v0": round(tdsp[0][1], 1), "q1": tdsp[-1][0], "v1": round(tdsp[-1][1], 1)},
        "household_debt": {"q0": debt[0]["q"], "v0": round(debt[0]["total"], 2), "q1": debt[-1]["q"], "v1": round(debt[-1]["total"], 2)},
        "top_rate": {str(y): top[y] for y in (1944, 1952, 1964, 1965, 1981, 1982, 1987, 1988, 1991, 1993, 2003, 2013, 2018) if y in top},
        "top_rate_last_year": max(top),
    }
    data["sources"] = {fn: sha(os.path.join(raw, fn)) for fn in sorted(os.listdir(raw))
                       if os.path.isfile(os.path.join(raw, fn))}

    s = json.dumps(data, separators=(",", ":"))
    open(OUT, "w").write(json.dumps(data, indent=1) + "\n")
    p = open(PAGE).read()
    p2, n = re.subn(r'(<script id="s87-data2" type="application/json">).*?(</script>)',
                    lambda m: m.group(1) + s + m.group(2), p, flags=re.S)
    if n == 1:
        open(PAGE, "w").write(p2)
    print(json.dumps({k: v for k, v in data.items() if k not in ("sources",)}, indent=1)[:6000])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
