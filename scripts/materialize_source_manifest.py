#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

IMAGE_EXTS={".png",".jpg",".jpeg",".tif",".tiff"}

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--input-root",default="datasets/validated-llm-v0.1")
    a.add_argument("--dataset-id",default="validated-llm-source-v0.2-candidate")
    a.add_argument("--output",default="datasets/source-drawings/validated-llm-source-v0.2-candidate/manifest.jsonl")
    args=a.parse_args()
    root=Path(args.input_root); out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    for proj in sorted(p for p in root.iterdir() if p.is_dir()):
        prov={}
        pp=proj/"provenance.json"
        if pp.is_file():
            try: prov=json.loads(pp.read_text(encoding="utf-8"))
            except Exception: prov={}
        for img in sorted(proj.rglob("images/*")):
            if not img.is_file() or img.suffix.lower() not in IMAGE_EXTS: continue
            rel=img.relative_to(root).as_posix()
            parts=set(img.parts)
            role="plan" if "plans" in parts else ("vertical-reference" if "elevations-sections" in parts else "unclassified")
            sh=sha256(img)
            rows.append({"dataset_id":args.dataset_id,"project_group_id":proj.name,"source_id":"sha256:"+sh,"page_id":img.stem,"filename":img.name,"sha256":sh,"size_bytes":img.stat().st_size,"source_path":rel,"page_role":role,"coordinate_space":"source-page","legacy_provenance":{"source":prov.get("source"),"status":prov.get("status")}})
    with out.open("w",encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r,sort_keys=True)+"\n")
    print(f"Wrote {len(rows)} source assets across {len({r["project_group_id"] for r in rows})} projects")

if __name__=="__main__": main()
