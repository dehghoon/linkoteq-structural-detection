# Structural Detection Label Ontology v0.2 — Candidate

## Status
Candidate for coordinated wall migration. This file does not activate v0.2 until the migration gate is satisfied.

## Version
- ontology_name: `linkoteq-structural-detection-labels`
- ontology_version: `0.2`
- detection_contract: `StructuralDetectionEvidence v0.2`
- core_reference: `Linkoteq Structural Core v0.5`

## Labels
The exact proposed label set is:
- `column`
- `beam`
- `wall`

`column` and `beam` retain their v0.1 detection-boundary semantics.

`wall` means visible source-drawing evidence whose primary semantic intent is a structural wall. It is detector evidence only, not a canonical Core `Surface` and not proof of engineering centerline, boundary, thickness, endpoints, openings, elevation, vertical extent, connectivity, or topology.

Exclude architectural partitions without reliable structural semantics, slab/foundation edges that are not wall graphics, grids, dimensions, leaders, notes, cut lines, ambiguous hatch regions, inferred continuation, and walls inferred only from schedules, other pages, or engineering assumptions. Route unresolved structural-vs-nonstructural cases to QA.

Do not create `ambiguous-wall`; ambiguity is QA metadata.

## Boundary
GPT-7 emits reviewed source-page detection evidence only. GPT-6 owns deterministic transforms, scale, geometry-semantic fusion, engineering reconstruction, wall centerline/boundary/thickness/openings, vertical extent, connectivity/topology, Core mapping, StructuralModel, and downstream 3D integration.

## Compatibility
v0.1 remains exactly `column` and `beam`. A `wall` record claiming v0.1 semantics is invalid.

## Activation gate
Do not activate v0.2 until annotation rules, validation rules, StructuralDetectionEvidence v0.2, wall-capable dataset migration, GPT-6 consumer regression, legacy v0.1 compatibility regression, provenance checks, and `source-page` checks are approved and passing.
