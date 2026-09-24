# Structural Drawing Dataset Admission Contract v0.2

Status: ACTIVE — mandatory for all new admission, re-review, and remediation work.

## Decision authority
LLM/vision review of the ACTUAL rendered drawing sheet is the only authority that may decide whether a page is a dataset candidate.
Text extraction, OCR, filename, sheet index, drawing index, sheet title, keyword matching, page-order inference, or Python scoring MUST NOT select or admit a page.
Scripts may download, render, crop after review, extract an explicitly approved page number, hash, copy, and package. Scripts MUST NOT decide which page is a plan/elevation or training input.

## YOLO plan admission — mandatory visible-content gate
A page called PLAN, FOUNDATION PLAN, FRAMING PLAN, ROOF PLAN, etc. is NOT automatically admissible.
The rendered sheet itself MUST visibly contain useful structural geometry for detection. At least one target family must be materially present at usable scale:
- structural columns / column layout;
- structural grid lines, grid bubbles, or grid intersections;
- beams / joists / structural framing members and their layout;
- structural walls / shear walls / bearing walls intended as structural geometry.

Preference is given to sheets containing multiple target families and clear plan-view relationships.

REJECT when the sheet is primarily:
- structural/general notes, design criteria, specifications, schedules, legends, code notes;
- details-only, connection details, typical details, isolated sections;
- cover/title sheet, drawing index, sheet index;
- site plan, civil plan, grading, utilities, landscape plan/key plan;
- architectural floor plan with no useful structural target geometry;
- roof/site outline without useful structural framing/column/grid/wall geometry;
- 3D/isometric/rendering only;
- blank, corrupted, unreadable, or wrong;
- structural geometry too small/fragmentary to be useful for detector labeling.

## Elevation/section admission
Keep elevation/section material for downstream structural understanding only when the rendered sheet is a real building/structural elevation or section and contributes useful building geometry, floor/storey context, framing/bracing/column/wall context, or other structural vertical information.
REJECT indexes, facade-only presentation sheets with no useful geometry, schedules/notes mislabeled as elevations, and detail-only sheets that do not serve the intended downstream task.

## Project completeness
A project is not validated merely because files exist.
Required states:
1. source_verified
2. pages_rendered
3. llm_visual_reviewed
4. useful_structural_plan_confirmed
5. elevation_or_section_confirmed when available/required
6. extracted_from_explicit_reviewed_page
7. post_extraction_visual_qa_passed
8. validated

If no useful structural plan exists, record REJECT_NO_USEFUL_YOLO_STRUCTURAL_PLAN; do not manufacture a candidate.
If a source cannot be downloaded but an authentic web render/image of the actual drawing is available, it may be retained as review evidence with provenance, but is not automatically validated.

## Required per-sheet review record
For every admitted sheet record:
- project/source identity and source URL;
- source PDF hash when available;
- physical source page number;
- sheet number and sheet title read from the actual sheet when legible;
- role: plan / elevation / section;
- visible target families: column, grid, beam/framing, structural wall;
- why useful for YOLO/downstream task;
- LLM visual-review status;
- extraction QA status;
- rejected alternatives and rejection reason where relevant.

## Negative rule
A text match is evidence for navigation only, never evidence of correctness.
No training_ready=true may be written until actual rendered content and the extracted output have both been visually reviewed.

## Known failure examples
- Mesecher-Goudreau candidate named S2_FRAMING_PLAN_2ND_FLOOR_LOWER_ROOF was actually structural design criteria/framing specifications: REJECT.
- Mesecher-Goudreau candidate named S1_FOUNDATION_PLAN was actually a details/sections sheet: REJECT.
- Landscape/site L5.xx key-plan example: REJECT.
- Tuscaloosa index page saved as S2.01/S2.02/A4.01: REJECT.

This contract supersedes any prior workflow that admitted pages from text/keyword scoring.
