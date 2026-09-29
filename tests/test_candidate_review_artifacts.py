import json
import subprocess
import sys
from pathlib import Path


def _row(i):
    return {
        "review_state": "pending-human-qa",
        "coordinate_space": "source-page",
        "page_role": "plan",
        "allowed_classes": ["column", "beam", "wall"],
        "labels": [],
        "project_group_id": f"pg-{i:03d}",
        "project_id": f"pg-{i:03d}",
        "source_id": f"src-{i}",
        "page_id": f"p-{i}",
        "qa_batch_id": "qa-batch-001",
        "image_path": f"{i}.png",
        "source_sha256": "a" * 64,
        "source_size_bytes": 123,
    }


def _contract(tmp_path):
    contract = {
        "contract_id": "candidate-qa-gates-v0.2",
        "coordinate_space": "source-page",
        "allowed_candidate_classes": ["column", "beam", "wall"],
        "promotion_rules": {
            "candidate_never_equals_ground_truth": True,
            "missing_candidate_never_automatically_becomes_background": True,
        },
        "boundary": {
            "enables_training": False,
            "emits_canonical_engineering_geometry": False,
        },
    }
    path = tmp_path / "contract.json"
    path.write_text(json.dumps(contract), encoding="utf-8")
    return path


def test_candidate_reviewer_artifact_contract_invariants(tmp_path):
    qa = tmp_path / "qa"
    qa.mkdir()
    rows = [_row(i) for i in range(20)]
    batch = qa / "qa-batch-001.jsonl"
    batch.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    index = {
        "review_wave_project_groups": 20,
        "review_wave_pages": 20,
        "batches": [{"batch_id": "qa-batch-001", "path": str(batch)}],
    }
    (qa / "index.json").write_text(json.dumps(index), encoding="utf-8")

    out = tmp_path / "review"
    subprocess.run([
        sys.executable, "scripts/build_candidate_review_artifacts.py",
        "--qa-dir", str(qa), "--output-dir", str(out),
        "--contract", str(_contract(tmp_path)),
    ], check=True)

    idx = json.loads((out / "index.json").read_text(encoding="utf-8"))
    assert idx["contract_id"] == "candidate-qa-gates-v0.2"
    assert idx["contract_validated"] is True
    assert idx["review_wave_project_groups"] == 20
    assert idx["review_state"] == "pending-human-qa"
    assert idx["training_eligible"] is False
    assert idx["ground_truth"] is False
    assert idx["empty_candidate_semantics"] == "unreviewed-not-background"

    records = [json.loads(x) for x in (out / "qa-batch-001-review.jsonl").read_text().splitlines()]
    assert len(records) == 20
    assert all(r["allowed_classes"] == ["column", "beam", "wall"] for r in records)
    assert all(r["coordinate_space"] == "source-page" for r in records)
    assert all(r["review"]["state"] == "pending-human-qa" for r in records)
    assert all(r["training_eligible"] is False and r["ground_truth"] is False for r in records)
    assert all(r["candidates"] == [] for r in records)
    assert all(r["empty_candidate_semantics"] == "unreviewed-not-background" for r in records)
    assert all("engineering_geometry" not in r and "reconstruction" not in r for r in records)


def test_candidate_reviewer_rejects_non_contract_coordinate_space(tmp_path):
    qa = tmp_path / "qa"
    qa.mkdir()
    rows = [_row(i) for i in range(20)]
    rows[0]["coordinate_space"] = "engineering"
    batch = qa / "qa-batch-001.jsonl"
    batch.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    (qa / "index.json").write_text(json.dumps({
        "review_wave_project_groups": 20,
        "review_wave_pages": 20,
        "batches": [{"batch_id": "qa-batch-001", "path": str(batch)}],
    }), encoding="utf-8")

    result = subprocess.run([
        sys.executable, "scripts/build_candidate_review_artifacts.py",
        "--qa-dir", str(qa), "--output-dir", str(tmp_path / "review"),
        "--contract", str(_contract(tmp_path)),
    ])
    assert result.returncode != 0


def test_workflow_builds_validates_and_uploads_reviewer_artifact():
    workflow = Path(".github/workflows/build-annotation-batch.yml").read_text(encoding="utf-8")
    assert "python scripts/build_candidate_review_artifacts.py" in workflow
    assert "--qa-dir annotation-queues/qa-batches-v0.2" in workflow
    assert "--contract contracts/candidate-qa-gates-v0.2.json" in workflow
    assert "candidate-review-wave-v0.2" in workflow
    assert "annotation-queues/reviewer-artifacts-v0.2" in workflow
