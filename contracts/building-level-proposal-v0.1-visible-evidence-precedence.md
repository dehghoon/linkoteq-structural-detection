# Building Level Proposal v0.1 — Visible-Evidence Precedence Addendum

## Status
Candidate addendum to `contracts/building-level-proposal-v0.1.md`. It does not activate proposal runtime handoff.

## Normative invariant
`Proposal MUST NOT replace available visible evidence.`

After BuildingLevelProposal Human confirmation/correction, GPT-7 MUST assess structural-information coverage separately for each component type and each relevant level/region before generating any inferred layout proposal.

The required precedence is:
`visible source evidence -> detection/extraction -> coverage assessment -> identify missing/incomplete structural information -> gap-only proposal -> Human QA`.

## Grid
When explicit source-drawn grid axes are present and sufficiently complete for a level/region, GPT-7 MUST use the source/detected grid context and MUST NOT generate a replacement proposed grid.

A proposed grid or proposed grid-axis is permitted only where explicit grid information is absent or materially incomplete. The absence/incompleteness decision MUST preserve source ID, page ID, region scope, confidence, and provenance.

An uncertain grid-coverage decision MUST route to QA rather than silently treating the grid as absent.

## Column
When visible column graphics are present, GPT-7 MUST detect them under the active StructuralDetectionEvidence contract.

A column-location proposal is permitted only where column layout is absent or materially incomplete for the relevant level/region. It MUST NOT overwrite, substitute for, or compete with visible column detection evidence.

A grid intersection without a visible column graphic remains contextual proposal evidence only and MUST NOT become a `column` detection.

## Wall
When visible structural-wall graphics are present, GPT-7 MUST detect them only under an approved wall-capable StructuralDetectionEvidence contract.

A wall-location proposal is permitted only where structural-wall layout is absent or materially incomplete for the relevant level/region, and it remains a Human-QA hypothesis.

Under StructuralDetectionEvidence v0.1, `wall` MUST remain rejected.

## Beam
Visible beams remain detection evidence under the active contract. This addendum does not authorize inferred beam proposals. Any future inferred beam proposal requires an approved versioned proposal contract.

## Mixed drawing sets
Coverage decisions are NOT project-global. A drawing set may contain complete structural grid/column information on one floor and only architectural context on another.

Coverage MUST therefore be evaluated independently by:
- component type;
- confirmed/proposed level;
- source page;
- relevant page region when necessary.

One component type may be detected while another component type on the same level enters proposal mode.

## Coverage states
The proposal layer MUST preserve exactly one coverage state for each assessed component/scope:
- `visible-complete`
- `visible-incomplete`
- `visible-absent`
- `uncertain`

`visible-complete` MUST suppress replacement proposal generation for that component/scope.

`visible-incomplete` MAY permit gap-only proposals. Existing visible evidence MUST remain authoritative for the visible portions, and proposals MUST be limited to identified gaps.

`visible-absent` MAY permit contextual proposals after the applicable Human-confirmed/corrected BuildingLevelProposal gate.

`uncertain` MUST NOT be silently converted to absence. It MUST route to Human QA before inferred replacement or gap proposals are promoted.

## Multi-floor behavior
Coverage is assessed per level/component/scope, while proposal reasoning MAY use the confirmed building-level multi-floor context.

Visible structural evidence on one floor MAY support contextual reasoning about another floor but MUST NOT be copied or fabricated as StructuralDetectionEvidence on that other floor.

When a component is visible on an upper floor but corresponding visible evidence is absent on a lower floor, GPT-7 MAY create a reviewed downward-continuity/layout proposal or QA issue under an approved proposal contract. It MUST NOT fabricate lower-floor detection evidence.

A lower-floor vertical component MAY terminate before an upper floor. Transfer structures, offsets, setbacks, podiums, system changes, irregular layouts, and other exceptions MUST remain possible and route to QA when evidence is insufficient.

## Building-level grid precedence
If explicit grids are available and sufficiently complete across the relevant confirmed floors, proposed-grid generation MUST remain suppressed for those covered scopes.

If explicit grids are absent or materially incomplete on some floors, a building-level proposed grid MAY be generated only for the uncovered scopes. It SHOULD seek cross-floor consistency with visible columns, structural-wall axes/centers, core geometry, perimeter/break geometry, and repeated bays without inventing project/global engineering coordinates.

Per-page realizations MUST remain in explicit `source-page` coordinates. GPT-7 MUST NOT create canonical Core `GridLine` or final engineering grid geometry.

## Provenance and review
Every coverage decision and every allowed proposal MUST preserve traceable source/page scope, model/rule name and version, confidence, provenance, and review state as required by the applicable approved contract.

Human confirmation of an inferred proposal does not retroactively convert it into visible source evidence.

## Validation requirements
Machine validation and regression coverage MUST include at least:
- complete visible grid suppresses proposed-grid replacement;
- absent grid permits a review-gated proposed grid;
- incomplete grid permits only gap proposals;
- uncertain grid coverage routes to QA;
- visible columns remain detections and suppress replacement column proposals for covered locations;
- absent/incomplete columns may enter proposal mode without becoming detection evidence;
- v0.1 rejects wall detection;
- mixed floors may use different coverage states;
- visible evidence on one floor is not copied as detection evidence to another floor;
- `visible-incomplete` preserves existing evidence and limits proposals to gaps;
- proposal output cannot overwrite or mutate StructuralDetectionEvidence records.

## Compatibility and activation
This addendum does not modify StructuralDetectionEvidence v0.1/v0.2 ontology and does not activate layout-proposal handoff.

Runtime proposal consumption remains disabled until the controlling proposal contracts, machine validation, datasets, Human QA workflow, GPT-7 regressions, GPT-6 consumer regressions, provenance/source-page coverage, legacy compatibility, and GPT-4 cross-repository activation are approved.
