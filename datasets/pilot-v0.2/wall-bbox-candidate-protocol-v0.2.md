# Wall BBox Candidate Protocol v0.2

## Status

Candidate protocol for the pilot v0.2 wall QA migration. It does not activate wall handoff and does not change the active StructuralDetectionEvidence v0.1 contract.

## Authoritative rules

- Class: `wall` only for visible source-drawing evidence with reliable structural-wall semantics.
- Geometry: tight axis-aligned `xmin, ymin, xmax, ymax` boxes.
- Coordinate space: `source-page` only.
- No hidden continuation, opening bridging, wall thickness inference, centerline reconstruction, or cross-page label transfer.
- Architectural partitions, grids, dimensions, leaders, notes, cut lines, and ambiguous hatch are excluded.
- Unresolved class/presence/overlap uses the v0.2 QA flags and cannot be promoted.
- Every new wall candidate requires human QA before approved training/evaluation use.

## Render to source-page conversion

The pilot `source-page-geometry.json` is authoritative for page bounds. For the two semantically confirmed Mx101 pages:

- `src-lacmark-242536-str-2024 / p02`: 3456 x 2592 PDF points, rotation 0.
- `src-p2026-130-260890-permit / p02`: 3456 x 2592 PDF points, rotation 0.
- The verification renders are 6912 x 5184 pixels, exactly 2 render pixels per source-page point on both axes.
- The detection dataset's source-page convention is top-left, x right, y down. For these verified renders: `x_source = x_px / 2`, `y_source = y_px / 2`.
- This dataset convention is intentionally different from raw PDF user space's bottom-left origin. Do not flip y again when writing dataset annotations.

## Candidate workflow

1. Render the exact pilot page and record render width/height.
2. Verify render size, CropBox, MediaBox, and rotation against `source-page-geometry.json`.
3. Inspect the plan region at high resolution. Use tiles only as a review aid; the final box is stored in full-page source coordinates.
4. Segment only visible structural-wall graphics into semantically separable instances.
5. Stop an instance at a visible opening or where hidden continuation would have to be inferred.
6. If corner/intersection ownership cannot be resolved from visible evidence, flag `overlap-ambiguous` rather than inventing segmentation.
7. Convert the tight render box to source-page coordinates using the verified page transform.
8. Emit `qa_state: review-required` for new candidates. No candidate is `approved` without human QA.

## Pilot scope disposition

The 14-page review checkpoint is the page-level queue. Only the two Mx101 pages currently have human-confirmed wall semantics. The three medium-evidence pages remain direct-visual-review candidates. Low-evidence pages must not be treated as valid wall negatives solely because v0.1 had no wall labels.

## GPT-6 boundary

These boxes are detection/annotation evidence only. They MUST NOT be converted by GPT-7 into engineering wall centerlines, boundaries, thicknesses, endpoints, openings, vertical extents, Core Surfaces, or final engineering geometry.
