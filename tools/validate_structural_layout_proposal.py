#!/usr/bin/env python3
import json, math, sys
from pathlib import Path

RULES_PATH = Path(__file__).resolve().parents[1] / "contracts" / "structural-layout-proposal-validation-rules-v0.1.json"
REQUIRED = ["proposal_id","source_id","page_id","project_group_id","proposal_type","coordinate_space",
            "proposal_geometry","evidence_basis","confidence","reason_codes","model_or_rule_name",
            "model_or_rule_version","provenance","review_state","coverage_state"]
REVIEWS = {"review-required","human-confirmed","human-corrected","human-rejected","adjudication-required"}
LEVEL_REVIEWS = {"human-confirmed","human-corrected"}

def load_rules(path=RULES_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def _finite(v):
    return not isinstance(v, bool) and isinstance(v,(int,float)) and math.isfinite(v)

def validate_record(r, rules=None):
    rules = rules or load_rules()
    if not isinstance(r, dict): return ["record must be an object"]
    e=[]
    for f in REQUIRED:
        if f not in r: e.append(f"missing required field: {f}")
    if e: return e
    for f in ("proposal_id","source_id","page_id","project_group_id","model_or_rule_name","model_or_rule_version"):
        if not isinstance(r[f],str) or not r[f].strip(): e.append(f"{f} must be non-empty")
    t=r["proposal_type"]; state=r["coverage_state"]
    if t not in rules["proposal_types"]: e.append("invalid proposal_type")
    if r["coordinate_space"] != rules["coordinate_space"]: e.append("coordinate_space must be source-page")
    if state not in rules["coverage_states"]: e.append("invalid coverage_state")
    c=r["confidence"]
    if not _finite(c) or not 0 <= c <= 1: e.append("confidence must be finite in [0,1]")
    if r["review_state"] not in REVIEWS: e.append("invalid review_state")
    reasons=r["reason_codes"]
    if not isinstance(reasons,list) or not reasons or any(not isinstance(x,str) or not x for x in reasons):
        e.append("reason_codes must be a non-empty string list")
    if state=="visible-complete": e.append("visible-complete suppresses replacement proposals")
    if state=="visible-incomplete" and r.get("proposal_scope")!="gap-only":
        e.append("visible-incomplete permits gap-only proposals")
    if state=="uncertain" and r["review_state"] not in {"review-required","adjudication-required"}:
        e.append("uncertain coverage must route to Human QA")
    if r.get("replaces_visible_evidence") is True: e.append("proposal must not replace visible evidence")
    if r.get("mutates_detection_evidence") is True: e.append("proposal must not mutate detection evidence")
    if r.get("serialized_as_detection") is True: e.append("proposal must not serialize as detection evidence")
    if r.get("multi_floor") is True:
        if not r.get("building_level_proposal_id"): e.append("multi-floor proposal requires building_level_proposal_id")
        if r.get("building_level_review_state") not in LEVEL_REVIEWS:
            e.append("multi-floor proposal requires human-confirmed/corrected BuildingLevelProposal")
        if not r.get("level_proposal_id"): e.append("multi-floor proposal requires level_proposal_id")
    g=r["proposal_geometry"]
    if not isinstance(g,dict): e.append("proposal_geometry must be an object"); return e
    if t=="grid-axis":
        vals=[g.get(k) for k in ("x1","y1","x2","y2")]
        if not all(_finite(v) for v in vals): e.append("grid-axis geometry must be finite")
        elif vals[0]==vals[2] and vals[1]==vals[3]: e.append("grid-axis must have distinct endpoints")
    elif t=="column-location":
        if not all(_finite(g.get(k)) for k in ("x","y")): e.append("column-location geometry must be a finite point")
    elif t=="wall-location":
        vals=[g.get(k) for k in ("x","y","width","height")]
        if not all(_finite(v) for v in vals): e.append("wall-location geometry must be finite")
        elif vals[0]<0 or vals[1]<0 or vals[2]<=0 or vals[3]<=0: e.append("wall-location must be a positive source-page box")
    if r["review_state"]=="human-corrected":
        if "original_proposal_geometry" not in r or "correction_provenance" not in r:
            e.append("human-corrected proposal must preserve original geometry and correction provenance")
    return e

def main():
    if len(sys.argv)!=2: raise SystemExit("usage: validate_structural_layout_proposal.py <jsonl>")
    failed=False
    for n,line in enumerate(Path(sys.argv[1]).read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try: r=json.loads(line)
        except json.JSONDecodeError as ex:
            print(f"{n}: invalid JSON: {ex}"); failed=True; continue
        for err in validate_record(r):
            print(f"{n}: {err}"); failed=True
    raise SystemExit(1 if failed else 0)
if __name__=="__main__": main()
