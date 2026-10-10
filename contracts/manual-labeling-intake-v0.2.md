# Manual Labeling Intake Contract v0.2
Status: Active. Owner: GPT-7. Boundary: LinkoTech Website -> GPT-7 dataset admission.

## Authority

This operational contract preserves ontology v0.2, StructuralDetectionEvidence v0.2, source-page semantics, and the GPT-6 reconstruction boundary. Active classes remain exactly `column`, `beam`, `wall`.

Manual annotations use annotation-spec v0.3 for new revisions. Existing annotation-spec v0.2 annotations remain valid and readable. GPT-7 retains ontology, dataset-admission, split, duplicate/leakage, export/training/evaluation, registry, and evidence authority. Website/Employees cannot create or redefine classes.

## Lifecycle and roles

`candidate -> suitable-for-labeling -> labeling-in-progress -> submitted-for-owner-qa -> owner-approved | owner-rejected | revision-required -> gpt7-dataset-admission`.

Owner approval is necessary but insufficient for GPT-7 dataset admission or training readiness.

## Minimum payload

Required:
- `schema_version=manual-labeling-intake-v0.2`
- stable `candidate_id`, `source_id`, `page_id`, `project_group_id`
- source origin/ref, lowercase SHA-256, original filename/page identity, preserved-artifact flag
- effective page geometry and validated reversible transform metadata when raster/display is used
- annotations with stable `annotation_id`, exact class, required axis-aligned `bbox`, `annotation_spec_version`, flags
- optional `oriented_bbox` under annotation-spec v0.3
- workflow state, operator/owner identities and timestamps, append-only audit/adjudication history, tool/version, provenance

Source artifacts are immutable/traceable and are not destructively overwritten.

## Annotation geometry

Every annotation MUST preserve the required source-page PDF-point `bbox`.

For annotation-spec v0.3, `oriented_bbox` MAY additionally be present:

```json
{
  "center_x": 0,
  "center_y": 0,
  "width": 1,
  "height": 1,
  "rotation_deg": 0
}
```

The required `bbox` MUST tightly enclose the oriented rectangle. `rotation_deg` is normalized to `[-180, 180)`. All oriented corners MUST be within effective source-page bounds.

Existing v0.2 annotations without `oriented_bbox` remain valid and are interpreted as zero-rotation axis-aligned annotations.

Missing, unresolved, ambiguous, or `NO-SAFE-BOX` regions are never negative/background evidence. GPT-6 proposals, reconstructed geometry, synthetic overlays, inferred continuation, or generated reconstruction artifacts are excluded from observed detector ground truth.

## Authoritative coordinates

Admitted annotations MUST use `coordinate_space="source-page"` and `unit="pdf-point"` with effective-page top-left origin, +x right, +y down. Pixel-only evidence cannot pass admission without deterministic validated reversible mapping.

## Review history

History is append-only. Employee cannot create Owner adjudication. Owner approval cannot create GPT-7 admission.

## Duplicates, splits, admission

Exact/near duplicates remain detectable and traceable; `project_group_id` is preserved. GPT-7 owns project-group isolation and cross-split duplicate/leakage gates.

GPT-7 admission requires valid identities/provenance/SHA-256, preserved source, active class/spec, complete human trail, valid source-page geometry and transform evidence where applicable, no blocking ambiguity, observed-source evidence, QA compliance, and duplicate/leakage/project-group compliance.

## YOLO/training boundary

Owner approval does not authorize training. Training remains disabled until the independent GPT-7 gates pass and a versioned immutable dataset release is produced.

## Compatibility

- manual-labeling-intake v0.1 remains readable.
- annotation-spec v0.2 remains readable.
- new oriented annotations use annotation-spec v0.3.
- downstream axis-aligned consumers MAY use the required `bbox` envelope but MUST preserve `oriented_bbox` in versioned intake artifacts.
