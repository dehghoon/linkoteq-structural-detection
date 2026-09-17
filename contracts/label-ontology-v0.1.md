# Structural Detection Label Ontology v0.1

## Purpose

This ontology defines the semantic labels used by GPT-7 for dataset annotation, detector training, evaluation, and the `StructuralDetectionEvidence` handoff to GPT-6.

The ontology is aligned with the engineering meaning of Linkoteq Structural Core v0.5, but detector labels are not Core entities and do not authorize canonical geometry.

## Version

```
ontology_name: linkoteq-structural-detection-labels
ontology_version: 0.1
detection_contract: StructuralDetectionEvidence v0.1
core_reference: Linkoteq Structural Core v0.5
```

## Approved initial labels

| Detector label | Meaning at the detection boundary | Potential Core entity after GPT-6 reconstruction |
| --- | --- | --- |
| `column` | Visual/semantic evidence of a column on the source drawing. A plan detection establishes horizontal location evidence only. | candidate `Member`, only after GPT-6 resolves transforms, scale, level/elevation, nodes, vertical extent, topology, and review |
| `beam` | Visual/semantic evidence of a beam on the source drawing. The detector box or mask is not an engineering centerline. | candidate `Member`, only after GPT-6 reconstructs centerline, orientation, endpoints, node associations, connectivity, and review |

## Canonical boundary rules

- GPT-7 must use the approved label strings exactly when emitting `StructuralDetectionEvidence.
- Dataset class indices and framework-private names must be adapted to these labels before handoff.
- GPT-7 must not emit cNode`, `Member`, `Surface`, `GridLine`, or any canonical Core geometry from detector output.
- A detection label is evidence, not an engineering decision.
- Raw bounding boxes, masks, OBBs, and detector centers must not become canonical Core geometry.
- GPT-6 owns the deterministic source-to-model transform, grid/OCR/scale fusion, engineering geometry, topology, review, and Core mapping.

## Change control

The label set is a versioned cross-product boundary. Adding, renaming, merging, or splitting a label requires:
1. an ontology version change;
2. a coordinated update to the GPT-7 dataset/adapter and GPT-6 consumer validation;
3. regression fixtures for the handoff contract;
4. a review of Core semantic alignment.

A Core version change alone does not require detector retraining unless the detection label semantics or the evidence contract actually change.
