# GPT-7 Dataset and Training Input Policy v0.1

## Status
Approved documentation/training-input reconciliation for active StructuralLayoutProposal v0.1. This policy does not authorize detector training or change StructuralDetectionEvidence v0.2, ontology, or ownership.

## Preserved boundary
StructuralDetectionEvidence v0.2 remains active; detector classes remain exactly `column`, `beam`, `wall`; coordinate space remains `source-page`; GPT-7 emits no canonical engineering geometry; legacy v0.1 column/beam compatibility and v0.1 wall rejection remain unchanged.

## StructuralLayoutProposal exclusion
Every GPT-6 StructuralLayoutProposal record, including proposed grids, columns, beams, or walls, is a reconstruction/proposal artifact and not a source observation. A proposal MUST NOT by itself become StructuralDetectionEvidence, a GPT-7 source annotation, detector training/evaluation ground truth, or negative/background source evidence. Human approval of an engineering proposal does not retroactively make it visible source evidence.

## Dataset admission
A proposal-corresponding label may enter an approved GPT-7 detection dataset only after an independent source-evidence/adjudication process establishes the corresponding observed `column`, `beam`, or `wall` under the active GPT-7 ontology, annotation specification, validation rules, and dataset QA contract. The admitted label MUST be derived from the independently adjudicated original source, preserve source/page provenance, `source-page` coordinates, and review state. The GPT-6 proposal may remain only as separate contextual provenance and is not ground-truth authority. If visible source evidence cannot be independently established, the proposal remains excluded. Unreviewed or missing labels MUST NOT become background/negative evidence.

## Synthetic/rendered overlays
Synthetic, rendered, or presentation overlays produced from GPT-6 proposals MUST NOT be reprocessed through GPT-7 to manufacture detector provenance, source observations, annotations, or ground truth. Any separately approved robustness experiment on such overlays remains experiment-only and cannot promote detector ground truth without the independent source-evidence/adjudication process above.

## Versioning and gates
Dataset evolution MUST create a new version rather than mutate a released baseline, preserving project-group split isolation and exact/near duplicate/leakage gates. This reconciliation does not satisfy YOLO training-readiness gates, authorize training, or authorize promotion. `enablesTraining` remains `false` until all applicable dataset/export/split/evaluation/registry/approval gates pass.

## Reconciliation evidence
GPT-6 activation reference: `dehghoon/linkoteq-drawing-reconstruction` commit `019290b100db152ab495f2ab10f6ed7409083e83`; GPT-6 contract `contracts/structural-layout-proposal-v0.1.md`; GPT-7 evidence contract `contracts/structural-detection-evidence-v0.2.md`; annotation contract `contracts/annotation-spec-v0.2.md`; continuous-improvement contract `contracts/detector-continuous-improvement-v0.1.md`.
