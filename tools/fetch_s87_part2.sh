#!/usr/bin/env bash
# Download the external sources behind the later sections of us-money-history.html (S87 items 4-8)
# into DIR, then print each file's SHA-256 so it can be checked against data/s87/SOURCES.md (part 2).
#   bash tools/fetch_s87_part2.sh /path/to/raw2
#   python3 tools/build_s87_part2.py /path/to/raw2
# Data files (FRED, OMB, World Bank, New York Fed, IRS) are revised from time to time; web pages
# (news reports, ICIJ, ITEP) change their markup, so their checksums record the copy that was read
# on November 18, 2026, not a fixed file. Pages that refuse scripted downloads (BLS union release;
# the Justice Department) were read through a fetch tool and are not downloaded here.
set -euo pipefail
D="${1:?usage: fetch_s87_part2.sh DIR}"
mkdir -p "$D"; cd "$D"
UA="Mozilla/5.0 (X11; Linux x86_64) research-reader"
get(){ curl -sS -L --retry 3 -m 180 -A "$UA" -o "$1" "$2"; }
fred(){ get "fred_$1.csv" "https://fred.stlouisfed.org/graph/fredgraph.csv?id=$1&cosd=${2:-1900-01-01}"; }

# Market and economic series (used in the build)
fred CBBTCUSD 2014-12-01; fred NASDAQCOM 2014-12-01; fred DTWEXBGS 2014-12-01
fred A053RC1A027NBEA; fred MSPUS; fred MEHOINUSA646N; fred OPHNFB; fred COMPRNFB; fred TDSP
get wb_CMO-Historical-Data-Monthly.xlsx "https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx"
get omb_hist02z1_fy2027.xlsx https://www.whitehouse.gov/wp-content/uploads/2026/04/hist02z1_fy2027.xlsx
get omb_hist02z2_fy2027.xlsx https://www.whitehouse.gov/wp-content/uploads/2026/04/hist02z2_fy2027.xlsx
get hhd_2026q3.xlsx https://www.newyorkfed.org/medialibrary/interactives/householdcredit/data/xls/hhd_c_report_2026q3.xlsx
get irs_histab23.xls https://www.irs.gov/pub/irs-soi/histab23.xls

# Documents cited in the text
get bitcoin.pdf https://bitcoin.org/bitcoin.pdf
get mempool_block0.json https://mempool.space/api/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
get christin_www13.pdf https://www.andrew.cmu.edu/user/nicolasc/publications/Christin-WWW13.pdf
get ic3_2024.pdf https://www.ic3.gov/AnnualReport/Reports/2024_IC3Report.pdf
get cg_trump.json "https://api.coingecko.com/api/v3/coins/official-trump?localization=false&tickers=false&community_data=false&developer_data=false"
get trumpmemes.html https://gettrumpmemes.com/
get npr_ulbricht2015.html https://www.npr.org/sections/thetwo-way/2015/05/29/410580782/silk-road-founder-ross-ulbricht-sentenced-to-life-in-prison
get npr_pardon.html https://www.npr.org/2025/01/21/nx-s1-5270051/trump-pardons-dark-web-marketplace-creator-ross-ulbricht
get npr_sbf.html https://www.npr.org/2024/03/28/1241210300/sam-bankman-fried-ftx-sentencing-crimes-crypto-mogul-greed
get npr_ftxrepay.html https://www.npr.org/2024/05/09/1250133251/ftx-says-it-will-return-money-to-most-of-its-customers
get npr_trump2.html https://www.npr.org/2025/01/20/nx-s1-5268759/donald-trump-melania-cryptocurrency-meme-coins
get pbs_trump1p2.html https://www.pbs.org/newshour/politics/trump-took-in-about-1-2-billion-from-crypto-businesses-last-year-financial-disclosure-shows
get cftc_8638.html https://www.cftc.gov/PressRoom/PressReleases/8638-22
get cftc_8938.html https://www.cftc.gov/PressRoom/PressReleases/8938-24
P=https://www.icij.org/investigations/panama-papers
get icij_faq.html $P/panama-papers-faq-all-you-need-to-know-about-the-2016-investigation/
get icij_recouped.html $P/hundreds-of-millions-more-dollars-recouped-by-governments-after-icij-investigations/
get icij_ten3.html $P/global-headlines-and-a-public-reckoning-ten-years-of-the-panama-papers-part-3/
get icij_trial.html $P/panama-papers-trial-concludes-with-all-defendants-absolved-of-money-laundering-charge/
get icij_cofounder.html $P/former-co-owner-of-panama-papers-law-firm-convicted-of-aiding-and-abetting-tax-evasion/
get icij_dcg_inq.html $P/malta-responsible-for-assassination-of-journalist-daphne-caruana-galizia-inquiry-finds/
get icij_dcgson.html $P/it-is-still-dangerous-to-be-a-journalist-daphne-caruana-galizias-son-reflects-on-her-life-and-legacy/
get icij_dcg_bro.html https://www.icij.org/inside-icij/2022/10/two-brothers-convicted-of-murdering-daphne-caruana-galizia-sentenced-to-40-years-in-prison/
get nber_missing.html https://www.nber.org/papers/w24701
get missingprofits.html https://missingprofits.world/
get gter24_exec.pdf https://taxobservatory.world//www-site/uploads/2023/10/Executive_Summary_English.pdf
get itep_tcja.html https://itep.org/corporate-tax-avoidance-trump-tax-law/
get itep_2025.html https://itep.org/corporate-tax-avoidance-2025/
get itep_2021.html https://itep.org/55-profitable-corporations-zero-corporate-tax/
get STATUTE-79-Pg1219.pdf https://www.govinfo.gov/content/pkg/STATUTE-79/pdf/STATUTE-79-Pg1219.pdf
get STATUTE-90-Pg2081.pdf https://www.govinfo.gov/content/pkg/STATUTE-90/pdf/STATUTE-90-Pg2081.pdf
get STATUTE-110-Pg56.pdf https://www.govinfo.gov/content/pkg/STATUTE-110/pdf/STATUTE-110-Pg56.pdf
get cornell_523.html https://www.law.cornell.edu/uscode/text/11/523
get cornell_1141.html https://www.law.cornell.edu/uscode/text/11/1141
get resource_brunner.html https://law.resource.org/pub/us/case/reporter/F2/831/831.F2d.395.41.87-5013.html
get ii_lbo.html https://www.institutionalinvestor.com/article/b1gfygl4r8661f/LBOs-Make-More-Companies-Go-Bankrupt-Research-Shows
get pew_tv2017.html https://www.pewresearch.org/short-reads/2017/05/11/buying-spree-brings-more-local-tv-stations-to-fewer-big-companies/
get pew_tv2014.html https://www.pewresearch.org/short-reads/2014/05/12/the-acquisition-binge-in-local-tv/
get medill_2025.html https://www.medill.northwestern.edu/news/2025/news-deserts-hit-new-high-and-50-million-have-limited-access-to-local-news-study-finds.html
get scripps_ceo.html https://www.scrippsnews.com/life/money/ceos-now-earn-325-times-more-than-workers-report-says
sha256sum ./*
