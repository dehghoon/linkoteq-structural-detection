#!/usr/bin/env python3
"""Validate Linkoteq structural-detection annotation JSONL records (v0.1/v0.2)."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path

RULES_DIR = Path(__file__).resolve().parents[1] / "contracts"
SUPPORTED_VERSIONS = {"0.1", "0.2"}
APPROVED_STATES = {"approved", "corrected-approved"}

def load_rules(version: str, rules_dir: Path = RULES_DIR) -> dict:
    if version not in SUPPORTED_VERSIONS:
        raise ValueError(f"unsupported spec_version: {version}")
    path = rules_dir / f"annotation-validation-rules-v{version}.json"
    return json.loads(path.read_text(encoding="utf-8"))

def load_geometry(path: Path) -> dict[tuple[str, str], tuple[float, float]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        (p["source_id"], p["page_id"]): (float(p["width_points"]), float(p["height_points"]))
        for p in data.get("pages", [])
    }

def validate_record(record: dict, page_width: float | None = None, page_height: float | None = None,
                    rules_dir: Path = RULES_DIR) -> list[str]:
    errors = []
    version = record.get("spec_version")
    try:
        rules = load_rules(version, rules_dir)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        return [str(exc)]

    required = set(rules["required_fields"])
    missing = sorted(required - record.keys())
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
    if record.get("coordinate_space") != rules["coordinate_space"]:
        errors.append(f"coordinate_space must be {rules['coordinate_space']}")
    allowed_classes = set(rules["allowed_classes"])
    if record.get("class_name") not in allowed_classes:
        errors.append("class_name must be one of: " + ", ".join(rules["allowed_classes"]))
    qa_states = set(rules["qa_states"])
    if record.get("qa_state") not in qa_states:
        errors.append(f"qa_state is not approved by v{version} validation rules")

    for key in ("annotation_id", "source_id", "page_id", "project_group_id"):
        if not isinstance(record.get(key), str) or not record.get(key, "").strip():
            errors.append(f"{key} must be non-empty")

    box = record.get("box")
    if not isinstance(box, dict):
        errors.append("box must be an object")
    else:
        vals = []
        for key in rules["box"]["fields"]:
            value = box.get(key)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
                errors.append(f"box.{key} must be finite")
            else:
                vals.append(value)
        if len(vals) == 4:
            xmin, ymin, xmax, ymax = vals
            if not xmin < xmax: errors.append("box requires xmin < xmax")
            if not ymin < ymax: errors.append("box requires ymin < ymax")
            if xmin < 0 or ymin < 0: errors.append("box must not start outside source-page bounds")
            if page_width is not None and xmax > page_width: errors.append("box.xmax exceeds source-page width")
            if page_height is not None and ymax > page_height: errors.append("box.ymax exceeds source-page height")

    raw_flags = record.get("flags", [])
    flags = set()
    if not isinstance(raw_flags, list):
        errors.append("flags must be a list")
    elif any(not isinstance(flag, str) for flag in raw_flags):
        errors.append("flags entries must be strings")
    else:
        flags = set(raw_flags)
        allowed_flags = set(rules["blocking_flags"]) | set(rules["allowed_edge_flags"])
        unknown = sorted(flags - allowed_flags)
        if unknown:
            errors.append("unapproved flag(s): " + ", ".join(unknown))
    if record.get("qa_state") in APPROVED_STATES and flags & set(rules["blocking_flags"]):
        errors.append("approved record contains unresolved blocking flag(s)")
    return errors

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl", type=Path)
    ap.add_argument("--geometry", type=Path)
    args = ap.parse_args()
    geometry = load_geometry(args.geometry) if args.geometry else {}
    failures, seen_ids = 0, set()
    for i, line in enumerate(args.jsonl.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip(): continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"{args.jsonl}:{i}: invalid JSON: {exc}"); failures += 1; continue
        annotation_id = record.get("annotation_id")
        if annotation_id in seen_ids:
            print(f"{args.jsonl}:{i}: duplicate annotation_id: {annotation_id}"); failures += 1
        elif isinstance(annotation_id, str):
            seen_ids.add(annotation_id)
        key = (record.get("source_id"), record.get("page_id"))
        page_width = page_height = None
        if geometry:
            if key not in geometry:
                print(f"{args.jsonl}:{i}: source_id/page_id not found in geometry"); failures += 1
            else:
                page_width, page_height = geometry[key]
        for error in validate_record(record, page_width, page_height):
            print(f"{args.jsonl}:{i}: {error}"); failures += 1
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
