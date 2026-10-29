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
    (ALL, r"(?:1×\s?[–-]\s?9×|1× to 9×|1x-9x|1-9x|\b9× base|9× ×|Phi-rate|Phi-Rate|Φ ≈ 1\.618|~1\.618|golden ratio)", PAR, "specification", "keep", "the framework's design (conversion tiers, Phi-rate)", "", ""),

    # ---- PTF overhead, theta, PTH penetration (summary blocks)
    (ALL, r"35–55% (?:empirical )?overhead reduction|overhead (?:cost )?reductions of 35–55%", EXT, "fact", "keep", "Mondragon/Eroski: Whyte & Whyte (1991) and a 2003 study, cited in the BLEI paper", "cited, not opened", "", r"^35–55%$"),
    (ALL, r"overhead (?:reduction|reduce)\w*.{0,40}40[–-]60%|40[–-]60%.{0,60}(?:framework design target|overhead)|reduc\w+ (?:collective )?overhead (?:by an estimated )?40[–-]60%", PAR, "design target", "keep", "framework design target, set against the 35-55% Mondragon figure", "", ""),
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
]

# Default class for a figure on a paper page that no rule above or generic rule matches.
PAPER_DEFAULTS = {}
