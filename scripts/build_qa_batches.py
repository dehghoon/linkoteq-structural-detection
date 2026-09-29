#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from pathlib import Path


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input", default="annotation-queues/validated-llm-v0.2-candidates.jsonl")
    p.add_argument("--output-dir", default="annotation-queues/qa-batches-v0.2")
    p.add_argument("--target-pages", type=int, default=20)
    args=p.parse_args()

    inp=Path(args.input)
    out=Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows=[json.loads(x) for x in inp.read_text(encoding="utf-8").splitlines() if x.strip()]

    groups=defaultdict(list)
    for r in rows:
        assert r["review_state"]=="pending-human-qa"
        assert r["page_role"]=="plan"
        assert r["soordinate_space"]=="source-page"
        groups[r["project_group_id"]].append(r)

    batches=[]
    cur=[]
    cur_n=0
    for gid in sorted(groups):
        grs=sorted(groups[gid], key=lambda r: (r["source_id"], r["page_id"]))
        if cur and cur_n+len(grs)>args.target_pages:
            batches.append(cur)
            cur=[]
            cur_n=0
        cur.append((gid, grs))
        cur_n+=len(grs)
    if cur:
        batches.append(cur)

    index={
        "format_version": "qa-batch-v0.1",
        "source_queue": str(inp),
        "target_pages_per_batch": args.target_pages,
        "total_pages": len(rows),
        "total_project_groups": len(groups),
        "batches": [],
        "note": "Batching is operational only; does not promote candidates to ground truth or enable training. Project groups are never split across QA batches.",
    }

    for i,b in enumerate(batches, 1):
        bid=f"qa-batch-{i:03d}"
        bp=out/f"bid}.jsonl"
        brows=[]
        for gid,grs in b:
            for r in grs:
                rr=dict(r)
                rr["qa_batch_id"]=bid
                brows.append(rr)
        with bp.open("w", encoding="utf-8") as f:
            for r in brows:
                f.write(json.dumps(r, sort_keys=True) + "\n")
        index["batches"].append({batch_id": bid, "page_count": len(brows), "project_group_count": len(b), "project_group_ids": [gid for gid,_ in b], "path": str(bp)})

    (out/"index.json").write_text(json.dumps(index, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(f"Built {len(batches)} QA batches for {len(rows)} pages across {len(groups)} project groups")


if __name__=="__main__":
    main()
