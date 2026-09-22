#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path


def hamming_hex(a, b):
    if len(a) != len(b):
        return None
    try:
        return (int(a, 16) ^ int(b, 16)).bit_count()
    except ValueError:
        return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--fingerprints", required=True, help="JSONL page fingerprint records")
    p.add_argument("--report", required=True)
    p.add_argument("--near-threshold", type=int, default=8)
    a = p.parse_args()

    manifest_path = Path(a.manifest)
    m = json.loads(manifest_path.read_text())
    splits = m.get("splits", {})
    assignments = {}
    dup_groups = []
    for split in ("train", "validation", "test"):
        for group in splits.get(split, []):
            if group in assignments and assignments[group] != split:
                dup_groups.append({
                    "project_group_id": group,
                    "splits": [assignments[group], split],
                })
            assignments[group] = split

    records = [
        json.loads(line)
        for line in Path(a.fingerprints).read_text().splitlines()
        if line.strip()
    ]
    required = {"source_id", "page_id", "project_group_id", "sha256", "phash"}
    bad = [
        (i, sorted(required - set(record)))
        for i, record in enumerate(records, 1)
        if required - set(record)
    ]

    exact, near = [], []
    for i, x in enumerate(records):
        sx = assignments.get(x["project_group_id"])
        for y in records[i + 1:]:
            sy = assignments.get(y["project_group_id"])
            if not sx or not sy or sx == sy:
                continue
            pair = {
                "a": {"source_id": x["source_id"], "page_id": x["page_id"], "split": sx},
                "b": {"source_id": y["source_id"], "page_id": y["page_id"], "split": sy},
            }
            if x["sha256"] == y["sha256"]:
                exact.append(pair)
                continue
            d = hamming_hex(x["phash"], y["phash"])
            if d is not None and d <= a.near_threshold:
                pair["distance"] = d
                near.append(pair)

    ok = not dup_groups and not bad and not exact and not near
    report = {
        "schema_version": "0.2",
        "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "near_threshold": a.near_threshold,
        "project_group_split_conflicts": dup_groups,
        "invalid_fingerprint_records": bad,
        "exact_cross_split_duplicates": exact,
        "near_cross_split_duplicates": near,
        "status": "PASS" if ok else "FAIL",
    }
    Path(a.report).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
