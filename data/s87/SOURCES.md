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
