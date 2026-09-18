# Structural Layout Proposal Contract v0.1 — Candidate

## Status
Candidate only. This contract does not activate runtime handoff and does not modify the active StructuralDetectionEvidence v0.1 contract or activate Candidate v0.2.

## Purpose
Define reviewable structural-layout hypotheses for source regions where grid, column, or structural-wall information is absent or materially incomplete. Proposals are not detection evidence and are not canonical engineering geometry.

## Precedence and gates
1. `Proposal MUST NOT replace available visible evidence.`
2. Building-level or multi-floor proposals MUST reference a `building_level_proposal_id` which is `human-confirmed` or `human-corrected`.
3. Coverage is assessed per component/level/page/region as `visible-complete`, `visible-incomplete`, `visible-absent`, or `uncertain`.
4. `visible-complete` suppresses replacement proposals. `visible-incomplete` permits only gap-only proposals. `uncertain` routes to Human QA.

## Proposal types
The initial proposal types are exactly:
 - `grid-axis`
 - `column-location`
 - `wall-location`

None of these are detector ontology classes.

## Required fields
Every proposal MUST preserve a stable `proposal_id`, `source_id`, `page_id`, `project_group_id`, `proposal_type`, `coordinate_space: source-page`, `proposal_geometry`, `evidence_basis`, `confidence` in `[0,1]`, non-empty `reason_codes`, `model_or_rule_name`, `model_or_rule_version`, `provenance`, and `review_state`. Multi-floor reasoning MUST also preserve `building_level_proposal_id` and the relevant `level_proposal_id`.

## Geometry
Proposal geometry remains review geometry in explicit `source-page` coordinates. grid-axis uses a source-page line with distinct finite endpoints. column-location uses a source-page point. wall-location initially uses a tight axis-aligned source-page review box. No proposal geometry establishes final column extent, wall centerline/boundary/thickness/endpoints/penings/vertical extent, connectivity, topology, engineering grid, or Core geometry.

## Grid proposal rules
A proposed grid is permitted only when explicit source-drawn grid information is absent or materially incomplete in the relevant scope. Explicit complete grids MUST  suppress replacement proposed grids.

Proposed axes may use visible column centers/faces, structural-wall axes/centers, stair/elevator/core corners, exterior and return corners, plan breaks/setbacks, main perimeter/load-bearing wall lines, repeated bays, and coherent orthogonal families when supported by the source. These are priors, not hard rules. Grid bubbles, names, and dimension chains absent from the source MUST NOT be invented as detected facts.

## Column proposal rules
Visible column graphics MUST be detected under the active StructuralDetectionEvidence contract. A column-location proposal is permitted only where column layout is absent or materially incomplete. Grid intersections, stair/elevator/core corners, exterior corners, return corners/plan breaks, visible wall/pier context, repeated bays, layout symmetry, and cross-floor alignment may increase proposal support. The user-supplied typical 4-7 m bay range may be used only as a weak system/architectural prior when units/scale are reliably available; it MUST NOT be a hard threshold or ground-truth rule. Facade openings, windows, main entrances, parking circulation, and architectural use may be used as contextual constraints, not as detection facts.

## Wall candidate rules
Wall candidate priority SHOULD increase when the visible wall-like graphic is thick, continuous, aligned between or toward vertical columns/walls, intersects or connects with other thick wall-like graphics, or visually participates in a coherent beam/column/wall network. Thick continuous wall graphics between columns, between beams, or at expected structural interfaces are stronger candidates.

Thin interior partitions inside a regular coherent beam/column frame SHOULD be deprioritized or routed to QA when structural semantics are not reliable. Thickness and network coherence are candidate signals, not proof of structural semantics or final connectivity. Do not infer hidden wall continuation.

A wall may align along a grid axis and may intersect other axes/structural elements; a wall is not required to exist only at a two-axis grid intersection.

## Structural network prior
For candidate scoring and QA only, GPT-7 may prefer layouts in which vertical structural elements (columns/walls) and horizontal beams form a coherent visible or proposed framing network. This may support confidence or QA priority but MUST NOT establish final connectivity or topology.

## Multi-floor rules
After the associated BuildingLevelProposal is Human-confirmed/corrected, proposal reasoning may use the confirmed building context. Columns and structural walls SHOULD be checked for cross-floor alignment. An upper-floor column/wall normally creates a downward-continuity expectation. If corresponding visible evidence is absent on a lower floor, GPT-7 may create a proposal/QA issue but MUST NOT fabricate detection evidence.

Lower-floor vertical elements may terminate before upper floors. Transfer structures, offsets, setbacks, podiums, system changes, irregular geometry, and other exceptions MUST remain possible and route to QA when evidence is insufficient. Proposed building grids SHOULD seek cross-floor consistency without creating common engineering coordinates.

## Reason codes Initial version includes: `grid-intersection`, `column-center-alignment`, `column-face-alignment`, `core-corner-alignment`, `perimeter-corner`, `plan-break`, `setback`, `thick-wall-alignment`, `load-bearing-wall-alignment`, `repeated-bay-spacing`, `orthogonal-axis-family`, `layout-symmetry`, `structural-network-coherence`, `cross-floor-alignment`, `downward-continuity-expectation`, and `building-level-grid-consistency`.

## Review
Review states are `review-required`, `human-confirmed`, `human-corrected`, `human-rejected`, and `adjudication-required`. Human corrections MUST preserve the original proposal and corrected geometry/provenance. Human confirmation does not retroactively convert a proposal into visible detection evidence.

## Self-training boundary
Reviewed proposals may feed a separate, versioned proposal-review dataset. Preserve project-group split isolation, duplicate gates, held-out test protection, reason codes, original proposal, confidence, model/rule version, reviewer decision, and correction provenance. Do not silently treat model-generated proposals as human ground truth or as visible-detector ground truth.

## GPT-6 boundary
GPT-7 stops at reviewed source-page detection evidence or reviewed proposals. GPT-6 owns source transforms, proposal consumer validation, engineering grids, final column/beam/wall geometry, levels/elevations/story heights, connectivity/topology, Core mapping, StructuralModel, and 3D integration.

## Activation gate
Runtime consumption remains disabled until this contract and machine validation are approved, proposal datasets/Human QA are versioned, GPT-7 regressions pass, GPT-6 consumer regressions pass, legacy v0.1 compatibility passes, provenance/source-page regressions pass, and GPT-4 cross-repository activation is approved.
