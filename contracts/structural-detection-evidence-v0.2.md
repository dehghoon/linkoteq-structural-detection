# Structural Detection Evidence Contract v0.2 — Candidate

## Status
Candidate contract for coordinated wall migration. v0.1 remains active until the migration gate is satisfied.

## Ownership boundary
GPT-7 owns detection evidence production. GPT-6 owns engineering reconstruction and Core mapping. Detector output is evidence only.

## Label ontology
`class_name` MUST conform to `contracts/label-ontology-v0.2.md` and be exactly one of:
- `column`
- `beam`
- `wall`

## Required evidence
Each detection MUST contain:
- `id`: stable non-empty detection ID.
- `source_id`: source drawing ID.
- `page_id`: source page ID.
- `class_name`: `column`, `beam`, or `wall`.
- `confidence`: finite number in `[0, 1]`.
- `source_box`: finite source-page `xmin`, `ymin`, `xmax`, `ymax` with positive area.
- `coordinate_space`: exactly `"source-page"`.
- `model_name`: approved detector name.
- `model_version`: approved detector version.
- `provenance`: non-empty traceable origin for the emitted evidence.
- `state`: one of `auto-accepted`, `review-required`, `rejected`, `preserved-off-grid`; default handoff state is `review-required`.

## Geometry rule
`source_box` is source-page detector evidence only. Raw pixels, normalized coordinates, calibrated coordinates, project/global engineering coordinates, detector masks, centers, or axes MUST NOT be written as canonical Core geometry by GPT-7.

For `wall`, the evidence box does not establish wall centerline, boundary, thickness, endpoints, openings, elevation, vertical extent, connectivity, topology, or a Core `Surface`.

GPT-6 owns deterministic source-to-normalized-to-calibrated-to-global transformation and canonical engineering reconstruction.

## Provenance
`provenance` MUST survive framework-specific inference and contract adaptation and remain traceable to the detector run/model artifact. A filename or display label alone is insufficient.

## Compatibility
- v0.1 evidence accepts only `column` and `beam`.
- v0.2 candidate evidence adds `wall`.
- A `wall` record represented as v0.1 evidence MUST be rejected.
- Legacy valid v0.1 records remain valid under their v0.1 contract.

## Activation gate
This contract is not active until ontology v0.2, annotation/validation v0.2, wall dataset QA migration, GPT-6 valid-wall acceptance regression, GPT-6 v0.1 wall-rejection regression, legacy compatibility regression, provenance regression, and `source-page` regression are approved.
