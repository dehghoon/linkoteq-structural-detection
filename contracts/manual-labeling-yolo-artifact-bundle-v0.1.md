# Manual Labeling YOLO Artifact Bundle v0.1

## Status

GPT-7 staging/materialization contract. This contract does not authorize training. `enablesTraining=false` remains mandatory.

## Required sample bundle

A YOLO sample is not complete with label text alone. After explicit GPT-7 dataset admission, each admitted sample must preserve the authoritative source drawing and materialize the exact deterministic raster used by YOLO:

```text
<sample_id>/
├── intake.json
├── manifest.json
├── source/original.pdf
├── images/<sample_id>.png
└── labels/<sample_id>.txt
```

`source/original.pdf` is immutable provenance. The PNG is derived from the admitted source page and validated transform. The TXT file is YOLO serialization for that exact PNG.

## Preconditions

Materialization requires:

- Owner QA state `owner-approved`.
- GPT-7 dataset admission `gpt7-admitted`.
- Preserved source artifact with verified SHA-256.
- Annotation coordinates in `source-page` / `pdf-point`.
- Validated reversible source-page/raster transform.
- Exact classes `column`, `beam`, `wall`.
- GPT-7 project-group, split, duplicate, and leakage decisions preserved.

Materialization does not set `training_ready=true`.

## Deterministic raster and labels

Raster dimensions must equal `transform.raster_width_px` and `transform.raster_height_px`. Screenshots, arbitrary PDF converters, rescaled copies, and user-modified images are not valid substitutes.

Transform all four source-page bounding-box corners through `source_page_to_raster_affine`, rebuild the raster-space axis-aligned box, then serialize:

```text
class_id x_center_ratio y_center_ratio width_ratio height_ratio

0 = column
1 = beam
2 = wall
```

Normalized values must be finite and within `[0,1]`, with positive width and height.

## Manifest

`manifest.json` must record bundle/sample/candidate/source/page/project-group IDs; source PDF, raster, and label paths plus SHA-256; raster dimensions; class map; transform/rendering version; dataset admission and split; Owner QA state; provenance; and:

```text
training_ready=false
training_enabled=false
enablesTraining=false
```

## GitHub and privacy

Website-uploaded structural drawings are private operational artifacts. The current `dehghoon/linkoteq-structural-detection` repository is public and must not receive private website source PDFs, rasters, or label bundles.

Runtime bundles may be archived to GitHub only in a dedicated repository whose visibility has been verified as `private`, or in approved private object storage referenced by a versioned GitHub manifest. GitHub remains the versioning/orchestration boundary. Never commit secrets, tokens, signed URLs, or authentication cookies.

## Immutability and boundary

Published bundles are append-only. A changed source, raster, transform, annotation set, split, or class serialization creates a new versioned bundle.

```text
Owner Approved
-> GPT-7 Dataset Admission
-> source PDF + deterministic raster + YOLO label bundle
-> GPT-7 split/duplicate/export gates
-> future training-readiness decision

enablesTraining = false
```
