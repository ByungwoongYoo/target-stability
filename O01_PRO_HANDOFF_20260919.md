# O01 PRO HANDOFF — claim-level novelty audit and publication GO/NO-GO

Date: 2026-09-19 (Asia/Seoul)
Working branch: `ByungwoongYoo/target-stability@o01-execution-scratch-20260919`
Current branch HEAD at handoff creation: `c3f136f4d68ab3ab73dcf394721b0202fcceae44`

## 0. Mission

Do NOT restart broad discovery and do NOT repeat already completed calculations unless a factual discrepancy is found.

Your job is now:

1. Perform a claim-level systematic novelty / prior-art audit for the current O01 result.
2. Decide whether O01 should be:
   - GO: manuscript-worthy now,
   - CONDITIONAL GO: requires one clearly specified extra analysis,
   - NO-GO: insufficient novelty/importance.
3. If GO/CONDITIONAL GO, define the strongest defensible manuscript claim set, journal tier, figure plan, and exact remaining work.
4. Explicitly distinguish:
   - verified result,
   - interpretation,
   - novelty inference,
   - speculation.
5. Do not revive the unsupported claim that 3D replication independently predicts clinical success better than 2D unless new pre-specified evidence genuinely supports it.

The target is not to force a Nature/Cell-style positive result. The target is to determine whether the already-observed reproducibility/confounding/model-validity result is itself publishable and how strong it really is.

## 1. Canonical state / read this first

Control Center project:
`publication-pipeline-2026`

Important Control Center commits, chronological:
- `3ab86a213daa85089d5df932acb69132f557a9e7` — O01 real-data cross-resource pilot
- `798db89b036e19fe32eb23c1f0d7b26b67b1658c` — adjusted clinical + exact CRC validation
- `7343f199675c110f83320c702d0d6f6cd971045e` — definitive filtered CRC validation
- `15c129fb2eeece2483afbf985393d77af72568d7` — novelty + independent PDO pharmacology
- `b5f6d92559c27a47447f8c99f1d5f452591708a5` — drug-level PDO validation

Do not create a new project for this work.

## 2. Primary scientific resources

Broad / DepMap Nature 2026:
- Neiswender et al., *A dependency map enhanced with next-generation 3D cancer models*
- DOI: https://doi.org/10.1038/s41586-026-10843-7

Sanger Nature 2026:
- Herranz-Ors et al., *A tumour-derived organoid biobank maps cancer gene dependencies*
- DOI: https://doi.org/10.1038/s41586-026-10830-y

Independent metastatic-CRC PDO pharmacology:
- Kryeziu et al., *Patient-derived organoids from metastatic colorectal cancer mirror tumor heterogeneity and predict patient survival and drug sensitivity*
- Cell Reports Medicine DOI: https://doi.org/10.1016/j.xcrm.2026.102840
- Mendeley Data v3 DOI: https://doi.org/10.17632/hr94h42xdc.3
- Data S5 was actually recovered and contains calculated DSS.

Open Targets:
- Platform release used: 26.06

## 3. Verified core numerical state

### 3.1 Initial cross-resource 3D replication
Shared Broad/Sanger gene universe:
- 15,008 genes

Using Sanger models that do NOT overlap Broad:
- Spearman rho Broad organoid mean gene effect vs Sanger mean LFC = 0.3242264827
- Pearson r = 0.5006670577
- q10 overlap = 729 / 1,501 per list
- Fisher OR = 15.5773
- q5 overlap = 422 / 751; OR = 54.3012
- q20 overlap = 1,350 / 3,002; OR = 5.12179; p = 2.09e-278

These results established real cross-resource reproducibility but did not establish 3D-specific superiority.

### 3.2 Exact lineage-matched CRC analysis
Broad paper-code definitions:
- 3D = `IsNextGen & ScreenType == "3DO"`
- 2D comparator = `IsAdherent2D` in same lineage

Exact CRC sample counts:
- Broad CRC 3D = 18 screens
- Broad CRC 2D = 67 screens
- Sanger CRC after removing Broad-overlap models = 81 models

Before published Fig5 non-common-essential filtering:
- shared genes = 16,318
- Broad CRC 3D vs Sanger CRC 3D: Spearman rho = 0.4762673
- Broad CRC 2D vs Sanger CRC 3D: Spearman rho = 0.4944996

After restricting to the Broad published Fig5 comparison universe:
- Broad Fig5 universe = 16,691 genes
- final shared filtered universe = 15,008 genes
- Broad CRC 3D vs Sanger CRC 3D:
  - Spearman rho = 0.3299897370
  - Pearson r = 0.5109250010
- Broad CRC 2D vs Sanger CRC 3D:
  - Spearman rho = 0.3531986912
  - Pearson r = 0.5181936194
- rho difference, 3D minus 2D = -0.0232089542
- gene-bootstrap 95% interval = [-0.0330344242, -0.0131187366]

Interpretation boundary:
- independent Sanger 3D agrees slightly MORE with Broad CRC 2D than with Broad CRC 3D in this matched/filtered analysis.
- This is evidence against a generic 3D-specific superiority claim.
- Do not overinterpret this as evidence that 3D is harmful or worse in all contexts.

### 3.3 Extreme-dependency reproducibility after final filtering

q5:
- two-3D overlap = 421 / 751
- OR = 53.8408
- universal 2D+both3D = 338
- 3D-specific consensus = 83
- 2D-only = 178

q10:
- two-3D overlap = 763 / 1,501
- OR = 17.8883
- universal 2D+both3D = 645
- 3D-specific consensus = 118
- 2D-only = 349

q20:
- two-3D overlap = 1,363 / 3,002
- OR = 5.2601
- universal 2D+both3D = 1,153
- 3D-specific consensus = 210
- 2D-only = 627

Interpretation boundary:
- 3D resources strongly reproduce extreme dependencies.
- Much of that reproducibility is universal, not uniquely 3D-specific.

## 4. Clinical-precedence result

Open Targets 26.06 CRC-specific clinical evidence:
- colorectal root: MONDO_0005575 plus descendants
- 88 disease IDs

q10 naive universal vs 2D-only:
- Phase II+: 36/645 = 5.58% vs 9/349 = 2.58%
  - OR = 2.2332
  - p = 0.03661
- Phase III+: 27/645 = 4.19% vs 3/349 = 0.86%
  - OR = 5.0388
  - p = 0.002901

But after adjustment for:
- continuous Broad CRC 2D dependency strength
- Open Targets common-essentiality

independent 3D-replication term:
- Phase II+: OR = 0.7414, 95% CI 0.3217–1.7085, p = 0.4824
- Phase III+: OR = 0.2370, 95% CI 0.0668–0.8413, p = 0.02592
- approval endpoint sparse / unstable

q10 3D-specific consensus vs 2D-only:
- Phase II+: 4/118 vs 9/349, OR = 1.3255, p = 0.7461
- Phase III+: 0/118 vs 3/349, p = 0.5751
- approval: 0 vs 0

Sensitivity:
- q5 and q20 do not rescue a positive independent 3D effect.

Interpretation boundary:
- naive apparent translational enrichment is strongly confounded by baseline dependency / essentiality structure.
- Do NOT claim 3D replication independently predicts clinical translation beyond 2D.

## 5. Independent mCRC PDO pharmacology — access was recovered

Previous Cloudflare blocker was solved.

Workflow:
- `.github/workflows/o01_mendeley_browser_api.yml`
- successful run: https://github.com/ByungwoongYoo/target-stability/actions/runs/35408378832

Recovered file:
- `Data S5.xlsx`
- 136,815 bytes
- 211 PDO rows x 62 columns
- 51 analyzable single-agent DSS labels after excluding combination-regimen columns

Examples:
- SN-38
- Carfilzomib
- Luminespib
- Volasertib
- AZD7762
- Trametinib
- Panobinostat
- Afatinib
- Regorafenib
- Cetuximab
- Oxaliplatin
- Sotorasib

## 6. Target-level PDO pharmacology result

Workflow:
- `.github/workflows/o01_pdo_pharmacology_validation.yml`
- successful run: https://github.com/ByungwoongYoo/target-stability/actions/runs/35408854800
- successful workflow commit: `1a35554f1c02b3f00ef85efd30d5c99c8760077e`

Mapping:
- 51 single-agent DSS labels
- 41/51 unambiguously mapped to OT drug molecules
- 35 drugs had inhibitory/antagonistic/blocking/degrading human target annotation

Primary single-target inhibitory set:
- n = 7 genes
- Broad CRC 3D vs median PDO DSS: rho = 0.5357, p = 0.2152
- Broad CRC 2D: rho = -0.0714, p = 0.8790
- Sanger CRC 3D: rho = -0.0714, p = 0.8790
- bootstrap Broad3D-minus-Broad2D delta mean = +0.5978
- 95% interval = [0.0382, 1.2549]

Important limitation:
- n=7
- only one q10 3D-specific consensus gene
- no estimable q10 class comparison
- exploratory only

Example:
- CSNK2A1 / Silmitasertib
  - median DSS 11.982
  - Broad CRC 3D dependency magnitude 0.2556
  - Broad CRC 2D 0.1301
  - Sanger CRC 3D 0.2936
- NOT a novelty claim; CK2/CSNK2A1/silmitasertib has prior CRC literature.

Secondary all-target sensitivity:
- 72 target genes
- Broad CRC 3D rho = 0.1906, p = 0.1088
- Broad CRC 2D rho = 0.1729, p = 0.1464
- Sanger CRC 3D rho = 0.0311, p = 0.7951
- Broad3D-minus-Broad2D bootstrap delta = 0.0169
- 95% interval = [-0.1294, 0.1610]

q10 mapped classes in this secondary set:
- universal = 6
- 3D-specific = 3
- 2D-only = 2
- other = 61

No robust class-level positive rescue.

## 7. Drug-level PDO validation — preferred pharmacology summary

This analysis was added specifically to reduce target-level pseudo-replication.

Workflow:
- `.github/workflows/o01_pdo_drug_level_validation.yml`
- commit: `c3f136f4d68ab3ab73dcf394721b0202fcceae44`
- successful run: https://github.com/ByungwoongYoo/target-stability/actions/runs/35409997973

26 inhibitory drugs had at least one target retained in the filtered dependency universe.

### All 26 mapped inhibitory drugs

Using strongest targeted dependency per drug:
- Broad CRC 3D vs median PDO DSS:
  - rho = 0.4200791
  - p = 0.03263
- Broad CRC 2D:
  - rho = 0.2947730
  - p = 0.14378
- Sanger CRC 3D:
  - rho = 0.3176291
  - p = 0.11383
- Broad3D-minus-Broad2D rho delta = +0.1253061
- bootstrap 95% interval = [-0.08612, +0.36223]
- leave-one-drug-out delta range = +0.05854 to +0.16221

Using median dependency across mapped targets per drug:
- Broad CRC 3D rho = 0.2428916, p = 0.23185
- Broad CRC 2D rho = 0.1959577, p = 0.33736
- Sanger CRC 3D rho = -0.0236423, p = 0.90873
- Broad3D-minus-Broad2D delta = +0.0469339
- bootstrap 95% interval = [-0.17130, +0.26653]

### Sensitivity: drugs with <=3 mapped targets, n=21

Strongest-target:
- Broad 3D rho = 0.3417029, p = 0.12951
- Broad 2D rho = 0.2993161, p = 0.18747
- Sanger 3D rho = 0.2484519, p = 0.27749
- 3D-minus-2D bootstrap CI includes zero

Median-target:
- Broad 3D rho = 0.4954385, p = 0.02238
- Broad 2D rho = 0.3174717, p = 0.16081
- Sanger 3D rho = 0.1851375, p = 0.42172
- delta = +0.1779667
- bootstrap 95% interval = [-0.04968, +0.44444]
- leave-one-drug-out delta range = +0.10196 to +0.21100

Interpretation boundary:
- Broad CRC 3D contains an exploratory dependency-to-PDO-pharmacology signal.
- There is NOT confirmatory evidence that Broad 3D significantly outperforms Broad 2D because the paired bootstrap delta CI includes zero.
- Sanger 3D does not reproduce the strongest Broad-3D pharmacology signal.
- This is useful nuance, not a rescue of the original field-level positive claim.

## 8. Closest prior art already identified

Do not stop at these; audit them claim-by-claim.

1. Han et al., Nature 2020
   - *CRISPR screens in cancer spheroids identify 3D growth-specific vulnerabilities*
   - DOI: https://doi.org/10.1038/s41586-020-2099-x
   - same-system 2D vs 3D and in-vivo relevance

2. Pacini et al., Nature Communications 2021
   - *Integrated cross-study datasets of genetic dependencies in cancer*
   - DOI: https://doi.org/10.1038/s41467-021-21898-7
   - independent Broad/Sanger CRISPR reproducibility/integration, but conventional cell lines

3. Pacini et al., Cancer Cell 2024
   - *A comprehensive clinically informed map of dependencies in cancer cells and framework for target prioritization*
   - DOI: https://doi.org/10.1016/j.ccell.2023.12.016
   - clinically informed target prioritization from 2D dependency maps

4. Broad Nature 2026
   - DOI above
   - matched 2D/3D within Broad resource

5. Sanger Nature 2026
   - DOI above
   - tumour-organoid dependency map

6. Bhattacharjee et al., Nature Communications 2026
   - DOI: https://doi.org/10.1038/s41467-026-73977-2
   - dependency-informed targeted therapy response modeling
   - not equivalent to the Broad-vs-Sanger organoid cross-resource audit

No direct prior-art match has yet been identified for the exact combined framework:
- independent Broad-3D vs Sanger-3D reproducibility
- lineage-matched Broad-2D comparator
- clinical-precedence adjustment for baseline 2D dependency / common-essentiality
- orthogonal independent metastatic-CRC PDO pharmacology

This is NOT proof of novelty.
Current novelty status: NEEDS_REVIEW.

## 9. Claims to audit one by one

Audit each claim separately and return:
- closest prior art
- exact overlap
- exact distinction
- novelty confidence
- importance
- fatal reviewer objection
- whether wording is defensible

Candidate Claim A:
"Independent large-scale 3D cancer dependency maps strongly reproduce extreme dependencies, but much of the overlap is universal rather than 3D-specific."

Candidate Claim B:
"In lineage-matched CRC, an independent 3D organoid resource is not more concordant with Broad 3D than with matched Broad 2D; after the published non-common-essential filter, Broad 2D is slightly more concordant."

Candidate Claim C:
"The apparent clinical-precedence enrichment of dependencies replicated in 3D collapses after adjustment for baseline 2D dependency strength and common essentiality."

Candidate Claim D:
"Independent mCRC PDO pharmacology shows that Broad CRC 3D dependency contains an exploratory drug-response signal, but does not establish a statistically robust advantage over matched 2D."

Candidate Claim E:
"Taken together, large-scale 3D dependency resources add context and novel individual vulnerabilities, but cross-resource reproducibility and translational value should not be interpreted as a generic 3D-specific advantage without controlling for baseline dependency structure."

## 10. Explicitly prohibited behaviors

- Do not cherry-pick q5/q10/q20 as separate confirmatory hypotheses.
- Do not claim a Nature/Cell-level positive result because one p-value is <0.05.
- Do not call individual targets novel without separate prior-art review.
- Do not treat CSNK2A1-silmitasertib, EGFR, HDAC7, or INSR as novel discoveries by default.
- Do not ignore the negative 3D-vs-2D bootstrap result.
- Do not merge the scratch branch into main.
- Do not modify target-stability main.
- Do not re-download/recompute everything unless required to resolve a discrepancy.
- Do not invent unavailable author-level biological validation.
- Do not treat absence of a search hit as proof of novelty.

## 11. Required PRO output

Return one integrated report with these sections:

### A. EXECUTIVE VERDICT
Choose exactly one:
- GO
- CONDITIONAL GO
- NO-GO

Then state:
- strongest publishable claim in 1 sentence
- what level of journal is realistically supportable
- what would make the paper fail peer review

### B. CLAIM-LEVEL NOVELTY MATRIX
For Claims A-E:
- claim
- closest prior papers
- overlap
- differentiator
- novelty status: GREEN / YELLOW / RED / UNKNOWN
- confidence
- citations

### C. PRIOR-ART SEARCH LOG
Search at minimum:
- PubMed
- Google Scholar-equivalent web search
- bioRxiv / medRxiv
- Crossref/publisher pages
- citation neighbors of the 2026 Broad and Sanger Nature papers
- 2026 reviews/preprints that may already discuss both papers together
Search through 2026-09-19.

### D. REVIEWER-2 ATTACK
Write the 10 strongest reviewer objections.
For each:
- whether fatal
- answer using current data
- additional analysis needed, if any

### E. MANUSCRIPT ARCHITECTURE
Only if GO or CONDITIONAL GO:
- title options
- abstract thesis
- 4-6 main figures
- supplement plan
- primary vs exploratory analyses
- exact claims to avoid

### F. JOURNAL FIT
Give 5-8 realistic journals.
Do not simply rank by impact factor.
For each:
- scope fit
- likely objection
- article type
- author cost / OA constraint if knowable
- why current evidence does or does not fit

### G. FINAL NEXT ACTION
If one extra analysis could materially change the decision, specify exactly ONE.
Otherwise say:
`NO_ADDITIONAL_ANALYSIS_BEFORE_DRAFT`

## 12. Desired tone

Be skeptical.
Prefer a correct NO-GO over a forced positive story.
A negative/confounding/model-validity paper is acceptable if genuinely novel and important.
Do not flatter the project.
Do not hide null or inverse results.
