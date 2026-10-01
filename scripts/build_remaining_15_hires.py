import argparse
import json
import pathlib
import subprocess

from remaining_15_source_resolver import resolve_sheet

TARGETS = {"003","004","010","012","015","016","017","018","020","021","022","024","025","029","030"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pack", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--dpi", type=int, default=400)
    a = p.parse_args()
    pack = json.loads(pathlib.Path(a.pack).read_text())
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {"coordinate_space": "source-page", "dpi": a.dpi, "items": []}

    for item in pack.get("items", []):
        qid = str(item.get("item_id") or "")
        num = qid.rsplit("-", 1)[-1]
        if num not in TARGETS:
            continue
        project = item.get("project_group_id")
        image_path = item.get("image_path")
        if not project or not image_path:
            raise SystemExit(f"{qid}: missing project/image metadata")
        try:
            src = resolve_sheet(project, image_path)
        except RuntimeError as e:
            raise SystemExit(f"{qid}: {e}")
        prefix = out / f"{qid}__{project}"
        page = int(src["pdf_page"])
        subprocess.run([
            "pdftoppm", "-f", str(page), "-l", str(page), "-singlefile",
            "-png", "-r", str(a.dpi), str(src["pdf"]), str(prefix)
        ], check=True)
        png = pathlib.Path(str(prefix) + ".png")
        manifest["items"].append({
            "item_id": qid,
            "project_group_id": project,
            "image_path": image_path,
            "pdf": str(src["pdf"]),
            "pdf_page": page,
            "source_page": src["source_page"],
            "sheet": src["sheet"],
            "title": src["title"],
            "resolver": src["resolver"],
            "raster": str(png),
            "review_state": "pending-human-qa",
            "training_ground_truth": False,
        })

    resolved = {x["item_id"].rsplit("-", 1)[-1] for x in manifest["items"]}
    missing = sorted(TARGETS - resolved)
    if missing or len(manifest["items"]) != 15:
        raise SystemExit(f"expected 15 targets, resolved {len(manifest['items'])}; missing={missing}")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"built 15 hi-res rasters at {a.dpi} DPI")


if __name__ == "__main__":
    main()
