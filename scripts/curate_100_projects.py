#!/usr/bin/env python3
import os,re,subprocess,urllib.request,shutil
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path("datasets/web-sourced-candidates-v0.1")
OUT=ROOT/"curated-100-projects"
OUT.mkdir(parents=True,exist_ok=True)
TARGET=100
KEY_PLAN=("foundation plan","framing plan","roof framing","floor framing","structural plan","foundation & roof framing","post plan","truss & bracing")
KEY_ELEV=("building elevation","exterior elevation","structural elevation","framing elevation","building section","structural section","elevations &")
urls=[]
for md in sorted(ROOT.glob("*.md")):
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
    # Dataset copy only: mask common title-block zones while retaining the source URL in provenance.
    d.rectangle((0,int(h*.925),w,h),fill="white")
    d.rectangle((int(w*.89),int(h*.68),w,h),fill="white")
    return im

MAN=ROOT/"curated-100-projects-manifest.tsv"
manifest=[x for x in MAN.read_text(errors="ignore").splitlines() if x.strip()] if MAN.exists() else []
existing_urls={x.split("\t")[1] for x in manifest if "\t" in x}
accepted=len(manifest)

for u in seen:
    if accepted>=TARGET: break
    if u in existing_urls: continue
    pid=f"project-{accepted+1:03d}"
    pdir=OUT/pid
    pdir.mkdir(exist_ok=True)
    pdf=pdir/"source.pdf"
    try:
        req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=20) as r:
            data=r.read(80_000_000)
        if not data.startswith(b"%PDF"): raise ValueError("not direct PDF")
        pdf.write_bytes(data)
    except Exception:
        shutil.rmtree(pdir,ignore_errors=True); continue
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
        shutil.rmtree(pdir,ignore_errors=True); continue
    selected=[("plan",plan[0]),("elevation",elev[0])]
    for kind,pn in selected:
        # Save selected original page PDF.
        sh("pdfseparate","-f",str(pn),"-l",str(pn),str(pdf),str(pdir/f"{kind}-page-%d.pdf"))
        rawpage=pdir/f"{kind}-page-{pn}.pdf"
        if rawpage.exists(): rawpage.rename(pdir/f"{kind}-original.pdf")
        # Render, mask title-block area, then save a clean PDF copy.
        prefix=pdir/f"{kind}-clean"
        sh("pdftoppm","-f",str(pn),"-singlefile","-r","180","-png",str(pdf),str(prefix))
        png=prefix.with_suffix(".png")
        if png.exists():
            im=Image.open(png).convert("RGB")
            mask_title(im).save(png,optimize=True)
            im=Image.open(png).convert("RGB")
            im.save(pdir/f"{kind}-clean.pdf","PDF",resolution=180.0)
            png.unlink(missing_ok=True)
    pdf.unlink(missing_ok=True); txt.unlink(missing_ok=True)
    (pdir/"provenance.txt").write_text(f"source_url={u}\nplan_page={plan[0]}\nelevation_page={elev[0]}\n")
    manifest.append(f"{pid}\t{u}\tplan={plan[0]}\televation={elev[0]}")
    MAN.write_text("\n".join(manifest)+"\n")
    accepted+=1
    existing_urls.add(u)

print(f"Materialized {accepted}/{TARGET} projects with original selected-page PDFs and title-block-masked clean PDFs.",flush=True)
