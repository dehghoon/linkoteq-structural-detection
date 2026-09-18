import importlib.util
from pathlib import Path

P=Path(__file__).resolve().parents[1]/"tools"/"validate_structural_layout_proposal.py"
s=importlib.util.spec_from_file_location("slp",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)

def rec(t="column-location", state="visible-absent", geom=None, **kw):
    geom=geom or ({"x":10,"y":20} if t=="column-location" else {"x1":0,"y1":0,"x2":10,"y2":0} if t=="grid-axis" else {"x":1,"y":2,"width":3,"height":4})
    r={"proposal_id":"p1","source_id":"s1","page_id":"pg1","project_group_id":"g1","proposal_type":t,
       "coordinate_space":"source-page","proposal_geometry":geom,"evidence_basis":{"kind":"context"},
       "confidence":.8,"reason_codes":["grid-intersection"],"model_or_rule_name":"fixture","model_or_rule_version":"1",
       "provenance":{"source":"fixture"},"review_state":"review-required","coverage_state":state}
    r.update(kw); return r

def test_valid_types(): 
    for t in ("grid-axis","column-location","wall-location"): assert m.validate_record(rec(t=t))==[]
def test_complete_suppresses(): assert m.validate_record(rec(state="visible-complete"))
def test_incomplete_gap_only():
    assert m.validate_record(rec(state="visible-incomplete",proposal_scope="gap-only"))==[]
    assert m.validate_record(rec(state="visible-incomplete",proposal_scope="replacement"))
def test_uncertain_routes_qa(): assert m.validate_record(rec(state="uncertain",review_state="human-confirmed"))
def test_wrong_coordinate_space(): assert m.validate_record(rec(coordinate_space="global"))
def test_no_replace_or_mutate_or_detection():
    assert m.validate_record(rec(replaces_visible_evidence=True))
    assert m.validate_record(rec(mutates_detection_evidence=True))
    assert m.validate_record(rec(serialized_as_detection=True))
def test_multi_floor_requires_confirmed_level():
    assert m.validate_record(rec(multi_floor=True))
    assert m.validate_record(rec(multi_floor=True,building_level_proposal_id="b1",level_proposal_id="l1",building_level_review_state="review-required"))
    assert m.validate_record(rec(multi_floor=True,building_level_proposal_id="b1",level_proposal_id="l1",building_level_review_state="human-confirmed"))==[]
def test_geometry_guards():
    assert m.validate_record(rec(t="grid-axis",geom={"x1":1,"y1":1,"x2":1,"y2":1}))
    assert m.validate_record(rec(t="column-location",geom={"x":float("nan"),"y":2}))
    assert m.validate_record(rec(t="wall-location",geom={"x":1,"y":2,"width":0,"height":4}))
def test_confidence_guards():
    assert m.validate_record(rec(confidence=True))
    assert m.validate_record(rec(confidence=float("inf")))
def test_human_correction_preserves_provenance():
    assert m.validate_record(rec(review_state="human-corrected"))
    assert m.validate_record(rec(review_state="human-corrected",original_proposal_geometry={"x":9,"y":9},correction_provenance={"reviewer":"human"}))==[]
def test_non_object_clean_failure(): assert m.validate_record([])==["record must be an object"]
