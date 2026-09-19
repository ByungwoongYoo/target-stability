# IRIS reproducibility + external BMP4 validation note

Date: 2026-09-19
Nature Methods DOI: 10.1038/s41592-026-03213-8

## 1. Public-code response-gene discrepancy

The paper Methods describes the response-gene baseline as the **sum of log-normalized expression** across a pathway's response genes.

The public `response_gene()` implementation instead:
1. log-normalizes;
2. z-scores the selected response genes within each cell;
3. sums those within-cell z-scores.

That sum is approximately zero by construction for non-degenerate rows.

On the historical public `screen_data.h5ad` recovered from the repository's earlier Git-LFS history
(SHA-256 `195155f2251f03a91ffe90a4133b7cf52dd2ab1b76b35975a6228a11f37e5ea1`), the Methods-style sum and current public implementation give:

| Pathway | Methods-style sum AUROC | released-code z-sum AUROC |
|---|---:|---:|
| RA | 0.7548 | 0.5123 |
| BMP | 0.8546 | 0.5023 |
| FGF | 0.6511 | 0.4957 |
| WNT | 0.7634 | 0.5194 |
| TGFβ | 0.5812 | 0.4997 |
| SHH | 0.5931 | 0.4857 |

The Methods-style values reproduce the qualitative pattern described in the manuscript.

This finding concerns the **public release / implementation contract**. It does not establish that the paper's main IRIS results are wrong.

## 2. Independent distant-cell BMP4 baseline

External dataset:
- GEO `GSE114988`
- adult mouse enteroendocrine organoid perturbation data
- BMP4 treatment, 24 h / 4 d conditions
- response-gene score uses the paper's preset BMP genes and the Methods-style log-normalized sum.

Four mixed-condition 384-cell files were evaluable.

| File | BMP genes recovered | pooled treated-v-control AUROC | 24h-v-control AUROC | 4d-v-control AUROC |
|---|---:|---:|---:|---:|
| JB-TC2 | 6 | 0.544 | 0.566 | 0.533 |
| JB_GIPcre | 8 | 0.753 | 0.722 | 0.768 |
| JB_venus2 | 8 | 0.709 | 0.778 | 0.674 |
| JB_venus3 | 7 | 0.572 | 0.801 | 0.458 |

Interpretation:
- the independent organoid dataset contains a detectable BMP response-gene signal in several files;
- the signal is heterogeneous across biological/sample contexts;
- strongest 24 h AUROC = **0.801**;
- strongest pooled AUROC = **0.753**;
- this is a **response-gene baseline gate, not a neural-network IRIS validation**.

## 3. Other public-release observations

- README documents `load_pretrained_model()`, but pretrained checkpoints are not apparent in the public repo.
- Upstream issue #2, opened 2026-09-09 by another user, asks where pretrained IRIS models are; no maintainer reply was recovered at audit time.
- README links `iris/examples/fig3+4.ipynb`, but the corresponding public path was absent in the audited tree.
- Additional code paths deserve separate unit tests before any public claim; they are not part of the primary result above.

## 4. Reproducibility pointers

Completed internal validation runs:
- historical-code / external-feasibility gate:
  https://github.com/ByungwoongYoo/target-stability/actions/runs/35447970401
- response-gene implementation audit:
  https://github.com/ByungwoongYoo/target-stability/actions/runs/35448795220
- independent GSE114988 BMP response-gene gate:
  https://github.com/ByungwoongYoo/target-stability/actions/runs/35449881345

Working branch:
https://github.com/ByungwoongYoo/target-stability/tree/iris-validation-sol-20260919

## 5. Boundary / next technical test

Do not infer authorship, paper invalidity, or failure of IRIS from these results.

The highest-value next technical test is a true out-of-domain IRIS model evaluation after obtaining or faithfully retraining the model under the paper's training contract. The response-gene discrepancy can be fixed independently with a minimal patch.
