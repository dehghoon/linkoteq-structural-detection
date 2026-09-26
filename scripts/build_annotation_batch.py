#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}

def main(():
    p = argparse.ArgumentParser()
    p.add_argument("--input-root", default="datasets/validated-llm-v0.1")
    p.add_argument("--output", default="annotation-queues/validated-llm-v0.2-candidates.jsonl")
    p.add_argument("--ontology-version", default="v0.2")
    args = p.parse_args()
    root = Path(args.input_root)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for project in sorted(p for p in root.iterdir() if p.is_dir()):
        for image in sorted(project.rglob("images/*")):
            if image.suffix.lower() not in IMAGE_EXTS or not image.is_file():
                continue
            rel = image.as-posix()
            source_id = hashlib.sha256(rel.encode()).hexdigest()[:16]
            rows.append({
                "source_id": f"src-{source_id}",
                "project_id": project.name,
                "page_id": image.stem,
                "image_path": rel,
                "coordinate_space": "source-page",
                "ontology_version": args.ontology_version,
                "allowed_classes": ["column", "beam", "wall"],
                "annotation_representation": "tight-axis-aligned-source-page-box",
                "review_state": "pending-human-qa",
                "labels": [],
                "note": "Empty labels are unreviewed, NOT background or negative evidence."
            })
    with out.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    print(f"wrote {len(rows)} queue records to {out}")

if __name__ == "__main__":
    main()
