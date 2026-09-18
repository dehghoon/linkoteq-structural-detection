#!/usr/bin/env python3
"""Validate Linkoteq structural-detection annotation JSONL records (v0.1)."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path

ALLOWED_CLASSES = {"column", "beam"}
BLOCKING_FLAGS = {"ambiguous-class", "ambiguous-presence", "overlap-ambiguous"}
APPROVED_STATES = {"approved", "corrected-approved"}
REQUIRED = {"annotation_id","source_id","page_id","project_group_id","class_name","box","coordinate_space","spec_version","qa_state"}

def validate_record(record: dict, page_width: float | None = None, page_height: float | None = None) -> list[str]:
    errors=[]
    missing=sorted(REQUIRED-record.keys())
    if missing: errors.append("missing required fields: "+", ".join(missing))
    if record.get("spec_version") != "0.1": errors.append("spec_version must be 0.1")
    if record.get("coordinate_space") != "source-page": errors.append("coordinate_space must be source-page")
    if record.get("class_name") not in ALLOWED_CLASSES: errors.append("class_name must be column or beam")
    for key in ("annotation_id","source_id","page_id","project_group_id"):
        if not isinstance(record.get(key),str) or not record.get(key,"").strip(): errors.append(f"{key} must be non-empty")
    box=record.get("box")
    if not isinstance(box,dict):
        errors.append("box must be an object")
    else:
        vals=[]
        for key in ("xmin","ymin","xmax","ymax"):
            v=box.get(key)
            if not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v):
                errors.append(f"box.{key} must be finite")
            else: vals.append(v)
        if len(vals)==4:
            xmin,ymin,xmax,ymax=vals
            if not xmin < xmax: errors.append("box requires xmin < xmax")
            if not ymin < ymax: errors.append("box requires ymin < ymax")
            if xmin < 0 or ymin < 0: errors.append("box must not start outside source-page bounds")
            if page_width is not None and xmax > page_width: errors.append("box.xmax exceeds source-page width")
            if page_height is not None and ymax > page_height: errors.append("box.ymax exceeds source-page height")
    flags=set(record.get("flags") or [])
    if record.get("qa_state") in APPROVED_STATES and flags & BLOCKING_FLAGS:
        errors.append("approved record contains unresolved blocking flag(s)")
    return errors

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("jsonl", type=Path)
    args=ap.parse_args()
    failures=0
    for i,line in enumerate(args.jsonl.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try: record=json.loads(line)
        except json.JSONDecodeError as e:
            print(f"{args.jsonl}:{i}: invalid JSON: {e}"); failures+=1; continue
        for error in validate_record(record):
            print(f"{args.jsonl}:{i}: {error}"); failures+=1
    return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())
