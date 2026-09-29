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


def load_records(review_dir: Path):
    records = []
    for path in sorted(review_dir.glob("qa-batch-*-review.jsonl")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            row = json.loads(line)
            row["_review_file"] = path.name
            row["_review_line"] = line_no
            records.append(row)
    return records


def build_report(review_dir: Path, dataset_root: Path):
    records = load_records(review_dir)
    by_sha = defaultdict(list)
    missing = []
    for row in records:
        rel = row["image_path"]
        src = dataset_root / rel
        if not src.is_file():
            missing.append(rel)
            continue
        digest = sha256_file(src)
        by_sha[digest].append({
            "project_group_id": row["project_group_id"],
            "image_path": rel,
            "review_file": row["_review_file"],
            "review_line": row["_review_line"],
        })

    groups = []
    for digest, members in sorted(by_sha.items()):
        if len(members) > 1:
            groups.append({
                "sha256": digest,
                "member_count": len(members),
                "cross_project_group": len({m["project_group_id"] for m in members}) > 1,
                "members": members,
            })

    return {
        "report_type": "qa-exact-source-duplicate-report",
        "hash_algorithm": "sha256",
        "scope": "reviewer-record-source-images",
        "record_count": len(records),
        "resolved_source_count": len(records) - len(missing),
        "unique_source_hash_count": len(by_sha),
        "duplicate_group_count": len(groups),
        "duplicate_record_count": sum(g["member_count"] for g in groups),
        "cross_project_duplicate_group_count": sum(1 for g in groups if g["cross_project_group"]),
        "missing_source_paths": sorted(set(missing)),
        "duplicate_groups": groups,
        "policy": {
            "qa_flag_only": True,
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
    report = build_report(args.review_dir, args.dataset_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in (
        "record_count", "resolved_source_count", "unique_source_hash_count",
        "duplicate_group_count", "cross_project_duplicate_group_count"
    )}, sort_keys=True))


if __name__ == "__main__":
    main()
