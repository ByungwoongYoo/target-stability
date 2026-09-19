#!/usr/bin/env python3
import json, requests, numpy as np, pandas as pd, anndata as ad
from pathlib import Path
from scipy import sparse
from sklearn.metrics import roc_auc_score, average_precision_score

ROOT=Path("iris_response_baseline"); OUT=ROOT/"results"; OUT.mkdir(parents=True,exist_ok=True)
url="https://media.githubusercontent.com/media/Pulin-Li-Lab/IRIS-signaling-inference/fc92c14078f2a106d2fea0b715b1743c7bac167c/data/screen_data.h5ad"
p=ROOT/"screen_data.h5ad"
if not p.exists():
    with requests.get(url,stream=True,timeout=180) as r:
        r.raise_for_status()
        with open(p,"wb") as f:
            for c in r.iter_content(1024*1024):
                if c:f.write(c)
a=ad.read_h5ad(p)

pathways={
"RA":["CYP26A1","HOXB1","HNF1B","CYP26C1","HOXA1","HOXB2","HOXA3","HOXA2","HOXB3"],
"Bmp":["ID2","BMPER","ID4","ID1","BAMBI","MSX1","ID3","MSX2","SMAD7"],
"Fgf":["SPRY1","SPRY2","DUSP6","SPRY4","ETV5","ETV4","FOS","SPRY2","MYC","JUNB","DUSP14"],
"Wnt":["AXIN1","CCND1","DKK1","MYC","NOTUM","AXIN2","SP5","LEF1"],
"TgfB":["SMAD7","TWIST1","TWIST2"],
"Shh":["GLI1","PTCH1","HHIP","FOXF1","FOXF2"],
}
X=a.X.copy()
if sparse.issparse(X):
    X=X.tocsr().astype(np.float64)
    totals=np.asarray(X.sum(axis=1)).ravel()
    X=sparse.diags(1e4/np.maximum(totals,1))@X
    X.data=np.log1p(X.data)
else:
    X=np.asarray(X,dtype=float)
    X=np.log1p(X*(1e4/np.maximum(X.sum(axis=1,keepdims=True),1)))

gene_to_idx={str(g).upper():i for i,g in enumerate(a.var_names)}
res={}
for sig,genes in pathways.items():
    cname=sig+"_class"
    if cname not in a.obs: continue
    idx=[gene_to_idx[g.upper()] for g in genes if g.upper() in gene_to_idx]
    if not idx: continue
    m=X[:,idx]
    if sparse.issparse(m): m=m.toarray()
    method_score=np.asarray(m).sum(axis=1)
    sd=np.asarray(m).std(axis=1,keepdims=True); sd[sd==0]=1
    repo_score=((np.asarray(m)-np.asarray(m).mean(axis=1,keepdims=True))/sd).sum(axis=1)
    y=(a.obs[cname].astype(str)=="Stim").to_numpy().astype(int)
    if len(np.unique(y))<2: continue
    res[sig]={
      "n":int(len(y)),
      "stim":int(y.sum()),
      "genes_used":[str(a.var_names[i]) for i in idx],
      "methods_sum_auroc":float(roc_auc_score(y,method_score)),
      "methods_sum_auprc":float(average_precision_score(y,method_score)),
      "repo_zsum_auroc":float(roc_auc_score(y,repo_score)),
      "repo_zsum_auprc":float(average_precision_score(y,repo_score)),
      "repo_zsum_max_abs":float(np.max(np.abs(repo_score))),
      "repo_zsum_sd":float(np.std(repo_score)),
    }
out={
  "historical_h5ad_shape":[int(a.n_obs),int(a.n_vars)],
  "result":res,
  "interpretation_boundary":"The Nature Methods text specifies a sum of log-normalized response-gene expression. The released GitHub response_gene() performs within-cell z-scoring across response genes before summing. This audit compares those two formulas on the recovered historical public h5ad; it does not prove which private analysis code produced the published figures."
}
(OUT/"report.json").write_text(json.dumps(out,indent=2))
with open(OUT/"REPORT.md","w") as f:
    f.write("# IRIS response-gene baseline formula audit\n\n")
    f.write(out["interpretation_boundary"]+"\n\n")
    for s,v in res.items():
        f.write("## "+s+"\n")
        for k,val in v.items(): f.write("- **"+str(k)+"**: "+str(val)+"\n")
print(json.dumps(out,indent=2))
