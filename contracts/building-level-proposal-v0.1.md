# Building Level Proposal Contract v0.1 — Candidate

## Status
Candidate pre-layout contract. It does not create canonical Core levels/elevations/story heights and does not activate StructuralDetectionEvidence v0.2 or structural-layout proposal handoff.

## Purpose
Before building-level grid, column, beam, or wall proposal generation, GPT-7 may analyze an uploaded drawing set and propose the building's level organization for Human QA. Inputs may contain multiple plans or a fuller architectural/early-structural set including plans, elevations, sections, details, and schedules.

## Ownership boundary
GPT-7 owns drawing-set understanding and reviewable level/height proposals used as contextual input to detection/proposal ML. GPT-6 owns final engineering levels, elevations, story heights, source transforms, reconstruction, and Core mapping.

A `BuildingLevelProposal` is contextual evidence/hypothesis only. It MUST NOT create a canonical Core Level, engineering Z coordinate, elevation, story height, StructuralModel, or 3D geometry.

## Required workflow gate
The intended workflow is:
`drawing set -> page/sheet understanding -> level/height evidence extraction -> cross-page fusion -> BuildingLevelProposal -> Human confirmation/correction -> building-level layout proposal -> component proposal/detection -> GPT-6 reconstruction`.

Building-level structural layout proposal generation MUST remain review-gated until the level proposal is human-confirmed or human-corrected. Detection of visible source graphics may continue independently, but inferred multi-floor layout MUST NOT be represented as visible detection evidence.

## Required proposal fields
A proposal MUST preserve:
- `building_level_proposal_id`: stable non-empty ID.
- `source_set_id`: stable drawing-set ID.
- `project_group_id`: split-isolation group.
- `source_ids`: source documents participating in the proposal.
- `page_evidence`: page IDs, drawing-type hypotheses, extracted labels/markers/dimensions, confidence, and provenance.
- `levels`: ordered proposed level records.
- `confidence`: finite number in `[0,1]`.
- `model_name` and `model_version`.
- `provenance`: traceable generation origin.
- `review_state`.
- reviewer decision/corrections when reviewed.

## Drawing-type understanding
GPT-7 MAY classify pages/regions as `plan`, `elevation`, `section`, `detail`, `schedule`, or `other` for proposal reasoning. Classification is contextual metadata and must preserve page/region provenance and confidence.

Plans, elevations, and sections SHOULD be cross-referenced rather than interpreted as independent drawings when evidence supports a common building/level.

## Level evidence
Useful source evidence MAY include visible level names, plan titles, section/elevation level markers, explicit elevation text, vertical dimension chains, floor/slab references, roof/basement/ground identifiers, and cross-references.

A proposed level record SHOULD preserve:
- stable `level_proposal_id`;
- proposed display name;
- proposed order/index;
- supporting source/page references;
- evidence type(s);
- confidence;
- proposed elevation or floor-to-floor height only when source evidence or cross-page inference supports it;
- explicit units when a dimensional value is proposed;
- uncertainty/conflict metadata.

Absent labels, elevations, dimensions, or units MUST NOT be invented as detected facts.

## Cross-page fusion
GPT-7 MAY associate a plan, section marker, elevation level line, and related text as evidence for the same proposed level. Every association MUST remain traceable to its source pages and must distinguish direct visible evidence from inferred association.

When plan, section, elevation, or dimension evidence conflicts, GPT-7 MUST preserve the conflict and route it to Human QA rather than silently choosing one source.

Sections/elevations may provide stronger direct evidence for vertical level relationships than plan names alone, but no source type is universally authoritative without review.

## Human confirmation gate
`review_state` MUST be one of:
- `review-required`
- `human-confirmed`
- `human-corrected`
- `human-rejected`
- `adjudication-required`

Before building-level inferred grid/column/wall proposals are promoted to reviewed proposal input, the associated BuildingLevelProposal MUST be `human-confirmed` or `human-corrected`.

Human corrections MUST preserve both original proposal and corrected values/provenance. Confirmation does not convert inferred values into source-visible facts.

## Multi-floor structural context
After level confirmation, GPT-7 MAY reason jointly across floors. Column and structural-wall proposals SHOULD be checked for cross-floor alignment and vertical load-path plausibility.

General proposal prior:
- a column or structural wall present/proposed on an upper level normally creates an expectation of aligned support/continuation on lower levels;
- a lower-level vertical element may terminate before an upper level where layout/use changes;
- missing visible continuation on a lower level creates a `downward-continuity` proposal/review issue, not fabricated StructuralDetectionEvidence;
- transfer structures, offsets, setbacks, podiums, irregular systems, and other exceptions MUST remain possible and route to QA when evidence is insufficient.

This is a contextual proposal prior, not proof of engineering continuity or final vertical extent.

## Building-level proposed grid
When explicit grids are absent or incomplete, GPT-7 MAY propose a building-level axis network after level confirmation. It SHOULD seek a compact, sufficient set of axes that explains structural layout across the confirmed floors rather than independently inventing unrelated grids per floor.

Proposed axes MAY use cross-floor column centers, structural-wall axes/centers, core geometry, perimeter/break geometry, repeated bays, and other approved contextual signals.

Columns are generally expected near intersections of relevant axis families. Structural walls may align along an axis and may intersect other axes; walls are not required to exist only at point intersections.

A proposed building grid MUST NOT be represented as a detected grid or canonical engineering `GridLine`. Final engineering grid geometry remains GPT-6-owned.

## Dependencies
Any later `StructuralLayoutProposal` intended to use multi-floor reasoning MUST reference the reviewed `building_level_proposal_id` and preserve the relevant level proposal IDs.

## Training and evaluation
Drawing-set understanding data MUST be versioned separately from visible-object detector annotations. Training examples SHOULD preserve page type, source text/markers, cross-page associations, proposed levels/heights, conflicts, Human QA decisions, and corrections.

Project-group split isolation, duplicate gates, held-out test protection, provenance, and immutable dataset/model versions apply. Human-confirmed/corrected proposal data may train a contextual proposal model but MUST NOT silently become visible-object detection ground truth.

Suggested evaluation dimensions include page-type accuracy, level-count accuracy after defined matching, level-order accuracy, height/elevation extraction error when source truth exists, cross-page association quality, calibration, conflict-detection recall, and human correction rate.

## Compatibility and activation
This contract does not modify StructuralDetectionEvidence v0.1/v0.2 ontology. It does not add `level`, `grid`, or proposal classes to detector ontology.

Runtime handoff/consumption remains disabled until machine validation, proposal datasets, Human QA workflow, GPT-7 regressions, GPT-6 consumer regressions, provenance/source coverage, and GPT-4 cross-repository activation are approved.
