#!/usr/bin/env python3
"""Validate Linkoteq structural-detection annotation JSONL records (v0.1)."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path

ALLOWED_CLASSES = {"column", "beam"}
BLOCKING_FLAGS = {"ambiguous-class", "ambiguous-presence", "overlap-ambiguous"}
ALLOWED_EDGE_FLAGS = {"partial", "occluded", "duplicate-render", "low-resolution", "scan-noise", "faded", "compression-artifact"}
ALLOWED_FLAGS = BLOCKING_FLAGS | ALLOWED_EDGE_FLAGS
QA_STATES = {"draft", "review-required", "adjudication-required", "approved", "corrected-approved", "excluded-ambiguous", "needs-reannotation"}
APPROVED_STATES = {"approved", "corrected-approved"}
REQUIRED = {"annotation_id","source_id","page_id","project_group_id","class_name","box","coordinate_space","spec_version","qa_state"}

def load_geometry(path: Path) -> dict[tuple[str, str], tuple[float, float]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        (p["source_id"], p["page_id"]): (float(p["width_points"]), float(p["height_points"]))
        for p in data.get("pages", [])
    }

def validate_record(record: dict, page_width: float | None = None, page_height: float | None = None) -> list[str]:
    errors = []
    missing = sorted(REQUIRED - record.keys())
    if missing: errors.append("missing required fields: " + ", ".join(missing))
    if record.get("spec_version") != "0.1": errors.append("spec_version must be 0.1")
    if record.get("coordinate_space") != "source-page": errors.append("coordinate_space must be source-page")
    if record.get("class_name") not in ALLOWED_CLASSES: errors.append("class_name must be column or beam")
    if record.get("qa_state") not in QA_STATES: errors.append("qa_state is not approved by v0.1 validation rules")
    for key in ("annotation_id","source_id","page_id","project_group_id"):
        if not isinstance(record.get(key), str) or not record.get(key, "").strip():
            errors.append(f"{key} must be non-empty")
    box = record.get("box")
    if not isinstance(box, dict):
        errors.append("box must be an object")
    else:
        vals = []
        for key in ("xmin","ymin","xmax","ymax"):
            v = box.get(key)
            if not isinstance(v, (int,float)) or isinstance(v,bool) or not math.isfinite(v):
                errors.append(f"box.{key} must be finite")
            else: vals.append(v)
        if len(vals) == 4:
            xmin,ymin,xmax,ymax = vals
            if not xmin < xmax: errors.append("box requires xmin < xmax")
            if not ymin < ymax: errors.append("box requires ymin < ymax")
            if xmin < 0 or ymin < 0: errors.append("box must not start outside source-page bounds")
            if page_width is not None and xmax > page_width: errors.append("box.xmax exceeds source-page width")
            if page_height is not None and ymax > page_height: errors.append("box.ymax exceeds source-page height")
    raw_flags = record.get("flags") or []
    if not isinstance(raw_flags, list):
        errors.append("flags must be a list")
        flags = set()
    else:
        flags = set(raw_flags)
        unknown = sorted(flags - ALLOWED_FLAGS)
        if unknown: errors.append("unapproved flag(s): " + ", ".join(unknown))
    if record.get("qa_state") in APPROVED_STATES and flags & BLOCKING_FLAGS:
        errors.append("approved record contains unresolved blocking flag(s)")
    return errors

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl", type=Path)
    ap.add_argument("--geometry", type=Path)
    args = ap.parse_args()
    geometry = load_geometry(args.geometry) if args.geometry else {}
    failures = 0
    seen_ids = set()
    for i,line in enumerate(args.jsonl.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"{args.jsonl}:{i}: invalid JSON: {e}"); failures += 1; continue
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
