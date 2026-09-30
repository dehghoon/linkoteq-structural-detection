#!/usr/bin/env python3
import json, shutil
from pathlib import Path

PACK = Path("runs/36530901509/images/human-annotation-pack.json")
OUT = Path("runs/36530901509/review-batches/remaining-29/work")

data = json.loads(PACK.read_text())
assert data["spec_version"] == "0.2"
assert data["coordinate_space"] == "source-page"
assert data["allowed_classes"] == ["column", "beam", "wall"]
items = [x for x in data["items"] if x["item_id"] != "qa-36530901509-002"]
assert len(items) == 29, f"expected 29, got {len(items)}"
(OUT / "images").mkdir(parents=True, exist_ok=True)

materialized = []
for x in items:
    src = Path(x["preview_path"])
    if not src.is_file():
        raise SystemExit(f"missing preview: {src}")
    dst = OUT / "images" / f"{x['item_id']}{src.suffix.lower()}"
    shutil.copy2(src, dst)
    materialized.append({
        "item_id": x["item_id"],
        "project_group_id": x["project_group_id"],
        "image_path": x["image_path"],
        "source_path": x["source_path"],
        "preview_path": x["preview_path"],
        "materialized_image": str(dst),
        "source_sha256": x["sha256"],
        "coordinate_space": "source-page",
        "review_state": "candidate-pending-human-qa",
        "annotations": []
    })

manifest = {
    "batch_id": "remaining-29-v0.2",
    "source_run_id": "36530901509",
    "spec_version": "0.2",
    "allowed_classes": ["column", "beam", "wall"],
    "annotation_geometry": "tight-axis-aligned-box",
    "coordinate_space": "source-page",
    "candidate_never_equals_ground_truth": True,
    "training_enabled": False,
    "items": materialized
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
