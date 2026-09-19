#!/usr/bin/env python3
import re, json, tarfile, warnings
from pathlib import Path
import requests, numpy as np, pandas as pd, anndata as ad
from scipy import sparse
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
warnings.filterwarnings("ignore")
ROOT=Path("iris_stage2"); OUT=ROOT/"results"; OUT.mkdir(parents=True,exist_ok=True)
R={"status":"STARTED"}
def download(url,path,chunk=1024*1024):
    path=Path(path)
    if path.exists() and path.stat().st_size>0: return path
    with requests.get(url,stream=True,timeout=180) as r:
        r.raise_for_status()
        with open(path,"wb") as f:
            for c in r.iter_content(chunk_size=chunk):
                if c: f.write(c)
    return path

# Recovered historical processed screen data.
h5=ROOT/"screen_data.h5ad"
download("https://media.githubusercontent.com/media/Pulin-Li-Lab/IRIS-signaling-inference/fc92c14078f2a106d2fea0b715b1743c7bac167c/data/screen_data.h5ad",h5)
a=ad.read_h5ad(h5)
R["train_shape"]=[int(a.n_obs),int(a.n_vars)]
R["train_var_head"]=list(map(str,a.var_names[:30]))
R["train_var_columns"]=list(map(str,a.var.columns))
R["species_counts"]={str(k):int(v) for k,v in a.obs["species"].astype(str).value_counts().items()}
R["celltype_top"]={str(k):int(v) for k,v in a.obs["celltype"].astype(str).value_counts().head(20).items()}
R["bmp_counts"]={str(k):int(v) for k,v in a.obs["Bmp_class"].astype(str).value_counts().items()}

# Independent distant-domain BMP4 enteroendocrine-organoid data.
base="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE114nnn/GSE114988/suppl/"
raw=ROOT/"GSE114988_RAW.tar"; download(base+"GSE114988_RAW.tar",raw)
exdir=ROOT/"GSE114988_RAW"; exdir.mkdir(exist_ok=True)
if not any(exdir.iterdir()):
    with tarfile.open(raw) as t: t.extractall(exdir)
mapf=ROOT/"GSE114988_Cellseq2barcodes.csv.gz"
download(base+"GSE114988_Cellseq2barcodes.csv.gz",mapf)
bm=pd.read_csv(mapf,sep="\t",header=None,names=["well","barcode"],compression="gzip")
bm["well"]=pd.to_numeric(bm["well"],errors="coerce"); bm=bm.dropna()
barcode_to_well={str(b).strip():int(w) for w,b in zip(bm["well"],bm["barcode"])}

p=exdir/"GSM3496194_JB-TAC-CRE1_AHNVLHBGX2_S1_R2.TranscriptCounts.tsv.gz"
df=pd.read_csv(p,sep="\t",compression="gzip",index_col=0)
R["external_raw_shape"]=[int(df.shape[0]),int(df.shape[1])]
R["external_gene_head"]=list(map(str,df.index[:30]))
R["external_col_head"]=list(map(str,df.columns[:30]))
def resolve_well(c):
    s=str(c).strip()
    if s in barcode_to_well: return barcode_to_well[s]
    for tok in re.split(r"[^A-Za-z0-9]+",s):
        if tok in barcode_to_well: return barcode_to_well[tok]
    hits=[w for b,w in barcode_to_well.items() if b in s]
    if len(hits)==1: return hits[0]
    m=re.search(r"(?:^|[^0-9])(\d{1,3})(?:[^0-9]|$)",s)
    if m:
        x=int(m.group(1))
        if 1<=x<=384: return x
    return None
wells=[resolve_well(c) for c in df.columns]
R["external_wells_resolved"]=int(sum(x is not None for x in wells))
labels=[]; times=[]; keep_cols=[]
for c,w in zip(df.columns,wells):
    if w is None: continue
    pos=((w-1)%24)+1
    if pos<=6: y=0; t="untreated"
    elif pos<=12: y=1; t="24h"
    else: y=1; t="4d"
    labels.append(y); times.append(t); keep_cols.append(c)
if len(keep_cols)<100: raise RuntimeError("Could not resolve enough external wells")
ext=df[keep_cols].T
tot=ext.sum(axis=1); valid=(tot>100).to_numpy()
ext=ext.loc[valid]
y=np.array(labels)[valid]; times=np.array(times)[valid]
R["external_cells_after_qc"]=int(ext.shape[0])
R["external_time_counts"]={str(k):int(v) for k,v in pd.Series(times).value_counts().items()}

# Map external IDs into the historical training namespace.
train_names=pd.Index(a.var_names.astype(str)); ext_names=pd.Index(ext.columns.astype(str))
train_ens_frac=float(np.mean(train_names.str.startswith(("ENSMUSG","ENSG"))))
ext_ens_frac=float(np.mean(ext_names.str.startswith(("ENSMUSG","ENSG"))))
R["train_ensembl_fraction"]=train_ens_frac; R["external_ensembl_fraction"]=ext_ens_frac
train_base=pd.Index([x.split(".")[0] for x in train_names]); ext_base=pd.Index([x.split(".")[0] for x in ext_names])
direct=set(train_base).intersection(set(ext_base)); R["direct_common_genes"]=len(direct)
mapped_symbols={}
if len(direct)<500 and ext_ens_frac>0.5:
    import mygene
    mg=mygene.MyGeneInfo()
    qr=mg.querymany(list(dict.fromkeys(ext_base.tolist())),scopes="ensembl.gene",fields="symbol",species="mouse",as_dataframe=False,verbose=False)
    for q in qr:
        if q.get("notfound"): continue
        if q.get("symbol"): mapped_symbols[str(q["query"])]=str(q["symbol"])
    R["external_mapped_symbols"]=len(mapped_symbols)
if len(direct)>=500:
    tk={b:i for i,b in enumerate(train_base)}; ek={b:i for i,b in enumerate(ext_base)}
    common=sorted(direct); train_idx=[tk[g] for g in common]; ext_idx=[ek[g] for g in common]
    common_names=common; mode="direct_id"
else:
    tk={str(x).upper():i for i,x in enumerate(train_names)}
    ek={}
    for i,b in enumerate(ext_base):
        s=mapped_symbols.get(str(b))
        if s: ek.setdefault(s.upper(),i)
    common=sorted(set(tk).intersection(ek))
    train_idx=[tk[g] for g in common]; ext_idx=[ek[g] for g in common]
    common_names=common; mode="ensembl_to_symbol"
R["mapping_mode"]=mode; R["common_gene_count"]=len(common_names); R["common_gene_head"]=common_names[:30]
if len(common_names)<1000: raise RuntimeError("Too few common genes: "+str(len(common_names)))

# Balanced training subset and normalized classifier benchmark.
mouse=(a.obs["species"].astype(str).str.lower()=="mouse").to_numpy()
if mouse.sum()<1000: mouse=np.ones(a.n_obs,dtype=bool)
yb=(a.obs["Bmp_class"].astype(str)=="Stim").to_numpy()
pool=np.where(mouse)[0]; rng=np.random.default_rng(13); rows=[]
for cls in [0,1]:
    z=pool[yb[pool]==cls]; n=min(len(z),2500); rows.extend(rng.choice(z,size=n,replace=False).tolist())
rows=np.array(sorted(rows)); R["training_cells_used"]=int(len(rows))
R["training_class_counts"]={str(k):int(v) for k,v in pd.Series(yb[rows].astype(int)).value_counts().items()}
Xsrc=a.layers["counts"] if "counts" in a.layers else a.X
Xt=Xsrc[rows,:][:,train_idx]
if sparse.issparse(Xt): Xt=Xt.tocsr().astype(np.float32)
else: Xt=np.asarray(Xt,dtype=np.float32)
Xe=ext.iloc[:,ext_idx].to_numpy(dtype=np.float32)
if sparse.issparse(Xt):
    sums=np.asarray(Xt.sum(axis=1)).ravel()
    Xt=sparse.diags(1e4/np.maximum(sums,1))@Xt; Xt.data=np.log1p(Xt.data)
    mean=np.asarray(Xt.mean(axis=0)).ravel(); mean2=np.asarray(Xt.power(2).mean(axis=0)).ravel()
    var=np.maximum(mean2-mean**2,0)
else:
    Xt=np.log1p(Xt*(1e4/np.maximum(Xt.sum(axis=1,keepdims=True),1))); var=np.var(Xt,axis=0)
Xe=np.log1p(Xe*(1e4/np.maximum(Xe.sum(axis=1,keepdims=True),1)))
hvg=np.argsort(var)[-min(2000,len(var)):]; R["hvg_count"]=int(len(hvg))
Xt2=Xt[:,hvg]; Xe2=Xe[:,hvg]
clf=make_pipeline(StandardScaler(with_mean=False),LogisticRegression(max_iter=1500,class_weight="balanced",solver="liblinear"))
clf.fit(Xt2,yb[rows].astype(int)); proba=clf.predict_proba(Xe2)[:,1]
R["linear_external_auroc"]=float(roc_auc_score(y,proba)); R["linear_external_auprc"]=float(average_precision_score(y,proba))
for tt in ["24h","4d"]:
    m=np.isin(times,["untreated",tt]); yy=(times[m]==tt).astype(int)
    R["linear_"+tt+"_auroc"]=float(roc_auc_score(yy,proba[m])); R["linear_"+tt+"_auprc"]=float(average_precision_score(yy,proba[m]))
pd.DataFrame({"cell":ext.index,"truth_bmp":y,"time":times,"linear_score":proba}).to_csv(OUT/"external_predictions_linear.csv",index=False)

# Released response-gene formula versus a sensible gene-wise signature.
bmp=["ID2","BMPER","ID4","ID1","BAMBI","MSX1","ID3","MSX2","SMAD7"]
if mode=="ensembl_to_symbol":
    sym2idx={}
    for i,b in enumerate(ext_base):
        s=mapped_symbols.get(str(b))
        if s: sym2idx.setdefault(s.upper(),i)
    avail=[g for g in bmp if g in sym2idx]
    R["bmp_signature_genes_available"]=avail
    if len(avail)>=3:
        raw_all=ext.to_numpy(dtype=np.float32)
        Xsig=raw_all[:,[sym2idx[g] for g in avail]]
        Xn=np.log1p(Xsig*(1e4/np.maximum(raw_all.sum(axis=1,keepdims=True),1)))
        sd=Xn.std(axis=0,keepdims=True); sd[sd==0]=1
        sensible=((Xn-Xn.mean(axis=0,keepdims=True))/sd).mean(axis=1)
        R["sensible_signature_auroc"]=float(roc_auc_score(y,sensible)); R["sensible_signature_auprc"]=float(average_precision_score(y,sensible))
        rsd=Xn.std(axis=1,keepdims=True); rsd[rsd==0]=1
        released=((Xn-Xn.mean(axis=1,keepdims=True))/rsd).sum(axis=1)
        R["released_formula_max_abs"]=float(np.max(np.abs(released))); R["released_formula_sd"]=float(np.std(released))

# One-signal IRIS-style SCVI/SCANVI transfer smoke test. Published pretrained weights are unavailable.
try:
    import scvi
    rows2=[]
    for cls in [0,1]:
        z=pool[yb[pool]==cls]; n=min(len(z),1500); rows2.extend(rng.choice(z,size=n,replace=False).tolist())
    rows2=np.array(sorted(rows2))
    Xtr=Xsrc[rows2,:][:,train_idx][:,hvg]
    if sparse.issparse(Xtr): Xtr=Xtr.tocsr().astype(np.float32)
    else: Xtr=sparse.csr_matrix(np.asarray(Xtr,dtype=np.float32))
    Xex=sparse.csr_matrix(ext.iloc[:,ext_idx].to_numpy(dtype=np.float32)[:,hvg])
    Xall=sparse.vstack([Xtr,Xex],format="csr")
    ot=pd.DataFrame(index=["tr_"+str(i) for i in range(len(rows2))])
    ot["batch"]=a.obs.iloc[rows2]["batch"].astype(str).to_numpy()
    ot["celltype"]=a.obs.iloc[rows2]["celltype"].astype(str).to_numpy()
    ot["Bmp_class"]=np.where(yb[rows2],"Stim","Ctrl")
    oe=pd.DataFrame(index=["ext_"+str(i) for i in range(len(ext))])
    oe["batch"]="external_EEC"; oe["celltype"]="external_EEC"; oe["Bmp_class"]="unknown"
    obs=pd.concat([ot,oe])
    for c in ["batch","celltype","Bmp_class"]: obs[c]=obs[c].astype("category")
    aa=ad.AnnData(X=Xall,obs=obs,var=pd.DataFrame(index=[common_names[i] for i in hvg])); aa.layers["counts"]=aa.X.copy()
    scvi.settings.seed=13
    scvi.model.SCVI.setup_anndata(aa,layer="counts",batch_key="batch",categorical_covariate_keys=["celltype"])
    vae=scvi.model.SCVI(aa,n_layers=2,n_latent=20,n_hidden=128,gene_likelihood="zinb")
    vae.train(max_epochs=20,validation_size=0.1,early_stopping=True,check_val_every_n_epoch=1)
    scan=scvi.model.SCANVI.from_scvi_model(vae,labels_key="Bmp_class",unlabeled_category="unknown")
    scan.train(max_epochs=8,check_val_every_n_epoch=1)
    pp=scan.predict(aa[-len(ext):],soft=True)
    sp=pp["Stim"].to_numpy() if isinstance(pp,pd.DataFrame) and "Stim" in pp.columns else np.asarray(pp).reshape(-1)
    R["iris_retrained_external_auroc"]=float(roc_auc_score(y,sp)); R["iris_retrained_external_auprc"]=float(average_precision_score(y,sp))
    for tt in ["24h","4d"]:
        m=np.isin(times,["untreated",tt]); yy=(times[m]==tt).astype(int)
        R["iris_retrained_"+tt+"_auroc"]=float(roc_auc_score(yy,sp[m])); R["iris_retrained_"+tt+"_auprc"]=float(average_precision_score(yy,sp[m]))
    pd.DataFrame({"cell":ext.index,"truth_bmp":y,"time":times,"iris_score":sp}).to_csv(OUT/"external_predictions_iris_retrained.csv",index=False)
    R["iris_retrained_status"]="SUCCESS"
    R["iris_retrained_boundary"]="One-signal retraining of intended SCVI/SCANVI architecture; not the unavailable published pretrained model."
except Exception as e:
    R["iris_retrained_status"]="FAILED"; R["iris_retrained_error"]=repr(e)

iris=R.get("iris_retrained_external_auroc"); lin=R.get("linear_external_auroc")
if iris is not None and iris>=0.75: decision="PROMISING_EXTERNAL_GENERALIZATION"
elif lin is not None and lin>=0.75 and R.get("iris_retrained_status")!="SUCCESS": decision="DATASET_SIGNAL_PRESENT_BUT_IRIS_REPRO_BLOCKED"
elif iris is not None and iris<0.60: decision="NEGATIVE_EXTERNAL_GENERALIZATION_SIGNAL"
else: decision="INCONCLUSIVE"
R["decision"]=decision; R["status"]="COMPLETE"
(OUT/"report.json").write_text(json.dumps(R,indent=2,sort_keys=True))
with open(OUT/"REPORT.md","w") as f:
    f.write("# IRIS distant-cell BMP external-validation smoke test\\n\\n")
    f.write("## Decision\\n\\n**"+decision+"**\\n\\n")
    f.write("Independent BMP4-stimulated intestinal enteroendocrine-organoid data: GSE114988. Published pretrained IRIS weights are not present in the current public repository, so the IRIS-style score below uses a bounded one-signal retraining smoke test and is not an exact reproduction of the published pretrained model.\\n\\n")
    keys=["train_shape","species_counts","bmp_counts","external_raw_shape","external_cells_after_qc","external_time_counts","mapping_mode","common_gene_count","training_cells_used","linear_external_auroc","linear_external_auprc","linear_24h_auroc","linear_4d_auroc","bmp_signature_genes_available","sensible_signature_auroc","released_formula_max_abs","iris_retrained_status","iris_retrained_external_auroc","iris_retrained_external_auprc","iris_retrained_24h_auroc","iris_retrained_4d_auroc","iris_retrained_boundary"]
    for k in keys:
        if k in R: f.write("- **"+k+"**: "+str(R[k])+"\\n")
    f.write("\\n## Boundary\\nA strong score supports a broader pre-specified validation; a weak score could reflect true domain-shift failure, mapping/preprocessing mismatch, or retraining differences. Neither outcome alone establishes or refutes the published Nature Methods conclusions.\\n")
print(json.dumps(R,indent=2)[:25000])
