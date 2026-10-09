# Dataset Source Assets Contract v0.1

## Status

Active GPT-7 dataset-asset location contract. This contract defines where immutable structural drawing inputs for training, validation, and test are stored. It does not activate ontology v0.2, wall production handoff, detector training, or YOLO training readiness.

## Storage classes

### Approved publishable dataset assets

Repository: `dehghoon/linkoteq-structural-detection`

Canonical root:

```text
datasets/source-drawings/<dataset_id>/
```

For the existing v0.2 pilot:

```text
datasets/source-drawings/pilot-v0.2/
```

This location applies only to source assets whose repository publication has already been approved. It must not be interpreted as authorization to publish private website-uploaded drawings.

### Private website manual-labeling assets

Structural drawings uploaded through the LinkoTech website are private operational artifacts. They MUST NOT be copied into a public repository.

Their authoritative source remains the protected website/Supabase storage boundary until GPT-7 admission. After admission, a complete immutable source/raster/label bundle may be archived to GitHub only when the target dataset repository has been verified as `private`, or stored in another approved private object/large-file store referenced by a versioned GitHub manifest.

The private archive root, once a dedicated private repository is configured, is:

```text
datasets/manual-labeling/<dataset_version>/<split>/<sample_id>/
```

The artifact bundle contract is:

```text
contracts/manual-labeling-yolo-artifact-bundle-v0.1.md
```

No repository name is invented by this contract. The runtime publisher must verify repository visibility before writing any private artifact.

## Split directories

- `train/` — source drawings whose `project_group_id` belongs to the approved train split.
- `validation/` — source drawings whose `project_group_id` belongs to the approved validation split.
- `test/` — source drawings whose `project_group_id` belongs to the approved test split.

The dataset manifest is authoritative for split membership. Source files MUST NOT be moved across split directories without a versioned manifest and split migration.

## Integrity and identity

Each source asset MUST match the `filename`, `sha256`, `size_bytes`, `source_id`, and `project_group_id` in the corresponding dataset manifest. A hash mismatch is a blocking dataset-integrity failure.

Do not rename or mutate source PDFs in place. A changed source drawing MUST be ingested as a new versioned source asset and reflected in a new dataset manifest version.

For private manual-labeling bundles, the deterministic raster and YOLO label MUST also be content-addressed by SHA-256 and bound to the exact admitted source page and validated transform.

## Provenance

Annotations, detector evaluation, and inference records MUST reference the manifest `source_id` and `page_id`. The storage path is repository/storage provenance only and MUST NOT be treated as an engineering coordinate space or geometry source.

## Project-group isolation

All derivatives of the same construction/design project MUST remain in the same `project_group_id` and split. Exact and near cross-split duplicate gates remain mandatory.

## Security and repository size

These files are dataset inputs, not source code. If an approved publishable source asset exceeds the repository host's regular file-size policy, it MUST be stored under the same logical path using the repository's approved large-file mechanism and the manifest must still preserve its content hash.

Private website-uploaded source PDFs, deterministic rasters, and labels require a verified private storage target. The public `dehghoon/linkoteq-structural-detection` repository MUST NOT receive those private runtime artifacts.

Secrets, access tokens, signed URLs, session cookies, and service credentials MUST NOT be committed to any dataset repository or manifest.

## Boundary

Source-drawing storage does not change GPT-7 ownership. GPT-7 stops at reviewed source-page detection evidence. No Core geometry, engineering scale, topology, or final 3D geometry may be derived by this contract.

Materializing a complete admitted source/raster/label bundle does not authorize training:

```text
training_ready = false
training_enabled = false
enablesTraining = false
```
