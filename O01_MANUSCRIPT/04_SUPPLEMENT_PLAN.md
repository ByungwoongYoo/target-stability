# O01 supplementary information — assembly specification and correction text

This is the specification for assembling existing results, not a claim that all supplementary data tables are already packaged. No new analysis is required or authorized before the first draft. Existing tables may be exported without altering their rows, definitions, estimates or thresholds.

## Supplementary Table S1 — Sources, versions and units

Provide source DOI, release, accession or endpoint, retrieval time from the original run where recorded, screen/model identifiers, overlap rule, model-to-donor availability, and hashes actually recorded. Distinguish 18 Broad 3D screens, 67 Broad 2D screens, 81 Sanger models and 211 PDO rows. Do not invent unique donor counts from these units. Include Broad Fig5 restriction (16,691) and shared filtered universe (15,008). State that raw CRISPR counts were not jointly reprocessed.

Sources: Broad 10.1038/s41586-026-10843-7; Sanger 10.1038/s41586-026-10830-y; independent pharmacology 10.1016/j.xcrm.2026.102840 and dataset 10.17632/hr94h42xdc.3; Open Targets release 26.06.

## Supplementary Table S2 — Joined gene values and rank membership

Export the frozen 15,008-gene table and source symbol mappings from existing outputs if retained. Columns: gene, BroadCRC3D, BroadCRC2D, SangerCRC3D, b3, b2, s3 and subclass. q10 primary counts: 1,501 per 3D list; overlap 763; all-three 645; exclusive-3D 118; 2D-only 349. Unreported three-set regions and per-gene values are not fabricated in this draft package. Full export remains a production item.

## Supplementary Table S3 — Existing descriptive sensitivities

| Quantile | Genes per 3D list | Two-3D intersection | Overlap OR | All-three | Exclusive-3D | 2D-only |
|---|---:|---:|---:|---:|---:|---:|
| q5 | 751 | 421 | 53.8408 | 338 | 83 | 178 |
| q10 | 1,501 | 763 | 17.8883 | 645 | 118 | 349 |
| q20 | 3,002 | 1,363 | 5.2601 | 1,153 | 210 | 627 |

Earlier unfiltered comparison: 16,318 genes, Broad3D/Sanger rho 0.4762673 and Broad2D/Sanger rho 0.4944996. It is a traceable earlier analysis, not a new alternative primary. Do not carry forward legacy q5/q20 adjusted Boolean-outcome ORs as event-oriented clinical results. Only q10 was explicitly corrected in the locked refit.

## Supplementary Table S4 — Clinical dictionary, full output and audit

Publish the original stage dictionary unchanged: UNKNOWN=0; PRECLINICAL=0.1; IND=0.5; EARLY_PHASE_1=0.75; PHASE_1=1; PHASE_1_2=1.5; PHASE_2=2; PHASE_2_3=2.5; PHASE_3=3; PREAPPROVAL=3.5; APPROVAL=4; PHASE_4=4; WITHDRAWAL=4. Unmapped stages and absent annotations were coded as zero. Explain that the upper category is not a current FDA/EMA approval endpoint. Disease set: MONDO_0005575 and descendants, 88 identifiers. Document the recursive essentiality flag, missing-value treatment and absence of tractability adjustment.

### Supplementary Methods — Endpoint coding audit and locked correction

During internal audit, a formula-based Boolean outcome was found to invert the event orientation in an earlier exploratory model. The locked q10 comparison was therefore refitted with an explicit numeric 0/1 endpoint without changing the comparison groups, threshold, disease scope or covariates. The final refit contained 994 genes: 645 all-three-profile genes and 349 2D-only genes, with 45 Phase II-or-higher events, 30 Phase III-or-higher events and three upper-stage events. Its outcome values were numeric 0 and 1.

The model was `endpoint ~ replicated3d + b2_z + essential_int`. Here, replicated3d denotes all-three-profile rather than exclusive-3D membership. The corrected Phase II-or-higher OR was 1.3487761406 (95% CI 0.5853139188–3.1080707618; P=0.4823844923), and the corrected Phase III-or-higher OR was 4.2187090214 (1.1886118578–14.9733537404; nominal P=0.0259240472). The earlier ORs 0.7414 and 0.2370 concerned the complementary event orientation and are retained only in the audit history. The prior narrative of collapse or inversion after adjustment is superseded. The three-event upper-stage model was unstable and is not interpreted.

The fingerprint `6916208707fb7779916359a6ccc5f61d5db306f435787d5328fdd4df77185bdb` covers the sorted gene/class/endpoint payload. It is not a fingerprint of every covariate, original input file or entire fitted object. Both the erroneous run and the correction must remain accessible; the correction is quality control, not a biological discovery or a newly selected favourable model.

Original definitive run: 35407055037. Correction run: 35414237376. Correction commit: 0a61f7940a65f323a1f48b7e7ba581931f41c1c9. The corresponding Control Center event is at commit 74e1a3401bd01e2da413a7dfbf1eb7b3b29b4986.

## Supplementary Table S5 — PDO labels, target annotations and missingness

Export existing per-drug and mapping tables. Include original DSS column labels, any _lib1/_lib2 consolidation, number of available PDO rows per drug, molecule ID resolution, action annotations, target list before and after the gene-universe restriction, and combination-label exclusions. The recorded funnel is 51 operational single-agent labels, 41 unambiguous molecule mappings, 35 drugs with eligible inhibitory annotations and 26 with retained targets. This is not a strict 24-harmonized-drug panel or patient-clustered analysis. Do not fill missing drug/patient records from the source paper's overall biobank count.

## Supplementary Table S6 — All completed pharmacology summaries

| Set and summary | n drugs | Broad3D rho / P | Broad2D rho / P | Sanger3D rho / P | Direct Broad3D−2D delta | Drug-bootstrap 95% interval |
|---|---:|---|---|---|---:|---|
| All, strongest target | 26 | 0.4200791 / 0.03263 | 0.2947730 / 0.14378 | 0.3176291 / 0.11383 | 0.1253061 | [−0.08612, 0.36223] |
| All, median target | 26 | 0.2428916 / 0.23185 | 0.1959577 / 0.33736 | −0.0236423 / 0.90873 | 0.0469339 | [−0.17130, 0.26653] |
| At most 3 retained targets, strongest | 21 | 0.3417029 / 0.12951 | 0.2993161 / 0.18747 | 0.2484519 / 0.27749 | 0.0423868 | [−0.17489, 0.27964] |
| At most 3 retained targets, median | 21 | 0.4954385 / 0.02238 | 0.3174717 / 0.16081 | 0.1851375 / 0.42172 | 0.1779667 | [−0.04968, 0.44444] |

Existing leave-one-drug-out delta ranges: 26-drug strongest summary +0.05854 to +0.16221; 21-drug median summary +0.10196 to +0.21100. These are ranges of point estimates, not confidence intervals or independent replications.

Earlier single-target gene analysis (n=7): Broad3D rho 0.5357, P=0.2152; Broad2D and Sanger3D each −0.0714, P=0.8790. Its reported bootstrap-mean delta is 0.5978 [0.0382,1.2549], not a direct point-estimate difference. All-target gene analysis (n=72): Broad3D 0.1906, P=0.1088; Broad2D 0.1729, P=0.1464; Sanger3D 0.0311, P=0.7951; bootstrap-mean delta 0.0169 [−0.1294,0.1610]. Target-level analyses can duplicate information from multi-target drugs and are retained only as exploratory chronology, not as positive headline rescue.

## Supplementary Table S7 — Chronology and execution records

Retain workflow paths, immutable commits, run IDs, actual successful-run package versions, inputs and outputs where available. Report that the scripts used runtime pip installations rather than a fully pinned environment. Exporting the original logs and frozen derived tables is unfinished production work, not authorization to recompute. Declare each test retrospective and preserve null, corrected and non-estimable outcomes. No additional analysis before the first draft.
