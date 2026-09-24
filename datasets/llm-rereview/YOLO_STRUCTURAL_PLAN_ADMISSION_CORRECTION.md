# YOLO structural-plan admission correction

## Admission rule
A sheet is admitted to the YOLO structural detection dataset only when the drawing itself visibly contains useful structural detection geometry, such as:
- column layout / columns
- structural grid / grid intersections
- beam or framing layout
- structural wall / shear-wall layout

A filename or sheet title containing Foundation, Framing, Plan, Roof, etc. is NOT sufficient.

## Explicit rejects confirmed by visual review
- Mesecher-Goudreau-Residence / S2_FRAMING_PLAN_2ND_FLOOR_LOWER_ROOF.pdf — REJECT. Saved sheet is structural design criteria / framing specifications, not a framing plan.
- Mesecher-Goudreau-Residence / S1_FOUNDATION_PLAN.pdf — REJECT. Saved sheet is details/sections marked D2, not a foundation plan.
- Any landscape/site/landscape sheet like the supplied L5.xx key-plan example — REJECT for YOLO structural detection; it does not provide the required structural column/grid/beam/wall plan geometry.

## Corrected selection policy
1. LLM/vision must inspect the rendered sheet itself.
2. Confirm visible structural geometry before admission.
3. Sheet-index/title/keyword matching cannot admit a sheet.
4. Python may only extract a page after LLM/vision explicitly approves that rendered page.
5. Rejected sheets remain out of training-ready datasets.
