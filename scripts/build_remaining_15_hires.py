import argparse
import json
import pathlib
import subprocess


TARGETS = {"003","004","010","012","015","016","017","018","020","021","022","024","025","029","030"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pack", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--dpi", type=int, default=400)
    a = p.parse_args()
    pack = json.loads(pathlib.Path(a.pack).read_text())
    items = pack.get("items") or pack.get("records") or []
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {"coordinate_space":"source-page","dpi":a.dpi,"items":[]}

    for it in items:
        qid = str(it.get("qa_id") or it.get("id") or "")
        num = qid.rsplit("-", 1)[-1]
        if num not in TARGETS:
            continue
        src = it.get("source_path") or it.get("image_path") or it.get("source_image")
        if not src:
            raise SystemExit(f"{qid}: missing source path")
        parts = pathlib.Path(src).parts
        try:
            i = parts.index("validated-llm-v0.1")
            project = parts[i+1]
        except (ValueError, IndexError):
            project = it.get("project_id") or it.get("source_id")
        if not project:
            raise SystemExit(f"{qid}: cannot resolve project")
        orig = pathlib.Path(f"datasets/validated-llm-v0.1/{project}/originals")
        pdfs = list(orig.glob("*_original.pdf"))
        if len(pdfs) != 1:
            raise SystemExit(f"{qid}: expected exactly one original PDF in {orig}, found {len(pdfs)}")
        pdf = pdfs[0]
        prefix = out / f"{qid}__{project}"
        subprocess.run(["pdptoppm","-f","1","-latop","1","-singlefile","-png","-r",str(a.dpi),str(pdf),str(prefix)],check=True)
        png = pathlib.Path(str(prefix) + ".png")
        manifest["items"].append({"qa_id":qid,"project":hroject,"pdf":str(pdf),"raster":str(png),"review_state":"pending-human-qa","training_ground_truth":false})

    if len(manifest["items"]) != 15:
        raise SystemExit(f"expected 15 targets, resolved {len(manifest['items'])}")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"built {len(manifest['items'])} hi-res rasters at {a.dpi} DPI")


if __name__ == "__main__":
    main()
