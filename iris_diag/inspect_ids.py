#!/usr/bin/env python3
import tarfile, requests, pandas as pd, anndata as ad
from pathlib import Path
R=Path("iris_diag"); R.mkdir(exist_ok=True)
def dl(u,p):
    p=Path(p)
    with requests.get(u,stream=True,timeout=180) as r:
        r.raise_for_status()
        with open(p,"wb") as f:
            for c in r.iter_content(1024*1024):
                if c:f.write(c)
h=R/"screen.h5ad"; dl("https://media.githubusercontent.com/media/Pulin-Li-Lab/IRIS-signaling-inference/fc92c14078f2a106d2fea0b715b1743c7bac167c/data/screen_data.h5ad",h)
a=ad.read_h5ad(h,backed="r")
print("TRAIN_VAR_HEAD",list(map(str,a.var_names[:80])))
print("TRAIN_VAR_COLS",list(map(str,a.var.columns)))
if len(a.var.columns):
    print("TRAIN_VAR_TABLE",a.var.head(20).to_dict())
print("SPECIES",a.obs["species"].astype(str).value_counts().to_dict())
a.file.close()
raw=R/"raw.tar"; dl("https://ftp.ncbi.nlm.nih.gov/geo/series/GSE114nnn/GSE114988/suppl/GSE114988_RAW.tar",raw)
with tarfile.open(raw) as t:t.extractall(R/"raw")
p=R/"raw"/"GSM3496194_JB-TAC-CRE1_AHNVLHBGX2_S1_R2.TranscriptCounts.tsv.gz"
d=pd.read_csv(p,sep="\t",compression="gzip",index_col=0,nrows=100)
print("EXT_GENE_HEAD",list(map(str,d.index[:80])))
print("EXT_COL_HEAD",list(map(str,d.columns[:30])))
