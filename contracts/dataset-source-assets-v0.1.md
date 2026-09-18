# Dataset Source Assets Contract v0.1

## Status
Active GPT-7 dataset-asset location contract. This contract defines where immutable input structural drawings for training, validation, and test are stored. It does not activate ontology v0.2 or wall production handoff.

## Canonical repository location
Repository: `dehghoon/linkoteq-structural-detection`

Canonical root:
`datasets/source-drawings/<dataset_id>/`

For the v0.2 pilot:
`datasets/source-drawings/pilot-v0.2/`

## Split directories
- `train/` — source drawings whose `project_group_id` belongs to the approved train split.
- `validation/` — source drawings whose `project_group_id` belongs to the approved validation split.
- `test/` — source drawings whose `project_group_id` belongs to the approved test split.

The dataset manifest is authoritative for split membership. Source files MUST NOT be moved across split directories without a versioned manifest and split migration.

## Integrity and identity
Each source asset MUST match the `filename`, `sha256`, `size_bytes`, `source_id`, and `project_group_id` in the corresponding dataset manifest. A hash mismatch is a blocking dataset-integrity failure.

Do not rename or mutate source PDFs in place. A changed source drawing MUST be ingested as a new versioned source asset and reflected in a new dataset manifest version.

## Provenance
Annotations, detector evaluation, and inference records MUST reference the manifest `source_id` and `page_id`. The storage path is repository provenance only and MUST NOT be treated as an engineering coordinate space or geometry source.

## Project-group isolation
All derivatives of the same construction/design project MUST remain in the same `project_group_id` and split. Exact and near cross-split duplicate gates remain mandatory.

## Security and repository size
These files are dataset inputs, not source code. If a source asset exceeds the repository host's regular file-size policy, it MUST be stored under the same logical path using the repository's approved large-file mechanism and the manifest must still preserve its content hash.

## Boundary
Source-drawing storage does not change GPT-7 ownership. GPT-7 stops at reviewed source-page detection evidence. No Core geometry, engineering scale, topology, or final 3D geometry may be derived by this contract.
