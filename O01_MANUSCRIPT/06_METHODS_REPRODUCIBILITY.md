# O01 methods and reproducibility companion

## Locked scope

This companion documents analyses already executed. It is not a new analysis plan. `NO_ADDITIONAL_ANALYSIS_BEFORE_FIRST_DRAFT` remains in force. The manuscript wording follows the producer code, including its limitations, rather than silently upgrading aggregation, adjustment or inference.

## Immutable execution anchors

| Purpose | Workflow | Immutable commit / run |
|---|---|---|
| Definitive filtered CRC comparison | `.github/workflows/o01_crc_definitive_20260919.yml` | 313659b61a45403ad29428e6478d25a89a39792a / 35407055037 |
| Historical target-level PDO analyses | `.github/workflows/o01_pdo_pharmacology_validation.yml` | 1a35554f1c02b3f00ef85efd30d5c99c8760077e / 35408854800 |
| Preferred drug-level PDO summary | `.github/workflows/o01_pdo_drug_level_validation.yml` | c3f136f4d68ab3ab73dcf394721b0202fcceae44 / 35409997973 |
| Explicit numeric-outcome correction | `.github/workflows/o01_q10_clinical_endpoint_orientation_correction.yml` | 0a61f7940a65f323a1f48b7e7ba581931f41c1c9 / 35414237376 |
| Pre-correction handoff | `O01_PRO_HANDOFF_20260919.md` | f8dfd52214d177c105c8fead7098a752fa2ba89d |
| Corrected authoritative event | Control Center project publication-pipeline-2026 | 74e1a3401bd01e2da413a7dfbf1eb7b3b29b4986 |

Repository: https://github.com/ByungwoongYoo/target-stability

## Input and processing provenance

Broad source: https://doi.org/10.1038/s41586-026-10843-7. The executed workflow used Breadbox matrix ID `fa1b635a-5116-4a93-b66d-84eca7e2a402` and `screen_nextgen_metadata`. CRC lineages were selected from the source label. 3D required IsNextGen and ScreenType=3DO; 2D required IsAdherent2D. Aggregation was across source screens, not proven unique patients or one randomly selected screen per model.

The restriction used the GeneSymbol column in sheet `Fig5b diff deps volcano`, source file `41586_2026_10843_MOESM12_ESM.xlsx`. Its 16,691-gene comparison universe must not be described as a newly estimated essentiality filter.

Sanger source: https://doi.org/10.1038/s41586-026-10830-y. Executed files inside `41586_2026_10830_MOESM3_ESM.zip`: `supplementary_table_2_revision.xlsx`, sheet `data_availability`, and `supplementary_table_6_revision.csv`. Selection required CRISPR_available=yes, primary_tumour_type=colorectal and no affirmative overlap_Broad_DepMap annotation. LFC values were averaged within sample_ID/gene and then across models. Overlap exclusion uses supplied annotations; it is not a new donor-genotype identity audit. Gene-symbol joins do not establish matched donor identity.

The 15,008-gene intersection supplied three complete mean profiles. q10 membership was value<=profile.quantile(.10). The exact legacy class definitions are: b2 & b3 & s3 = UNIVERSAL; ~b2 & b3 & s3 = exclusive-3D; b2 & ~b3 & ~s3 = 2D-only. Other patterns were excluded from the reported clinical class contrasts, not from the correlation universe.

## Statistical specification actually used

Spearman/Pearson correlations compare profile values over genes. Two thousand aligned gene-bootstrap resamples supplied the 3D-minus-2D Spearman interval, seed 20260919. This is conditional on cohort means and does not estimate model-recruitment or donor uncertainty. One-sided Fisher tested 3D top-list overlap; clinical contingency tests were two-sided Fisher. The overlap test's numerically underflowed P is not an exact zero.

Open Targets release 26.06 supplied target, target_essentiality, disease and evidence_clinical_precedence. CRC comprised MONDO_0005575 plus descendants (88 IDs). Per-gene maximum coded stage used the exact dictionary in 04_SUPPLEMENT_PLAN.md, including WITHDRAWAL=4 and missing=0. Thus the upper-stage flag is not a current regulatory-approval adjudication. The essentiality flag recursively marks any true isEssential within geneEssentiality, collapses by symbol and treats missing as false. The analysis did not add tractability or development-investment covariates.

The locked GLM used 994 selected genes, replicated3d as all-three-profile membership, b2_z as standardized raw BroadCRC2D effect (population SD, ddof=0), and essential_int. More negative raw effect denotes stronger dependency. Corrected outcomes are explicit integers 0/1. Phase II+/III+ events are 45/30. The model is Binomial logit, with Wald CI exp(beta±1.96*SE). The three-event upper-stage result is unstable and not interpreted. No multiplicity correction or prospective confirmation is asserted.

PDO source: https://doi.org/10.17632/hr94h42xdc.3; Data S5.xlsx, 211 rows and 62 columns. The script excludes metadata columns and specified combination labels, strips _lib1/_lib2 suffixes, averages available matching columns within each PDO row, and takes the per-drug median over rows. It does not perform patient balancing or strict 24-drug harmonization. Missing values are not zeros. The 51 retained operational labels are not 51 independently verified selective inhibitors.

Drug-molecule aliases must map unambiguously to one OT/ChEMBL ID. Human target annotations are restricted by the executed negative-action pattern (INHIB, ANTAGON, BLOCK, DEGRAD, NEGATIVE, SUPPRESS, DISRUPT) and the shared gene universe. The 26-drug analysis uses maximum or median negative gene-effect magnitude over each retained target set. The maximum can select a different target in each resource. Ten thousand paired drug-bootstrap resamples estimate the direct correlation difference; leave-one-drug-out ranges are point-estimate diagnostics. The <=3-target sensitivity counts targets after the shared-universe restriction. These are not patient-clustered, target-family-clustered or mechanistically selective drug estimates.

## Correction verification boundary

The original formula Boolean outcome produced the complementary event orientation. The completed correction changes to numeric 0/1 and retains the q10 rule, disease scope, comparison and covariates. Its locked assertions cover group sizes and event counts. The recorded gene/class/endpoint hash is `6916208707fb7779916359a6ccc5f61d5db306f435787d5328fdd4df77185bdb`; do not label it a raw-file or full-covariate hash. The final clinical values in the manuscript are from the actual numeric refit, not merely reciprocals calculated during the preceding audit.

## Reproducibility deliverables still to assemble

Export existing joined inputs, the 994-row fitted table including covariates, all 26 drug rows, mapping tables, original logs, actual run versions and machine-readable result JSONs into a persistent source-data archive. The inspected branch contains workflow source and handoff, not a verified complete standalone input archive. Runtime pip installations were not fully version-pinned; preserve the successful-run environment logs instead of inventing a lock file. Confirm public reviewer access before submission. These are evidence packaging and production tasks, not additional hypothesis tests.

Do not rerun workflows simply to write manuscript files. Existing scratch pushes trigger workflows; document-only commits must skip CI. Target-stability main must remain unchanged. This draft build dispatches no computational jobs and makes no new effect estimates.
