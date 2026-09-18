# Wall Detection Ontology Impact Analysis — v0.2 Proposal

## Status

Proposal only. This document does not approve or activate a new detector class. The currently approved runtime ontology remains `contracts/label-ontology-v0.1.md` with `column` and `beam` only.

## Proposed ontology

Proposed ontology version: `0.2`.

- `column`
- `beam`
- `wall`

`wall` means visible source-drawing evidence whose primary semantic intent is a structural wall. It is detector evidence only.

Exclude architectural partitions without reliable structural semantics, slab/foundation edges that are not wall graphics, grids, dimensions, leaders, notes, section/detail cut lines, ambiguous hatch regions, hidden/inferred continuation, and walls inferred only from schedules, notes, other pages, or engineering assumptions.

Unresolved structural-vs-nonstructural wall semantics must go to QA and stay out of approved training/evaluation until adjudicated. Do not create an `ambiguous-wall` class.

## Geometry

For the first wall ontology version, retain the existing axis-aligned `source-page` bounding box. The box tightly contains one visible structural-wall graphic and excludes adjacent text, leaders, dimensions, grids, and unrelated graphics.

Detector boxes, masks, centers, or long axes are not canonical Core `Surface` geometry, engineering wall centerlines, thicknesses, endpoints, elevations, topology, or final geometry.

Segmentation may be benchmarked internally later if boxes are insufficient, but masks must not cross the GPT-6 boundary without an explicitly versioned evidence contract.

## Core alignment

Linkoteq Structural Core v0.5 allows canonical `Surface` entities to represent slabs/walls. This does not authorize GPT-7 to emit a Core `Surface`. GPT-6 owns reconstruction and any eventual Core mapping.

## Contract impact

`label-ontology-v0.1.md` must not be edited in place to add `wall`; create a versioned ontology.

`StructuralDetectionEvidence v0.1` restricts `class_name` to `column` or `beam`. Wall handoff therefore requires a coordinated versioned evidence-contract update and GPT-6 consumer migration. Until that is complete, GPT-7 MUST NOT emit `wall` as StructuralDetectionEvidence v0.1.

## Dataset impact

Pilot v0.1 is the two-class baseline and should remain reproducible.

For a three-class dataset:
1. Create a new dataset version bound to ontology v0.2.
2. Re-review every included page for structural walls; missing wall labels in v0.1 are not valid wall negatives.
3. Preserve existing `project_group_id` split assignments unless separately reviewed.
4. Keep exact/near cross-split duplicate gates release-blocking.
5. Preserve provenance and version bindings for reproducibility.

## Annotation impact

A versioned annotation specification must define:
- structural-wall inclusion/exclusion;
- instance separation at intersections and corners;
- openings and occlusion;
- paired boundary lines, poche/hatch, and single-line conventions;
- partial/occluded/low-quality handling;
- examples distinguishing structural walls from partitions, slab/foundation edges, and detail linework.

Run a small multi-drafter wall pilot before bulk annotation and adjudicate disagreements.

## Evaluation impact

Keep v0.1 two-class metrics separately reportable. For v0.2 report per-class precision, recall, AP/mAP where applicable, confusion analysis, and false-positive categories.

Wall error analysis must include architectural-partition false positives, slab/foundation-edge false positives, merged/split wall instances, low-contrast/hatched misses, and wall/beam confusion.

Benchmark bounding-box detection first. Add segmentation only if evidence shows a measurable need and the contract is versioned accordingly.

## Model and registry impact

Existing two-class artifacts remain bound to ontology v0.1 and must not be relabeled. A v0.2 model requires a new class-index mapping and model version. Fine-tuning from a v0.1 checkpoint is allowed only with parent-artifact provenance.

## GPT-6 consumer impact

Before wall handoff, GPT-6 must accept `wall` in its versioned evidence validator and add regression fixtures.

GPT-6 continues to own source-to-model transforms, engineering scale, wall reconstruction, thickness/centerline interpretation, levels/elevations, vertical extent, connectivity/topology, human review, final engineering geometry, and Core mapping.

GPT-7 stops at reviewed source-page wall evidence.

## Regression requirements

Migration is incomplete until tests cover:
1. ontology v0.2 exact-label validation;
2. annotation acceptance of `wall` and rejection of unknown labels;
3. legacy v0.1 fixtures under their original contract;
4. GPT-6 acceptance of valid wall evidence under the new contract;
5. GPT-6 rejection of wall evidence mislabeled as v0.1;
6. explicit `coordinate_space: source-page` and traceable provenance;
7. split leakage and duplicate gates;
8. wall annotation QA/adjudication examples.

## Approval gate

`wall` becomes approved only after versioned ontology approval, dataset/annotation migration, versioned validation rules, versioned StructuralDetectionEvidence coordinated with GPT-6, GPT-6 consumer regression, pilot wall QA, and evaluation/model-registry updates.

Until then, wall observations are research/QA candidates only and MUST NOT be serialized as approved v0.1 annotations or StructuralDetectionEvidence v0.1.
