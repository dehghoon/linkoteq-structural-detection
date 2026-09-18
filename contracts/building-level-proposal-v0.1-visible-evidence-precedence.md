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
The proposal layer SHOULD preserve one of these coverage states:
- `visible-complete`
- `visible-incomplete`
- `visible-absent`
- `uncertain`

`visible-complete` MUST suppress replacement proposal generation for that component/scope.

`visible-incomplete` MAY permit gap-only proposals,
