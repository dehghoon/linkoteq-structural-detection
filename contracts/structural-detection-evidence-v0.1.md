# Structural Detection Evidence Contract v0.1

## Ownership boundary

GPT-7 owns dataset preparation, annotation, detector selection, training/fine-tuning, evaluation, active learning, model registry, artifact approval, and inference.

GPT-6 owns grid/OCR/scale, geometry-semantic fusion, column association, beam centerline/endpoints, topology reconstruction, human-review evidence, Core mapping, and 3D structural reconstruction.

Detector output is evidence only. GPT-7 MUST NOT emit canonical Core Node, Member, Surface, GridLine, or engineering geometry.

## Required evidence

Each detection MUST contain:
- `id`: stable non-empty detection ID.
- `source_id`: source drawing ID.
- `page_id`: source page ID.
- `class_name`: `column` or `beam`.
- `confidence`: finite number in `[0, 1]`.
- `source_box`: finite source/page-space `xmin`, `ymin`, `xmax`, `ymax` with positive area.
- `model_name`: approved detector name.
- `model_version`: approved detector version.
- `state`: one of `auto-accepted`, `review-required`, `rejected`, `preserved-off-grid`; default handoff state is `review-required`.

## Coordinate rule

`source_box` is detector/source-page evidence only. Raw pixel/source coordinates MUST NOT be written into Core. GPT-6 owns deterministic source-to-normalized-to-calibrated-to-global transformation and canonical engineering geometry.

## Compatibility rule

GPT-7 may use YOLO, RF-DETR, RT-DETR, OBB, segmentation, or another approved detector internally. Framework-specific output MUST be adapted to this contract before handoff.

Any contract change requires coordinated GPT-7/GPT-6 migration evidence and regression tests.
