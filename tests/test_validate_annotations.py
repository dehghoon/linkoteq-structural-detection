import importlib.util
import json
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "validate_annotations",
    Path(__file__).parent.parent / "tools" / "validate_annotations.py",
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

def record(version="0.1", class_name="column"):
    return {
        "annotation_id": "ann-1", "source_id": "src-1", "page_id": "p01",
        "project_group_id": "prj-1", "class_name": class_name,
        "box": {"xmin": 1.0, "ymin": 2.0, "xmax": 3.0, "ymax": 4.0},
        "coordinate_space": "source-page", "spec_version": version,
        "qa_state": "review-required", "flags": [],
    }

def test_valid_v01_column_passes():
    assert MOD.validate_record(record()) == []

def test_valid_v01_beam_passes():
    assert MOD.validate_record(record(class_name="beam")) == []

def test_v01_wall_is_rejected():
    errors = MOD.validate_record(record(class_name="wall"))
    assert any("class_name must be one of: column, beam" in e for e in errors)

def test_valid_v02_wall_passes():
    assert MOD.validate_record(record("0.2", "wall")) == []

def test_valid_v02_column_and_beam_pass():
    assert MOD.validate_record(record("0.2", "column")) == []
    assert MOD.validate_record(record("0.2", "beam")) == []

def test_unsupported_version_is_rejected():
    assert MOD.validate_record(record("9.9", "wall")) == ["unsupported spec_version: 9.9"]

def test_rejects_non_source_page_coordinates():
    r = record("0.2", "wall"); r["coordinate_space"] = "pixel"
    assert "coordinate_space must be source-page" in MOD.validate_record(r)

def test_rejects_non_positive_box():
    r = record(); r["box"]["xmax"] = 1.0
    assert "box requires xmin < xmax" in MOD.validate_record(r)

def test_rejects_box_outside_page_bounds():
    r = record(); r["box"]["xmax"] = 101.0
    assert "box.xmax exceeds source-page width" in MOD.validate_record(r, 100.0, 100.0)

def test_rejects_unknown_qa_state_version_aware():
    r = record("0.2", "wall"); r["qa_state"] = "ready"
    assert "qa_state is not approved by v0.2 validation rules" in MOD.validate_record(r)

def test_rejects_unknown_flag():
    r = record("0.2", "wall"); r["flags"] = ["made-up-flag"]
    assert "unapproved flag(s): made-up-flag" in MOD.validate_record(r)

def test_rejects_non_string_flag_without_crashing():
    r = record("0.2", "wall"); r["flags"] = [{"bad": True}]
    assert "flags entries must be strings" in MOD.validate_record(r)

def test_approved_record_cannot_have_blocking_flag():
    r = record("0.2", "wall"); r["qa_state"] = "approved"; r["flags"] = ["ambiguous-class"]
    assert "approved record contains unresolved blocking flag(s)" in MOD.validate_record(r)

def test_load_geometry_indexes_source_and_page(tmp_path):
    path = tmp_path / "geometry.json"
    path.write_text(json.dumps({"pages": [{
        "source_id": "src-1", "page_id": "p01",
        "width_points": 100.0, "height_points": 200.0,
    }]}), encoding="utf-8")
    assert MOD.load_geometry(path) == {("src-1", "p01"): (100.0, 200.0)}
