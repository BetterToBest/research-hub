"""Reviewed classing rules for tools/class_claims.py (step S23, Oct 29, 2026).

Each rule was written after reading the passage it matches. A rule is
  (page regex, "section ¦ sentence" regex, class, claimed, action, source, checked, note[, figure regex])
and the first rule that matches a figure classes it. Cross-page rules come first: the same
figure often appears on the front page, the research summary, the paper, its PDF and the wiki.
A note that starts with "[S5-nn]" carries the session-5 claims record id (audits/corrections-package-s5.md
in research-update) into the `prior_id` column.

How the classes are applied (Claude's reading of research rule 5; the most cautious reading where the text is silent):
- A value the framework chooses (an allocation, price, rate, cap, tier boundary, or a stated target)
  is a design parameter. A target written as if it were an expected outcome is relabelled.
- Arithmetic that follows from figures printed beside it is derived; `source` names where, and
  `checked` says whether it was recomputed (recompute.py and s5_checks.py are the S29 and session-5 scripts).
- A figure presented as a model or simulation result with no release, command or run behind it is
  "no basis found" (claimed: simulation result). S30 looks for the code that may have produced it.
- A figure presented as a real-world fact is "external source" only if the text cites a source;
  `checked` says whether the source was opened. An uncited real-world figure is "no basis found"
  (claimed: fact), with action "correct" (find and cite a source) where it is plausible.
- A worked example, stylized household or scenario that the text presents as such is an
  illustrative projection. A forecast stated as fact with no model is "no basis found" and relabelled.
"""
DER, EXT, PAR, ILL, META, NONE, SIM = ("derived", "external source", "design parameter",
    "illustrative projection", "corpus metadata", "no basis found", "simulation")
ALL = r"."
BLEI = "BLEI paper (basic-living-economic-index.html)"
SUM = r"^(index|research-summary)\.html$|^wiki/"

REVIEW = [
    # ---- corpus metadata, every page
    (ALL, r"CC BY|Creative Commons|licen[cs]", META, "licence", "keep", "the page itself", "", "licence version"),
    (ALL, r"©|copyright", META, "copyright years", "keep", "the page itself", "", ""),
    (ALL, r"Ontology version|\bupdated 20\d\d|Last updated|Version \d|\(v\d+\.\d+ update\)", META, "version or date", "keep", "the page itself", "", ""),
    (ALL, r"\b1[57]\+? (?:core |open-access |peer-reviewable )?(?:research |working )?papers|Papers: 17|collection of 17|comprising 17", META, "count of papers", "keep", "the Hub's paper list", "", ""),
    (r"^index\.html$", r"Symmetrical Geometric Construction ¦", PAR, "emblem geometry", "keep", "site emblem", "", "geometry of the site's emblem, not a research figure"),

    # ---- CCO conversion design (front page, summary, papers)
    (ALL, r"14\.56", DER, "calculation", "keep", "9 × 1.618, printed beside it", "recomputed: 14.56", "", r"14\.56"),
    (ALL, r"Octave 1 = 1,000|Octave \d = [\d,]+ BU|Cbase × 2", DER, "calculation", "keep", "capacity doubling formula printed beside it", "recomputed", "illustrative base of 1,000 BU"),
    (ALL, r"stadium-concert band|small café with limited hours", ILL, "example", "keep", "the page presents it as an example", "", ""),
    (ALL, r"(?:1×\s?[–-]\s?9×|1× to 9×|1x-9x|1-9x|\b9× base|9× ×|Phi-rate|Phi-Rate|Φ ≈ 1\.618|~1\.618|golden ratio)", PAR, "specification", "keep", "the framework's design (conversion tiers, Phi-rate)", "", "", r"[×x]$|1\.618"),

    # ---- PTF overhead, theta, PTH penetration (summary blocks)
    (ALL, r"35–55% (?:empirical )?overhead reduction|overhead (?:cost )?reductions of 35–55%", EXT, "fact", "keep", "Mondragon/Eroski: Whyte & Whyte (1991) and a 2003 study, cited in the BLEI paper", "cited, not opened", "", r"^35–55%$"),
    (ALL, r"overhead (?:reduction|reduce)\w*.{0,40}40[–-]60%|40[–-]60%.{0,60}(?:framework design target|overhead)|reduc\w+ (?:collective )?overhead (?:by an estimated )?40[–-]60%", PAR, "design target", "keep", "framework design target, set against the 35-55% Mondragon figure", "", "", r"40[–-]60"),
    (ALL, r"stress-tested across a range of participation rate scenarios to establish the 0\.15–0\.25", NONE, "simulation result", "correct", "", "", "Says theta comes from Monte Carlo runs with a confidence interval; no run is published. Theta is a design parameter range (uniform 0.15-0.25 in the engine before v4.4): say so"),
    (ALL, r"θ\)?:? 0\.15–0\.25|Uniform 0\.15–0\.25|synergy coefficient.{0,30}0\.15", PAR, "model coefficient", "keep", "design parameter of the engine's wealth function", "", "a swept design parameter, not an estimate (research rule 3)"),
    (ALL, r"density-gated synergy|0 below 55% PTF density|scales to 0\.25 at 90", PAR, "model coefficient", "keep", "engine design parameter (v4.4 Table 6 in the BLEI paper)", "", ""),
    (SUM, r"50% (?:PTH share|market share) within 5–19", ILL, "projection", "keep", "PTH government-integration paper's three pathways; labelled illustrative", "", ""),
    (r"^research-summary\.html$", r"modeling showing 50% market penetration achievable within 5–19", NONE, "simulation result", "relabel", "", "", "'modeling showing' but no run is published; the front page calls the same range illustrative"),
    (r"^research-summary\.html$", r"from pilot programs \(\$50B\) to transformational scale \(\$500B\)", PAR, "scenario sizes", "keep", "PTH government-integration paper's scenarios", "", "", r"\$"),
    (r"^research-summary\.html$", r"financial architecture demonstrating 50% PTH market penetration", NONE, "simulation result", "relabel", "", "", "'demonstrating': no run is published; an illustrative projection"),

    # ---- BLEI suite (front page, summary, wiki, BLEI paper)
    (ALL, r"Crisis \(0–6\)|Tier 0 Crisis|Six tiers|<\s?7 days|> ?730 days|Flourishing threshold of 730", PAR, "specification", "keep", BLEI + ", tier table", "", ""),
    (ALL, r"US baseline near-poverty: ~?0\.625|0\.625 \(baseline market rent\)|EDC = 0\.625|EDC_baseline = 0\.625", DER, "calculation", "keep", BLEI + ", Index II: rent $1,300 / income $2,083", "recomputed: 0.624", "stylized profile A, not a measured US figure", r"0\.625"),
    (ALL, r"CCO-PTH target: 0\.025|EDC target under CCO-PTF: ~0\.025|→ 0\.025 \(PTH|EDC_CCO = 0\.025", PAR, "design target", "keep", BLEI + ", Index II", "", "", r"0\.025"),
    (ALL, r"\$2,502", DER, "calculation", "keep", BLEI + ": 360×$2.75 + 840×$1.80 = $990 + $1,512", "recomputed: 2,502", "", r"2,502"),
    (ALL, r"5\.80×|5\.80x", DER, "calculation", "keep", BLEI + ", Index III: ($2,083+$2,502−$52)/($2,083×0.375)", "recomputed: 5.80", "", r"5\.80|4,533|781|1\.00×"),
    (ALL, r"3\.40–6\.70×", DER, "sensitivity", "keep", BLEI + ", Section 5 sensitivity table", "not recomputed", "", r"3\.40"),
    (ALL, r"\$2,281", DER, "calculation", "keep", BLEI + ", Appendix B.4: $2,083+$1,200−$950−$52", "s5_checks.py (session 5): reproduces", "[S5-12] conditional on the EDC target 0.025; label it (C29)", r"2,281|\$0|0\.025"),
    (ALL, r"Baseline: \$0 \(deficit\)|\$0/month deficit|from \$0 deficit", DER, "calculation", "keep", BLEI + ", FBS table: max(0, $2,083−$1,950−$250)", "recomputed: −$117 → $0", ""),
    (ALL, r"CSI\(i,t\)", DER, "formula constant", "keep", BLEI, "", "months per year in a formula"),
    (ALL, r"360 BU × \$2\.75|360 BU food|\$990|840 (?:utility )?BU|\$150 cash utility", DER, "calculation", "keep", BLEI + ", Section 4.0b", "recomputed: 360×2.75 = 990", "BU split and $2.75 market equivalent are design parameters", r"990|\$2\.75|360|840|\$150|\$1\.80|1,512"),
    (ALL, r"BU at face value \$1,200|BU allocation flat at \$1,200|approximately \$1,200 per adult|\$1,200/adult/month", PAR, "specification", "keep", "framework design: BU allocation", "", ""),
    (ALL, r"γ \(liquidity coefficient\): 0\.12|0\.12 at entry", PAR, "model coefficient", "keep", BLEI + ", Index I (motivated by Carroll 1997, values chosen)", "", ""),
    (ALL, r"300\+ CLTs, 46 US states", EXT, "fact", "keep", "National CLT Network (2023), cited in the BLEI paper", "cited, not opened", "", r"300|46"),
    (ALL, r"validates r_a range 2–7%", PAR, "model coefficient", "relabel", BLEI + ": r_a base 0.04, sensitivity 0.02-0.07", "", "'validates' overstates: CLT data are consistent with the range; the range is a design parameter", r"2–7"),
    (ALL, r"ε_food = 2\.64: Mondragon", EXT, "fact", "keep", "Mondragon/Eroski, cited in the BLEI paper", "cited, not opened", "", r"35–55"),
    (ALL, r"ε_food = 2\.64|1\.00/\(0\.350\+0\.028\)", DER, "calculation", "keep", BLEI + ", Section 3.3: 1.00/(0.350+0.028)", "recomputed: 2.646", "cost shares are design assumptions"),
    (ALL, r"2\.64× effective value of food BU", DER, "calculation", "keep", BLEI + ", Section 3.3", "recomputed: 2.646", ""),
    (ALL, r"BU: \$990 for BLEI, \$2,502 for EPPM", DER, "accounting rule", "keep", BLEI + ", Section 4.0b", "", ""),
    (ALL, r"Poverty target: <2% extreme poverty within 15 years", PAR, "target", "keep", "framework target", "", "labelled a target"),
    (ALL, r"Workweek target: 25-hour", PAR, "target", "keep", "framework target", "", "labelled a target"),
    (ALL, r"Gini coefficient target|nominal CCO target \(≤0\.25|Gini ≤ ?0\.2[25]", PAR, "target", "correct", "framework target", "", "[S5-13] the Gini measure (income or wealth, which population) is never named; the engine measures EDC-adjusted Gini 0.518 at v4.4 (C30)"),
    (ALL, r"US baseline: 0\.44–0\.46 \(EDC-adjusted\)", NONE, "fact", "remove", "", "", "EDC-adjusted Gini is the framework's own measure; no computation of the US value is published"),
    (ALL, r"Nordic reference benchmark", NONE, "fact", "correct", "", "", "plausible for Nordic income Gini, but uncited: cite a source (e.g. OECD IDD) and name the measure"),
    (ALL, r"BLEI Threshold Rate: 97%|BLEI Secure Rate: 84%", NONE, "projection", "remove", "", "", "not in the BLEI paper and produced by no published run"),
    (ALL, r"~33 months \(sensitivity range: 28–47|~?33 months|approximately 33 months|month 33|Month 33", NONE, "calculation", "correct", "", "", "[S5-11] no derivation of ~33 months or the 28-47 range is published; 730+ days at month 33 depends on an unstated saving rate (S5-10, C27-C28)", r"33|28–47|1\.50|3\.00|730"),
    (ALL, r"18\.3 days", DER, "calculation", "keep", BLEI + ", Appendix B.1: $1,249.96 / $68.33", "s5_checks.py: reproduces", "[S5-08]", r"18\.3"),
    (ALL, r"71\.3 days", DER, "calculation", "correct", BLEI + ", Appendix B.2", "s5_checks.py: the paper's own inputs give 70.7", "[S5-09] restate as 70.7 (C27)", r"71\.3"),
    (ALL, r"\$22,800|\$59,900", NONE, "estimate", "relabel", "", "", "IPBI channel values (crime, health, productivity, property, market) are stated, not derived from cited elasticities; label as an illustrative projection", r"22,800|59,900"),
    (ALL, r"under the baseline, they never approach it|Near-poverty participants reach this threshold", NONE, "calculation", "correct", "", "", "[S5-10] see ~33 months"),
    (ALL, r"cooperative overhead reduction underlying ε ≥ 2\.0×|ε ≥ 2\.0×", PAR, "design condition", "keep", BLEI + ", Section 3", "", ""),
    (ALL, r"community land trusts across 46 US states", EXT, "fact", "keep", "National CLT Network (2023), cited in the BLEI paper", "cited, not opened", ""),

    # ---- research-summary paper blurbs
    (r"^research-summary\.html$", r"\$1\.5 trillion in prohibition costs", NONE, "finding", "remove", "", "", "[S5-01] matches none of the drug-policy paper's totals (C23)", r"1\.5"),
    (r"^research-summary\.html$", r"\$847 billion in potential savings over 25", NONE, "finding", "remove", "", "", "[S5-02] one line of one scenario, not the net (C23)"),
    (r"^research-summary\.html$", r"15–20% market penetration within a decade", NONE, "simulation result", "correct", "", "", "[S5-03] contradicted by the real-estate paper's own rollout table (C24)", r"15–20"),
    (r"^research-summary\.html$", r"average household wealth accumulation of \$70,000", ILL, "simulation result", "correct", "us-real-estate-transformation 4.3 (20-year figure; no model published)", "", "[S5-04] say it is a 20-year illustrative figure (C24)", r"70,000"),
    (r"^research-summary\.html$", r"poverty reduction below 5% within 15 years", NONE, "finding", "remove", "", "", "B053: with the paper's p* = 11.8% the rate never reaches 5% (recompute.py)", r"5%|15"),
    (r"^research-summary\.html$", r"ROI of \$1,847", NONE, "finding", "remove", "", "", "[S5-05] an NPV, not an ROI, and the paper's formula gives $2,046 (C25, B097)", r"1,847"),
    (r"^research-summary\.html$", r"\$85,000 in interest savings", NONE, "finding", "remove", "", "", "[S5-06] not reproducible: with the table's payments the avalanche saves about $900 (C26, B005)", r"85,000"),
    (r"^research-summary\.html$", r"sustainability demonstrated at just 30–40", PAR, "finding", "relabel", "PTH financing paper 6.1 break-even table (assumed)", "", "[S5-07] an assumed break-even table, not a demonstration (C26)", r"30–40"),
    (r"^research-summary\.html$", r"25-hour workweeks with CCO supplementation maintain productivity while reducing overhead 35–50%", NONE, "finding", "relabel", "", "", "'key findings' with no run or source behind them; 25 hours is a design target"),

    # ---- papers/index.html blurbs (same claims as the research summary; B-ids from S29)
    (r"^papers/index\.html$", r"Symmetrical Geometric Construction ¦", PAR, "emblem geometry", "keep", "site emblem", "", "geometry of the site's emblem, not a research figure"),
    (r"^papers/index\.html$", r"\$1\.5 trillion in prohibition costs", NONE, "finding", "remove", "", "", "matches none of the drug-policy paper's totals; $847B is one line of one scenario (C23, B003)"),
    (r"^papers/index\.html$", r"15-20% market penetration within a decade", NONE, "simulation result", "correct", "", "", "contradicted by the real-estate paper's own rollout table (C24)", r"15-20"),
    (r"^papers/index\.html$", r"\$70,000 average wealth accumulation", ILL, "simulation result", "correct", "us-real-estate-transformation 4.3 (20-year figure; no model published)", "", "say it is a 20-year illustrative figure (C24, B066)", r"70,000"),
    (r"^papers/index\.html$", r"poverty reduction below 5% within 15 years", NONE, "finding", "remove", "", "", "B053: with the paper's p* = 11.8% the rate never reaches 5% (recompute.py)"),
    (r"^papers/index\.html$", r"ROI of \$1,847", NONE, "finding", "remove", "", "", "an NPV, not an ROI; the paper's formula gives $2,046 (C25, B097)"),
    (r"^papers/index\.html$", r"\$85,000 in interest savings", NONE, "finding", "remove", "", "", "with the table's payments the avalanche saves about $900 (C26, B005)"),
    (r"^papers/index\.html$", r"sustainability with just 30-40 pay-in", PAR, "finding", "relabel", "PTH financing paper 6.1 break-even table (assumed)", "", "an assumed break-even table, not a demonstration (C26, B116)"),
    (r"^papers/index\.html$", r"pilot programs \(\$50B\) to revolutionary transformation \(\$500B\)", PAR, "scenario sizes", "keep", "PTH government-integration paper's scenarios", "", ""),
    (r"^papers/index\.html$", r"demonstrating 50% market penetration achievable within 5-19", NONE, "simulation result", "relabel", "", "", "'demonstrating': no run is published; an illustrative projection"),
    (r"^papers/index\.html$", r"25-hour workweeks with CCO supplementation maintain productivity", NONE, "finding", "relabel", "", "", "'key findings' with no run or source; 25 hours is a design target"),
    (r"^papers/index\.html$", r"personal multiplier rates \(1x to 14x\+\)|CCO basic units enable 25-hour|PTF workers receive 50% conversion bonus|Phi rate \(1\.618x\)", PAR, "specification", "keep", "the framework's design", "", ""),

    # ---- the simulation claim that recurs across the Hub (S30)
    (ALL, r"10,000\+? (?:Monte Carlo )?(?:simulation )?iterations|98% poverty elimination|validation_iterations|achieving 98% poverty", NONE, "simulation result", "remove", "", "", "no published run of 10,000 iterations or of a 98% figure; S30 checks pre-v5 engines and printed code", r"10,000|98%"),

    # ---- wiki/index.html
    (r"^wiki/index\.html$", r"Key Terms Defined|FAQ Answers|Research Papers|22\+ research papers|17 hosted", META, "page counts", "keep", "the wiki and Hub themselves", "", "16+ here vs 17 elsewhere: make the counts agree"),
    (r"^wiki/index\.html$", r"same 500 simulated adults|500 paired runs", PAR, "simulation design", "keep", "Compassionism Simulation (engine settings)", "", "describes the engine's run size, not a result"),
    (r"^wiki/index\.html$", r"PTF venues reduce Creative Collective overhead by 40–60%", PAR, "design target", "relabel", "framework design target (see front page)", "", "stated as an effect; the front page calls it a design target"),

    # ---- wiki/faq.html and wiki/glossary.html
    (r"^wiki/(faq|glossary)\.html$", r"expire after 35 days|35-day expiry|expiring after 35 days|expire 35 days", PAR, "specification", "keep", "the framework's design (BU expiry)", "", ""),
    (r"^wiki/(faq|glossary)\.html$", r"marginal tax rates (?:above|exceeding) 100%", NONE, "fact", "correct", "", "", "true for some benefit cliffs but uncited: cite a source (e.g. CBO or Urban Institute studies of effective marginal tax rates)"),
    (r"^wiki/faq\.html$", r"Personal Multiplier Rate|How Assessment Works|elevated conversion rates of 2×–4×|may qualify for a 3× conversion|Diverse Contribution Recognition|personal multiplier rates \(1× to 14×", PAR, "specification", "keep", "the framework's design (conversion tiers)", "", ""),
    (r"^wiki/faq\.html$", r"Example: A PTF restaurant", ILL, "example", "keep", "the page presents it as an example", "", ""),
    (r"^wiki/faq\.html$", r"^Phase \d: .*months\) ¦|Year 1–2:|Year 2–3:|Year 3–5:", PAR, "plan", "keep", "the framework's implementation plan", "", "planned durations, not forecasts"),
    (r"^wiki/faq\.html$", r"Assumed preconditions include", ILL, "scenario assumption", "keep", "the page calls it a best-case scenario", "", ""),
    (r"^wiki/glossary\.html$", r"Maria receives|Lisa has|When she converts 1,000|Marcus, at Octave 3|Northside Creative Collective|Greendale Commons|Kim's groundbreaking|community educator who consistently teaches|In a traditional means-tested system, Sarah", ILL, "example", "keep", "the glossary's worked examples", "", "fictional examples"),
    (r"^wiki/glossary\.html$", r"Portland Metro SZH coordinates 15", ILL, "example", "relabel", "the glossary's worked examples", "", "reads as a real Portland body; mark it as hypothetical"),
    (r"^wiki/glossary\.html$", r"Octave 1 allows 1,000|multipliers ranging from 1× to 14×|7×–9×\+ \(exquisite|baseline 1× \(productive\)|would yield 1×|minimum of 50 members|50-member minimum|appeal within 30 days", PAR, "specification", "keep", "the framework's design", "", ""),

    # ---- implementation roadmaps (wiki) and the international guide
    (r"^wiki/(implementation-roadmap|international-adaptation-guide)\.html$", r"Success Metrics ¦", PAR, "target", "keep", "a success metric (target) set by the plan", "", "targets, not forecasts; no run or source supports reaching them"),
    (r"^wiki/(implementation-roadmap|international-adaptation-guide)\.html$", r"Funding: \$|Staff: \d", NONE, "cost estimate", "relabel", "", "", "cost and staffing estimates with no derivation: label as rough planning assumptions"),
    (r"^wiki/(implementation-roadmap|international-adaptation-guide)\.html$", r"Months? \d|Key Milestones|Primary Objectives ¦|Communities: |Participants: |Select 3-5 villages|Phase \d", PAR, "plan", "keep", "the implementation plan", "", "planned scale and timing, not forecasts"),
    (r"^wiki/international-adaptation-guide\.html$", r"Parameter Adjustments ¦|Emergency Parameters ¦", PAR, "specification", "keep", "the framework's design, adapted by context", "", ""),

    # ---- referendum.html (proposed legal text)
    (r"^referendum\.html$", r"political spending increasing by over 360%", NONE, "fact", "correct", "", "", "uncited: cite a source (e.g. OpenSecrets) and the decade meant, or remove"),
    (r"^referendum\.html$", r".", PAR, "proposed rule", "keep", "the referendum's proposed text", "", "thresholds, deadlines and sizes the proposal sets"),

    # ---- 404, satire, notes, downloads README
    (r"^404\.html$", r"404", META, "error code", "keep", "the page itself", "", ""),
    (r"^404\.html$", r"14 open-access research papers", META, "count of papers", "correct", "the Hub's paper list", "", "stale: the Hub lists 17+"),
    (r"^research-summary\.md$", r"14 peer-reviewable papers", META, "count of papers", "correct", "the Hub's paper list", "", "stale Markdown copy: the HTML says 17+"),
    (r"^comedy\.(md|html)$", r".", META, "satire", "keep", "the satire page", "", "jokes, not research claims"),
    (r"^new-frame-and-lens\.(md|html)$", r"LEFT: 1-3|RIGHT: 1-3|HEAD: 1-4|5 categories × 3 topics|UPDATED", META, "page format", "keep", "the page itself", "", ""),
    (r"^assets/downloads/README\.md$", r"Python:|RAM:|OS:", META, "software requirements", "remove", "assets/downloads/README.md", "", "describes a download package that is not in the repository"),
    (r"^assets/downloads/README\.md$", r".", NONE, "simulation package", "remove", "", "", "the zip files and '10,000 Monte Carlo results' it lists are not in the repository"),

    # ---- cco-ptf-simulation/README.md (describes the current engine)
    (r"^cco-ptf-simulation/README\.md$", r"500 simulated adults|500 paired runs", PAR, "simulation design", "keep", "Compassionism Simulation (engine settings)", "", "run size, not a result"),

    # ---- data/optimal-parameters.json (S30 item 4 checks each value against code)
    (r"optimal-parameters\.json$", r"^simulation_metadata\.(version|last_updated)|^citation\.|^technical_specifications\.", META, "file metadata", "keep", "the file itself", "", "the Python package it names is not on the Hub"),
    (r"optimal-parameters\.json$", r"validation_confidence|confidence_level|confidence_interval|^validation_benchmarks\.|validation_iterations", NONE, "validation result", "remove", "", "", "no validation run, sensitivity test or cross-validation is published"),
    (r"optimal-parameters\.json$", r"^simulation_metadata\.description|^system_outcomes\.", NONE, "simulation result", "remove", "", "", "outcomes stored as parameters; no run produced them (S30)"),
    (r"optimal-parameters\.json$", r"median_wealth_accumulation", NONE, "simulation result", "correct", "", "", "$82,000 sits among the inputs but the papers report it as a result with an interval (B093; S30 item 4)"),
    (r"optimal-parameters\.json$", r"participation_rate\.value|peer_review_accuracy\.value|governance_efficiency\.value|uptake_rate\.value|break_even_threshold|_size\.optimal", PAR, "optimal value", "relabel", "the file lists it as an 'optimal parameter'", "", "a behavioural or design assumption; no optimisation is published (B022), so call it an assumption"),
    (r"optimal-parameters\.json$", r".", PAR, "model input", "keep", "data/optimal-parameters.json", "", "design or environment parameter"),

    # ---- BLEI paper (HTML and PDF)
    (r"basic-living-economic-index", r"3\.9× improvement|3\.9×$|\| 3\.9×", DER, "calculation", "correct", BLEI + ", Section 7.1: 71.3/18.3", "recomputed: 3.9 (3.86 with the corrected 70.7)", "follows S5-09", r"3\.9"),
    (r"basic-living-economic-index", r"16\.6×|303 days", DER, "calculation", "correct", BLEI + ", Section 7.1 table", "not recomputed: the month-12 inputs (savings, AE) are not all stated", "show the month-12 derivation (cf. S5-10)", r"16\.6|303|12"),
    (r"basic-living-economic-index", r"Month 60.*1,328|72\.6×|~392 days|1,675", NONE, "calculation", "correct", "", "", "month-60 BLEI depends on a saving rate the paper does not state (as S5-10)"),
    (r"basic-living-economic-index", r"Flourishing tier \(730 days\) is reached between 40 and 55 months", NONE, "calculation", "correct", "", "", "conflicts with '~33 months, range 28-47' in the abstract and summaries; no derivation of either (S5-11)"),
    (r"basic-living-economic-index", r"BLEI scores remain above Tier 2 Threshold|above the Tier 2 Threshold \(30 days\) for CCO-PTF participants across all tested|All combinations maintain BLEI ≥ Tier 2|maintain BLEI above 35 days|still produces Tier 3–4|remain above Threshold tier|BLEI outcomes remain above the Threshold", DER, "sensitivity", "keep", BLEI + ", Section 5 Table 2", "not recomputed", ""),
    (r"basic-living-economic-index", r"^5\. Sensitivity Analysis ¦ \|", DER, "sensitivity", "correct", BLEI + ", Section 5 Table 2", "not recomputed", "the base value 71.3 should be 70.7 (S5-09); month-12 column needs its inputs stated"),
    (r"basic-living-economic-index", r"^5\. Sensitivity Analysis ¦|BLEI sensitivity analysis — Profile A", DER, "sensitivity", "keep", BLEI + ", Section 5", "not recomputed", ""),
    (r"basic-living-economic-index", r"62–68% of gross income to rent", EXT, "fact", "keep", "cited [9] in the BLEI paper", "cited, not opened", ""),
    (r"basic-living-economic-index", r"70% lower foreclosure", EXT, "fact", "keep", "cited [22] in the BLEI paper", "cited, not opened", ""),
    (r"basic-living-economic-index", r"Burlington Community Land Trust \(founded 1984\)", NONE, "fact", "correct", "", "", "plausible but uncited: cite a source for the 25-30% vs 40-50% shares"),
    (r"basic-living-economic-index", r"r_a values of 2–5% as consistent", PAR, "model coefficient", "keep", BLEI, "", ""),
    (r"basic-living-economic-index", r"Conventional food retail prices embed", NONE, "fact", "correct", "", "", "retail cost shares stated without a source; cite one (they set ε)"),
    (r"basic-living-economic-index", r"PTF prices are set to cover direct costs|Early-phase ε 1\.50–2\.00|Early-phase PTF operations may achieve|ε values of 2\.5–3\.0×|ε values closer to 1\.5–2\.0×", PAR, "model coefficient", "keep", BLEI + ", Section 3.3", "", "design assumptions behind ε"),
    (r"basic-living-economic-index", r"Base-case denominator 37\.8%|reduce overhead by 40–55%|gross margins 30–45% below", EXT, "fact", "keep", "Whyte & Whyte (1991), cited in the BLEI paper", "cited, not opened", ""),
    (r"basic-living-economic-index", r"PTF breakfast priced at 3 Basic Units", PAR, "specification", "keep", "the framework's design (PTF prices)", "", "market prices of meals are illustrative"),
    (r"basic-living-economic-index", r"ε_util = 1\.80×|ε_util", PAR, "model coefficient", "keep", BLEI, "", ""),
    (r"basic-living-economic-index", r"Alaska Permanent Fund Dividend \(APF\) distributes|Over 40 years of operation, the APF", EXT, "fact", "keep", "Alaska Permanent Fund Dividend records (cited section 3.1)", "cited, not opened", ""),
    (r"basic-living-economic-index", r"approximately 7× the APF annual dividend", DER, "calculation", "keep", "$1,200 × 12 / $2,072", "recomputed: 6.95", ""),
    (r"basic-living-economic-index", r"Monthly income: \$6,215 \(\$74,580/year, Census 2023\)", EXT, "fact", "correct", "US Census Bureau, Income in the United States: 2022 (released Sept 2023)", "not opened: $74,580 is the 2022 median household income; the 2023 median is $80,610", "label the year as 2022, or update", r"6,215|74,580"),
    (r"basic-living-economic-index", r"^7\.\d Profile|Profile A|Profile B|Monthly income: \$2,083|Liquid savings|Homeowner, 30-year mortgage|Year-1 interest|Annual income: \$200,000|Appendix B: Worked Numerical Example ¦ The following", ILL, "stylized household", "keep", BLEI + ", Section 7 profiles", "", "stylized inputs; outputs are derived from them", r"^\$?2,083$|1,000$|1,300|30$|7%|420K|1,960|30,000|200,000|\$600$|4%|\$0$|−\$700|\$400|360|720|\$717|\$2,236|100%"),
    (r"basic-living-economic-index", r"^7\.\d Profile|Profile B|EPPM \| 1\.00× \| 2\.79×", DER, "calculation", "keep", BLEI + ", Section 7", "not recomputed", "from the stylized profile"),
    (r"basic-living-economic-index", r"^7\.3 Profile C|Total annual IPBI|Health insurance premium reduction|Property value appreciation|Labor productivity gain|Market expansion|Crime reduction \(security", NONE, "estimate", "relabel", "", "", "IPBI channel values: cited sources give context, but the per-household values are not derived from them; label as an illustrative projection"),
    (r"basic-living-economic-index", r"Anderson \(1999\) estimated total US crime costs", EXT, "fact", "keep", "Anderson (1999), cited [6]", "cited, not opened", "", r"1\.0T"),
    (r"basic-living-economic-index", r"^Index VI|treating CR and PV as independent likely overstates", NONE, "estimate", "relabel", "", "", "IPBI channel values are not derived from the cited sources; label as an illustrative projection"),
    (r"basic-living-economic-index", r"^Index V — Compound|r_wealth under|compounded at r_a/12", PAR, "model coefficient", "keep", BLEI + ", Index V", "", "assumed return ranges"),
    (r"basic-living-economic-index", r"Month \d+[–-]\d+ \| 0\.\d+|Month 60\+ \| 0\.8|Calibrated against CLT early-exit|h_AE = 0\.60 for medium-term|Sensitivity tests across h_AE|Haircut tiers are calibrated", PAR, "model coefficient", "keep", BLEI + ", Table 1a (h_AE schedule)", "", "set against CLT exit data; not estimated"),
    (r"basic-living-economic-index", r"^BLEI Temporal Stability Tiers|^\d+[–-]\d+ days$|One disruption from crisis|Flourishing tier threshold of 730|>730-day tier|730-day threshold", PAR, "specification", "keep", BLEI + ", tier table", "", ""),
    (r"basic-living-economic-index", r"^Index II|Rent_full: full rental", DER, "calculation", "keep", BLEI + ", Index II", "recomputed: $2,083 × 0.625 × 12 = 15,623", ""),
    (r"basic-living-economic-index", r"^Index III|EPPM = 1\.00 in the absence", DER, "calculation", "keep", BLEI + ", Index III", "recomputed: 5.80", ""),
    (r"basic-living-economic-index", r"^Index IV|^4\.0b|FBS = max|C_basic_cash_monthly|EDC_residual", DER, "calculation", "keep", BLEI + ", Index IV", "recomputed: $2,280.92", ""),
    (r"basic-living-economic-index", r"λ ~ U\(0\.0001654|operational calibration|8× relative heterogeneity", PAR, "engine calibration", "keep", "Compassionism Simulation v4.4 (engine constant)", "", ""),
    (r"basic-living-economic-index", r"^Index I —|C_basic = daily cost|AE\(n\) = H", DER, "calculation", "keep", BLEI + ", Index I", "recomputed: $68.33, $31.67", ""),
    (r"basic-living-economic-index", r"Below approximately 40% PTF merchant participation", PAR, "model assumption", "relabel", BLEI + ", Section 6.1", "", "an assumption, not an estimate; it also differs from the engine's 55% density gate"),
    (r"basic-living-economic-index", r"self-funding threshold of approximately 60–65%|estimates 60–65% participation", NONE, "analysis result", "relabel", "", "", "'preliminary analysis' is not published; participation thresholds are settled from runs in S5"),
    (r"basic-living-economic-index", r"limit non-essential market inflation to below 1\.5%", NONE, "analysis result", "relabel", "", "", "'preliminary analysis' is not published"),
    (r"basic-living-economic-index", r"12% conversion tax|Below approximately 60% CCO participation|PTF market share target of 18%", PAR, "specification", "keep", "the framework's design", "", ""),
    (r"basic-living-economic-index", r"seed 42, 20 years|20-year simulation horizon|flat 50% rather than", PAR, "engine setting", "keep", "Compassionism Simulation v4.4 (engine settings)", "", ""),
    (r"basic-living-economic-index", r"N=5,000 large-N study|Gini at 0\.518|Baseline's own 0\.858", SIM, "simulation result", "correct", "Compassionism Simulation v4.4, Full Integration preset, N=5,000", "release cited; no command, seeds or results file", "rerun on the release with a recorded command (S40)"),
    (r"basic-living-economic-index", r"CFG\.TARGET_GINI|previously cited 0\.22", PAR, "target", "keep", "engine constant CFG.TARGET_GINI", "", ""),
    (r"basic-living-economic-index", r"Nordic post-redistribution Gini range", NONE, "fact", "correct", "", "", "plausible but uncited: cite a source and name the measure"),
    (r"basic-living-economic-index", r"^9\.1 On|^9\. Discussion|^8\. Simulation Parameter|^Appendix A", PAR, "specification", "keep", BLEI, "", ""),
    (r"basic-living-economic-index", r"70\.7 ≈ 71\.3", DER, "calculation", "correct", BLEI + ", Appendix B.2", "recomputed: 70.7", "[S5-09] 70.7 is not 71.3 by rounding (C27)", r"70\.7|71\.3"),
    (r"basic-living-economic-index", r"= 0\.744|EDC ≈ 0\.625 at the lower end", DER, "calculation", "correct", BLEI + ", Appendix B.3", "recomputed: 0.744 by the paper's own definition", "the worked example computes 0.744 (rent + debt interest) but uses 0.625 (rent only) everywhere else"),
    (r"basic-living-economic-index", r"^Appendix B", DER, "calculation", "keep", BLEI + ", Appendix B", "recomputed", ""),
    (r"basic-living-economic-index", r"Lusardi|Jones and Marinescu|Mullainathan|Davis and Demetrowitz|National CLT Network|Mondragon comprises", EXT, "fact", "keep", "cited in the BLEI paper", "cited, not opened", ""),
    (r"basic-living-economic-index", r"\$3,400\+/month|2\.4× further|\$104 to \$43", DER, "calculation", "keep", BLEI + ", Section 7.2", "not recomputed", "from the stylized profile"),
    (r"basic-living-economic-index", r"shareholder return and profit extraction at|conventional overhead including marketing", NONE, "fact", "correct", "", "", "retail cost shares stated without a source; cite one (they set ε)"),
    (r"basic-living-economic-index", r"ε = Market price / PTF price|ε = 2\.64 base case|2\.64× face value", DER, "calculation", "keep", BLEI + ", Section 3.3", "recomputed: 2.22, 2.65, 2.94", "cost shares are design assumptions"),
    (ALL, r"Johnson, D\.|Johnson, Duke|Duke Johnson", META, "authorship", "keep", "the page itself", "", ""),
    (r"basic-living-economic-index\.pdf$", r"Mincome", EXT, "fact", "keep", "Forget (2011), cited in the BLEI paper", "cited, not opened", "", r"^$"),
    (r"basic-living-economic-index\.pdf$", r".", DER, "table fragment", "keep", BLEI + " (PDF)", "", "a fragment of a figure classed on the HTML page"),

    # ---- economic-modeling-simulation (HTML and PDF). Nearly every result here is stated as the output of
    # "10,000+ simulation iterations" or an agent-based model; no run, code release or results file exists (S30).
    (r"economic-modeling-simulation", r"^Economic Modeling and Simulation Analysi.*Date:|Date: August", META, "date", "keep", "the page itself", "", ""),
    (r"economic-modeling-simulation", r"^4\.1 Parameter Uncertainty|~ (?:Beta|Normal|Uniform)", PAR, "simulation input", "keep", "the paper's parameter distributions (Section 4.1)", "", "inputs of a simulation that is not published; S30 runs the printed code"),
    (r"economic-modeling-simulation", r"^A\.\d|random\.uniform|n_iterations|def |self\.", PAR, "simulation input", "keep", "the paper's printed code (Appendix A)", "", "S30 runs this code as printed"),
    (r"economic-modeling-simulation", r"^B\.2 Behavioral Parameter|Blundell|Aiyagari|Duflo|\(2013\) \| 0\.08", EXT, "calibration", "keep", "sources named in Appendix B.2", "cited, not opened", "whether the values match the sources is unchecked; the 95% intervals are not from those sources"),
    (r"economic-modeling-simulation", r"below 60% median income", EXT, "definition", "keep", "OECD/EU relative-poverty line convention", "standard definition", ""),
    (r"economic-modeling-simulation", r"below \$2/day PPP", EXT, "definition", "correct", "World Bank extreme-poverty line", "standard definition", "the line has been $2.15/day (2017 PPP) since 2022, $3.00 (2021 PPP) since 2025"),
    (r"economic-modeling-simulation", r"across 20-year projections|^C\.1 |Higher basic amounts|Lower basic amounts", PAR, "simulation design", "keep", "the paper's design", "", ""),
    (r"economic-modeling-simulation", r"Recession Scenario \(GDP -8%|Inflation Surge \(CPI \+6%|Unemployment Shock \(joblessness to 12%", ILL, "scenario definition", "keep", "the paper's stress scenarios", "", ""),
    (r"economic-modeling-simulation", r"\| Parameter \| Base Value \| Low \(-25%\)", PAR, "sensitivity design", "keep", "Section 5.4 table header", "", ""),
    (r"economic-modeling-simulation", r"gbase = 0\.015|gCCO = 0\.008|gPTF = 0\.005", PAR, "model coefficient", "relabel", "Section 8.1", "", "assumed components, presented as model estimates"),
    (r"economic-modeling-simulation", r"Total productivity growth: 2\.8% annually", DER, "calculation", "relabel", "Section 8.1: 0.015 + 0.008 + 0.005", "recomputed: 2.8%", "B071: the sum of assumed components, presented as a model result; label it as an assumption", r"2\.8%"),
    (r"economic-modeling-simulation", r"Total productivity growth: 2\.8% annually", EXT, "fact", "correct", "", "", "1.5% baseline productivity growth: plausible, uncited", r"1\.5%"),
    (r"economic-modeling-simulation", r"Target: \d|Target: All U\.S\. adults|^10\.1 Phased Rollout.*Phase \d: .*\(Years", PAR, "plan", "keep", "the paper's rollout plan", "", "planned scale and timing"),
    (r"economic-modeling-simulation", r"Universal UBI \(\$1200/mo\)", DER, "calculation", "keep", "$1,200 × 12 × about 258M adults", "recomputed: about $3.7T", "", r"1200|3\.7T"),
    (r"economic-modeling-simulation", r"\| Current System \| 11%", NONE, "fact", "correct", "", "", "11% matches the 2023 official poverty rate (11.1%) but is uncited; $1.2T has no source", r"11%"),
    (r"economic-modeling-simulation", r"\| (?:US Current Trajectory|Nordic Model|Singapore Model|China Model|Expanded EITC|Job Guarantee|Current System)", NONE, "fact or projection", "remove", "", "", "comparison figures with no source; the projected columns have no model"),
    (r"economic-modeling-simulation", r"\(r=0\.\d+\)", NONE, "simulation result", "remove", "", "", "correlations with no data or run"),
    (r"economic-modeling-simulation", r"\$37,000|\$82,000|85% poverty reduction|98% poverty reduction", NONE, "simulation result", "remove", "", "", "S30 headline: median wealth and poverty reduction with intervals, from no published run; replace with release results (S48, S25)"),
    (r"economic-modeling-simulation", r".", NONE, "simulation result", "remove", "", "", "stated as the output of simulations or agent-based models that are not published; S30 looks for the code; S25 replaces them with release results"),

    # ---- drug-policy-reform (HTML and PDF)
    (r"drug-policy-reform", r"Date: August", META, "date", "keep", "the page itself", "", ""),
    (r"drug-policy-reform", r"We examine 70 years|Measure 110|^4\.1 Cumulative Prohibition Costs \(1953-2024\) ¦ 4\.1", META, "scope or name", "keep", "the page itself", "", ""),
    (r"drug-policy-reform", r"\$1\.5 trillion|\$1\.52 trillion", NONE, "finding", "correct", "", "", "B009: the paper's own table sums to $4,616B; no source for either total (C23)"),
    (r"drug-policy-reform", r"\$847 ?(?:billion|B)", NONE, "finding", "remove", "", "", "B003/B018: one line of one scenario, presented as the net (C23)"),
    (r"drug-policy-reform", r"Hart \(2013\)|Miron and Waldock \(2010\)", EXT, "fact", "keep", "Hart (2013); Miron & Waldock (2010), cited", "cited, not opened", ""),
    (r"drug-policy-reform", r"Greenwald \(2009\) documented|deaths fell by 95%", EXT, "fact", "correct", "Greenwald (2009, Cato); ONDCP critique (ojp.gov/pdffiles1/ondcp/Portugal.pdf)", "opened: ONDCP critique (Greenwald's PDF could not be fetched)", "B028: the critique, quoting Greenwald's sources, gives drug-induced deaths of 369 (1999), 280 (2001), 152 (2003), 314 (2007); nothing supports 'fell by 95%' or 'crime dropped by 50%'"),
    (r"drug-policy-reform", r"^5\.1 Portugal Model|Drug-related deaths: 369|20-Year Outcomes \(2001-2021\)", EXT, "fact", "correct", "uncited; ONDCP critique (ojp.gov/pdffiles1/ondcp/Portugal.pdf) for the deaths series", "opened: ONDCP critique", "369 is the 1999 count, not the 2001 baseline (280); deaths rose again to 314 by 2007; the '27' and the other rows have no source"),
    (r"drug-policy-reform", r"Switzerland's heroin-assisted treatment programs showed 60%", EXT, "fact", "keep", "Swiss heroin-assisted treatment evaluations (named, not cited)", "cited, not opened", ""),
    (r"drug-policy-reform", r"Overdose Deaths: 107,543", EXT, "fact", "correct", "CDC provisional overdose counts", "not opened: 107,543 is CDC's provisional count for 2023 (May 2024 release), not 2024", "fix the year", r"107,543"),
    (r"drug-policy-reform", r"\$7 saved per \$1 spent \(CDC 2024\)", EXT, "fact", "keep", "CDC (2024), cited", "cited, not opened", "", r"^\$7$|^\$1$"),
    (r"drug-policy-reform", r"^4\.2 Human Impact|^5\.2 Netherlands|^5\.3 Switzerland|^5\.4 Lessons|^A\.1 Comprehensive Country|^A\.2 Policy Timeline", NONE, "fact", "correct", "", "", "real-world figures with no citation: cite a source for each or remove"),
    (r"drug-policy-reform", r"^4\.3 Enforcement Effectiveness|^4\.1 Cumulative Prohibition", NONE, "fact", "remove", "", "", "tables with no source (B009 for the totals)"),
    (r"drug-policy-reform", r"Phi multiplier \(1\.618x\)", PAR, "specification", "keep", "the framework's design", "", ""),
    (r"drug-policy-reform", r"^8\.1 Phased Implementation|Pilot programs in 3-5|Expansion to 25 jurisdictions|^B\.3 Community Engagement", PAR, "plan", "keep", "the paper's implementation plan", "", ""),
    (r"drug-policy-reform", r"100,000 preventable deaths|500,000 unnecessary", NONE, "fact", "remove", "", "", "B084: not in the body and uncited"),
    (r"drug-policy-reform", r".", NONE, "projection", "remove", "", "", "25-year costs, savings, net values, break-even and ROI with no model or valuation published (B044, B008)"),

    # ---- pth-independent-financing (HTML and PDF)
    (r"pth-independent-financing", r"Date: September", META, "date", "keep", "the page itself", "", ""),
    (r"pth-independent-financing", r"Pool all payments: \$7,050|Freed-up \$7,050|Acre Equity accumulation: \$84,600", DER, "calculation", "keep", "Section 2.2 table: sum of payments, × 12", "recomputed", ""),
    (r"pth-independent-financing", r"^2\.2 Five-Homeowner|Target Homeowner C|Continue with Homeowner E|Then Homeowner A", ILL, "worked example", "keep", "the paper's five-homeowner example", "", "inputs of a stylized example"),
    (r"pth-independent-financing", r"\$85,000|\$68,000|Payoff time: 1\.8 years|Collective debt freedom: 10 years|40% faster|^2\.3 Implementation Strategy ¦ Phase", DER, "calculation", "correct", "the five-homeowner example (Section 2.2)", "recompute.py (S29): does not reproduce; with the table's payments the payoff takes 18.3 years and saves about $900", "[S5-06] B005, C26"),
    (r"pth-independent-financing", r"18-142 years|5-19 years|5-7x faster", NONE, "projection", "relabel", "", "", "no model of market penetration is published; the front page already calls 5-19 years illustrative"),
    (r"pth-independent-financing", r"^3\.3 Hybrid Progressive", ILL, "scenario assumption", "keep", "the paper's hybrid scenario", "", ""),
    (r"pth-independent-financing", r"philanthropic endowment scenarios from \$1 million|Endowments from \$1M to \$1B|^4\.\d .*¦ 4\.\d|: \$[\d.]+M(?: \(|$)|Platform development|Operations/reserves|Infrastructure: |Operations: |Technology platform|Regional expansion|Reserves: |10 major metro", PAR, "plan", "keep", "the paper's endowment scenarios (budget splits)", "", "chosen allocations, not estimates"),
    (r"pth-independent-financing", r"^4\.\d", NONE, "projection", "relabel", "", "", "household counts and community wealth by year with no model: label as an illustrative projection"),
    (r"pth-independent-financing", r"44 million renter", NONE, "fact", "correct", "", "", "plausible (ACS counts about 44 million renter households) but uncited"),
    (r"pth-independent-financing", r"^5\.2 Buy-In|^5\.3 Sell-In", ILL, "worked example", "keep", "the paper's pathway examples", "", ""),
    (r"pth-independent-financing", r"Net improvement: \$1,000-1,500", ILL, "worked example", "correct", "Section 5.3 example", "", "B045: the net improvement assumes a mortgage the example does not state"),
    (r"pth-independent-financing", r"\(\d+ credits\): ", PAR, "specification", "correct", "the earn-in schedule (Section 5.4)", "recompute.py: the timelines are 4-40 times slower than the stated credit rates imply", "B010"),
    (r"pth-independent-financing", r"^5\.4 Earn-In", PAR, "specification", "keep", "the earn-in schedule (Section 5.4)", "", ""),
    (r"pth-independent-financing", r"30-40 pay-in households|^6\.1 Break-Even", PAR, "assumption", "relabel", "the paper's break-even table (assumed)", "", "[S5-07] an assumed break-even table, not a demonstration (C26, B116)"),
    (r"pth-independent-financing", r"Percentage of income model", PAR, "specification", "keep", "the framework's design", "", ""),
    (r"pth-independent-financing", r"^6\.2 Revenue|^6\.3 Cost Structure", NONE, "estimate", "relabel", "", "", "revenue shares and cost savings with no source: label as planning assumptions"),
    (r"pth-independent-financing", r"^7\.\d Phase|Target 20-30 founding|Scale to 80-100|200\+ households across", PAR, "plan", "keep", "the paper's implementation plan", "", ""),
    (r"pth-independent-financing", r"5-year equity: \$57,600|Community wealth created: \$2\.88M|Acre Equity accumulation: \$960", DER, "calculation", "keep", "Section 9.1 example: $960 × 60; × 50 households", "recomputed", "the 80% equity share is an assumption"),
    (r"pth-independent-financing", r"^9\.1 Urban", ILL, "worked example", "keep", "the paper's case example", "", ""),
    (r"pth-independent-financing", r"^9\.2 Suburban", ILL, "worked example", "correct", "the paper's case example", "", "B038: inconsistent with the Section 2.2 example; the $92,000 and 10 years are not derived"),
    (r"pth-independent-financing", r"Community wealth created: \$35M|Total households served: 500\+|Average cost reduction: 45%", NONE, "projection", "relabel", "", "", "no derivation"),
    (r"pth-independent-financing", r"^9\.3 Mixed", ILL, "worked example", "keep", "the paper's case example", "", ""),
    (r"pth-independent-financing", r"Monthly savings: \$600|20-year wealth building: \$151,200|Acre Equity accumulation: \$630", DER, "calculation", "keep", "Section 5.2 example", "recomputed: 630 × 240 = 151,200 (no appreciation)", ""),
    (r"pth-independent-financing\.pdf$", r"Property portfolios for pay-in in 10 metros|Mortgage conversion programs: \$|Research and advocacy|Reserves and growth capital|Technology and systems", PAR, "plan", "keep", "the paper's endowment scenario (PDF version)", "", "", r"\$\d+M$"),
    (r"pth-independent-financing\.pdf$", r"Initial capacity|Year 5: 75,000|Year 10: 3", NONE, "projection", "relabel", "", "", "household counts with no model"),
    (r"pth-independent-financing\.pdf$", r"Monthly payment: \$800-1,400|Direct monthly payments|Acre Equity conversion: 70-80%|Required reserve fund", PAR, "specification", "keep", "the framework's design (PDF version)", "", ""),

    # ---- pth-government-integration (HTML and PDF)
    (r"pth-government-integration", r"Date: September", META, "date", "keep", "the page itself", "", ""),
    (r"pth-government-integration", r"2\.5x greater efficiency|40% cost reduction compared to standalone|Total cost reduction: 40%", DER, "calculation", "correct", "Section 5.1", "recompute.py (S29): 2.5x is the wealth-building column; with the 40% cost cut it is 4.2x; 15% + 12% + 18% gives 45%, not 40%", "B052: name the metric"),
    (r"pth-government-integration", r"\(0\.25x HUD\)|\(50x HUD\)|^3\.\d .*\(\d+x HUD|0\.25x HUD = |\$12\.5 billion to \$2\.5 trillion|x HUD = \$", PAR, "scenario sizes", "keep", "the paper's investment scenarios (multiples of HUD's budget)", "", ""),
    (r"pth-government-integration", r"HUD\)? spends approximately \$50 billion|current HUD programs that spend \$50 billion|^2\.1 HUD Budget|Waiting lists|Administrative overhead: 15-20%|\$470 billion over 10 years", NONE, "fact", "correct", "", "", "HUD budget figures with no citation; the lines sum to exactly $50.0B, which HUD's budget does not: cite the FY2024 budget tables"),
    (r"pth-government-integration", r"Average assistance: \$10,638|\| Traditional HUD \| \$10,638", DER, "calculation", "keep", "$50B / 4.7M households", "recomputed: 10,638", "inherits the uncited inputs"),
    (r"pth-government-integration", r"Cost per household: \$50,000-83,000", DER, "calculation", "keep", "$12.5B / 250,000 and / 150,000", "recomputed", ""),
    (r"pth-government-integration", r"\$12-20B annually", NONE, "projection", "correct", "", "", "B004: 96-160% of the one-time outlay every year, with no derivation"),
    (r"pth-government-integration", r"Investment: \$|Returns: \$|Net benefit: \$|ROI: \d", DER, "calculation", "relabel", "Section 7.3 sums", "recomputed: 350 − 75 = 275, 350/75 = 4.7; 1.45T − 0.35T = 1.1T, 4.1", "the arithmetic holds; the savings and multiplier inputs are assumptions, so label the result as illustrative"),
    (r"pth-government-integration", r"^3\.\d .*¦ (?:Pay-in housing|Mortgage conversion|Technical assistance|Platform development|Research and evaluation|Direct funding|Property acquisition|Infrastructure|Operations support|Universal pay-in|Comprehensive conversion|Infrastructure development|Workforce|Innovation and research|Seed funding|\$50M average|Average \$25-50M|1,000-2,000 community trusts)", PAR, "plan", "keep", "the scenario's budget split", "", "chosen allocations"),
    (r"pth-government-integration", r"70-80% of rent converts|Initial 3-5 year support|Phi rate \(1\.618x\)", PAR, "specification", "keep", "the framework's design", "", ""),
    (r"pth-government-integration", r"^6\.\d Year .*¦ (?:Pilot programs|Programs in|\d)", PAR, "plan", "keep", "the paper's rollout plan", "", "enrolment targets"),
    (r"pth-government-integration", r"44 million", NONE, "fact", "correct", "", "", "plausible (ACS renter households) but uncited"),
    (r"pth-government-integration", r"^7\.1 Return|^7\.2 Comparative", NONE, "estimate", "relabel", "", "", "per-unit savings and multipliers with no source: cite or label as assumptions"),
    (r"pth-government-integration", r".", NONE, "projection", "relabel", "", "", "households served, wealth, jobs, savings and penetration with no model: label as illustrative projections"),

    # ---- integrated-implementation-roadmap (a plan: phases, legislation, training, specs)
    (r"integrated-implementation-roadmap", r"Public mandate through 70%", ILL, "scenario assumption", "keep", "the roadmap's stated core assumptions", "", ""),
    (r"integrated-implementation-roadmap", r"Poverty rate \(from ~12%\)|Gini coefficient \(from 0\.48\)", NONE, "fact", "correct", "", "", "US baselines, plausible (official poverty rate 11-12%; Census income Gini about 0.48) but uncited: cite and name the measure", r"12%|0\.48"),
    (r"integrated-implementation-roadmap", r"TLS 1\.3|AES-256", META, "technical standard", "keep", "the page itself", "", ""),
    (r"integrated-implementation-roadmap", r"^Projected |^Zone Distribution Projection|^Labor Market Evolution|^Innovation Metrics Projection|^Resource Optimization", NONE, "projection", "relabel", "", "", "projections with no model: label as targets or illustrative"),
    (r"integrated-implementation-roadmap", r"^Success Metrics|^Success Criteria|^Innovation Acceleration Goals|^Carbon Footprint Reduction Targets", PAR, "target", "keep", "a target set by the roadmap", "", "targets; no run or source supports reaching them"),
    (r"integrated-implementation-roadmap", r".", PAR, "plan", "keep", "the roadmap's design (phases, legislation, training, specifications)", "", ""),

    # ---- public-trust-financial (HTML and PDF)
    (r"public-trust-financial", r"Monte Carlo|10,000 scenarios|^6\.\d |median IRR of 8\.5%", NONE, "simulation result", "remove", "", "", "no simulation, code or results file is published (S30)"),
    (r"public-trust-financial", r"^2\.1 Per-Unit Economics", ILL, "cost assumption", "keep", "the paper's per-unit cost table", "", "assumed costs, uncited"),
    (r"public-trust-financial", r"^2\.2 Portfolio Scale|market penetration: \$", DER, "calculation", "correct", "Section 2.1 unit cost × an implied 37.5M units", "recomputed: consistent with $200,000 × 37.5M units × share", "the Section 4.1 table reaches 50% with $750B and 3.75M units, which contradicts $3.8 trillion here"),
    (r"public-trust-financial", r"^4\.1 Active Investment", PAR, "plan", "correct", "the paper's investment schedule", "recomputed: $200,000 per unit", "the penetration column implies 7.5M units in total, against 37.5M in Section 2.2"),
    (r"public-trust-financial", r"^4\.2 Passive|18-142|35-142|5-19 years|25-120 years faster|\$1\.2 trillion|\$250 billion over 10", NONE, "projection", "relabel", "", "", "no model of either path is published; label as illustrative"),
    (r"public-trust-financial", r"^5\.1 Typical PTH Project Capital Stack", PAR, "specification", "keep", "the paper's capital-stack design", "", ""),
    (r"public-trust-financial", r"Weighted average: 3\.2%", DER, "calculation", "correct", "Section 5.1 capital stack", "recomputed: 3.5-3.9% with the table's own rates (equity at 8-12%)", "", r"3\.2%"),
    (r"public-trust-financial", r"Weighted average: 3\.2%|30% below-market rents", NONE, "fact or estimate", "correct", "", "", "6.5% market rate uncited; 30% below-market rents not derived"),
    (r"public-trust-financial", r"^3\.\d |Market Size: \$500 billion", NONE, "estimate", "relabel", "", "", "yields and market sizes with no source: cite or label as assumptions"),
    (r"public-trust-financial", r"^7\.\d |^9\.1 10-Year Acceleration", PAR, "plan", "keep", "the paper's proposed programs and plan", "", ""),
    (r"public-trust-financial", r"^8\.1 Singapore|^8\.2 Vienna", NONE, "fact", "correct", "", "", "plausible but uncited: Singapore's homeownership rate is about 89% (HDB houses about 78% of residents); Vienna's social-housing share is usually given as 40-60%; cite sources"),
    (r"public-trust-financial", r"\$50 billion can catalyze \$200 billion", NONE, "estimate", "relabel", "", "", "a 4x leverage ratio with no derivation"),
    (r"public-trust-financial", r"can mobilize|mobilize \$250", NONE, "projection", "relabel", "", "", "no derivation"),
    (r"public-trust-financial\.pdf$", r"770,000 people experiencing homelessness", NONE, "fact", "correct", "", "", "matches HUD's 2024 point-in-time count (771,480) but is uncited"),
    (r"public-trust-financial\.pdf$", r"\$70,000|\$380,000", ILL, "simulation result", "correct", "PDF Section 6 comparison table (no model)", "", "the $70,000-over-20-years figure (B066, C24): say it is illustrative and which scenario"),
    (r"public-trust-financial\.pdf$", r"Investment Required|Property acquisition: \$|Renovation: \$|Operations: \$|Federal investment|State/local|Private/philanthropy|Leveraged financing|Scale: \d", PAR, "plan", "keep", "the PDF version's scaling plan", "", ""),
    (r"public-trust-financial\.pdf$", r"α = Equity conversion rate|ractive = 1\.0|Basic unit allocation|Work contributions|Reduced payments|Break-even typically achieved", PAR, "specification", "keep", "the PDF version's model definitions", "", ""),
    (r"public-trust-financial\.pdf$", r".", NONE, "projection", "relabel", "", "", "PDF only: outcomes with no model; the PDF is an older version of the paper"),
]

# Default class for a figure on a paper page that no rule above or generic rule matches.
PAPER_DEFAULTS = {}
