# O01 main-figure production plan — frozen first draft

Status: five figure specifications and complete legends, not five rendered publication files. All values below originate from completed O01 runs. No new tests, thresholds, subgroups or model fitting are authorized by this plan. Exporting a frozen table or drawing its existing estimates is production, not a new scientific analysis. Do not reconstruct a missing scatterplot from summary correlations.

## Figure 1 — Study design and resource harmonization

Use a flow diagram separating three purposes: cross-resource reproducibility; comparison against the lineage-matched 2D profile; historical-precedence and exploratory pharmacologic associations. Input boxes: Broad CRC 3D 18 screens, Broad CRC adherent 2D 67 screens, Sanger CRC 81 models with no annotated Broad overlap. Gene-selection boxes: published Broad Figure 5 universe 16,691, shared complete-case universe 15,008. Downstream clinical box: 88 CRC disease identifiers; adjusted q10 contrast 645+349=994 genes. Pharmacology box: Data S5 211 PDO rows by 62 columns, 51 operational single-agent labels, 41 unambiguous molecule mappings, 35 eligible inhibitory annotations, 26 drugs with retained targets.

Statistical unit: screens/models are source coverage; genes are the cross-resource and clinical units; drugs are the pharmacology unit. This figure is descriptive: no test or CI. Do not draw patient-matched arrows, a randomized 2D/3D comparison, or 211 independent patients.

## Figure 2 — Extreme-dependency overlap and the 2D baseline

Panel A: two strongest-decile lists, 1,501 genes each; intersection 763; universe 15,008. Panel B: decompose the intersection into 645 all-three-profile genes and 118 exclusive-3D rank members. Panel C: separate box for 349 2D-only rank members. Display 645/763=84.53% as descriptive membership arithmetic. Avoid a full three-set Venn/UpSet with unsupplied regions.

Unit: gene. Test: one-sided Fisher exact overlap test; OR 17.8883. No OR CI was estimated. The stored P underflowed; do not print P=0. The q5/q20 analyses belong to Supplement S3. “Universal” denotes this three-profile intersection, not universal cellular essentiality. Exclusive-3D denotes rank membership, not a tested interaction.

## Figure 3 — Concordance with the independent Sanger CRC profile

Panel A: display the two Spearman point estimates, Broad3D 0.3299897370 and Broad2D 0.3531986912. A publication scatterplot requires the frozen joined gene table, which is not recreated here. Panel B: show the directly estimated 3D-minus-2D difference −0.0232089542 with conditional gene-bootstrap 95% interval [−0.0330344,−0.0131187]. Pearson companions, 0.5109250 and 0.5181936, can be placed in the caption or an inset without invented uncertainty intervals.

Unit: 15,008 genes conditional on fixed aggregate profiles. Bootstrap: 2,000 aligned gene draws; original seed 20260919. Neither models nor patients were resampled. The plot does not establish biological inferiority or causal culture-format effects.

## Figure 4 — Historical clinical precedence, not clinical success

Panel A: proportions with numerator/denominator labels for all-three-profile versus 2D-only: Phase II+ 36/645 versus 9/349; Phase III+ 27/645 versus 3/349. Panel B: corrected adjusted OR forest plot only: Phase II+ 1.3487761406 [0.5853139188,3.1080707618], P=0.4823844923; Phase III+ 4.2187090214 [1.1886118578,14.9733537404], nominal P=0.0259240472. A log x-axis with an OR=1 reference is appropriate.

Panel C, visibly separate: exclusive-3D versus 2D-only, Phase II+ 4/118 versus 9/349 (OR 1.3255, P=0.7461), Phase III+ 0/118 versus 3/349 (P=0.5751). Show the sparse highest-stage endpoint as counts and “not interpretable”; no extreme approval OR on the forest plot.

Unit: gene. Adjusted set: 994 genes, 45/30 events for Phase II+/III+. Same numeric-outcome Binomial GLM with replicated3d, b2_z and essential_int. CI is Wald; unadjusted tests are two-sided Fisher. These are secondary retrospective endpoints, not multiplicity-adjusted confirmations. Corrected run: 35414237376. The adjusted contrast is not exclusive-3D versus 2D-only.

## Figure 5 — Independent PDO drug-level pharmacologic association

Panel A: 26-drug strongest-target correlation summary: Broad3D 0.4200791, Broad2D 0.2947730, Sanger3D 0.3176291. If plotting points, export the 26-row table from the existing successful run; do not invent points from rho. Panel B: direct Broad3D-minus-Broad2D differences for strongest-target +0.1253061 [−0.08612,+0.36223] and median-target +0.0469339 [−0.17130,+0.26653]. Mark the entire figure exploratory.

Unit: drug, not patient, PDO row or drug-target pair. Response: per-drug median over available PDO rows after the existing within-row label processing. Bootstrap: 10,000 paired drug draws, seed 20260919. Target selection can differ between resources in the strongest-target summary. These intervals do not include patient-cluster or target-family uncertainty. The 21-drug sensitivities and earlier target-level analyses remain in Supplement S6.

## Production and cost constraints

Use grayscale-safe shapes, line types and direct labels. No inference should depend on colour. BJC explicitly lists a free standard licence but charges for chosen print/PDF colour; do not select that paid option. Render original figures from existing outputs before submission. Do not copy source-paper panels or present this plan as completed artwork.

## Frozen sources

- Handoff: https://github.com/ByungwoongYoo/target-stability/blob/f8dfd52214d177c105c8fead7098a752fa2ba89d/O01_PRO_HANDOFF_20260919.md
- Definitive CRC run: https://github.com/ByungwoongYoo/target-stability/actions/runs/35407055037
- Numeric-endpoint correction: https://github.com/ByungwoongYoo/target-stability/actions/runs/35414237376
- Drug-level PDO run: https://github.com/ByungwoongYoo/target-stability/actions/runs/35409997973
- BJC guide, checked 2026-09-19: https://www.nature.com/bjc/authors-and-referees/gta
