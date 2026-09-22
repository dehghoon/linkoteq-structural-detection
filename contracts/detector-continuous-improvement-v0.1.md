# Detector Continuous Improvement Contract v0.1

## Status

Approved lifecycle contract for GPT-7 detector improvement. This contract does not change the active label ontology or StructuralDetectionEvidence handoff contract.

## Ownership

GPT-7 owns detector QA feedback ingestion, active-learning queues, dataset versioning, training, evaluation, model registry, promotion evidence, and rollback artifacts. Security remains GPT-5 ownership; cross-repository deployment/orchestration remains GPT-4 ownership.

## Feedback and training eligibility

User usage or a model prediction MUST NOT automatically become training ground truth. Only human-approved QA evidence under the approved annotation specification may be promoted to the training/evaluation pool. Unreviewed, ambiguous, or missing labels MUST NOT be treated as background.

All promoted evidence MUST preserve source/page provenance, coordinate space, review state, and applicable class/ontology version.

## Retraining triggers

Retraining is event-driven, not timer-driven. During the initial low-volume production phase:

- QA feedback SHOULD be aggregated continuously.
- An admin review SHOULD be produced monthly even if no retraining is warranted.
- A standard retraining candidate SHOULD be considered after approximately 100-200 new human-approved corrections/annotations, provided they are sufficiently diverse across projects, drawing types, and active classes.
- The count threshold is a starting operational default, not a quality substitute. Data diversity and error value may defer retraining even after the count is met.
- A critical or repeated error pattern across independent projects MAY trigger early candidate training without waiting for the standard count threshold.
- When feedback volume remains low, a typical retraining cadence is expected to be roughly every 2-3 months, but the trigger criteria remain authoritative.

## Dataset gates

Before training, GPT-7 MUST version the dataset rather than mutating a released baseline. Project-group split isolation MUST be preserved. Exact and near cross-split duplicate gates MUST pass. Unapproved regions MUST be ignored or excluded so that missing labels do not become false negatives.

## Candidate model

Every retraining run MUST create a new versioned candidate model. A run MUST record at least: base model version, dataset version, split manifest, training configuration, artifact identity, per-class metrics, and regression results.

## Promotion gate

A candidate MUST NOT automatically replace the production model. Promotion requires:

1. applicable annotation and evidence contract validation;
2. project-group split isolation and duplicate/leakage gates;
3. evaluation on a frozen regression set  plus the new QA challenge set;
4. per-class evaluation for all active classes;
. no unresolved critical regression in known failure modes;
. admin approval of the candidate for production promotion.

Per-class metrics MUST include at least precision and recall. Additional metrics may be versioned by the benchmark specification.

## Model registry and rollback

The production model, candidates, dataset versions, evaluation results, promotion decisions, and rollback targets MUST be traceable in the model registry. Promotion MUST preserve a rollback path to the previous production model.

## Safety and boundaries

Continuous improvement changes the detector, not the ownership boundary. GPT-7 MUST NOT create canonical engineering geometry or topology from training feedback. Framework-private detector output remains evidence only until adapted to the active StructuralDetectionEvidence contract.
