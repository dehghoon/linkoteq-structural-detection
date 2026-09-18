#!/usr/bin/env python3
import json, math, sys
from pathlib import Path

RULES_PATH = Path(__file__).resolve().parents[1] / "contracts" / "building-level-proposal-validation-rules-v0.1.json"

def load_rules(path=RULES_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def validate_record(record, rules=None):
    rules = rules or load_rules()
    errors = []
    if not isinstance(record, dict):
        return ["record must be an object"]
    for field in rules["required_coverage_fields"]:
        if field not in record:
            errors.append(f"missing required field: {field}")
    if errors:
        return errors
    if record["component_type"] not in rules["component_types"]:
        errors.append("invalid component_type")
    state = record["coverage_state"]
    if state not in rules["coverage_states"]:
        errors.append("invalid coverage_state")
    c = record["confidence"]
    if isinstance(c, bool) or not isinstance(c, (int, float)) or not math.isfinite(c) or not 0 <= c <= 1:
        errors.append("confidence must be finite in [0,1]")
    if not isinstance(record["coverage_id"], str) or not record["coverage_id"].strip():
        errors.append("coverage_id must be non-empty")
    if not isinstance(record["source_id"], str) or not record["source_id"].strip():
        errors.append("source_id must be non-empty")
    if not isinstance(record["page_id"], str) or not record["page_id"].strip():
        errors.append("page_id must be non-empty")
    if record["review_state"] not in rules["review_states"]:
        errors.append("invalid review_state")
    proposal = record.get("proposal")
    if state == "visible-complete" and proposal is not None:
        errors.append("visible-complete suppresses proposal")
    if state == "visible-incomplete" and proposal is not None and proposal.get("scope") != "gap-only":
        errors.append("visible-incomplete permits gap-only proposal")
    if state == "uncertain" and record["review_state"] not in ("review-required","adjudication-required"):
        errors.append("uncertain coverage must route to QA")
    if proposal is not None:
        if not isinstance(proposal, dict):
            errors.append("proposal must be an object")
        else:
            if proposal.get("coordinate_space") != rules["coordinate_space"]:
                errors.append("proposal coordinate_space must be source-page")
            if proposal.get("replaces_visible_evidence") is True:
                errors.append("proposal must not replace visible evidence")
            if proposal.get("mutates_detection_evidence") is True:
                errors.append("proposal must not mutate detection evidence")
            if proposal.get("copied_cross_floor_as_detection") is True:
                errors.append("cross-floor context must not become detection evidence")
    if record["component_type"] == "wall" and record.get("detection_contract_version") == "0.1" and record.get("emits_wall_detection") is True:
        errors.append("StructuralDetectionEvidence v0.1 rejects wall")
    return errors

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_building_level_proposal.py <jsonl>")
    failed = False
    for lineno, line in enumerate(Path(sys.argv[1]).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"{lineno}: invalid JSON: {exc}")
            failed = True
            continue
        for error in validate_record(record):
            print(f"{lineno}: {error}")
            failed = True
    raise SystemExit(1 if failed else 0)

if __name__ == "__main__":
    main()
