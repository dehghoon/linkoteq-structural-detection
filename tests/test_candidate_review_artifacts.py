import json
import subprocess
import sys
from pathlib import Path

def test_candidate_reviewer_artifact_is_pending_and_non_training(tmp_path):
    qa = tmp_path / "qa"
    qa.mkdir()
    row = {
        "review_state": "pending-human-qa",
        "coordinate_space": "source-page",
        "page_role": "plan",
        "allowed_classes": ["column", "beam", "wall"],
        "labels": [],
        "project_group_id": "pg-001",
        "project_id": "pg-001",
        "source_id": "src-1",
        "page_id": "p-1",
        "qa_batch_id": "qa-batch-001",
        "image_path": "x.png",
        "source_sha256": "a" * 64,
        "source_size_bytes": 123,
    }
    (qa / "qa-batch-001.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
    index = {
        "review_wave_project_groups": 20,
        "review_wave_pages": 1,
        "batches": [{
            "batch_id": "qa-batch-001",
            "path": str(qa / "qa-batch-001.jsonl"),
        }],
    }
    # The production script intentionally requires exactly 20 groups. Build 20 one-page groups.
    rows = []
    for i in range(20):
        r = dict(row)
        r["project_group_id"] = f"pg-{i:03d}"
        r["project_id"] = r["project_group_id"]
        r["source_id"] = f"src-{i}"
        r["page_id"] = f"p-{i}"
        rows.append(json.dumps(r))
    (qa / "qa-batch-001.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")
    index["review_wave_pages"] = 20
    (qa / "index.json").write_text(json.dumps(index), encoding="utf-8")

    out = tmp_path / "review"
    subprocess.run([
        sys.executable, "scripts/build_candidate_review_artifacts.py",
        "--qa-dir", str(qa), "--output-dir", str(out)
    ], check=True)

    d = json.loads((out / "index.json").read_text(encoding="utf-8"))
    assert d["review_wave_project_groups"] == 20
    assert d["training_eligible"] is False
    assert d["ground_truth"] is False
    records = [json.loads(x) for x in (out / "qa-batch-001-review.jsonl").read_text().splitlines()]
    assert len(records) == 20
    assert all(r["review"]["state"] == "pending-human-qa" for r in records)
    assert all(r["candidates"] == [] for r in records)
    assert all(r["training_eligible"] is False for r in records)
    assert all(r["coordinate_space"] == "source-page" for r in records)
