#!/usr/bin/env python3
import argparse, hashlib, json, pathlib, sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--report", required=True)
    a = p.parse_args()
    m = json.loads(Pathlib(a.manifest).read_text())
    splits = m.get("splits", {})
    assignment = {g: s for s in ("train", "validation", "test") for g in splits.get(s, [])}
    sources = m.get("sources")
    if sources is None:
        print("FAIL: manifest has no embedded source inventory; cannot prove duplicate gate", file=sys.stderr)
        return 2

    exact, near = [], []
    seen = {}
    for src in sources:
        g = src["project_group_id"]; s = assignment.get(g)
        if not s: continue
        h = src.get("sha256")
        if h:
            if h in seen and seen[h][0] != s: exact.append({"sha256":h, "a": seen[h], "b": [s,g]})
            seen[h] = (s,g)

    # Near-duplicate requires page-level fingerprints (pHash/dHash or equivalent).
    # Fail closed if they are not present; do not claim PASS from filenames/metadata.
    has_near_fingerprints = all("page_fingerprints" in src for src in sources)
    report = {
        "schema_version": "0.1",
        "manifest": a.manifest,
        "manifest_sha256": hashlib.sha256(Pathlib(a.manifest).read_bytes()).hexdigest(),
        "project_group_split_disjoint": len(assignment) == sum(len(splits.get(s,[])) for s in ("train","validation","test")),
        "exact_cross_split_duplicates": exact,
        "near_check_status": "not-executable-without-page-fingerprints" if not has_near_fingerprints else "not-implemented",
        "status": "FAIL"
    }
    Pathlib(a.report).write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
