# LLM visual re-review — authoritative status

Status: IN PROGRESS

The legacy `curated-100-projects` output is **quarantined / NOT TRAINING-READY**. Its automatic sheet selections must not be used as ground truth or training input.

## Review rule
Sheet admission is decided by LLM review of the actual drawing sheet and its sheet identity/content, not by keyword occurrence. A sheet index, notes page, cover, detail-only page, or a page merely referencing a plan/elevation is rejected.

For each building:
- inspect all sheets;
- admit every useful structural plan (foundation/anchor, floor/mezzanine framing, roof framing, etc.), not arbitrarily only one;
- admit actual building/structural elevations or sections needed for floor/vertical context;
- preserve source/project/revision/page/sheet provenance;
- treat revisions of one building as one project unless they are genuinely separate buildings;
- title-block removal occurs only after sheet-specific visual review; no fixed percentage mask.

## Current legacy set
Projects 001–076: **PENDING LLM RE-REVIEW**. No legacy `plan=` / `elevation=` selection in the old manifest is authoritative.

## User-supplied projects
The recently supplied P2025/P2026/Lacmark drawing packages are part of the same review population. They are not to be omitted merely because they were uploaded after the web-sourced batch.

### First reviewed source identity
P2025-177 R3 — Entrepôt U-Haul Gatineau:
- EsMx001: 3D views / sheet list — reject as training plan/elevation.
- EsMx201: mezzanine plans — structural-plan candidate.
- EsMx401: roof & mezzanine plan — structural-plan candidate.
- EsMx501: elevations, wall sections, schedules — elevation/section candidate subject to visual sheet QA.
- EsMx502: elevations — elevation candidate subject to visual sheet QA.
- EsMx503: sections — section candidate subject to visual sheet QA.
R2/R3 are revisions of the same building and do not count as separate projects.

No project becomes VALIDATED until its admitted sheets have passed this review.
