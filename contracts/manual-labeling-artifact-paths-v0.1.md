# Manual Labeling Repository Artifact Paths v0.1

Status: Active. Owner: GPT-7. Boundary: LinkoTech Website -> GPT-7 repository artifact storage.

## Purpose

This contract defines repository path presentation for manual-labeling handoffs. It does not change manual-labeling intake identity, annotation geometry, dataset admission, or training readiness.

## Stable Identity

The full `candidate_id` remains the authoritative handoff identity.

Repository directory names are presentation metadata and MUST NOT replace `candidate_id`, `source_id`, `page_id`, or `project_group_id`.

The full stable identifiers MUST remain inside the exported machine-readable artifacts.

## New Export Path

New website handoffs SHOULD use:

```text
datasets/manual-labeling-inbox/<drawing-stem>__page-<NNNN>__<candidate-prefix>/
```

Example:

```text
datasets/manual-labeling-inbox/S3.0_ROOF_FRAMING_PLAN__page-0001__5f997e3e/
```

Rules:

- `<drawing-stem>` is a filesystem-safe form of the original filename without its final extension.
- `<NNNN>` is the one-based page number padded to four digits.
- `<candidate-prefix>` is the first eight filesystem-safe characters of the stable `candidate_id`.
- The candidate prefix is only a collision-avoidance and human-navigation suffix.
- `manifest.json` remains the authoritative provenance record.

## Compatibility

Legacy UUID-only paths remain valid:

```text
datasets/manual-labeling-inbox/<candidate-id>/
```

Existing legacy handoffs MUST remain readable and MUST NOT be destructively renamed solely for consistency.

Consumers SHOULD use the stored export-path receipt or manifest references instead of reconstructing a repository path from `candidate_id`.

## Human QA Preview

A flattened annotated preview MAY be stored at:

```text
preview/annotated-page-<NNNN>.png
```

The preview is human-QA-only. `annotations.json` remains the canonical machine-readable annotation source.

Readable preview renderers MAY draw class badges, but MUST NOT alter annotation classes, geometry, coordinate systems, or source provenance.
