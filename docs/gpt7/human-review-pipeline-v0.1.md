# Human Review Pipeline v0.1

## Scope

This pipeline governs GPT-7 review for `column` and `beam` detection candidates. It does not create Core entities, engineering centerlines/endpoints, topology, scale, levels, or global engineering geometry.

## Controlling contracts

- `contracts/label-ontology-v0.1.md`
- `contracts/annotation-spec-v0.1.md`
- `contracts/structural-detection-evidence-v0.1.md`
- Core reference: Linkoteq Structural Core v0.5

## Mandatory review gates

### Added columns

Any newly added column candidate beyond the already human-confirmed set MUST remain `review-required` and MUST be shown to the user for visual confirmation. Detector confidence, vector similarity, or pattern matching alone cannot promote it to an approved annotation.

### Beam candidates

Beam candidates shown in the QA overlay, including the orange review candidates, MUST remain `review-required` until explicitly confirmed by the user.

A candidate whose visible graphic reaches a human-confirmed column at at least one end is a high-priority beam review candidate. This is a review-routing heuristic only. It MUST NOT be serialized as engineering connectivity, a canonical endpoint, or a Core member relation.

## Pipeline

1. Detect visible `column` and `beam` candidates in `source-page` coordinates.
2. Assign stable candidate/annotation IDs and preserve provenance.
3. Preserve already human-confirmed annotations and distinguish them from newly added candidates.
4. Keep newly added columns and beam candidates in `review-required`.
5. Render a QA overlay that visually distinguishes:
   - confirmed columns;
   - newly added column candidates requiring user confirmation;
   - beam candidates requiring user confirmation, including high-priority candidates meeting a confirmed column at at least one visible end.
6. Collect an explicit user disposition: `confirmed`, `rejected`, `correction-required`, or `unresolved`.
7. Preserve the review trail with candidate IDs, class, user disposition, and review scope.
8. Only user-confirmed instances may proceed toward `approved` / `corrected-approved`, and only after bounding-box tightness QA and automated validation pass.
9. Rejected or unresolved candidates MUST NOT enter an approved training/evaluation set.

## GPT-6 handoff gate

Only detections that complete the required review and validation may be adapted to `StructuralDetectionEvidence v0.1`. The handoff remains detector evidence only and MUST preserve `coordinate_space: source-page` and traceable provenance.
