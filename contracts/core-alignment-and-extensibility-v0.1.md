# Core Alignment and Detection Extensibility v0.1

## Status

Non-activating architecture guidance for GPT-7. This document does not change the active detection ontology, does not activate `wall` handoff, and does not extend Core. The latest approved `dehghoon/linkoteq-structural-core` runtime contract remains authoritative.

## Principle

A detection class is drawing evidence, not a canonical Core entity.

`atext
source drawing -> GPT-7 detection evidence -> GPT-6 reconstruction -> Core canonical model
```

GPT-7 must not create canonical `Node`, `Member`, `Surface`, topology, engineering coordinates, final member endpoints, wall centerlines/boundaries/thickness/openings, or final 3D geometry.

## Current ontology boundary

- Approved v0.1 detection classes: `column`, `beam`.
- Candidate v0.2 detection classes: `column`, `beam`, `wall`.
- Future classes such as `joist`, `slab`, `brace`, foundation elements, symbols, and load-related evidence are not added to v0.2 by this document. They require a future versioned ontology, annotation rules, validation rules, dataset migration, and consumer regression before handoff.

## Core-aligned semantic mapping guidance

| Detection evidence | Expected reconstruction direction | Core boundary |
| --- | --- | --- |
| `column` | GPT-6 determines member identity, nodes, final endpoints, level/vertical extent and connectivity | Canonical linear structural behavior is represented through Core `Member` and `Node` records |
| `beam` | GPT-6 determines member identity, nodes, final endpoints, connectivity and section association | Canonical linear structural behavior is represented through Core `Member` and `Node` records |
| `wall` (candidate v0.2) | GPT-6 determines engineering centerline/boundary, thickness, openings, levels, vertical extent and topology | Core `Surface` represents walls/slabs; detection boxes are not canonical Surface geometry |
| `juist` (future) | Detection evidence may preserve the source-drawing semantic; GPT-6 must determine canonical member mapping and geometry | Current Core does not define a distinct `joist` canonical entity; do not invent one in GPT-7 |
| `slab` (future) | Region/mask or other approved evidence representation may be more appropriate than a box | Core `Surface` represents slabs/walls; GPT-6 owns final engineering boundary and thickness |
| Load-related drawing evidence (future) | GPT-7 may eventually detect symbols, arrows, text/regions and visual associations as evidence only | Canonical loads must use Core `LoadSource`, `LoadCase` and appropriate load primitives such as `NodalLoad`, `MemberPointLoad`, `MemberDistributedLoad` or `SurfacePressureLoad`; GPT-7 must not create these from visual hints alone |

## Extensibilility rules

1. Keep source-drawing semantic classes separate from Core entity types. Names may map closely but they are not identical.
2. Every future class addition requires a versioned ontology change; do not silently extend an active allow-list.
3. Keep `coordinate_space` explicit. For the current detection contract, use `source-page` unless a later approved contract changes it.
4. Preserve stable detection identity, source/page identity, confidence, model/version, provenance and review state across adapter boundaries.
5. Keep detector-private geometry out of Core. A box, mask, center or axis is evidence, not canonical engineering geometry.
6. If a future class cannot be mapped without redefining Core semantics, stop at the boundary and require a versioned Core change before enabling handoff.

## Regression expectations

- v0.1 consumer behavior must remain unchanged: `wall` is rejected.
- While v0.2 remains candidate, `wall` may only appear in candidate/review data and must not be emitted to the active v0.1 consumer.
- Future classes must not be emitted until their own migration and consumer regressions are approved.
- No detection record may imply canonical Core geometry merely because its class name resembles a Core concept.
