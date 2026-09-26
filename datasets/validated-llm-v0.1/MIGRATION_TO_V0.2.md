# validated-llm-v0.1 — v0.2 migration notice

Status: legacy baseline / quarantined from new training admission.

This directory is preserved in place and MUST NOT be mutated into a v0.2 three-class dataset. The active v0.2 ontology is `column`, `beam`, `wall`, but legacy v0.1 pages were not annotated for `wall`; therefore, missing wall annotations here MUST NOT be treated as negative wall labels.

## Required migration path

1. Verify the authoritative source asset and provenance.
2. Render and visually review the actual drawing sheet. Filenames, OCR, titles, keywords, sheet indexes, and scripts are navigation aids only and MUST not decide admission.
3. Admit only sheets with usable visible structural geometry under `datasets/contracts/STRUCTURAL_DRAWING_DATASET_ADMISSION_CONTRACT_v0.2.md`.
4. Re-review every admitted page for `column`, `beam`, and `wall` under `contracts/annotation-spec-v0.2.md`.
5. Use tight axis-aligned boxes in original `source-page` coordinates. Do not infer engineering centerlines, thickness, openings, levels, topology, or final engineering geometry.
6. Route ambiguous candidates to QA/adjudication. Do not create an `ambiguous-wall` class.
7. Promote only human-approved evidence to a new versioned dataset. Preserve project-group isolation and exact/near cross-split duplicate gates.

## Training gate

This directory is NOT a source of automatic training ground truth. Unreviewed predictions, missing labels, and legacy absence of `wall` MUST NOT be converted into background/negative evidence.

A new versioned dataset is needed before any v0.2 training candidate.
