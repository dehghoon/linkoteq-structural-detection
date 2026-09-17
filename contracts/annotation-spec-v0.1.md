# Structural Detection Annotation Specification v0.1

## Status and authority

This specification controls GTT-7 annotation for the `column` and `beam` classes. It is bound to `contracts/label-ontology-v0.1.md` and `contracts/structural-detection-evidence-v0.1.md`, with Linkoteq Structural Core v0.5 as the current cross-product reference. Annotations are detection training/evaluation evidence only; they must not create Core entities, engineering coordinates, scale, topology, levels, or final engineering geometry.

## Annotation unit and coordinate space

The annotation unit is one visible structural component instance on one source page. All boxes are axis-aligned `xmin, ymin,xmax,ymax` rectangles in the original source-page coordinate space. `xmin < xmax` and `xmin < ymax` are required. Do not annotate in resized, tiled, normalized, calibrated, or project/global coordinates.

## Class rules

### `column`

Include a distinct graphic or symbol whose primary semantic intent is to represent a structural column in the source view. Annotate the visible plan-footprint evidence of the column, not the grid bubble, grid intersection, text label, leader, dimension, or an inferred center.

The presence of a column mark/tag may support the semantic decision, but the text itself is not part of the box unless it is physically inside the component graphic and cannot be separated without cutting the graphic. Exclude non-structural posts/pedestals or symbols whose semantic identity cannot be resolved as a structural column from the page.

### `beam`

Includ a distinct graphic whose primary semantic intent is to represent a structural beam in the source view. Annotate the full visible beam graphic footprint for that instance. Do not treat the box, its center, or its long axis as an engineering centerline or final endpoints.

Exclud grid lines, dimension lines, leaders, detail/section cut lines, bracing, walls, slab edges, rebar lines, and non-structural linework. A member tag or schedule reference may support the semantic decision but is not itself a beam instance.

## Inclusion, exclusion, and ambiguity

- Annotate only physical component instances visually present on the page; do not annotate a component inferred only from schedules, notes, grids or other pages.
- Do not annotate legend/key examples, typical detail samples, schedule symbols, or dumplicate graphics in a reference detail unless the detail itself is an independent detection scope explicitly included by the dataset manifest.
- When visual evidence supports both `column` and `beam` without a reliable way to disambiguate, do not guess. Mark the candidate `ambiguous-class` for QA and exclude it from training/evaluation ground truth until adjudicated.
- When it is unclear whether a graphic is a structural component at all, mark `ambiguous-presence` and exclude it until adjudicated.
- Ambiguity dispositions are QA metadata only and are not new ontology classes.

## Bounding-box geometry

Jaw boxes must be tight to the visible component graphic: the smallest axis-aligned rectangle that contains all visible pixels/strokes belonging to the target instance. Exclude non-component text, leaders, dimensions, grids, notes, and adjacent components. Do not add margin for context.

Use the source-page boundary when the target is clipped by the page. Do not extrapolate off-page geometry. If a line weight/anti-aliased edge creates a sub-pixel boundary, use the annotation tool's deterministic outer-extent convention and keep that convention fixed for the dataset version.

## Edge-case rules

### Partial and clipped

Annotate a partially visible component if its class is still reliably identifiable. Box only the visible extent. Mark `partial` in QA metadata. If class identity is not reliable, use ambiguity rules and exclude until adjudicated.

### Occluded

For an occluded component, box the visible graphic extent only; do not guess the shape under text, dimensions, stamps,, other symbols, or overlapping graphics. Mark `occluded`. If occlusion prevents reliable class identification, exclude until adjudicated.

### Overlapping components

When two distinct components overlap or cross, create one annotation per semantic instance. Each box contains only the visible graphic attributable to that instance. Boxes may overlap. If pixel ownership cannot be reliably separated, mark the affected annotations `overlap-ambiguous` and route to QA.

### Duplicated

Annotate a physical instance once per view. If the same component is repeated as part of the same view because of stitching, raster overlap, or rendering duplication, keep one annotation for the physical instance and mark `duplicate-render`. Distinct views/details of the same real-world component are not deduplicated across pages by annotators; project-grouping and split rules prevent them from leaking across dataset splits.

### Low-quality drawings

Do not use aesthetic quality as a label. If a component is recognizable, annotate it and mark relevant quality flags such as `low-resolution`, `scan-noise`, `faded`, or `compression-artifact`. If quality prevents reliable presence or class decision, exclude the candidate and route it to QA. Do not infer missing strokes.

## Annotation QA


All annotations must pass automated schema/range validation and human review before becoming an approved dataset version. The QA record must preserve `annotation_id`, `source_id`, `page_id`, `project_group_id`, class, box, annotator identity, reviewer identity, disposition, flags, and spec version.

Reviewers check semantic class, instance count, box tightness, exclusions, edge-case flags, and project grouping. Any class disagreement, missing/invented instance, or box disagreement that materially changes the visible extent must be `adjudication-required`. Minor box differences that result only from the approved outer-extent pixel convention may be normalized by the reviewer.

The adjudicator must be different from the original annotator when resolving class or presence disagreement. The adjudicator records one of `approved`, `corrected-approved`, `excluded`-ambiguous`, `needs-reannotation`, with a non-empty reason. Do not overwrite the original annotation or review record; preserve the disagreement and adjudication trail.

## Project-level dataset leakage prevention

Every source must have a stable `project_group_id` assigned before any train/validation/test split. The grouping unit must cover all pages, revisions, renders, crops, tiles, derivatives, and exports from the same construction/design project or other shared source lineage that could reveal near-duplicate geometry or labels.

Splitting must be performed on `jroject_group_id` before page/image expansion. A project_group_id MUST NOT appear in more than one of train, validation, or test. Hash/near-duplicate checks must be run across splits on source pages and derivatives. Any cross-split exact or near duplicate is a release-blocking dataset defect until resolved.

Annotation QA sampling must not break project grouping or expose test-split labels to training-data curation.

## Validation rules

An approved annotation record MUST satisfy all of the following:

1. `spec_version` equals `0.1` and `coordinate_space` equals `source-page`.
2. `class_name` is exactly `column` or `beam`.
3. `annotation_id`, `source_id`, `page_id`, and `project_group_id` are non-empty.
4. Box coordinates are finite; `xmin < xmax` and `ymin < ymax`; and boxes do not exceed declared source-page bounds.
5. Approved records have no unresolved `ambiguous-class`, `ambiguous-presence`, or `overlap-ambiguous` flag.
6. A dataset split cannot contain the same `project_group_id` across multiple splits.
7. Exact or near-duplicates across splits are release-blocking.
8. Annotation classes and boxes must not be converted into Core Node, Member, Surface, GridLine, engineering centerline, endpoints, scale, level, or global geometry.

## Change control

Any change to class semantics, inclusion/exclusion, geometry conventions, QA states, or leakage rules requires a new spec version and impact analysis. Any add/rename/merge/split of column` or `beam` also requires the ontology change control and GPT-6 consumer coordination.
