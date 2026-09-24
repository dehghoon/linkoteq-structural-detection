# WEB BATCHES 050-100 — LLM VISUAL RE-REVIEW REQUIRED

Effective immediately, every project materialized from web batches 050-100 is **NOT TRAINING-READY** until an LLM/vision review has inspected the actual drawing pages.

## Mandatory selection rule
- LLM/vision must inspect actual rendered pages and decide which sheets are plans, elevations, or sections.
- Sheet-index text, pdftotext matches, keyword scoring, or Python page-selection logic MUST NOT make the selection decision.
- Python/scripts may only perform mechanical work *after* the LLM has supplied explicit source page numbers: extraction, rendering, filenames, JSON/TXT generation.
- Index/cover/general-notes pages are never accepted as a target merely because they mention a target sheet.
- A project returns to validated status only after selected pages have been visually checked against drawing content and title block.

## Scope
Applies to manifests:
- batch-050-059
- batch-060-069
- batch-070-079
- batch-080-089
- batch-090-100

Tuscaloosa-DHR-Building-1 is a confirmed failure example: S2.01, S2.02 and A4.01 were all incorrectly extracted from source page 2 (drawing index).

Status for this scope: **QUARANTINED FROM TRAINING PENDING LLM VISUAL QA**.
