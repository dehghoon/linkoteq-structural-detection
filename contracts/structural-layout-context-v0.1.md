# Structural Layout Context Contract v0.1

## Purpose
Shared contextual engineering rules for GPT-7 detection QA and GPT-6 reconstruction. These rules classify evidence strength; they do not create canonical Core geometry.

## Rule strength
- **hard gate**: invalid evidence/annotation or forbidden inference.
- **review trigger**: ambiguity requiring review/adjudication, not automatic rejection.
- **contextual prior**: supporting evidence only; never sufficient alone to create, delete, or relabel an element.

## Ownership
GPT-7 uses this contract for annotation QA, dataset QA, error analysis, and review routing, and stops at approved StructuralDetectionEvidence.
GPT-6 uses the same semantics for fusion, reconstruction review, topology, levels, the vertical extents, and Core mapping. GPT-6 owns canonical engineering decisions.

## Grid presence and absence
- **Hard gate:** never assume every drawing has a grid. No-grid drawings are valid inputs.
- **Hard gate:** never invent grid axes or labels merely to regularize a layout.
- **Contextual prior:** explicit grid alignment and intersections may strengthen interpretation of structural layout.
- **Review trigger:** materially off-grid candidates in otherwise regular framing are preserved and reviewed; they are not force-snapped.
- GPT-7 may detect approved classes in `source-page` coordinates without a grid. GPT-6 may reconstruct a reference system only from sufficient deterministic drawing evidence and review.

## Column presence and placement
- **Hard gate:** never assume every grid intersection contains a column.
- **Hard gate:** absence of a visible or detected column is not proof that no structural column exists.
- **Hard gate:** never create a column solely from regular spacing, a grid intersection, beam intersection, or typical-building convention.
- **Contexual prior:** repeated column symbols, grid alignment, beam framing, dimensions, and corresponding positions on related plans may strengthen column evidence.
- **Review trigger:** missing, ambiguous, conflicting, or materially off-grid column evidence at a likely framing location requires review rather than automatic creation or rejection.
- Drawings without explicit column symbols remain valid inputs.

## Story and level context
- `story_count` is contextual project evidence only.
- **Hard gate:** story count alone must not create columns, elevations, story heights, levels, or vertical member extents.
- **Contextual prior:** repeated column evidence at corresponding positions across levels strengthens evidence of vertical continuity.
- **Review trigger:** appearance, disappearance, relocation, offset, or section/symbol change across adjacent levels may indicate transfer, setback, termination/start, framing change, drawing inconsistency, or detection error.
- **Hard gate:** GPT-7 must not hallucinate a column on one level because it exists on another.
- GPT-6 decides level association and vertical extent only from sufficient level, elevation, and topology evidence and review.

## Structural versus nonstructural wall context
These rules prepare a wall-capable migration; they do not activate `wall` under StructuralDetectionEvidence v0.1.
- **Hard gate:** architectural partitions must not be promoted to structural walls solely from wall-like graphics.
- **Contexual prior:** a wall located inside a column-grid bay is commonly compatible with a nonstructural partition interpretation, but location is not proof.
- **Review trigger:** an internal wall proposed as structural requires supporting structural semantics or context, or adjudication.
- Internal shear walls and core walls are explicit counterexamples to automatic nonstructural classification.
- **Contexual prior:** primary-framing interaction, structural notes/symbols, core configuration, cross-level continuity, and reviewed structural evidence may strengthen a structural-wall interpretation.
- **Hard gate:** perimeter, grid, or column proximity alone is not proof of structural-wall status.
- **Hard gate:** unresolved structural-vs-nonstructural wall semantics must not enter approved training/evaluation labels until adjudicated.

## Beam relationships
Beam-to-column, beam-to-wall, and beam-to-beam relationships are contextual evidence. Detector box corners are not engineering endpoints. Apparent framing discontinuities are routed to GPT-6 review rather than repaired by GPT-7.

## GPT-7 QA gate mapping
**Hard fail:** invented grids/columns from regularity; cross-level hallucination; automatic structural-wall promotion from graphics/location; unresolved wall semantics used as approved labels; active ontology/evidence-contract violations.

**Mandatory review:** materially off-grid candidates in regular framing; missing/ambiguous column evidence at likely framing locations; cross-level column discontinuity/relocation; an internal proposed structural wall without sufficient semantics; conflicting related plans.

**Context only:** grid alignment/intersections; regular spacing; inside-bay/perimeter/core location; cross-story repetition; beam framing.

## GPT-6 reconstruction gate
GPT-6 may fuse these signals with deterministic transforms, scale, OCR/grid evidence, detector evidence, dimensions, related drawings, and human review. No contextual prior independently authorizes canonical Core geometry. No-grid and no-visible-column drawings remain representable without invented geometry.

## Compatibility
StructuralDetectionEvidence v0.1 remains exactly `column` and `beam`; `wall` must not be serialized under v0.1. Wall activation requires a versioned GPT-7 ontology/annotation contract, a wall-capable evidence contract, GPT-6 consumer regression, and coordinated approval.

## Regression expectations
1. no-grid input is accepted without invented grids;
2. grid intersections do not automatically create columns;
3. missing visible columns do not become automatic negative engineering conclusions;
4. story count creates no vertical geometry;
5. cross-level repetition is context only;
6. cross-level column discontinuity routes to review;
7. inside-grid walls are not automatically structural or nonstructural;
8. partitions are not promoted from graphics alone;
9. unresolved wall semantics route to adjudication;
10. v0.1 still rejects `wall`;
11. GPT-7 output remains evidence only;
12. GPT-6 owns canonical reconstruction.
