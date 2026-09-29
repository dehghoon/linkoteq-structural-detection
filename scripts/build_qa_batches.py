#!/usr/bin/env python3
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def stable_rank(gid: str) -> str:
    # Deterministic and order-independent. This is operational
    # triage only; it does not imply approval or training eligibility.
    return hashlib.sha256(gid.encode("utf-8")).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="annotation-queues/validated-llm-v0.2-candidates.jsonl")
    p.add_argument("--output-dir", default="annotation-queues/qa-batches-v0.2")
    p.add_argument("--target-pages", type=int, default=20)
    p.add_argument("--review-project-groups", type=int, default=20,
                   help="Number of project groups to include in the immediate QA review wave; 0 means all.")
    args = p.parse_args()

    inp = Path(args.input)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(x) for x in inp.read_text(encoding="utf-8").splitlines() if x.strip()]

    groups = defaultdict(list)
    for r in rows:
        assert r["review_state"] == "pending-human-qa"
        assert r["page_role"] == "plan"
        assert r["coordinate_space"] == "source-page"
        groups[r["project_group_id"]].append(r)

    all_gids = sorted(groups, key=stable_rank)
    if args.review_project_groups < 0:
        raise SystemExit("--review-project-groups must be >= 0")
    if args.review_project_groups == 0:
        selected_gids = all_gids
    else:
        selected_gids = all_gids[:args.review_project_groups]
    selected_set = set(selected_gids)
    deferred_gids = [g for g in all_gids if g not in selected_set]

    batches = []
    cur = []
    cur_n = 0
    for gid in selected_gids:
        grs = sorted(groups[gid], key=lambda r: (r["source_id"], r["page_id"]))
        if cur and cur_n + len(grs) > args.target_pages:
            batches.append(cur)
            cur = []
            cur_n = 0
        cur.append((gid, grs))
        cur_n += len(grs)
    if cur:
        batches.append(cur)

    selected_pages = sum(len(groups[g]) for g in selected_gids)
    deferred_pages = sum(len(groups[g]) for g in deferred_gids)
    index = {
        "format_version": "qa-batch-v0.2",
        "source_queue": str(inp),
        "target_pages_per_batch": args.target_pages,
        "total_queue_pages": len(rows),
        "total_queue_project_groups": len(groups),
        "review_wave_pages": selected_pages,
        "review_wave_project_groups": len(selected_gids),
        "deferred_pages": deferred_pages,
        "deferred_project_groups": len(deferred_gids),
        "selection_method": "sha256-stable-rank-v1",
        "deferred_project_group_ids": deferred_gids,
        "batches": [],
        "note": "Staged QA triage only; selection does not approve, promote, or enable training. Deferred records remain pending-human-qa and MUST NOT be treated as background or negative evidence. Project groups are never split across QA batches.",
    }

    for i, b in enumerate(batches, 1):
        bid = f"qa-batch-{i:03d}"
        bp = out / f"{bid}.jsonl"
        brows = []
        for gid, grs in b:
            for r in grs:
                rr = dict(r)
                rr["qa_batch_id"] = bid
                brows.append(rr)
        with bp.open("w", encoding="utf-8") as f:
            for r in brows:
                f.write(json.dumps(r, sort_keys=True) + "\n")
        index["batches"].append({
            "batch_id": bid,
            "page_count": len(brows),
            "project_group_count": len(b),
            "project_group_ids": [gid for gid, _ in b],
            "path": str(bp),
        })

    (out / "index.json").write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Built {len(batches)} QA batches for {selected_pages} pages across {len(selected_gids)} project groups; deferred {deferred_pages} pages across {len(deferred_gids)} project groups")


if __name__ == "__main__":
    main()
