# Structuctural Detection Annotation Specification v0.2 — Active

## Status and authority
Active specification for `column`, `beam`, and `wall` under the active v0.2 ontology. It is bound to `contracts/label-ontology-v0.2.md` and `contracts/structural-detection-evidence-v0.2.md`. Legacy v0.1 remains valid for `column` and `beam` and MUST reject `wall`.

Annotations are detection training/evaluation evidence only and MUST NOT create Core entities, engineering coordinates, scale, topology, levels, or final engineering geometry.

## Annotation unit and coordinates
One annotation represents one visible structural component instance on one source page. Use tight axis-aligned `xmin,ymin,xmax,ymax` boxes in original `source-page` coordinates with positive area. Do not store resized, tiled, normalized, calibrated, project, or global coordinates.

## Class rules
### `column`
Annotate the visible plan-footprint graphic whose primary semantic intent is a structural column. Exclude grids, labels, leaders, dimensions, inferred centers, nonstructural posts/pedestals, and unresolved symbols.

### `beam`
Annotate the full visible beam graphic footprint. A box center or long axis is not an engineering centerline or endpoint. Exclude grids, dimensions, leaders, cut lines, bracing, walls, slab edges, rebar, and nonstructural linework.

### `wall`
Annotate only visible source-drawing graphics whose primary semantic intent is a structural wall.

Include a wall when structural-wall semantics are reliable from the visible source view and the wall graphic itself is physically present.

Exclude: architectural partitions without reliable structural semantics; slab or foundation edges that are not wall graphics; grids, dimensions, leaders, notes, and cut lines; ambiguous hatch/poche regions whose ownership or structural meaning is unresolved; hidden or inferred continuation; and walls inferred only from schedules, notes, other pages, or engineering assumptions.

Do not create `ambiguous-wall`. Use QA metadata and adjudication.

For the first wall-capable dataset, box the visible wall graphic using the smallest axis-aligned rectangle containing the visible wall strokes/poche/hatch that belong to the instance. Do not convert paired boundary lines into an engineering centerline, infer thickness, bridge openings, or extrapolate beyond visible graphics.

## Wall QA and dataset migration
Every new wall candidate requires human QA before promotion to approved training/evaluation evidence. Do not mutate the v0.1 two-class baseline. Re-review every included page for walls; missing wall annotations in v0.1 are not valid negative wall labels. Preserve stable `project_group_id` grouping and train/validation/test isolation. Exact or near cross-split duplicates block release.

## QA record
Preserve annotation ID, source ID, page ID, project group ID, class, box, annotator, reviewer, disposition, flags, and spec version. Preserve original, review, and adjudication trail. Approved/corrected-approved records must have no unresolved blocking ambiguity flags.

## GPT-6 boundary
Annotation boxes are source-page detector evidence only. GPT-6 owns transforms, scale, wall centerline/boundary/thickness/openings, levels/elevations/vertical extents, connectivity/topology, engineering geometry, Core mapping, StructuralModel, and 3D integration.

## Activation evidence
Activation prerequisites are recorded as PASS in `contracts/migration-v0.1-to-v0.2-verification-2026-09-21.json`. Detection CI run #8 / run ID 35688458443 succeeded for commit `a8fd4d27886ece4e1b2e8babe69b14b8e28b29cf`. GPT-6 consumer CI run #119 / run ID 35687979404 succeeded for commit `ee9ee5db6d5c382b9eb72d0b3c399de4947987b1`.
