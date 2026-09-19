#!/usr/bin/env python3
import json, tarfile, hashlib, re
from pathlib import Path
import requests
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score
import mygene

ROOT=Path("iris_external_bmp")
OUT=ROOT/"results"
OUT.mkdir(parents=True,exist_ok=True)

GEO_BASE="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE114nnn/GSE114988/suppl/"
BMP_GENES=["ID2","BMPER","ID4","ID1","BAMBI","MSX1","ID3","MSX2","SMAD7"]

def download(url,path):
    path=Path(path)
    if path.exists() and path.stat().st_size>0:
        return path
    with requests.get(url,stream=True,timeout=180) as r:
        r.raise_for_status()
        with open(path,"wb") as f:
            for c in r.iter_content(1024*1024):
                if c:f.write(c)
    return path

def map_genes(ids):
    ids=[str(x) for x in ids]
    # direct symbol hits first
    out={}
    upper={x.upper():x for x in ids}
    for g in BMP_GENES:
        if g.upper() in upper:
            out[upper[g.upper()]]=g
    unresolved=[x for x in ids if x not in out]
    if not unresolved:
        return out,{"mode":"direct_symbol","mapped":len(out)}

    # infer namespace
    probe=unresolved[:100]
    ens_frac=sum(x.upper().split(".")[0].startswith("ENSMUSG") for x in probe)/max(1,len(probe))
    num_frac=sum(re.fullmatch(r"\d+",x) is not None for x in probe)/max(1,len(probe))
    mg=mygene.MyGeneInfo()
    if ens_frac>0.5:
        clean=[x.split(".")[0] for x in unresolved]
        q=mg.querymany(clean,scopes="ensembl.gene",fields="symbol",species="mouse",as_dataframe=False,returnall=False,verbose=False)
        for src,res in zip(unresolved,q):
            sym=res.get("symbol") if isinstance(res,dict) else None
            if sym: out[src]=str(sym)
        mode="ensembl.gene"
    elif num_frac>0.5:
        q=mg.querymany(unresolved,scopes="entrezgene",fields="symbol",species="mouse",as_dataframe=False,returnall=False,verbose=False)
        for src,res in zip(unresolved,q):
            sym=res.get("symbol") if isinstance(res,dict) else None
            if sym: out[src]=str(sym)
        mode="entrezgene"
    else:
        # generic exact query as last resort
        q=mg.querymany(unresolved,scopes="symbol,ensembl.gene,entrezgene",fields="symbol",species="mouse",as_dataframe=False,returnall=False,verbose=False)
        for src,res in zip(unresolved,q):
            sym=res.get("symbol") if isinstance(res,dict) else None
            if sym: out[src]=str(sym)
        mode="generic"
    return out,{"mode":mode,"mapped":len(out),"total":len(ids)}

rawtar=download(GEO_BASE+"GSE114988_RAW.tar",ROOT/"GSE114988_RAW.tar")
bcfile=download(GEO_BASE+"GSE114988_Cellseq2barcodes.csv.gz",ROOT/"GSE114988_Cellseq2barcodes.csv.gz")
readme=download(GEO_BASE+"GSE114988_readme.txt",ROOT/"GSE114988_readme.txt")
extract=ROOT/"raw"
extract.mkdir(exist_ok=True)
if not any(extract.iterdir()):
    with tarfile.open(rawtar) as t:t.extractall(extract)

bc=pd.read_csv(bcfile,sep="\t",header=None,names=["well","barcode"],compression="gzip")
bc["well"]=pd.to_numeric(bc["well"],errors="coerce")
bc=bc.dropna(subset=["well","barcode"])
bc["well"]=bc["well"].astype(int)
barcode_to_well={str(r.barcode):int(r.well) for _,r in bc.iterrows()}

all_results=[]
gene_map_info=None
gene_map=None
first_ids=None

for p in sorted(extract.glob("*.gz")):
    try:
        df=pd.read_csv(p,sep="\t",compression="gzip",index_col=0)
    except Exception as e:
        all_results.append({"file":p.name,"error":repr(e)})
        continue

    if first_ids is None:
        first_ids=[str(x) for x in df.index[:100]]
    if gene_map is None:
        gene_map,gene_map_info=map_genes(df.index)
        # save only BMP-relevant mapping + first identifiers
        pd.DataFrame({"raw_id":list(gene_map.keys()),"symbol":list(gene_map.values())}).to_csv(OUT/"gene_map.tsv",sep="\t",index=False)

    sym_to_raw={}
    for raw,sym in gene_map.items():
        if sym.upper() in {g.upper() for g in BMP_GENES}:
            sym_to_raw.setdefault(sym.upper(),raw)
    used=[sym_to_raw[g.upper()] for g in BMP_GENES if g.upper() in sym_to_raw]
    used_syms=[gene_map[x] for x in used]

    # derive well number for each cell column
    wells=[]
    for c in df.columns:
        s=str(c)
        w=None
        if s in barcode_to_well:
            w=barcode_to_well[s]
        else:
            m=re.fullmatch(r"(\d+)(?:\.0)?",s)
            if m:
                x=int(m.group(1))
                if 1<=x<=384:w=x
            if w is None:
                # occasionally barcode may be embedded in a larger string
                for b,wb in barcode_to_well.items():
                    if b in s:
                        w=wb;break
        wells.append(w)

    mat=df.T.astype(float)
    totals=mat.sum(axis=1).replace(0,np.nan)
    if used:
        expr=np.log1p(mat[used].div(totals,axis=0)*1e4)
        score=expr.sum(axis=1)
    else:
        score=pd.Series(np.nan,index=mat.index)

    special24="JBTac1_24h" in p.name
    special4="JBTac1_d4" in p.name
    labels=[]
    classes=[]
    for w in wells:
        if special24:
            cls="24h"
        elif special4:
            cls="4d"
        elif w is None:
            cls=None
        else:
            k=((int(w)-1)%24)+1
            cls="ctrl" if k<=6 else ("24h" if k<=12 else "4d")
        classes.append(cls)
        labels.append(None if cls is None else int(cls!="ctrl"))

    tmp=pd.DataFrame({"score":score.values,"class":classes,"label":labels})
    tmp=tmp.dropna(subset=["score","label"])
    rec={
      "file":p.name,
      "shape":[int(df.shape[0]),int(df.shape[1])],
      "mapped_wells":int(sum(w is not None for w in wells)),
      "n_cells_eval":int(len(tmp)),
      "bmp_genes_used":used_syms,
      "n_bmp_genes":int(len(used_syms)),
      "class_counts":{str(k):int(v) for k,v in pd.Series(classes).value_counts(dropna=False).items()}
    }
    if len(tmp) and tmp["label"].nunique()==2:
        y=tmp["label"].astype(int).to_numpy()
        s=tmp["score"].to_numpy()
        rec["pooled_treated_vs_ctrl_auroc"]=float(roc_auc_score(y,s))
        rec["pooled_treated_vs_ctrl_auprc"]=float(average_precision_score(y,s))
        # 24h and 4d pairwise against controls
        for cls in ["24h","4d"]:
            sub=tmp[tmp["class"].isin(["ctrl",cls])].copy()
            if len(sub) and sub["class"].nunique()==2:
                yy=(sub["class"]==cls).astype(int).to_numpy()
                ss=sub["score"].to_numpy()
                rec[f"{cls}_vs_ctrl_auroc"]=float(roc_auc_score(yy,ss))
                rec[f"{cls}_vs_ctrl_auprc"]=float(average_precision_score(yy,ss))
                rec[f"{cls}_n"]=int((sub["class"]==cls).sum())
                rec["ctrl_n"]=int((sub["class"]=="ctrl").sum())
    all_results.append(rec)

report={
  "dataset":"GSE114988",
  "question":"Does the Nature Methods response-gene BMP score generalize to an independent adult mouse enteroendocrine organoid BMP4 perturbation dataset?",
  "gene_mapping":gene_map_info,
  "first_row_ids":first_ids,
  "results":all_results,
  "boundary":"This is a response-gene baseline validation, not IRIS neural-network validation. It is intended to establish whether the external dataset has usable ground-truth and a pathway signal before attempting a retrained IRIS test."
}
(OUT/"report.json").write_text(json.dumps(report,indent=2))
with open(OUT/"REPORT.md","w") as f:
    f.write("# IRIS external BMP response-gene gate\n\n")
    f.write(report["question"]+"\n\n")
    f.write(f"- Gene mapping: {gene_map_info}\n")
    f.write(f"- First row IDs: {first_ids[:20]}\n\n")
    for r in all_results:
        f.write("## "+r.get("file","unknown")+"\n")
        for k,v in r.items():
            if k!="file": f.write(f"- **{k}**: {v}\n")
        f.write("\n")
    f.write("## Boundary\n"+report["boundary"]+"\n")
print(json.dumps(report,indent=2)[:30000])
