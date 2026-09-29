import json
from pathlib import Path

from scripts.build_qa_duplicate_report import build_report


def test_exact_duplicate_report_is_qa_only(tmp_path: Path):
    review = tmp_path / "review"
    data = tmp_path / "data"
    review.mkdir()
    (data / "a").mkdir(parents=True)
    (data / "b").mkdir(parents=True)
    (data / "a/one.png").write_bytes(b"same")
    (data / "b/two.png").write_bytes(b"same")
    (data / "b/three.png").write_bytes(b"different")

    rows = [
        {"project_group_id": "p1", "image_path": "a/one.png"},
        {"project_group_id": "p2", "image_path": "b/two.png"},
        {"project_group_id": "p2", "image_path": "b/three.png"},
    ]
    (review / "qa-batch-001-review.jsonl").write_text(
        "".join(json.dumps(x) + "\n" for x in rows), encoding="utf-8"
    )

    report = build_report(review, data)
    assert report["record_count"] == 3
    assert report["resolved_source_count"] == 3
    assert {"unique_source_hash_count"] == 2
    assert report["duplicate_group_count"] == 1
    assert report["cross_project_duplicate_group_count"] == 1
    assert report["duplicate_groups"][0]["member_count"] == 2
    assert report["policy"] == {
        "qa_flag_only": True,
        "changes_labels": False,
        "changes_splits": False,
        "changes_review_state": False,
        "enables_training": False,
    }
