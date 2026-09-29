#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

PENDING_STATE = "pending-human-qa"


def stable_candidate_set_id(row: dict) -> str:
    key = "|".join([
        row["project_group_id"],
        row["source_id"],
        row["page_id"],
        row.get("qa_batch_id", ""),
    ])
    return "candidate-set-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]


def load_contract(path: Path) -> dict:
    contract = json.loads(path.read_text(encoding="utf-8"))
    assert contract["contract_id"] == "candidate-qa-gates-v0.2"
    assert contract["coordinate_space"] == "source-page"
    assert contract["allowed_candidate_classes"] == ["column", "beam", "wall"]
    assert contract["promotion_rules"]["candidate_never_equals_ground_truth"] is True
    assert contract["promotion_rules"]["missing_candidate_never_automatically_becomes_background"] is True
    assert contract["boundary"]["enables_training"] is False
    assert contract["boundary"]["emits_canonical_engineering_geometry"] is False
    return contract


def build_record(row: dict, contract: dict) -> dict:
    allowed_classes = contract["allowed_candidate_classes"]
    coordinate_space = contract["coordinate_space"]
    assert row["review_state"] == PENDING_STATE
    assert row["coordinate_space"] == coordinate_space
    assert row["page_role"] == "plan"
    assert row["allowed_classes"] == allowed_classes
    assert row.get("labels") == [], "staged QA input must remain unreviewed; labels must be empty"

    return {
        "artifact_version": "candidate-review-v0.2",
        "candidate_set_id": stable_candidate_set_id(row),
        "qa_batch_id": row["qa_batch_id"],
        "project_group_id": row["project_group_id"],
        "project_id": row.get("project_id", row["project_group_id"]),
        "source_id": row["source_id"],
        "page_id": row["page_id"],
        "image_path": row["image_path"],
        "source_sha256": row["source_sha256"],
        "source_size_bytes": row["source_size_bytes"],
        "page_role": "plan",
        "coordinate_space": coordinate_space,
        "ontology_version": "v0.2",
        "allowed_classes": allowed_classes,
        "annotation_representation": "tight-axis-aligned-source-page-box",
        "candidate_generator": {
            "name": "staged-qa-review-envelope",
            "version": "v0.2",
            "mode": "reviewer-scaffold",
        },
        "candidates": [],
        "empty_candidate_semantics": "unreviewed-not-background",
        "review": {
            "state": PENDING_STATE,
            "reviewer_id": None,
            "reviewed_at": None,
            "decision": None,
            "notes": None,
        },
        "training_eligible": False,
        "ground_truth": False,
        "instructions": {
            "visible_evidence_only": True,
            "metadata_is_non_authoritative": True,
            "wall_requires_human_qa": True,
            "ambiguous_routes_to_review": True,
            "missing_candidate_is_not_background": True,
            "no_hidden_continuation": True,
        },
    }


def validate_record(record: dict, contract: dict) -> None:
    assert record["coordinate_space"] == contract["coordinate_space"]
    assert record["allowed_classes"] == contract["allowed_candidate_classes"]
    assert record["review"]["state"] == PENDING_STATE
    assert record["training_eligible"] is False
    assert record["ground_truth"] is False
    assert record["empty_candidate_semantics"] == "unreviewed-not-background"
    assert record["candidate_generator"]["mode"] == "reviewer-scaffold"
    assert record["instructions"]["missing_candidate_is_not_background"] is True
    assert record["instructions"]["wall_requires_human_qa"] is True
    assert record["candidates"] == []
    forbidden = {"engineering_geometry", "structural_model", "core_geometry", "reconstruction"}
    assert forbidden.isdisjoint(record)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--qa-dir", default="annotation-queues/qa-batches-v0.2")
    p.add_argument("--output-dir", default="annotation-queues/reviewer-artifacts-v0.2")
    p.add_argument("--contract", default="contracts/candidate-qa-gates-v0.2.json")
    args = p.parse_args()

    qa_dir = Path(args.qa_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    contract = load_contract(Path(args.contract))
    index = json.loads((qa_dir / "index.json").read_text(encoding="utf-8"))

    outputs = []
    seen_groups = set()
    total_records = 0
    for batch in index["batches"]:
        src = Path(batch["path"])
        if not src.is_absolute() and not src.exists():
            src = qa_dir / src.name
        rows = [json.loads(x) for x in src.read_text(encoding="utf-8").splitlines() if x.strip()]
        records = [build_record(r, contract) for r in rows]
        for record in records:
            validate_record(record, contract)
        groups = sorted({r["project_group_id"] for r in records})
        overlap = seen_groups.intersection(groups)
        assert not overlap, f"project groups split across reviewer artifacts: {sorted(overlap)}"
        seen_groups.update(groups)

        dest = out_dir / f'{batch["batch_id"]}-review.jsonl'
        with dest.open("w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, sort_keys=True) + "\n")
        outputs.append({
            "batch_id": batch["batch_id"],
            "path": str(dest),
            "record_count": len(records),
            "project_group_ids": groups,
        })
        total_records += len(records)

    review_index = {
        "format_version": "candidate-review-index-v0.2",
        "contract_id": contract["contract_id"],
        "contract_validated": True,
        "source_qa_index": str(qa_dir / "index.json"),
        "review_state": PENDING_STATE,
        "training_eligible": False,
        "ground_truth": False,
        "empty_candidate_semantics": "unreviewed-not-background",
        "candidate_generator": "staged-qa-review-envelope-v0.2",
        "review_wave_project_groups": index["review_wave_project_groups"],
        "review_wave_pages": index["review_wave_pages"],
        "artifacts": outputs,
        "note": (
            "Reviewer artifact only. Empty candidates are unreviewed and MUST NOT be treated as "
            "background/negative evidence. Human QA is required before any annotation promotion. "
            "This artifact does not approve labels, enable training, release a dataset, or emit engineering geometry."
        ),
    }
    assert review_index["review_wave_project_groups"] == 20
    assert len(seen_groups) == 20
    assert total_records == review_index["review_wave_pages"]
    (out_dir / "index.json").write_text(
        json.dumps(review_index, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Built and contract-validated {len(outputs)} reviewer artifacts for {len(seen_groups)} project groups / {total_records} pages")


if __name__ == "__main__":
    main()
