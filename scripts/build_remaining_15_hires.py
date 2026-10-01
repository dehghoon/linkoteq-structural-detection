import argparse
import json
import pathlib
import subprocess

TARGETS = {"003","004","010","012","015","016","017","018","020","021","022","024","025","029","030"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--pack", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--dpi", type=int, default=400)
    a=p.parse_args()
    pack=json.loads(pathlib.Path(a.pack).read_text())
    items=pack.get("items") or []
    out=pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    manifest={"coordinate_space":"source-page","dpi":a.dpi,"items":[]}
    for it in items:
        qid=str(it.get("item_id") or "")
        num=qid.rsplit("-",1)[-1]
        if num not in TARGETS: continue
        project=it.get("project_group_id")
        image_path=it.get("image_path")
        if not project or not image_path:
            raise SystemExit(f"{qid}: missing project_group_id or image_path")
        if not image_path.startswith(project + "/"):
            raise SystemExit(f"{qid}: image_path/project mismatch")
        orig=pathlib.Path(f"datasets/validated-llm-v0.1/{project}/originals")
        pdfs=list(orig.glob("*_original.pdf"))
        if len(pdfs)!=1:
            raise SystemExit(f"{qid}: expected exactly one original PDF in {orig}, found {len(pdfs)}")
        pdf=pdfs[0]
        prefix=out/f"{qid}__{project}"
        subprocess.run(["pdftoppm","-f","1","-l","1","-singlefile","-png","-r",str(a.dpi),str(pdf),str(prefix)],check=True)
        png=pathlib.Path(str(prefix)+".png")
        manifest["items"].append({"item_id":qid,"project_group_id":project,"image_path":image_path,"pdf":str(pdf),"raster":str(png),"review_state":"pending-human-qa","training_ground_truth":False})
    resolved={x["item_id"].rsplit("-",1)[-1] for x in manifest["items"]}
    missing=sorted(TARGETS-resolved)
    if missing or len(manifest["items"])!=15:
        raise SystemExit(f"expected 15 targets, resolved {len(manifest['items'])}; missing={missing}")
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(f"built 15 hi-res rasters at {a.dpi} DPI")

if __name__=="__main__":
    main()
