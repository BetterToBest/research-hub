#!/usr/bin/env python3
"""Build the data for us-money-history.html (S87: money, metals and the modern economy).

Descriptive history only: no simulation run and no model figure. Every series is an external
source, opened, or a derived calculation from those sources (this file):

  mw_gold_result.html   MeasuringWorth, "What Was the Price of Gold Then?" (Officer and Williamson):
                        New York market price of gold, US official price, gold/silver price ratio,
                        annual, 1791-2025
  mw_cpi_result.html    MeasuringWorth, US consumer price index, annual (1982-84 = 100; BLS CPI-U
                        annual average from 1913)
  usprice_cust.xls      US Census Bureau, median and average sales price of new houses sold, annual, 1963-
  d24_tabn330.10.xlsx   NCES, Digest of Education Statistics 2024, Table 330.10, average
                        undergraduate tuition, fees, room and board, all institutions, current dollars
  MIN_WAGE below        US Department of Labor, Wage and Hour Division, "History of Federal Minimum
                        Wage Rates Under the Fair Labor Standards Act, 1938 - 2009" (opened Nov 17, 2026)
  WORKWEEK below        Fair Labor Standards Act of 1938, sec. 7(a), 52 Stat. 1060, 1063
  COIN_OZ_PER_DOLLAR    Coinage Act of 1873, secs. 13 and 15, 17 Stat. 424: the half dollar weighs
                        12.5 grams, the quarter and dime one-half and one-fifth of that, all 900 fine;
                        so a dollar of face value in dimes, quarters or halves holds 22.5 grams of pure
                        silver = 0.7234 troy ounces. These weights held until the Coinage Act of 1965
                        (79 Stat. 254) ended 900-fine dimes and quarters.
  s75-us-eras.json      this Hub's US policy eras data: December-to-December change in the BLS CPI-U
                        food, shelter and medical-care indexes (from 1948; built by build_s75_eras.py)

Usage: python3 tools/build_s87_money.py RAWDIR      (RAWDIR from tools/fetch_s87_sources.sh)
Writes data/s87/*.csv, data/s87-money-history.json and the page's inline data block.
"""
import csv
import hashlib
import html
import json
import os
import re
import sys

HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(HUB, "us-money-history.html")
OUTDIR = os.path.join(HUB, "data", "s87")
OUT = os.path.join(HUB, "data", "s87-money-history.json")
TODAY = 2025          # last full year in every annual source used here
TROY_G = 31.1034768   # grams in a troy ounce
COIN_OZ_PER_DOLLAR = 22.5 / TROY_G   # 0.72340 oz of pure silver per $1 face (1873 Act weights, 900 fine)
COIN_OZ_WORN = 0.715  # the trade convention for circulated 90% coin (a little lost to wear); shown as a check

# DOL WHD history chart, 1938 Act coverage column (effective date, dollars an hour)
MIN_WAGE = [("1938-10-24", 0.25), ("1939-10-24", 0.30), ("1945-10-24", 0.40), ("1950-01-25", 0.75),
            ("1956-03-01", 1.00), ("1961-09-03", 1.15), ("1963-09-03", 1.25), ("1967-02-01", 1.40),
            ("1968-02-01", 1.60), ("1974-05-01", 2.00), ("1975-01-01", 2.10), ("1976-01-01", 2.30),
            ("1978-01-01", 2.65), ("1979-01-01", 2.90), ("1980-01-01", 3.10), ("1981-01-01", 3.35),
            ("1990-04-01", 3.80), ("1991-04-01", 4.25), ("1996-10-01", 4.75), ("1997-09-01", 5.15),
            ("2007-07-24", 5.85), ("2008-07-24", 6.55), ("2009-07-24", 7.25)]
# FLSA 1938 sec. 7(a): 44 hours in the first year from Oct 24, 1938, 42 in the second, 40 after
WORKWEEK = [("1938-10-24", 44), ("1939-10-24", 42), ("1940-10-24", 40)]

# Events marked on the price chart; each checked against the statute or order named
EVENTS = [
    {"date": "1792-04-02", "label": "Coinage Act: dollar defined in silver and gold, 15 to 1",
     "source": "1 Stat. 246, sec. 11 (\"the proportional value of gold to silver ... shall be as fifteen to one\")"},
    {"date": "1834-06-28", "label": "Coinage Act of 1834: gold coin made lighter (about 16 to 1)",
     "source": "4 Stat. 699 (approved June 28, 1834)"},
    {"date": "1873-02-12", "label": "Coinage Act of 1873: the standard silver dollar dropped",
     "source": "17 Stat. 424, sec. 15 (silver coins listed: trade dollar, half, quarter, dime)"},
    {"date": "1900-03-14", "label": "Gold Standard Act: gold the single standard",
     "source": "31 Stat. 45 (approved March 14, 1900): the dollar of 25.8 grains of gold nine-tenths fine \"shall be the standard unit of value\""},
    {"date": "1913-12-23", "label": "Federal Reserve Act",
     "source": "38 Stat. 251 (December 23, 1913)"},
    {"date": "1933-04-05", "label": "Executive Order 6102: private gold delivered to the Federal Reserve by May 1",
     "source": "Executive Order 6102, April 5, 1933 (American Presidency Project text)"},
    {"date": "1934-01-31", "label": "Gold Reserve Act (Jan 30) and Proclamation 2072 (Jan 31): $35 an ounce",
     "source": "48 Stat. 337; Proclamation 2072 fixes the gold dollar at 15 5/21 grains nine-tenths fine, which is $35.00 per fine ounce"},
    {"date": "1965-07-23", "label": "Coinage Act of 1965: silver taken out of dimes and quarters",
     "source": "79 Stat. 254 (Public Law 89-81, July 23, 1965)"},
    {"date": "1968-06-24", "label": "Silver certificates no longer redeemable in silver",
     "source": "81 Stat. 77 (Public Law 90-29, June 24, 1967), sec. 2: exchangeable for silver bullion for one year after enactment"},
    {"date": "1971-08-15", "label": "Gold window closed: dollar's convertibility into gold suspended",
     "source": "President Nixon's address of August 15, 1971 (American Presidency Project text)"},
    {"date": "1974-12-31", "label": "Private gold ownership legal again",
     "source": "88 Stat. 445 (Public Law 93-373, approved August 14, 1974): effective December 31, 1974, or earlier"},
]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def text_of(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s))


def num(x):
    return float(x.replace(",", ""))


def read_gold(path):
    t = text_of(path)
    t = t[t.index("London Market Price"):]
    t = t[t.index(")", t.index("per fine ounce")) + 1:]
    rows = {}
    for m in re.finditer(r"\b(1[789]\d\d|20\d\d) ([\d,]+\.\d\d) ([\d,]+\.\d\d) ([\d,]+\.\d\d) (?:£|\$) ([\d,]+\.\d\d)", t):
        y = int(m.group(1))
        rows[y] = {"official": num(m.group(2)), "gold": num(m.group(3)), "ratio": num(m.group(4))}
    assert rows and min(rows) == 1791 and max(rows) == TODAY, (min(rows), max(rows))
    assert len(rows) == TODAY - 1791 + 1
    return rows


def read_cpi(path):
    t = text_of(path)
    t = t[t.index("U.S. Consumer Price Index"):]
    rows = {int(m.group(1)): num(m.group(2)) for m in re.finditer(r"\b(1[789]\d\d|20\d\d) ([\d,]+\.\d\d)\b", t)}
    rows = {y: v for y, v in rows.items() if 1774 <= y <= TODAY}
    assert len(rows) == TODAY - 1774 + 1
    return rows


def read_houses(path):
    """Census table: year, median price, average price of new houses sold. Returns (median, average)."""
    import xlrd
    s = xlrd.open_workbook(path).sheet_by_index(0)
    med, avg = {}, {}
    for r in range(s.nrows):
        a, b, c = s.row_values(r)[:3]
        if isinstance(a, float) and isinstance(b, float) and isinstance(c, float) and 1900 < a < 2100:
            med[int(a)], avg[int(a)] = b, c
    return med, avg


def read_tuition(path):
    import openpyxl
    ws = openpyxl.load_workbook(path, data_only=True).active
    out, on = {}, False
    for row in ws.iter_rows(values_only=True):
        lab = str(row[0] or "").strip()
        if lab.startswith("All institutions"):
            on = True
            continue
        if on and lab and not lab[:1].isdigit():
            break
        m = re.match(r"(\d{4})-\d\d", lab)
        if on and m:
            out[int(m.group(1))] = {"total": num(str(row[1]).replace("$", "")),
                                    "tuition": num(str(row[4]).replace("$", ""))}
    return out


def in_effect(table, date):
    v = None
    for d, x in table:
        if d <= date:
            v = x
    return v


def main(raw):
    gold = read_gold(os.path.join(raw, "mw_gold_result.html"))
    cpi = read_cpi(os.path.join(raw, "mw_cpi_result.html"))
    houses, houses_avg = read_houses(os.path.join(raw, "usprice_cust.xls"))
    tuition = read_tuition(os.path.join(raw, "d24_tabn330.10.xlsx"))
    s75 = json.load(open(os.path.join(HUB, "data", "s75-us-eras.json")))["timeline"]

    years = list(range(1791, TODAY + 1))
    g = [gold[y]["gold"] for y in years]
    # Silver per fine ounce = gold price / gold-silver ratio. MeasuringWorth builds the ratio from the
    # same New York prices for 1968 on, and for 1915-1967 from the official gold price, which is the
    # New York price in those years except 1933-1934, which they correct (GoldBackground.pdf, sec. V).
    sv = [gold[y]["gold"] / gold[y]["ratio"] for y in years]
    c = [cpi[y] for y in years]
    k = cpi[TODAY]

    # Minimum wage: the rate and the legal workweek in effect on July 1 of each year (1938: Oct 24)
    mw = []
    for y in years:
        d = "1938-10-24" if y == 1938 else "%d-07-01" % y
        rate, hrs = in_effect(MIN_WAGE, d), in_effect(WORKWEEK, d)
        if rate is None:
            mw.append(None)
            continue
        week = rate * hrs
        i = y - 1791
        mw.append({"year": y, "rate": rate, "hours": hrs, "week": round(week, 2),
                   "coin_oz": round(week * COIN_OZ_PER_DOLLAR, 2) if y <= 1964 else 0.0,
                   "coin_oz_worn": round(week * COIN_OZ_WORN, 2) if y <= 1964 else 0.0,
                   "market_oz": round(week / sv[i], 2),
                   "gold_oz": round(week / g[i], 4),
                   "week_today": round(week * k / c[i], 2)})
    # The same at each change of rate or workweek (the silver price is that year's average)
    changes = []
    for d in sorted(set([x[0] for x in MIN_WAGE] + [x[0] for x in WORKWEEK])):
        y = int(d[:4]); i = y - 1791
        rate, hrs = in_effect(MIN_WAGE, d), in_effect(WORKWEEK, d)
        week = rate * hrs
        changes.append({"date": d, "rate": rate, "hours": hrs, "week": round(week, 2),
                        "coin_oz": round(week * COIN_OZ_PER_DOLLAR, 2) if y <= 1964 else 0.0,
                        "market_oz": round(week / sv[i], 2), "silver_price": round(sv[i], 4)})

    # Items whose prices the page converts into other units
    hourly = {r["year"]: r["rate"] for r in mw if r}
    items = {
        "house": {"label": "Median new house (Census)", "kind": "price",
                  "years": sorted(houses), "usd": [houses[y] for y in sorted(houses)]},
        "house_avg": {"label": "Average new house (Census)", "kind": "price",
                      "years": sorted(houses_avg), "usd": [houses_avg[y] for y in sorted(houses_avg)]},
        "college": {"label": "A year of college: tuition, fees, room and board (NCES, all institutions)",
                    "kind": "price", "years": sorted(tuition), "usd": [tuition[y]["total"] for y in sorted(tuition)],
                    "note": "Academic year starting in the autumn of the year shown"},
        "tuition": {"label": "A year of college: tuition and required fees only (NCES)", "kind": "price",
                    "years": sorted(tuition), "usd": [tuition[y]["tuition"] for y in sorted(tuition)]},
        "minwage": {"label": "A week at the federal minimum wage", "kind": "price",
                    "years": [r["year"] for r in mw if r], "usd": [r["week"] for r in mw if r]},
        "cpi": {"label": "The CPI basket (all items)", "kind": "index", "years": years, "usd": c},
    }
    # Food, shelter and medical care: chained from the December-to-December changes on the policy
    # eras page (BLS indexes), 1948 on; level 100 in December 1947. The page's 1946-1947 values are
    # the all-items rate and are not used.
    ty = s75["years"]
    for key, lab in (("food", "Food"), ("shelter", "Shelter"), ("medical", "Medical care")):
        lv, ys, out = 100.0, [], []
        for y, r in zip(ty, s75[key]):
            if y < 1948:
                continue
            lv *= 1 + r / 100.0
            ys.append(y); out.append(round(lv, 3))
        items[key] = {"label": lab + " prices (CPI-U index, December 1947 = 100)", "kind": "index",
                      "years": ys, "usd": out}
    for it in items.values():
        it["today_usd"], it["gold_oz"], it["silver_oz"], it["minwage_hours"] = [], [], [], []
        for y, v in zip(it["years"], it["usd"]):
            i = y - 1791
            it["today_usd"].append(round(v * k / c[i], 2))
            it["gold_oz"].append(round(v / g[i], 5))
            it["silver_oz"].append(round(v / sv[i], 4))
            it["minwage_hours"].append(round(v / hourly[y], 2) if y in hourly else None)

    data = {
        "_about": "Built by research-hub tools/build_s87_money.py from external sources (data/s87/SOURCES.md). Descriptive history; no simulation figure.",
        "today": TODAY,
        "coin_oz_per_dollar": round(COIN_OZ_PER_DOLLAR, 5),
        "coin_oz_worn": COIN_OZ_WORN,
        "metals": {"years": years, "gold": g, "silver": [round(x, 4) for x in sv],
                   "official": [gold[y]["official"] for y in years],
                   "ratio": [gold[y]["ratio"] for y in years], "cpi": c,
                   "gold_today": [round(x * k / ci, 2) for x, ci in zip(g, c)],
                   "silver_today": [round(x * k / ci, 3) for x, ci in zip(sv, c)]},
        "events": EVENTS,
        "minwage": [r for r in mw if r],
        "minwage_changes": changes,
        "items": items,
        "sources": {f: sha(os.path.join(raw, f)) for f in sorted(os.listdir(raw))
                    if f in ("mw_gold_result.html", "mw_cpi_result.html", "usprice_cust.xls",
                             "d24_tabn330.10.xlsx", "GoldBackground.pdf", "STATUTE-52-Pg1060.pdf",
                             "STATUTE-17-Pg424.pdf", "STATUTE-79-Pg254.pdf")},
    }

    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "metals.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "gold_ny_usd_per_oz", "us_official_gold_usd", "gold_silver_ratio",
                    "silver_usd_per_oz_derived", "cpi_1982_84_100", "gold_%d_usd" % TODAY, "silver_%d_usd" % TODAY])
        m = data["metals"]
        for j, y in enumerate(years):
            w.writerow([y, m["gold"][j], m["official"][j], m["ratio"][j], m["silver"][j], m["cpi"][j],
                        m["gold_today"][j], m["silver_today"][j]])
    with open(os.path.join(OUTDIR, "minimum-wage-silver.csv"), "w", newline="") as f:
        w = csv.writer(f)
        cols = ["year", "rate", "hours", "week", "coin_oz", "coin_oz_worn", "market_oz", "gold_oz", "week_today"]
        w.writerow(cols)
        for r in data["minwage"]:
            w.writerow([r[x] for x in cols])
    with open(os.path.join(OUTDIR, "items.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item", "year", "usd", "usd_%d" % TODAY, "gold_oz", "silver_oz", "minwage_hours"])
        for key, it in items.items():
            for j, y in enumerate(it["years"]):
                w.writerow([key, y, it["usd"][j], it["today_usd"][j], it["gold_oz"][j], it["silver_oz"][j],
                            it["minwage_hours"][j]])
    s = json.dumps(data, separators=(",", ":"))
    open(OUT, "w").write(json.dumps(data, indent=1) + "\n")
    if os.path.exists(PAGE):
        p = open(PAGE).read()
        p2 = re.sub(r'(<script id="s87-data" type="application/json">).*?(</script>)',
                    lambda mm: mm.group(1) + s + mm.group(2), p, count=1, flags=re.S)
        open(PAGE, "w").write(p2)
    print("wrote", OUT)


if __name__ == "__main__":
    main(sys.argv[1])
