#!/usr/bin/env bash
# Download the external sources behind us-money-history.html (S87) into DIR, then
# print each file's SHA-256 so it can be checked against data/s87/SOURCES.md.
#   bash tools/fetch_s87_sources.sh /path/to/raw
# Sources can revise their series; a changed checksum means a revised file, and the
# build is then rerun and the page's figures checked again.
set -euo pipefail
D="${1:?usage: fetch_s87_sources.sh DIR}"
mkdir -p "$D"; cd "$D"
get(){ curl -sS -L --retry 3 -m 120 -o "$1" "$2"; }
post(){ curl -sS -L --retry 3 -m 120 -o "$1" -d "$2" "$3"; }

# MeasuringWorth: gold prices (New York market, US official) and the gold/silver price ratio
post mw_gold_result.html "london=on&goldsilver=on&newyork=on&us=on&year_source=1791&year_result=2025" \
  https://www.measuringworth.com/datasets/gold/result.php
get GoldBackground.pdf https://www.measuringworth.com/docs/GoldBackground.pdf
# MeasuringWorth: US consumer price index, 1774 onward (BLS CPI-U from 1913)
post mw_cpi_result.html "year_source=1774&year_result=2025" https://www.measuringworth.com/datasets/uscpi/result.php
# Census: median sales price of new houses sold, annual
get usprice_cust.xls https://www.census.gov/construction/nrs/xls/usprice_cust.xls
# NCES Digest of Education Statistics 2024, Table 330.10: undergraduate tuition, fees, room and board
get d24_tabn330.10.xlsx https://nces.ed.gov/programs/digest/d24/tables/xls/tabn330.10.xlsx
# Statutes at Large (govinfo): FLSA 1938, Coinage Acts 1873 and 1965
get STATUTE-52-Pg1060.pdf https://www.govinfo.gov/content/pkg/STATUTE-52/pdf/STATUTE-52-Pg1060.pdf
get STATUTE-17-Pg424.pdf https://www.govinfo.gov/content/pkg/STATUTE-17/pdf/STATUTE-17-Pg424.pdf
get STATUTE-79-Pg254.pdf https://www.govinfo.gov/content/pkg/STATUTE-79/pdf/STATUTE-79-Pg254.pdf
sha256sum ./*
