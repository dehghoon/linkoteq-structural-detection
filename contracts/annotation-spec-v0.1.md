# Structural Detection Annotation Specification v0.1

## Status and authority

This specification controls GTT-7 annotation for the `column` and `beam` classes. It is bound to `contracts/label-ontology-v0.1.md` and `contracts/structural-detection-evidence-v0.1.md`, with Linkoteq Structural Core v0.5 as the current cross-product reference. Annotations are detection training/evaluation evidence only; they must not create Core entities, engineering coordinates, scale, topology, levels, or final engineering geometry.

## Annotation unit and coordinate space

The annotation unit is one visible structural component instance on one source page. All boxes are axis-aligned `xmin, ymin, xmax, ymax` rectangles in the original source-page coordinate space. `xmin < xmax` and `ymin < ymax` are required. Do not annotate in resized, tiled, normalized, calibrated, or project/global coordinates.

## Class rules

### `column`

Include a distinct graphic or symbol whose primary semantic intent is to represent a structural column in the source view. Annotate the visible plan-footprint evidence of the column, not the grid bubble, grid intersection, text label, leader, dimension, or an inferred center. The presence of a column mark/tag may support the semantic decision, but the text itself is not part of the box unless it is physically inseparable from the component graphic. Exclude non-structural posts/pedestals or unresolved symbols.

### `beam`

Include a distinct graphic whose primary semantic intent is to represent a structural beam in the source view. Annotate the full visible beam graphic footprint for that instance. Do not treat the box, its center, or its long axis as an engineering centerline or final endpoints. Exclude grid lines, dimension lines, leaders, detail/section cut lines, bracing, walls, slab edges, rebar lines, and non-structural linework. A member tag or schedule reference may support the semantic decision but is not itself a beam instance.

## Inclusion, exclusion, and ambiguity

- Annotate only physical component instances visually present on the page; do not infer from schedules, notes, grids, or other pages.
- Do not annotate legend/key examples, typical detail samples, schedule symbols, or duplicate reference graphics unless the dataset manifest explicitly includes the detail as an independent detection scope.
- When class or presence is unresolved, do not guess. Use `ambiguous-class` or `ambiguous-presence` as QA metadata and exclude until adjudicated.
- Ambiguity dispositions are QA metadata only, not ontology classes.

## Bounding-box geometry

Boxes must be tight to the visible component graphic: the smallest axis-aligned rectangle that contains all visible pixels/strokes belonging to the target instance. Exclude non-component text, leaders, dimensions, grids, notes, and adjacent components. Do not add context margin. Use the source-page boundary for clipped targets; do not extrapolate off-page geometry. Keep the annotation tool's deterministic outer-extent convention fixed for the dataset version.

## Edge-case rules

- `partial`: annotate only if class is reliable; box only the visible extent.
- `occluded`: box the visible extent only; do not guess shape under other graphics.
- Overlapping components: one annotation per semantic instance; boxes may overlap. If ownership cannot be separated, use `overlap-ambiguous` and route to QA.
- `duplicate-render`: keep one annotation for the physical instance when stitching, raster overlap, or rendering duplication repeats it. Distinct views/details are not deduped across pages.
- Low-quality: if recognizable, annotate and flag `low-resolution`, `scan-noise`, `faded`, or `compression-artifact`. If unreliable, exclude and route to QA.

## Annotation QA

All annotations must pass automated schema/range validation and human review before becoming an approved dataset version. The QA record preserves `annotation_id`, `source_id`, `page_id`, `project_group_id`, class, box, annotator, reviewer, disposition, flags, and spec version. Reviewers check class, instance count, box tightness, exclusions, edge-case flags, and project grouping.

Class disagreement, missing/invented instance, or material box-extent disagreement requires `adjudication-required`. The adjudicator must differ from the original annotator for class or presence disagreents. Final dispositions are `approved`, `corrected-approved`, `excluded-ambiguous`, or `needs-reannotation`, with a non-empty reason. Preserve the original, review, and adjudication trail.

## Project-level dataset leakage prevention

Assign a stable `project_group_id` before any split. The grouping unit covers all pages, revisions, renders, crops, tiles, derivatives, and exports from the same project or shared source lineage. Split by `project_group_id` before page/image expansion. A project group MUST NOT appear in more than one of train, validation, or test. Exact or near cross-split duplicates block release. QA sampling must not expose test labels to training curation.

## Validation rules

An approved annotation record MUST satisfy:

1. `spec_version` = `0.1` and `coordinate_space` = `source-page`.
2. `class_name` is exactly `column` or `beam`.
3. `annotation_id`, `source_id`, `page_id`, and `project_group_id` are non-empty.
4. Box coordinates are finite; `xmin < xmax` and `ymin < ymax`; and boxes do not exceed source-page bounds.
5. Approved records have no unresolved `ambiguous-class`, `ambiguous-presence`, or `overlap-ambiguous` flag.
6. A dataset split cannot contain the same `project_group_id` across multiple splits.
7. Exact or near-duplicates across splits are release-blocking.
8. Annotation classes and boxes must not be converted into Core entities, engineering centerlines/endpoints, scale, level, or global geometry.

## Change control

Any change to class semantics, inclusion/exclusion, geometry conventions, QA states, or leakage rules requires a new spec version and impact analysis. Any add/rename/merge/split of `column` or `beam` also requires the ontology change control and GPT-6 consumer coordination.
