#!/usr/bin/env python3
import argparse, json
from pathlib import Path


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest", default="datasets/source-drawings/validated-llm-source-v0.2-candidate/manifest.jsonl")
    p.add_argument("--output", default="annotation-queues/validated-llm-v0.2-candidates.jsonl")
    p.add_argument("--ontology-version", default="v0.2")
    args=p.parse_args()
    manifest=Path(args.manifest); out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        s=json.loads(line)
        # include only explicit plan pages in detector annotation QA.
        # vertical-reference and unclassified pages remain preserved in the source manifest and are NOT negatives.
        if s.get("page_role") != "plan": continue
        rows.append({
            "source_id":s["source_id"],
            "project_id":s["project_group_id"],
            "project_group_id":s["project_group_id"],
            "page_id":s["page_id"],
            "image_path":s["source_path"],
            "source_sha256":s["sha256"],
            "source_size_bytes":s["size_bytes"],
            "page_role":"plan",
            "coordinate_space":"source-page",
            "ontology_version":args.ontology_version,
            "allowed_classes":["column","beam","wall"],
            "annotation_representation":"tight-axis-aligned-source-page-box",
            "review_state":"pending-human-qa",
            "labels":[],
            "note":"Empty labels are unreviewed, NOT background or negative evidence. Non-plan source pages are preserved outside this detector QA queue."
        })
    with out.open("w",encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r, sort_keys=True)+"\n")
    print(f"Wrote {len(rows)} plan pages to {out}")

if __name__=="__main__": main()
