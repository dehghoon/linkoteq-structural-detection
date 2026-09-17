# Structural Detection Evidence Contract v0.1

## Ownership boundary

GPT-7 owns dataset preparation, annotation, detector selection, training/fine-tuning, evaluation, active learning, model registry, artifact approval, and inference.

GPT-6 owns grid/OCR/scale, geometry-semantic fusion, column association, beam centerline/endpoints, topology reconstruction, human-review evidence, Core mapping, and 3D structural reconstruction.

Detector output is evidence only. GPT-7 MUST NOT emit canonical Core Node, Member, Surface, GridLine, or engineering geometry.

## Label ontology

`class_name` MUST conform to `contracts/label-ontology-v0.1.md`. The initial approved semantic classes are `column` and `beam`. These labels are detection semantics, not canonical Core entity types.

## Required evidence

Each detection MUST contain:
- `id`: stable non-empty detection ID.
- `source_id`: source drawing ID.
- `page_id`: source page ID.
- `class_name`: `column` or `beam`, as limted by the label ontology.
- `confidence`: finite number in `[0, 1]`.
- `source_box`: finite source-page space `xmin`, `ymin`, `xmax`, `ymax` with positive area.
- `coordinate_space`: must be exactly `"source-page"` in v0.1.
- `model_name`: approved detector name.
- `model_version`: approved detector version.
- `provenance`: non-empty traceable origin for the emitted evidence, such as inference run/artifact reference.
- `state`: one of `auto-accepted`, `review-required`, `rejected`, `preserved-off-grid`; default handoff state is `review-required`.

## Coordinate rule

`source_box` is detector source-page evidence only. The declared `coordinate_space` is mandatory so the consumer does not infer a frame. Raw pixel/source coordinates MUST NOT be written into Core. GPT-6 owns the deterministic source-to-normalized-to-calibrated-to-global transformation and canonical engineering geometry.

## Provenance rule

``rovenance` MUST be preserved across framework-specific inference and the contract adapter. It MUST NOT be replaced by a filename or display label that cannot be traced to the detector run/model artifact.

## Compatibility rule

GPT-7 may use YOLO, RF-DETR, RT-DETR, OBB, segmentation, or another approved detector internally. Framework-specific output MUST be adapted to this contract before handoff.

Any contract change requires coordinated GPT-7/GPT-6 migration evidence and regression tests.
