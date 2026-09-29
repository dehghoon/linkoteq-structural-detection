import json
from pathlib import Path

from scripts.build_unique_qa_manifest import build_unique_manifest


def test_unique_manifest_preserves_alias_provenance(tmp_path: Path):
    review = tmp_path / "review"
    data = tmp_path / "data"
    review.mkdir()
    (data / "p1").mkdir(parents=True)
    (data / "p2").mkdir(parents=True)
    (data / "p1/a.png").write_bytes(b"same")
    (data / "p1/a-copy.png").write_bytes(b"same")
    (data / "p2/b.png").write_bytes(b"different")

    rows = [
        {"project_group_id": "p1", "image_path": "p1/a.png"},
        {"project_group_id": "p1", "image_path": "p1/a-copy.png"},
        {"project_group_id": "p2", "image_path": "p2/b.png"},
    ]
    (review / "qa-batch-001-review.jsonl").write_text(
        "".join(json.dumps(x) + "\n" for x in rows), encoding="utf-8"
    )

    manifest = build_unique_manifest(review, data)

    assert manifest["source_record_count"] == 3
    assert manifest["unique_review_count"] == 2
    assert sum(x["alias_count"] for x in manifest["representatives"]) == 1
    assert manifest["policy"] == {
        "review_one_representative_per_exact_source_hash": True,
        "preserves_all_record_provenance": True,
        "changes_labels": False,
        "changes_splits": False,
        "changes_review_state": False,
        "enables_training": False,
    }
