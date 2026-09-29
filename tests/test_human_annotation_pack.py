from scripts.build_human_annotation_pack import build_pack


def test_human_annotation_pack_starts_pending_and_empty():
    manifest = {
        "source_record_count": 3,
        "unique_review_count": 2,
        "representatives": [
            {
                "sha256": "a" * 64,
                "representative": {
                    "project_group_id": "p1",
                    "image_path": "p1/plans/images/a.png",
                },
                "alias_count": 1,
                "aliases": [{"project_group_id": "p1", "image_path": "p1/plans/images/a-copy.png"}],
            },
            {
                "sha256": "b" * 64,
                "representative": {
                    "project_group_id": "p2",
                    "image_path": "p2/plans/images/b.png",
                },
                "alias_count": 0,
                "aliases": [],
            },
        ],
    }

    pack = build_pack(manifest, "123")

    assert pack["unique_review_count"] == 2
    assert pack["allowed_classes"] == ["column", "beam", "wall"]
    assert pack["coordinate_space"] == "source-page"
    assert pack["review_state"] == "pending-human-qa"
    assert pack["annotation_geometry"] == "tight-axis-aligned-box"
    assert all(item["annotations"] == [] for item in pack["items"])
    assert all(item["review_state"] == "pending-human-qa" for item in pack["items"])
    assert pack["items"][0]["alias_count"] == 1
    assert pack["policy"]["wall_requires_human_qa"] is True
    assert pack["policy"]["enables_training"] is False
    assert pack["policy"]["emits_canonical_engineering_geometry"] is False
