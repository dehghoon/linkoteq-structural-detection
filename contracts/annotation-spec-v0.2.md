# Structural Detection Annotation Specification v0.2 — Candidate

## Status and authority
Candidate specification for `column`, `beam`, and `wall`. It is bound to candidate `contracts/label-ontology-v0.2.md` and `contracts/structural-detection-evidence-v0.2.md`. v0.1 remains the active baseline until the migration gate passes.

Annotations are detection training/evaluation evidence only and MUST NOT create Core entities, engineering coordinates, scale, topology, levels, or final engineering geometry.

## Annotation unit and coordinates
One annotation represents one visible structural component instance on one source page. Use tight axis-aligned `xmin,ymin,xmax,ymax` boxes in original `source-page` coordinates with positive area. Do not store resized, tiled, normalized, calibrated, project, or global coordinates.

## Class rules
### `column`
Retain v0.1 semantics: annotate the visible plan-footprint graphic whose primary semantic intent is a structural column. Exclude grids, labels, leaders, dimensions, inferred centers, nonstructural posts/pedestals, and unresolved symbols.

### `beam`
Retain v0.1 semantics: annotate the full visible beam graphic footprint. A box center or long axis is not an engineering centerline or endpoint. Exclude grids, dimensions, leaders, cut lines, bracing, walls, slab edges, rebar, and nonstructural linework.

### `wall`
Annotate only visible source-drawing graphics whose primary semantic intent is a structural wall.

Include a wall when structural-wall semantics are reliable from the visible source view and the wall graphic itself is physically present.

Exclude:
- architectural partitions without reliable structural semantics;
- slab or foundation edges that are not wall graphics;
- grids, dimensions, leaders, notes, and cut lines;
- ambiguous hatch/poche regions whose ownership or structural meaning is unresolved;
- hidden or inferred continuation;
- walls inferred only from schedules, notes, other pages, or engineering assumptions.

Do not create `ambiguous-wall`. Use QA metadata and adjudication.

For the first wall-capable dataset, box the visible wall graphic using the smallest axis-aligned rectangle containing the visible wall strokes/poche/hatch that belong to the instance. Do not convert paired boundary lines into an engineering centerline, infer thickness, bridge openings, or extrapolate beyond visible graphics.

At corners/intersections, annotate according to visible semantic instance separation. If ownership between wall instances cannot be resolved reliably, use `overlap-ambiguous` and route to QA rather than inventing segmentation.

Openings interrupt visible wall evidence. Do not fill an opening or infer hidden wall through it. Occluded wall graphics use visible extent only and `occluded` when class remains reliable.

Single-line, paired-line, poche, or hatch wall conventions are acceptable only when structural-wall semantics are reliable for that drawing convention. Low-quality or structurally ambiguous cases go to QA.

## Inclusion, exclusion, and ambiguity
Annotate only physical component instances visually present on the page. Do not infer instances from schedules, notes, grids, or other pages. Exclude legends, typical-detail samples, schedule symbols, and duplicate reference graphics unless the dataset manifest explicitly includes that view as detection scope.

Unresolved class uses `ambiguous-class`; unresolved presence uses `ambiguous-presence`; unresolved overlap ownership uses `overlap-ambiguous`. These are QA metadata, not ontology classes.

## Bounding boxes
Boxes must be tight to visible component graphics with no context margin. Exclude unrelated text, leaders, dimensions, grids, notes, and adjacent components. Clip to the source-page boundary and never extrapolate off-page. Keep a deterministic outer-visible-extent convention for the dataset version.

## Edge cases
- `partial`: annotate visible extent only if class is reliable.
- `occluded`: annotate visible extent only; do not guess hidden shape.
- `duplicate-render`: keep one annotation for a duplicated rendering of the same physical instance in the same view.
- Low quality: if recognizable, annotate and flag `low-resolution`, `scan-noise`, `faded`, or `compression-artifact`; otherwise exclude and route to QA.
- Overlap: one annotation per semantic instance; boxes may overlap. Unresolved ownership is blocking QA.

## Wall QA
Every new wall candidate requires human QA before promotion to approved training/evaluation evidence. Reviewers check structural-vs-architectural semantics, instance count, box tightness, visible-only treatment, openings/occlusion, corners/intersections, paired-line/poche/hatch/single-line conventions, exclusions, and project grouping.

A small multi-drafter wall pilot with adjudication is required before bulk wall annotation.

## Dataset migration
Do not mutate the v0.1 two-class baseline. Create a new wall-capable dataset version bound to ontology/spec v0.2. Re-review every included page for walls; missing wall annotations in v0.1 are not valid negative wall labels.

Preserve stable `project_group_id` grouping and train/validation/test isolation unless separately reviewed. Exact or near cross-split duplicates block release.

## QA record
Preserve annotation ID, source ID, page ID, project group ID, class, box, annotator, reviewer, disposition, flags, and spec version. Preserve original, review, and adjudication trail.

Approved/corrected-approved records must have no unresolved blocking ambiguity flags.

## GPT-6 boundary
Annotation boxes are source-page detector evidence only. GPT-6 owns transforms, scale, wall centerline/boundary/thickness/openings, levels/elevations/vertical extents, connectivity/topology, engineering geometry, Core mapping, StructuralModel, and 3D integration.

## Activation gate
Do not use v0.2 annotations as approved production handoff until ontology v0.2, validation rules v0.2, StructuralDetectionEvidence v0.2, wall dataset QA migration, GPT-6 consumer regression, legacy v0.1 compatibility, provenance regression, and `source-page` regression are approved and passing.
