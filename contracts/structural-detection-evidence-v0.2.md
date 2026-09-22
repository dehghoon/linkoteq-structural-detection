# Structural Detection Evidence Contract v0.2 — Active

## Status
Active contract for the coordinated v0.2 handoff. Legacy v0.1 remains valid for `column` and `beam` and MUST reject `wall`.

## Ownership boundary
GPT-7 owns detection evidence production. GPT-6 owns engineering reconstruction and Core mapping. Detector output is evidence only.

## Label ontology
`class_name` MUST conform to `contracts/label-ontology-v0.2.md` and be exactly one of: `column`, `beam`, `wall`.

## Required evidence
Each detection MUST contain: `id` stable non-empty detection ID; `source_id`; `page_id`; `class_name`; `confidence` finite in `[0,1]`; `source_box` finite `xmin,ymin,xmax,ymax` with positive area; `coordinate_space` exactly `"source-page"`; `model_name`; `model_version`; non-empty traceable `provenance`; and `state` one of `auto-accepted`, `review-required`, `rejected`, `preserved-off-grid`. Default handoff state is `review-required`.

## Geometry rule
`source_box` is source-page detector evidence only. Raw pixels, normalized coordinates, calibrated coordinates, project/global engineering coordinates, detector masks, centers, or axes MUST NOT be written as canonical Core geometry by GPT-7.

For `wall`, the evidence box does not establish wall centerline, boundary, thickness, endpoints, openings, elevation, vertical extent, connectivity, topology, or a Core `Surface`. GPT-6 owns deterministic source-to-normalized-to-calibrated-to-global transformation and canonical engineering reconstruction.

## Provenance
`provenance` MUST survive framework-specific inference and contract adaptation and remain traceable to the detector run/model artifact. A filename or display label alone is insufficient.

## Compatibility
- v0.1 evidence accepts only `column` and `beam`.
- v0.2 evidence adds `wall`.
- A `wall` record represented as v0.1 evidence MUST be rejected.
- Legacy valid v0.1 records remain valid under their v0.1 contract.

## Activation evidence
The coordinated activation prerequisites are recorded as passing in `contracts/migration-v0.1-to-v0.2-verification-2026-09-21.json`. Detection CI run #8 / run ID 35688458443 succeeded for commit `a8fd4d27886ece4e1b2e8babe69b14b8e28b29cf`. GPT-6 consumer CI run #119 / run ID 35687979404 succeeded for commit `ee9ee5db6d5c382b9eb72d0b3c399de4947987b1`. Provenance, `source-page`, valid v0.2 wall acceptance, v0.1 wall rejection, and legacy v0.1 column/beam compatibility are required and preserved.

## Training boundary
Activation of this evidence handoff does NOT imply detector training readiness. Training remains gated by separate dataset completeness, freeze, export, model and evaluation prerequisites.
