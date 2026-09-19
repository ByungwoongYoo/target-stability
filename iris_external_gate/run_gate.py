#!/usr/bin/env python3
import os, re, json, tarfile, gzip, io, hashlib
from pathlib import Path
import requests
import numpy as np
import pandas as pd
import anndata as ad

OUT = Path("iris_external_gate/results")
OUT.mkdir(parents=True, exist_ok=True)
report = {"status":"STARTED"}

def download(url, path, chunk=1024*1024):
    path = Path(path)
    if path.exists() and path.stat().st_size > 0:
        return path
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for part in r.iter_content(chunk_size=chunk):
                if part:
                    f.write(part)
    return path

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(1024*1024), b""):
            h.update(c)
    return h.hexdigest()

# 1) Upstream reproducibility audit
base = "https://raw.githubusercontent.com/Pulin-Li-Lab/IRIS-signaling-inference/fa5866ef3a1a608b59b5bb6eec219f24086ec369"
readme = requests.get(base + "/README.md", timeout=30)
readme.raise_for_status()
readme_text = readme.text
iris_py = requests.get(base + "/iris/src/iris.py", timeout=30)
iris_py.raise_for_status()
iris_text = iris_py.text
(OUT/"upstream_README.md").write_text(readme_text)
(OUT/"upstream_iris.py").write_text(iris_text)

example_url = base + "/iris/examples/fig3%2B4.ipynb"
ex = requests.get(example_url, timeout=30)
report["example_notebook_http_status"] = ex.status_code

tree = requests.get(
    "https://api.github.com/repos/Pulin-Li-Lab/IRIS-signaling-inference/git/trees/fa5866ef3a1a608b59b5bb6eec219f24086ec369?recursive=1",
    timeout=30,
)
tree.raise_for_status()
treej = tree.json().get("tree", [])
paths = [x["path"] for x in treej]
weight_like = [p for p in paths if re.search(r"(model|weight|checkpoint|\.pt$|\.pth$|\.ckpt$|\.pkl$)", p, re.I)]
report["repository_path_count"] = len(paths)
report["weight_like_paths"] = weight_like
report["examples_paths"] = [p for p in paths if "example" in p.lower()]

# Static consistency checks in released code
report["load_pretrained_stores_signal_key"] = "self.models[signal]" in iris_text
report["run_model_reads_class_key"] = "self.models[val]" in iris_text
report["run_model_multisignal_controlflow_risk"] = (
    "if not self.models:" in iris_text and
    "self.models[val] = scanvae" in iris_text and
    "else:\n                scanvae = self.models[val]" in iris_text
)
report["find_predicted_state_undefined_matches_mapping"] = "matches_mapping &= signal_matches" in iris_text

# Algebraic check for response_gene row-wise z-score then row sum
rng = np.random.default_rng(7)
mat = rng.normal(size=(100,9))
std = np.std(mat, axis=1, keepdims=True)
z = (mat - np.mean(mat,axis=1,keepdims=True))/std
sums = z.sum(axis=1)
report["response_gene_rowwise_zsum_max_abs_random"] = float(np.max(np.abs(sums)))
report["response_gene_degenerate_formula_detected"] = (
    "std = np.std(mat, axis=1)" in iris_text and
    "mat = (mat - np.mean(mat, axis=1))/std" in iris_text and
    "mat.sum(axis=1)" in iris_text
)

# 2) Recover the historical processed h5ad via Git LFS media endpoint
h5ad_url = "https://media.githubusercontent.com/media/Pulin-Li-Lab/IRIS-signaling-inference/fc92c14078f2a106d2fea0b715b1743c7bac167c/data/screen_data.h5ad"
h5ad_path = Path("iris_external_gate/screen_data.h5ad")
try:
    download(h5ad_url, h5ad_path)
    report["historical_h5ad_downloaded"] = True
    report["historical_h5ad_size"] = h5ad_path.stat().st_size
    report["historical_h5ad_sha256"] = sha256(h5ad_path)
    a = ad.read_h5ad(h5ad_path, backed="r")
    report["historical_h5ad_shape"] = [int(a.n_obs), int(a.n_vars)]
    report["historical_h5ad_obs_columns"] = list(map(str,a.obs.columns))
    report["historical_h5ad_layers"] = list(map(str,a.layers.keys()))
    report["historical_h5ad_obsm"] = list(map(str,a.obsm.keys()))
    class_cols = [c for c in a.obs.columns if str(c).endswith("_class")]
    report["class_columns"] = list(map(str,class_cols))
    report["metadata_columns_present"] = {k: (k in a.obs.columns) for k in ["batch","celltype","species","stage"]}
    distributions = {}
    for c in class_cols:
        vc = a.obs[c].astype(str).value_counts(dropna=False)
        distributions[str(c)] = {str(k):int(v) for k,v in vc.head(20).items()}
    report["class_distributions"] = distributions
    a.file.close()
except Exception as e:
    report["historical_h5ad_downloaded"] = False
    report["historical_h5ad_error"] = repr(e)

# 3) External BMP4 organoid dataset: cheap ground-truth suitability gate
geo_base = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE114nnn/GSE114988/suppl/"
rawtar = Path("iris_external_gate/GSE114988_RAW.tar")
try:
    download(geo_base + "GSE114988_RAW.tar", rawtar)
    report["gse114988_downloaded"] = True
    report["gse114988_size"] = rawtar.stat().st_size
    extract_dir = Path("iris_external_gate/GSE114988_RAW")
    extract_dir.mkdir(exist_ok=True)
    with tarfile.open(rawtar) as t:
        t.extractall(extract_dir)
    files = sorted([p.name for p in extract_dir.iterdir()])
    report["gse114988_files"] = files

    # Try to obtain readme and barcode map too.
    for fn in ["GSE114988_readme.txt","GSE114988_Cellseq2barcodes.csv.gz"]:
        try:
            download(geo_base + fn, Path("iris_external_gate")/fn)
        except Exception as e:
            report[fn+"_error"] = repr(e)
    rp = Path("iris_external_gate/GSE114988_readme.txt")
    if rp.exists():
        txt=rp.read_text(errors="replace")
        (OUT/"GSE114988_readme.txt").write_text(txt)
        report["gse114988_readme_excerpt"] = txt[:5000]
    bp = Path("iris_external_gate/GSE114988_Cellseq2barcodes.csv.gz")
    if bp.exists():
        try:
            bc=pd.read_csv(bp, compression="gzip")
            report["barcode_map_columns"]=list(map(str,bc.columns))
            report["barcode_map_shape"]=[int(bc.shape[0]),int(bc.shape[1])]
            bc.head(50).to_csv(OUT/"barcode_map_head.csv", index=False)
        except Exception as e:
            report["barcode_map_parse_error"]=repr(e)

    # Expression-file gene coverage and coarse file-level signature summary.
    bmp_genes = ["ID2","BMPER","ID4","ID1","BAMBI","MSX1","ID3","MSX2","SMAD7"]
    file_summaries={}
    for p in extract_dir.glob("*.gz"):
        if "TranscriptCounts" not in p.name and "coutt" not in p.name:
            continue
        try:
            df=pd.read_csv(p,sep="\t",compression="gzip",index_col=0)
            # normalize orientation: genes as rows
            idx_upper = {str(x).upper():x for x in df.index}
            col_upper = {str(x).upper():x for x in df.columns}
            row_hits=[g for g in bmp_genes if g in idx_upper]
            col_hits=[g for g in bmp_genes if g in col_upper]
            if len(col_hits) > len(row_hits):
                df=df.T
                idx_upper={str(x).upper():x for x in df.index}
                row_hits=[g for g in bmp_genes if g in idx_upper]
            avail=[idx_upper[g] for g in bmp_genes if g in idx_upper]
            summ={"shape":[int(df.shape[0]),int(df.shape[1])],"bmp_genes_present":[str(x) for x in avail]}
            if len(avail)>=3 and df.shape[1]>=3:
                X=df.loc[avail].T.astype(float)
                # CPM-like normalization per cell, then log1p.
                totals=df.T.astype(float).sum(axis=1).replace(0,np.nan)
                Xn=np.log1p(X.div(totals,axis=0)*1e4)
                # Gene-wise z-score across cells (sensible signature baseline)
                Z=(Xn-Xn.mean(axis=0))/Xn.std(axis=0).replace(0,np.nan)
                score=Z.mean(axis=1,skipna=True)
                summ["bmp_signature_mean"]=float(score.mean())
                summ["bmp_signature_sd"]=float(score.std())
                summ["n_cells"]=int(len(score))
            file_summaries[p.name]=summ
        except Exception as e:
            file_summaries[p.name]={"error":repr(e)}
    report["gse114988_expression_summaries"]=file_summaries
except Exception as e:
    report["gse114988_downloaded"]=False
    report["gse114988_error"]=repr(e)

# 4) Current hESC barcode table availability (small file): check retraining metadata.
gse289_url="https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM8799nnn/GSM8799996/suppl/GSM8799996_bar_table_full_complete.csv.gz"
try:
    p=Path("iris_external_gate/GSM8799996_bar_table_full_complete.csv.gz")
    download(gse289_url,p)
    bt=pd.read_csv(p,compression="gzip")
    report["gse289836_bar_table_shape"]=[int(bt.shape[0]),int(bt.shape[1])]
    report["gse289836_bar_table_columns"]=list(map(str,bt.columns))
    bt.head(100).to_csv(OUT/"GSM8799996_bar_table_head.csv",index=False)
except Exception as e:
    report["gse289836_bar_table_error"]=repr(e)

# High-level gate
blockers=[]
if report.get("example_notebook_http_status") != 200:
    blockers.append("README example notebook path is not present at the pinned public commit")
if not report.get("weight_like_paths"):
    blockers.append("No obvious pretrained-model/checkpoint files in public repository tree")
if report.get("run_model_multisignal_controlflow_risk"):
    blockers.append("run_model scratch-training path appears to become keyed to first class then fails on later signals")
if report.get("load_pretrained_stores_signal_key") and report.get("run_model_reads_class_key"):
    blockers.append("pretrained-model storage key and run_model lookup key appear inconsistent (signal vs signal_class)")
if report.get("response_gene_degenerate_formula_detected"):
    blockers.append("response_gene baseline uses row-wise z-scoring followed by row sum, which is algebraically degenerate")
report["blocking_findings"]=blockers
report["status"]="COMPLETE"

(OUT/"report.json").write_text(json.dumps(report,indent=2,sort_keys=True))
with open(OUT/"REPORT.md","w") as f:
    f.write("# IRIS external-validation feasibility gate\n\n")
    f.write("This is a bounded reproducibility/feasibility audit, not a claim that the Nature Methods paper is invalid.\n\n")
    for k,v in report.items():
        if k in {"gse114988_readme_excerpt","gse114988_expression_summaries","class_distributions"}: continue
        f.write(f"- **{k}**: \`{v}\`\n")
    f.write("\n## Blocking findings\n")
    for x in blockers: f.write(f"- {x}\n")
    f.write("\n## Boundary\nThe paper may have been run with internal notebooks/models not fully represented in the current public repo. Public-release reproducibility issues are not evidence that the published biological conclusions are false.\n")
print(json.dumps(report,indent=2)[:20000])
