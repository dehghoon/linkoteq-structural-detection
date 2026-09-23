#!/usr/bin/env python3
import os,re,subprocess,hashlib,urllib.request
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path("datasets/web-sourced-candidates-v0.1")
OUT=ROOT/"curated-28-projects"
OUT.mkdir(parents=True,exist_ok=True)
KEY_PLAN=("foundation plan","framing plan","roof framing","floor framing","structural plan")
KEY_ELEV=("building elevation","exterior elevation","structural elevation","framing elevation","building section","structural section")
urls=[]
for md in ROOT.glob("*.md"):
    txt=md.read_text(errors="ignore")
    urls += re.findall(r'https?://[^\s)]+',txt)
seen=[]
for u in urls:
    u=u.rstrip('.,;')
    if u not in seen: seen.append(u)

def sh(*a):
    return subprocess.run(a,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

def mask_title(im):
    w,h=im.size
    d=ImageDraw.Draw(im)
    # common full-width bottom title strip
    d.rectangle((0,int(h*.90),w,h),fill="white")
    # common lower-right vertical title block
    d.rectangle((int(w*.86),int(h*.62),w,h),fill="white")
    return im

accepted=0
manifest=[]
EXISTING_MANIFEST=ROOT/"curated-28-projects-manifest.tsv"
existing=[]
if EXISTING_MANIFEST.exists():
    existing=[x for x in EXISTING_MANIFEST.read_text(errors="ignore").splitlines() if x.strip()]
existing_urls={x.split("\t")[1] for x in existing if "\t" in x}
accepted=len(existing)
manifest=list(existing)

for idx,u in enumerate(seen,1):
    if u in existing_urls:
        continue
    if accepted>=28: break
    pid=f"project-{accepted+1:02d}"
    pdir=OUT/pid
    pdir.mkdir(exist_ok=True)
    pdf=pdir/"source.pdf"
    try:
        req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=10) as r:
            data=r.read(45_000_000)
        if not data.startswith(b"%PDF"): raise ValueError("not direct PDF")
        pdf.write_bytes(data)
    except Exception as e:
        pdir.rmdir()
        continue
    txt=pdir/"source.txt"
    sh("pdftotext","-layout",str(pdf),str(txt))
    raw=txt.read_text(errors="ignore") if txt.exists() else ""
    pages=raw.split("\f")
    plan=[]; elev=[]
    for n,t in enumerate(pages,1):
        lo=t.lower()
        if any(k in lo for k in KEY_PLAN): plan.append(n)
        if any(k in lo for k in KEY_ELEV): elev.append(n)
    if not plan or not elev:
        for x in pdir.iterdir(): x.unlink()
        pdir.rmdir(); continue
    chosen=[("plan",plan[0]),("elevation",elev[0])]
    for kind,pn in chosen:
        prefix=pdir/f"{kind}"
        sh("pdftoppm","-f",str(pn),"-singlefile","-r","150","-png",str(pdf),str(prefix))
        png=prefix.with_suffix(".png")
        if png.exists():
            im=Image.open(png).convert("RGB")
            mask_title(im).save(png,optimize=True)
    # source PDF intentionally not committed; keep provenance URL and selected page IDs
    pdf.unlink(missing_ok=True); txt.unlink(missing_ok=True)
    (pdir/"provenance.txt").write_text(f"source_url={u}\nplan_page={plan[0]}\nelevation_page={elev[0]}\n")
    manifest.append(f"{pid}\t{u}\tplan={plan[0]}\televation={elev[0]}")
    accepted+=1

(ROOT/"curated-28-projects-manifest.tsv").write_text("\n".join(manifest)+"\n")
print(f"Materialized {accepted}/28 projects; committing successful partial results.", flush=True)
