# Linkoteq Structural Detection

GPT-7 owns datasets, labeling, detector selection, training, evaluation, model registry, and inference.

GPT-6 owns grid/OCR/scale, geometry-semantic fusion, topology, Core mapping, and 3D reconstruction.

The handoff is detector-agnostic `StructuralDetectionEvidence`. Detector output is evidence only and must never be written directly as Core geometry.
