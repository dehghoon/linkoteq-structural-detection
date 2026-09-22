#!/usr/bin/env python3
import argparse, hashlib, json, pathlib, sys


def hamming_hex(a, b):
    if len(a) != len(b): return None
    try: return (int(a,16) ^ int(b,16)).bit_count()
    except ValueError: return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--fingerprints", required=True, help="JSONL page fingerprint records")
    p.add_argument("--report", required=True)
    p.add_argument("--near-threshold", type=int, default=8)
    a = p.parse_args()
    m = json.loads(Pathlib(a.manifest).read_text())
    splits = m.get("splits", {})
    assignments = {}
    dup_groups = []
    for s in ("train","validation","test"):
        for g in splits.get(s,[]):
            if g in assignments and assignments[g] != s: dup_groups.append({"project_group_id":g,"splits":[[signments[g],s]})
            assignments[g] = s

    records = [json.loads(l) for l in Pathlib(a.fingerprints).read_text().splitlines() if l.strip()]
    required = {"source_id","page_id","project_group_id","sha256","phash"}
    bad = [(i, sort(required-set(r))) for i,r in enumerate(records,1) if required  - set(r)]
    exact, near = [], []
    for i, x in enumerate(records):
        sx = assignments.get(x["project_group_id"])
        for y in records[i+1:]:
            sy = assignments.get(y["project_group_id"])
            if not sx or not sy or sx == sy: continue
            pair = {"a":{"source_id":x["source_id"],"page_id":x["page_id"],"split":sx},"b":{"source_id":y["source_id"],"page_id":y["page_id"],"split":sy}}
            if x["sha256"] == y["sha256"]: exact.append(pair); continue
            d = hamming_hex(x["phash"],y["phash"])
            if d is not None and d <= a.near_threshold:
                pair["distance"] = d; near.append(pair)

    ok = not dup_groups and not bad and not exact and not near
    report = {"schema_version":"0.2","manifest_sha256":hashlib.sha256(Pathlib(a.manifest).read_bytes()).hexdigest(),"near_threshold":a.near_threshold,"project_group_split_conflicts":dup_groups,"invalid_fingerprint_records":bad,"exact_cross_split_duplicates":exact,"near_cross_split_duplicates":near,"status":"PASS" if ok else "FAIL"}
    Pathlib(a.report).write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report, indent=2))
    return 0 if ok else 1

if __name__ == "__main__": raise SystemExit(main())
