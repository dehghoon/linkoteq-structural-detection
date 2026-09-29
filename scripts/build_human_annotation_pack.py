#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


ALLOWED_CLASSES = ["column", "beam", "wall"]


def build_pack(manifest: dict, run_id: str) -> dict:
    items = []
    for i, entry in enumerate(manifest["representatives"], 1):
        rep = entry["representative"]
        image_path = rep["image_path"]
        stem = image_path[:-4] if image_path.lower().endswith(".png") else image_path
        items.append({
            "item_id": f"qa-{run_id}-{i:03d}",
            "sha256": entry["sha256"],
            "project_group_id": rep["project_group_id"],
            "image_path": image_path,
            "source_path": f"runs/{run_id}/images/source/{image_path}",
            "preview_path": f"runs/{run_id}/images/previews/{stem}.jpg",
            "alias_count": entry["alias_count"],
            "aliases": entry["aliases"],
            "coordinate_space": "source-page",
            "allowed_classes": ALLOWED_CLASSES,
            "review_state": "pending-human-qa",
            "annotations": [],
            "review_notes": [],
        })
    return {
        "pack_type": "human-annotation-pack",
        "spec_version": "0.2",
        "contract_id": "candidate-qa-gates-v0.2",
        "source_run_id": run_id,
        "source_record_count": manifest["source_record_count"],
        "unique_review_count": manifest["unique_review_count"],
        "allowed_classes": ALLOWED_CLASSES,
        "coordinate_space": "source-page",
        "review_state": "pending-human-qa",
        "annotation_geometry": "tight-axis-aligned-box",
        "items": items,
        "policy": {
            "annotations_start_empty": True,
            "no_auto_approval": True,
            "wall_requires_human_qa": True,
            "no_hidden_continuation_inference": True,
            "candidate_never_equals_ground_truth": True,
            "enables_training": False,
            "emits_canonical_engineering_geometry": False,
        },
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--unique-manifest", required=True, type=Path)
    p.add_argument("--run-id", required=True)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    manifest = json.loads(args.unique_manifest.read_text(encoding="utf-8"))
    pack = build_pack(manifest, args.run_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(pack, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"item_count": len(pack["items"]), "review_state": pack["review_state"]}, sort_keys=True))


if __name__ == "__main__":
    main()
