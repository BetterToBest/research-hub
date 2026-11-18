# Sources behind us-money-history.html (S87)

Every figure on the page is an external source, opened, or a calculation from those sources in `tools/build_s87_money.py` (the derived-calculation file). No simulation figure appears on the page. All files were opened on November 17, 2026. `bash tools/fetch_s87_sources.sh DIR` downloads them again; `python3 tools/build_s87_money.py DIR` rebuilds `data/s87-money-history.json`, the CSV files in this folder and the page's inline data. A changed checksum means the source has revised its series.

## Series

| File | Source | Used for | SHA-256 |
|---|---|---|---|
| `mw_gold_result.html` | MeasuringWorth, *What Was the Price of Gold Then?* (Lawrence H. Officer and Samuel H. Williamson), measuringworth.com/datasets/gold, years 1791-2025 | New York market price of gold (US dollars per fine ounce, annual); US official price; gold/silver price ratio | `149e327094026ad29a0e6ad8581376f220c977baffb18c4f12b33e3463395c21` |
| `GoldBackground.pdf` | MeasuringWorth's note on how the series are built | how the silver price is recovered (below) | `77afb9f03e793a2d3faf5a3f21cdad647c64ec99544c8ccf29a68d48ea754567` |
| `mw_cpi_result.html` | MeasuringWorth, US consumer price index, 1774-2025 (1982-84 = 100; the BLS CPI-U annual average from 1913) | today's dollars (2025 dollars) | `6ecd5fb53bccf98835de1b4264f1742dd9f18c4bf4d6e0fe46bd949a076cfba3` |
| `usprice_cust.xls` | US Census Bureau, Median and Average Sales Prices of New Homes Sold in United States, annual (1963-2023 in the file opened) | the house | `08161fe065709e9cd8da71b4326b11c5b3e0e108174a335639fbf178ad18d69f` |
| `d24_tabn330.10.xlsx` | NCES, Digest of Education Statistics 2024, Table 330.10 (all institutions, current dollars; 1963-64, then 1968-69 to 2023-24) | a year of college | `a4cbf83f27549ec3c17b13f37d84480c8441c41428be76ef53adcabdc8ac9410` |
| (in the build file) | US Department of Labor, Wage and Hour Division, *History of Federal Minimum Wage Rates Under the Fair Labor Standards Act, 1938 - 2009* (dol.gov/agencies/whd/minimum-wage/history/chart), the 1938 Act column | the federal minimum wage | page text, read through a fetch tool; the site refuses scripted downloads |
| `STATUTE-52-Pg1060.pdf` | Fair Labor Standards Act of 1938, 52 Stat. 1060: sec. 6(a) 25 cents in the first year, 30 cents for the next six; sec. 7(a) a 44-hour workweek in the first year, 42 in the second, 40 after; effective 120 days after June 25, 1938 | the legal week | `e43cb6756f72ee8305c229ecde4f82f0746b3f67d785974025bdff0c4cfcde00` |
| `STATUTE-17-Pg424.pdf` | Coinage Act of 1873, 17 Stat. 424: sec. 13, coins 900 parts in 1,000 pure; sec. 15, the half dollar 12.5 grams, the quarter and dime one-half and one-fifth of that | silver in a dollar of coin: 22.5 g pure = 0.7234 troy oz | `37f32ac3b490fa6c9b92efb098a97c04bc898370d4cf2080863fb10b778b5f5f` |
| `STATUTE-79-Pg254.pdf` | Coinage Act of 1965, 79 Stat. 254 (Public Law 89-81, July 23, 1965): clad dimes and quarters; a 40%-silver half dollar | the end of 90% silver coin | `d13d01dc42769928ddc88d573e62f0baf4e80b4862f7896131df6807ca7ca8c0` |
| `data/s75-us-eras.json` | this Hub's policy eras data: December-to-December changes in the BLS CPI-U food, shelter and medical-care indexes | food, shelter and medical prices (chained from 1948; December 1947 = 100) | in this repository |

## The silver price
MeasuringWorth publishes gold prices and the gold/silver ratio (ounces of silver per ounce of gold), not a silver price. The silver price per fine ounce is gold price ÷ ratio. Their note (GoldBackground.pdf, section V) says the ratio is built from New York prices of both metals from 1968, and for 1915-1967 from the official gold price, which equals their New York gold price in those years except 1933 and 1934, which they correct to the market price. So gold ÷ ratio recovers the silver price they used. Check: 1938 gives $0.435 an ounce; 2024 gives $28.48.

## Events marked on the price chart (each checked against the statute or order)
| Date | Event | Checked against |
|---|---|---|
| Apr 2, 1792 | Coinage Act: gold and silver at 15 to 1 | 1 Stat. 246, sec. 11 (govinfo scan of the first page; the ratio clause read in the Wikisource transcription of the Act) |
| Jun 28, 1834 | Coinage Act of 1834: lighter gold coin (about 16 to 1; official gold price $20.69, then $20.67 from the Act of Jan 18, 1837) | 4 Stat. 699; 5 Stat. 136 |
| Feb 12, 1873 | Coinage Act of 1873: the standard silver dollar left off the list of coins | 17 Stat. 424, sec. 15 |
| Mar 14, 1900 | Gold Standard Act | 31 Stat. 45 |
| Dec 23, 1913 | Federal Reserve Act | 38 Stat. 251 |
| Apr 5, 1933 | Executive Order 6102: gold coin, bullion and certificates delivered by May 1, 1933, paid for in other currency at face value; exempt: up to $100 a person, rare coins, gold for industry, profession or art | the Order's text (American Presidency Project) |
| Jan 30-31, 1934 | Gold Reserve Act; Proclamation 2072 fixes the gold dollar at 15 5/21 grains nine-tenths fine, $35.00 an ounce | 48 Stat. 337; Proclamation 2072 (American Presidency Project) |
| Jul 23, 1965 | Coinage Act of 1965 | 79 Stat. 254 |
| Jun 24, 1968 | Silver certificates no longer exchangeable for silver | 81 Stat. 77 (Public Law 90-29, June 24, 1967), sec. 2 |
| Aug 15, 1971 | Convertibility of the dollar into gold suspended | President Nixon's address, Aug 15, 1971 (American Presidency Project) |
| Dec 31, 1974 | Private gold ownership legal again | 88 Stat. 445 (Public Law 93-373, Aug 14, 1974) |

## For and against metal backing (text sources, opened Nov 17, 2026)
- Michael D. Bordo, "Gold Standard", *Concise Encyclopedia of Economics*, Econlib (econlib.org/library/Enc/GoldStandard.html): inflation 0.1% a year 1880-1914 against 4.1% 1946-2003; coefficient of variation of prices 17.0 (1879-1913) against 0.88 (1946-1990), of real output 3.5 (1879-1913) against 0.4 (1946-2003); unemployment 6.8% against 5.9%; Friedman's resource-cost estimate for 1960, more than 2.5% of GNP; wartime suspensions resumed at the old parity, strengthening credibility; renewed interest after the high inflation of the late 1970s and early 1980s.
- Kent A. Clark Center for Global Markets (Chicago Booth), US Economic Experts Panel, "Gold Standard", January 12, 2012 (kentclarkcenter.org/surveys/gold-standard): Question A, 36 answered: 0 agree, 15 disagree, 21 strongly disagree.
- Gary Richardson, Alejandro Komai and Michael Gou, "Roosevelt's Gold Program", Federal Reserve History (federalreservehistory.org/essays/roosevelts-gold-program): the internal and external drains consumed the Federal Reserve's free gold (March 1933); recovery began when countries suspended the gold standard and reflated (citing Eichengreen and Sachs); Roosevelt's reflation accelerated recovery.
- Sandra Kollen Ghizoni, "Nixon Ends Convertibility of U.S. Dollars to Gold and Announces Wage/Price Controls", Federal Reserve History (federalreservehistory.org/essays/gold-convertibility-ends): foreign-held dollars came to exceed US gold; vulnerability to a run; a London run took gold to $40 an ounce on October 20, 1960.

## Part 2: crypto, offshore money and corporate tax, college and student debt, media, other changes (opened Nov 18, 2026)

Sections 4 to 8 of the page. `bash tools/fetch_s87_part2.sh DIR2` downloads these files again; `python3 tools/build_s87_part2.py DIR2` rebuilds `data/s87-part2.json`, the `part2-*.csv` files in this folder and the page's second inline data block. Web pages (news reports, ICIJ, ITEP) change their markup, so their checksums identify the copy that was read, not a fixed file.

| File | Source | Used for | SHA-256 |
|---|---|---|---|
| `STATUTE-110-Pg56.pdf` | Telecommunications Act of 1996, Public Law 104-104 (Feb 8, 1996), sec. 202 | section 7 | `593889127a83cbca36f2e7c3b14f79cbdf215e7ed2f5b9fa25ecadd11ab9bc41` |
| `STATUTE-79-Pg1219.pdf` | Higher Education Act of 1965, Public Law 89-329 (Nov 8, 1965), 79 Stat. 1219, Part B | section 6 | `61dbbb4ccefcc1a432925e17e6754fe9ccfa68048a8d022717ee178cee4209a2` |
| `STATUTE-90-Pg2081.pdf` | Education Amendments of 1976, Public Law 94-482 (Oct 12, 1976), sec. 439A: five years or undue hardship, from Sep 30, 1977 | section 6 | `78c03eaf96356420bffbdfe98d1131fc85e232ae0b1cda07e8dcca71af10139c` |
| `bitcoin.pdf` | Satoshi Nakamoto, "Bitcoin: A Peer-to-Peer Electronic Cash System" (bitcoin.org) | section 4: what Bitcoin is; "no central authority to issue them" | `b1674191a88ec5cdd733e4240a81803105dc412d6c6708d53ab94fc248f4f553` |
| `cftc_8638.html` | CFTC press release 8638-22 (Dec 13, 2022): charges against Bankman-Fried, FTX and Alameda; over $8 billion in customer deposits lost | section 4: FTX | `12d6cd53d0f6d6195bb610c10949a846f1c6dfb52e72c04efa3ccd7f4dca0d37` |
| `cftc_8938.html` | CFTC press release 8938-24 (Aug 8, 2024): $12.7 billion judgment against FTX and Alameda | section 4: FTX | `90db7a19d2349f2bb33af59fcb25485c1bee8b635d1ae10b808309b76b5a31b2` |
| `cg_trump.json` | CoinGecko API, coin official-trump, read Nov 18, 2026 00:22 UTC: high $73.43 on Jan 19, 2025; price $0.97 | section 4 | `d35818b86807b6af1488abd18e1bec01cb32c2bc6f1e5346a07f643e56195d74` |
| `christin_www13.pdf` | Nicolas Christin, "Traveling the Silk Road: A Measurement Analysis of a Large Anonymous Online Marketplace", WWW 2013 | section 4: Silk Road | `b574ed3d572647090fdc9fab43684c1ff3cb0cb077a37aa29046b58521cade55` |
| `cornell_1141.html` | 11 U.S.C. 1141(d): confirmation of a Chapter 11 plan discharges the debtor; sec. 523 exceptions apply to individuals | section 6 | `04b19681612811e071c2c48e8dc3f62df5f7b736a729c86d2b1f5ed4ae41922d` |
| `cornell_523.html` | 11 U.S.C. 523, with its amendment notes (1978 enactment; 1990 seven years; 1998 removal of the time route; 2005 qualified education loans) | section 6 | `f603baeb80ae8880e529b835e872877d2fbef8eafde75a9bf561e068732da50f` |
| `fred_A053RC1A027NBEA.csv` | BEA, corporate profits before tax without IVA and CCAdj, annual, $ billions (FRED A053RC1A027NBEA) | section 5: share of profits | `a9d3cf9dbfeb2481748d436610bc819fb160236645482ced42b0b7ba529598b2` |
| `fred_CBBTCUSD.csv` | Coinbase, Bitcoin price in US dollars, daily (FRED CBBTCUSD), from Dec 1, 2014 | section 4: price, swings, chart | `d00ae42ea2864cd90c39e9ed6c12fca962aed3bfd133e2083939786c3ee2298d` |
| `fred_COMPRNFB.csv` | BLS, nonfarm business real hourly compensation, index (FRED COMPRNFB) | section 8 | `a8746c4dfc3aca19b771ea3962d0ebcbc79424836af5cd91478213034e6dd906` |
| `fred_DTWEXBGS.csv` | Federal Reserve Board, nominal broad US dollar index, daily (FRED DTWEXBGS) | section 4: the dollar | `fdf877b02fd69d833873bb790f18436d256fc997863a53d21ef77a9b118d3bb0` |
| `fred_MEHOINUSA646N.csv` | Census, median household income, current dollars, annual (FRED MEHOINUSA646N) | section 8 | `2052185cf05506b963bfe3aaee5dbbc1783e1518b144b74ecd85058b43de4bfc` |
| `fred_MSPUS.csv` | Census and HUD, median sales price of houses sold, quarterly (FRED MSPUS) | section 8 | `a9f5886d44aeb6f0bbb14d823b1c2b397e8fb7775fb47b6dfd4c67073fdbea32` |
| `fred_NASDAQCOM.csv` | NASDAQ OMX, NASDAQ Composite index, daily (FRED NASDAQCOM) | section 4: shares | `89f5efa47ec417bc88787df11a756026dd8003fe7f3b2e88a4d543c74ba5cdb0` |
| `fred_OPHNFB.csv` | BLS, nonfarm business labor productivity, index (FRED OPHNFB) | section 8 | `22388ed7f795285daabcbb663e5064fc357261aacd4d76304c8bdf479e877d24` |
| `fred_TDSP.csv` | Federal Reserve Board, household debt service payments, % of disposable personal income (FRED TDSP; from 2005 Q1 in the file read) | section 8 | `7c9538093b5b4c6245dc4245dcb810c0c3fcf5d380300dc75f4a172ac7f0eda8` |
| `gter24_exec.pdf` | EU Tax Observatory, Global Tax Evasion Report 2024, executive summary: $1 trillion in 2022, 35% | section 5 | `8fe8c63372a937eb9a82c1a4a2fb200503556232fbb6bbc63df42e171902e576` |
| `hhd_2026q3.xlsx` | Federal Reserve Bank of New York, Household Debt and Credit Report, 2026 Q3, page 3 data | sections 6 and 8: student and household debt | `f6370608a1e0dcf5e2781afc812fa789ac4d55cae6036361bbf42d41976b72a3` |
| `ic3_2024.pdf` | FBI Internet Crime Complaint Center, 2024 IC3 Annual Report | section 4: crypto fraud losses | `ba494b0a1bd991c722cf65619eb518329175b898fb508e8c84fc7dd12e07cac0` |
| `icij_cofounder.html` | ICIJ, former co-owner of Mossack Fonseca convicted in Cologne, Apr 24, 2026; firm closed within two years | section 5 | `04b58f2b8ce7fc0bbb8e422757f285e0b75e244bc389667e80506410488fd52b` |
| `icij_dcg_bro.html` | ICIJ, two brothers convicted of murdering Daphne Caruana Galizia, Oct 16, 2022 (date and place of the killing) | section 5 | `3350097cffb0bdf06a28f5f838fe7366c7c5d3a015bf3ea25813230f08c1d272` |
| `icij_dcg_inq.html` | ICIJ, "Malta responsible for assassination of journalist Daphne Caruana Galizia, inquiry finds", Jul 30, 2021 | section 5 | `af6483d6c1e9f77cc332b10ab2838b6df791901c6a47113ccaaaa72fac2ae745` |
| `icij_dcgson.html` | ICIJ, interview with Paul Caruana Galizia (she was reporting Panama Papers revelations) | section 5 | `a92e44f86666f8f28a06b4e8f6e4bd21b73105037068991b6b7a66a8f2695f90` |
| `icij_faq.html` | ICIJ, Panama Papers FAQ | section 5 | `d53668dbf0b814525901fad75315f3ae20dce1dc3767a2e23244dab7c1ab6288` |
| `icij_recouped.html` | ICIJ, "Hundreds of millions more dollars recouped by governments after ICIJ investigations", Apr 3, 2025: $1.3 billion tally | section 5 | `a271a290dad7f2498d56a1cfb837d80b5f9f30ccff32e0feb94214b8e9be4dab` |
| `icij_ten3.html` | ICIJ, "Global headlines and a public reckoning: ten years of the Panama Papers, part 3" | section 5: Gunnlaugsson within 48 hours | `99a185b0b5d59a9c77ab3dbb69a4e5e25eca80b8e6e61ceafcc15d3ce5987682` |
| `icij_trial.html` | ICIJ, Panama Papers trial concludes with all defendants absolved, Jun 28, 2024 | section 5 | `68d60f4a4b083974d213ab0c2938335026e509b8d79573307a1ee3bd3d8c9f0c` |
| `ii_lbo.html` | Institutional Investor, "LBOs Make (More) Companies Go Bankrupt, Research Shows", Jul 26, 2019, reporting Ayash and Rastad (published Finance Research Letters 38, 2021, 101452) | section 6 | `41f7118c53f966117b21f769a7421185264d3289e3209f6be4673b11c0a1dc75` |
| `irs_histab23.xls` | IRS Statistics of Income, Historical Table 23 (rates to tax year 2018) | section 8: top legal rate | `57aed4c02ac6c6dcd39d0fea18ca231ebe22085acedf098b3b993fb154399557` |
| `itep_2021.html` | ITEP, "55 Corporations Paid $0 in Federal Taxes on 2020 Profits" (context; the statutory rate) | section 5 | `70b750c2a68805e37424f034049c740c5f9f757f2ae6892ded9ad33fd22ff7ba` |
| `itep_2025.html` | ITEP, corporate tax avoidance in 2025, Oct 22, 2026: 706 companies, 114 paid nothing, 10.4% | section 5 | `85f7cdc0839084875aeae9032015d3d2430bbcc4b10439e234aff98dd7006aa8` |
| `itep_tcja.html` | ITEP, "Corporate Tax Avoidance Under the Tax Cuts and Jobs Act", Feb 29, 2024: 342 companies, 23, 109, 14.1% | section 5 | `570d85e0f19ed47f73922a05201b140eed03c643556bf9c0302c0b7db7a5f7a9` |
| `medill_2025.html` | Medill (Northwestern University), news release on the State of Local News Report 2025 | section 7 | `a2bfb0e4861d12c4f00ec2c4be337c0a4e1e2299bdf599cbb8c2d2e1c6f65717` |
| `mempool_block0.json` | mempool.space block explorer, block 0: timestamp 1231006505 = Jan 3, 2009, 18:15:05 UTC | section 4: first block | `d890732201b59ac7b00433c76f4d513340edafe549e1714b3528f707e086b52d` |
| `missingprofits.html` | missingprofits.world (the same authors): close to $1 trillion in 2019; 10% of corporate tax receipts; US multinationals about 60% | section 5 | `236bf0051c0dc00c4f2040247c2c0407f5ae4e9a5020d1658fc9bab681e06e00` |
| `nber_missing.html` | Tørsløv, Wier and Zucman, "The Missing Profits of Nations", NBER Working Paper 24701, abstract: close to 40% | section 5 | `dd91ddcab6c27256b03ff9f5c01cf3bbbb96596707a5069bd6607d36b10e8f92` |
| `npr_ftxrepay.html` | NPR, "FTX says it will return money to most of its customers", May 9, 2024 | section 4: FTX | `c6823c44839e23827c9afe02fd055ffcdef0fb2cfa55a16e88f0b9c9b844b242` |
| `npr_pardon.html` | NPR, "Trump pardons Ross Ulbricht, creator of the Silk Road dark web marketplace", Jan 21, 2025 | section 4 | `cc1a9ba0562575c22921065453d3a26e0ff3f20da9a9c238f6651c13f63121ce` |
| `npr_sbf.html` | NPR, "Sam Bankman-Fried sentenced to 25 years in prison for his FTX crimes", Mar 28, 2024 | section 4: FTX | `a72f0f66d31592b5eb7a78e93e556e30dbef21131a0f4be113aa5dc1b0f8b4cc` |
| `npr_trump2.html` | NPR, "What to know about Trump cryptocurrency meme coins", Jan 20, 2025 | section 4: $TRUMP launch price and high | `dab0b9bc031d27f12809eedecc390e793955d0690390bd17a92588a8a38e57e2` |
| `npr_ulbricht2015.html` | NPR, "Silk Road Founder Ross Ulbricht Sentenced To Life In Prison", May 29, 2015 | section 4 | `42c36a1cb0cda423eb0112386ad7ace0b2022269d5e13a5a8b8cc94993d06718` |
| `omb_hist02z1_fy2027.xlsx` | OMB, Historical Tables, Table 2.1, receipts by source, FY 1934-2031 (actual to 2025) | section 5: corporate tax in dollars | `1212da86947a71d9a0268e23d3de789402bcfb80b308cd48a32926a65b2e7bc3` |
| `omb_hist02z2_fy2027.xlsx` | OMB, Historical Tables, Table 2.2, percentage composition of receipts, FY 1934-2031 | section 5: share of federal receipts | `9e2bc741ca3a92929551ca65c6db55901a1d96bac0cae43788c89cfac4f0fe55` |
| `pbs_trump1p2.html` | PBS NewsHour (AP), "Trump took in about $1.2 billion from crypto businesses last year, financial disclosure shows", Jun 30, 2026 | section 4: CIC Digital's meme-coin sales | `543dadc484768195018f0377e025f7addebe032111c83ee6c23c249207340745` |
| `pew_tv2014.html` | Pew Research Center, "The acquisition binge in local TV", May 12, 2014 | section 7 | `587276e177cf0b0bd8b73cc6cd314716a2cc89e2392ce0c968421fd6dd2d2567` |
| `pew_tv2017.html` | Pew Research Center, "Buying spree brings more local TV stations to fewer big companies", May 11, 2017 | section 7 | `2d89420817509a9a22e218fbdc43cc29c9410afb00d8d5797ae58c588a50e9a1` |
| `resource_brunner.html` | Brunner v. New York State Higher Education Services Corp., 831 F.2d 395 (2d Cir., decided Oct 14, 1987) | section 6: the three-part test | `3de2474f2730c89c91138938f2d862419dec854b8de791012069b37803b1aeaf` |
| `scripps_ceo.html` | Scripps News, "CEOs now earn 325 times more than workers, report says" (reporting the Economic Policy Institute) | section 8 | `a70d598250bbedc97515ab06a1c894d70d37eaa34fce4ca2d340347dfc7e86d6` |
| `trumpmemes.html` | gettrumpmemes.com, the issuer's site: allocation, unlocking schedule, statements quoted | section 4 | `0d8c8b03108ec1a5c0fd5f590509b1181f7d89e64619ae475644b25dba8653c3` |
| `wb_CMO-Historical-Data-Monthly.xlsx` | World Bank, Commodity Price Data (Pink Sheet), monthly, updated Nov 3, 2026: Gold, $/troy oz | section 4: gold | `3c8d9d8dbb48342fdbf24777c39a8ce8964cc2fd0958f72f6779e6e4ad99cde2` |

Read through a fetch tool (the sites refuse scripted downloads), so no file or checksum:
- US Bureau of Labor Statistics, *Union Members — 2025* (news release, Feb 18, 2026, bls.gov/news.release/union2.nr0.htm): 10.0 percent in 2025; 20.1 percent and 17.7 million in 1983.

Not opened, so not used: the Justice Department's press releases on Ulbricht and Bankman-Fried (the site refused automated reading; NPR's and the CFTC's reports were used instead); the Economic Policy Institute's own report on CEO pay (refused; reported through Scripps News and labelled so); the full Medill 2025 report (certificate error; its news release was used); Ben Bagdikian's counts of media owners (books not opened; the page says so); the full text of Ayash and Rastad (publisher and SSRN refused; Institutional Investor's report was used and the page says so).

### Calculations (tools/build_s87_part2.py)
- Yearly averages of market prices: the mean of the twelve monthly means of daily values (gold: the World Bank's monthly averages).
- Volatility: the standard deviation of month-to-month log changes of the monthly averages, January 2015 to December 2025, times the square root of 12.
- Largest fall: the largest drop from a previous monthly-average high to a later month, 2015-2025; for bitcoin also on daily prices.
- Corporate tax as a share of profits: OMB Table 2.1 corporation income taxes (fiscal year, $ millions) ÷ (1,000 × BEA profits before tax, same calendar year). Fiscal years ended June 30 until 1976 and September 30 after, so the two do not cover the same months.
- House price to income: the yearly mean of quarterly MSPUS ÷ that year's median household income.
- Output per hour and pay: percent change of the yearly mean of each quarterly index between the years named.
