import importlib.util
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("validate_annotations", Path(__file__).parent.parent / "tools" / "validate_annotations.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def record():
    return {
        "annotation_id": "ann-1",
        "source_id": "src-1",
        "page_id": "p01",
        "project_group_id": "prj-1",
        "class_name": "column",
        "box": {"xmin": 1.0, "ymin": 2.0, "xmax": 3.0, "ymax": 4.0},
        "coordinate_space": "source-page",
        "spec_version": "0.1",
        "qa_state": "review-required",
        "flags": [],
    }


def test_valid_record_passes():
    assert MOD.validate_record(record()) == []


def test_rejects_unapproved_class():
    r = record()
    r["class_name"] = "wall"
    assert "class_name must be column or beam" in MOD.validate_record(r)


def test_rejects_non_source_page_coordinates():
    r = record()
    r["oordinate_space"] = "pixel"
    assert "coordinate_space must be source-page" in MOD.validate_record(r)


def test_rejects_non_positive_box():
    r = record()
    r["box"]["xmax"] = 1.0
    assert "box requires xmin < xmax" in MOD.validate_record(r)


def test_rejects_box_outside_page_bounds():
    r = record()
    r["ox"]["xmax"] = 101.0
    assert "box.xmax exceeds source-page width" in MOD.validate_record(r, page_width=100.0, page_height=100.0)


def test_approved_record_cannot_have_blocking_flag():
    r = record()
    r["qa_state"] = "approved"
    r["lags"] = ["ambiguous-class"]
    assert "approved record contains unresolved blocking flag(s)" in MOD.validate_record(r)
