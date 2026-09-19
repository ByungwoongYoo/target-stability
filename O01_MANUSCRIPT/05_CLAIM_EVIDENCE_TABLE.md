# O01 claim-to-evidence table — corrected first draft

Authoritative numerical basis: handoff f8dfd52214d177c105c8fead7098a752fa2ba89d except that the corrected clinical run 35414237376 and Control Center commit 74e1a3401bd01e2da413a7dfbf1eb7b3b29b4986 supersede the earlier Boolean-outcome interpretation. No new discovery or priority claim is made.

| Claim | Evidence retained | Defensible wording | Boundary | Manuscript location |
|---|---|---|---|---|
| A: cross-resource extreme-rank reproducibility | 15,008 genes; 763/1,501 intersection; overlap OR 17.8883; 645/763=84.53% also top-decile 2D | The resources share strongly ranked CRC dependencies, most also highly ranked in the lineage-matched 2D profile. | Three aggregate top-decile profiles do not define essentiality in every model. This is an empirical extension of existing cross-study work, not a new principle. | Results 1–2, Figure 2 |
| B: incremental concordance | rho3D 0.3299897370; rho2D 0.3531986912; delta −0.0232089542; conditional gene-bootstrap CI [−0.0330344,−0.0131187] | In the observed CRC cohorts, the aggregate Sanger profile was not more concordant with Broad3D than Broad2D. | Lineage-matched, not identical models; no culture-format causal effect, equivalence or biological superiority. | Results 3, Figure 3 |
| C: historical development association | 994 selected genes; corrected Phase II+ OR 1.3488 [0.5853,3.1081]; Phase III+ OR 4.2187 [1.1886,14.9734] | Among the selected strong-2D genes, all-three-profile membership was associated with historical Phase III+ precedence after the specified adjustment; the Phase II+ association was not significant. | Secondary retrospective nominal association. Adjusted contrast is UNIVERSAL versus 2D_ONLY, not exclusive-3D. Not future clinical success, current approval or complete confounder control. | Abstract, Results 4, Discussion, Figure 4 |
| C, separate exclusive-3D contrast | Phase II+ 4/118 vs9/349, P=0.7461; Phase III+ 0/118 vs3/349, P=0.5751 | No significant historical-precedence enrichment was observed for the exclusive-3D rank class. | Non-significance does not establish equivalence or no true effect. Do not mix this denominator with the 994-gene GLM. | Results 4, Figure 4 |
| D: exploratory external pharmacology | 26 drugs; Broad3D rho .4200791, P .03263; direct delta .1253061, CI [−.08612,.36223]; all reported delta intervals include zero | Broad3D showed an exploratory association with cohort-level PDO DSS, without an established incremental advantage over Broad2D. | Independent data source, not patient-clustered inference; no significance-versus-significance comparison. Sanger association varies with target summary. | Results 5, Figure 5 |
| E: synthesis | A–D are different estimands with different units and uncertainty | Cross-resource agreement, information beyond the 2D baseline, historical development and pharmacologic association represent distinct dimensions of model validity. | A synthesis supported by this case study, not a universal law or a claim that either source paper promised generic 3D superiority. | Introduction and final Discussion |

## Language guardrails

Do not assert clinical validation, prospective treatment prediction, all-confounding removal, FDA/EMA-verified approval rates, generic 3D superiority/inferiority, patient-level validation, causal culture effects, or a new CSNK2A1/HDAC7/EGFR/INSR therapeutic discovery. Do not retain the superseded “clinical enrichment collapses or reverses” narrative.

Use “all-three-profile” in prose before the legacy code label UNIVERSAL. Use “exclusive-3D rank class” when “3D-specific” might be confused with a tested biological interaction. Keep “nominal,” “secondary,” “retrospective” and the exact comparison visible for Phase III+. A non-significant between-resource difference is uncertain, not a demonstration of equivalence.

## Source hierarchy and prior-art boundary

Primary results: completed O01 workflows and corrected Control Center event. Biological/source-method context: references 1–10 in 00_MANUSCRIPT_FULL.md. The independent Broad/Sanger comparison, 2D/3D context effects and dependency-informed pharmacology each have prior art; the draft does not call these concepts new. This build does not reopen the completed novelty search.

Clean evidence links:
- https://github.com/ByungwoongYoo/target-stability/actions/runs/35414237376
- https://github.com/ByungwoongYoo/target-stability/actions/runs/35407055037
- https://github.com/ByungwoongYoo/target-stability/actions/runs/35409997973
- https://github.com/ByungwoongYoo/control-center/commit/74e1a3401bd01e2da413a7dfbf1eb7b3b29b4986
