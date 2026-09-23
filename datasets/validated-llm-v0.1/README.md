# validated-llm-v0.1

Authoritative destination for LLM/visual-reviewed structural drawing sheets.

A project is admitted only after source and sheet identity are reviewed. The legacy curated-100-projects outputs are not inherited as ground truth.

Per-project structure:
- plans/ — admitted structural plan sheets
- elevations-sections/ — admitted elevation/section sheets used for vertical/floor context
- originals/ — source-preserving selected sheet copies when materialized
- provenance.json — source URL, sheet IDs/titles, decisions, and QA state

Title blocks are removed only after page-specific visual review. No fixed-percentage masking is allowed.

Status values:
- source_verified: source/package identity checked
- sheets_identified: correct sheet IDs/titles identified
- materialized: correct selected sheet PDFs copied here
- visual_qa_passed: actual selected page visually checked
- validated: all required gates passed
