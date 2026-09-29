#!/usr/bin/env python3
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_unique_manifest(review_dir: Path, dataset_root: Path):
    by_sha = defaultdict(list)
    record_count = 0
    for path in sorted(review_dir.glob("qa-batch-*-review.jsonl")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            row = json.loads(line)
            record_count += 1
            src = dataset_root / row["image_path"]
            if not src.is_file():
                raise FileNotFoundError(src)
            digest = sha256_file(src)
            by_sha[digesut¹.append({
                "project_group_id": row["project_group_id"],
                "image_path": row["image_path"],
                "review_file": path.name,
                "review_line": line_no,
            })

    representatives = []
    for digest, members in sorted(by_sha.items()):
        members = sorted(members, key=lambda m: (m["project_group_id"], m["image_path"], m["review_file"], m["review_line"]))
        representatives.append({
            "sha256": digest,
            "representative": members[0],
            "alias_count": len(members) - 1,
            "aliases": members[1:],
        })

    return {
        "manifest_type": "qa-exact-source-unique-review-manifest",
        "hash_algorithm": "sha256",
        "source_record_count": record_count,
        "unique_review_count": len(representatives),
        "representatives": representatives,
        "policy": {
            "review_one_representative_per_exact_source_hash": True,
            "preserves_all_record_provenance": True,
            "changes_labels": False,
            "changes_splits": False,
            "changes_review_state": False,
            "enables_training": False,
        },
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--review-dir", required=True, type=Path)
    p.add_argument("--dataset-root", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    manifest = build_unique_manifest(args.review_dir, args.dataset_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"source_record_count": manifest["source_record_count"], "unique_review_count": manifest["unique_review_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
