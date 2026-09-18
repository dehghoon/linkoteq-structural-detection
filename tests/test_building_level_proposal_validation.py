import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "validate_building_level_proposal.py"
spec = importlib.util.spec_from_file_location("proposal_validator", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def rec(state="visible-absent", component="column", proposal=None, review="review-required"):
    return {
        "coverage_id":"cov-1","source_id":"src-1","page_id":"p1",
        "component_type":component,"coverage_state":state,"confidence":0.8,
        "provenance":{"model":"fixture"},"review_state":review,"proposal":proposal
    }

def proposal(**kw):
    p={"coordinate_space":"source-page","scope":"gap-only"}
    p.update(kw)
    return p

def test_complete_suppresses_proposal():
    assert mod.validate_record(rec("visible-complete", proposal=proposal()))

def test_incomplete_allows_gap_only():
    assert mod.validate_record(rec("visible-incomplete", proposal=proposal())) == []

def test_incomplete_rejects_replacement_scope():
    assert mod.validate_record(rec("visible-incomplete", proposal=proposal(scope="replacement")))

def test_absent_allows_review_gated_proposal():
    assert mod.validate_record(rec("visible-absent", proposal=proposal(scope="contextual"))) == []

def test_uncertain_requires_qa():
    assert mod.validate_record(rec("uncertain", proposal=None, review="human-confirmed"))

def test_proposal_cannot_replace_visible_evidence():
    assert mod.validate_record(rec(proposal=proposal(replaces_visible_evidence=True)))

def test_cross_floor_context_cannot_be_detection():
    assert mod.validate_record(rec(proposal=proposal(copied_cross_floor_as_detection=True)))

def test_wrong_coordinate_space_rejected():
    assert mod.validate_record(rec(proposal=proposal(coordinate_space="global")))

def test_v01_wall_detection_rejected():
    r=rec(component="wall")
    r["detection_contract_version"]="0.1"
    r["emits_wall_detection"]=True
    assert mod.validate_record(r)

def test_non_object_record_fails_cleanly():
    assert mod.validate_record([]) == ["record must be an object"]

def test_nonfinite_and_bool_confidence_rejected():
    r=rec(); r["confidence"]=float("nan")
    assert mod.validate_record(r)
    r=rec(); r["confidence"]=True
    assert mod.validate_record(r)
