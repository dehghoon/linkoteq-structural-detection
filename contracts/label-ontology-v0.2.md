# Structural Detection Label Ontology v0.2 — Active

## Status
Active for the coordinated StructuralDetectionEvidence v0.2 handoff. Legacy v0.1 remains compatible for `column` and `beam`; `wall` is invalid under v0.1.

## Version
- ontology_name: `linkoteq-structural-detection-labels`
- ontology_version: `0.2`
- detection_contract: `StructuralDetectionEvidence v0.2`
- core_reference: `Linkoteq Structural Core v0.5`

## Labels
The exact active label set is:
- `column`
- `beam`
- `wall`

`column` and `beam` retain their v0.1 detection-boundary semantics.

`wall` means visible source-drawing evidence whose primary semantic intent is a structural wall. It is detector evidence only, not a canonical Core `Surface` and not proof of engineering centerline, boundary, thickness, endpoints, openings, elevation, vertical extent, connectivity, or topology.

Exclude architectural partitions without reliable structural semantics, slab/foundation edges that are not wall graphics, grids, dimensions, leaders, notes, cut lines, ambiguous hatch regions, inferred continuation, and walls inferred only from schedules/other pages. Route unresolved cases to QA.

Do not create `ambiguous-wall`; ambiguity is QA metadata.

## Boundary
GPT-7 emits reviewed source-page detection evidence only. GPT-6 owns transforms, scale, geometry-semantic fusion, engineering reconstruction, wall centerline/boundary/thickness/openings/vertical extent, connectivity/topology, Core mapping, StructuralModel, and downstream 3D integration.

## Compatibility
v0.1 remains exactly `column` and `beam`. A `wall` record claiming v0.1 semantics is invalid.

## Activation evidence
Activation prerequisites are recorded in `contracts/migration-v0.1-to-v0.2-verification-2026-09-21.json`. Detection CI run #8 / run ID 35688458443 succeeded for commit `a8fd4d27886ece4e1b2e8babe69b14b8e28b29cf`; GPT-6 consumer CI run #119 / run ID 35687979404 succeeded for commit `ee9ee5db6d5c382b9eb72d0b3c399de4947987b1`.
