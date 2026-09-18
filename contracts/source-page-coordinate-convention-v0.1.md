# Source-Page Coordinate Convention v0.1

## Scope

This document fixes the detector-side coordinate convention used by the pilot dataset and by StructuralDetectionEvidence v0.1 serialization. It does not define engineering coordinates, scale, topology, levels, member centerlines, or final member endpoints.

## Coordinate frame

- `coordinate_space` is exactly `source-page`.
- Units are PDF points (`1/72 inch`).
- The origin is the top-left corner of the effective source page.
- Positive `x` points right.
- Positive `y` points down.
- Axis-aligned boxes are serialized as `xmin`, `ymin`, `xmax`, `ymax`.
- Valid boxes require finite coordinates, `xmin < xmax`, and `ymin < ymax`.

## Effective page box

For pilot-v0.1, the effective page is the recorded CropBox in `datasets/pilot-v0.1/source-page-geometry.json`. When CropBox and MediaBox are equal, the shared extent is used. A future source whose CropBox differs from MediaBox must be normalized to the effective CropBox before annotation serialization and must retain both boxes in source-page geometry metadata.

## Rotation

The stored source-page frame is the displayed page after applying the recorded PDF page rotation. Pilot-v0.1 currently contains only selected pages with rotation `0`. Non-zero rotation requires an explicit tested transform before such pages may enter an approved dataset version.

## Render-to-source mapping

Rendering is an annotation aid only. Pixel coordinates must never be stored as annotation coordinates.

For an unrotated effective page rendered without translation at scale factors `sx` and `sy`:

`x_source = x_pixel / sx`

`y_source = y_pixel / sy`

For a crop/tile rendered from source-page origin `(crop_xmin, crop_ymin)`:

`x_source = crop_xmin + x_pixel / sx`

`y_source = crop_ymin + y_pixel / sy`

Any renderer-specific translation or rotation must be represented by an explicit invertible render matrix and inverted before serialization.

## Bounding-box outer extent

Annotation boxes contain the full visible graphic footprint. For stroked vector primitives, the visible outer stroke extent is included. Text, leaders, grids, dimensions, notes, and adjacent component graphics are excluded unless the annotation specification explicitly states otherwise.

## Consumer boundary

These coordinates are detector evidence only. GPT-6 owns deterministic source-to-normalized/calibrated/global transforms and any engineering geometry derived after evidence fusion. GPT-7 must not write source-page coordinates directly into canonical Core geometry.
