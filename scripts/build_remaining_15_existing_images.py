import argparse
import json
import pathlib
import shutil

DATASET_ROOT = pathlib.Path("datasets/validated-llm-v0.1")
TARGETS = {"003","004","010","012","015","016","017","018","020","021","022","024","025","029","030"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pack", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    pack = json.loads(pathlib.Path(a.pack).read_text())
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {
        "coordinate_space": "source-page",
        "source": "existing-validated-llm-image",
        "review_state": "pending-human-qa",
        "training_ground_truth": False,
        "items": [],
    }
    seen = set()
    for item in pack.get("items", []):
        qid = str(item.get("item_id") or "")
        num = qid.rsplit("-", 1)[-1]
        if num not in TARGETS:
            continue
        if num in seen:
            raise SystemExit(f"duplicate target {num}")
        project = item.get("project_group_id")
        image_path = item.get("image_path")
        if not project or not image_path:
            raise SystemExit(f"{qid}: missing project_group_id or image_path")
        rel = pathlib.PurePosixPath(image_path)
        try:
            rel = rel.relative_to(project)
        except ValueError:
            pass
        src = DATASET_ROOT / project / pathlib.Path(rel.as_posix())
        if not src.is_file():
            raise SystemExit(f"{qid}: missing existing image {src}")
        ext = src.suffix.lower()
        if ext not in {".png", ".jpg", ".jpeg"}:
            raise SystemExit(f"{qid}: unsupported image type {ext}")
        dst = out / f"{qid}__{project}{ext}"
        shutil.copy2(src, dst)
        seen.add(num)
        manifest["items"].append({\n            "item_id": qid,
            "project_group_id": project,
            "image_path": image_path,
            "source_file": str(src),
            "artifact_file": dst.name,
            "review_state": "pending-human-qa",
            "training_ground_truth": False,
        })
    missing = sorted(TARGETS - seen)
    if missing or len(seen) != 15:
        raise SystemExit(f"expected 15 targets, copied={len(seen)}, missing={missing}")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("EXISTING-IMAGE PASS 15/15")


if __name__ == "__main__":
    main()
