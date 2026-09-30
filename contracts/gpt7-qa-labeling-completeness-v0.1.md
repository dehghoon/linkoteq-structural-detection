# GPT-7 QA Labeling Completeness Contract v0.1

## Status and authority
Mandatory GPT-7 annotation-completeness companion to `contracts/annotation-spec-v0.2.md`.
This contract does not change ontology, geometry representation, training readiness, or the GPT-7/GPT-6 boundary.
When annotating or reviewing v0.2 source pages, GPT-7 MUST read and apply both this contract and the active annotation specification before producing or declaring a page complete.

## Failure mode this contract prevents
A sparse conservative pass that labels only a few obvious components while omitting repeated, visually supported structural instances MUST NOT be represented as annotation-complete.
LLM memory, prior chat context, detector confidence, or a previous sparse pass MUST NOT substitute for this checklist.

## Mandatory pre-annotation gate
Before every annotation/re-annotation pass GPT-7 MUST confirm:
- active ontology and annotation specification from GitHub;
- coordinate space is `source-page`;
- active classes are exactly the contract-approved classes;
- human-QA state and provenance are preserved;
- this completeness contract has been applied.

If this gate cannot be confirmed, the pass remains incomplete/review-required.

## Column completeness rule
For `column`, review the entire applicable plan region for every visible structural-column footprint/symbol.
Repeated column-square/column-footprint patterns, especially at grid intersections, MUST be checked instance-by-instance.
GPT-7 MUST NOT cherry-pick only the clearest subset of a repeated column pattern.
Grid graphics, labels, leaders, dimensions, inferred centers, unresolved symbols, and nonstructural posts/pedestals remain excluded under the active annotation specification.

## Beam completeness rule
For `beam`, review the entire applicable plan region for visually consistent structural beam graphics.
The review MUST include:
1. visible beams supported between identifiable columns; and
2. visually consistent structural members for which at least one visible end meets an identifiable column.

Connection to two columns is stronger evidence but is NOT a prerequisite for review as a beam candidate.
Line continuity, repeated member pattern, graphic thickness/style, and consistency with nearby confirmed beams MAY support classification, but MUST NOT override contradictory source evidence or create inferred hidden continuation.
Each visible beam instance is reviewed independently; a large box around a framing system MUST NOT replace instance boxes.

## Wall completeness rule
For `wall`, follow `annotation-spec-v0.2.md` strictly: only physically visible source-drawing graphics with reliable structural-wall semantics.
Architectural partitions without reliable structural semantics, slab/foundation edges that are not wall graphics, grids, dimensions, leaders, notes, cut lines, ambiguous hatch/poche, schedule-only walls, and inferred continuation MUST NOT be labeled as wall.
No `ambiguous-wall` class is permitted.

## Tight source-page boxes
Every accepted component instance uses the smallest practical axis-aligned box containing the visible component graphic in original `source-page` coordinates.
Boxes are detector evidence only. They MUST NOT encode engineering centerlines, endpoints, connectivity, topology, scale, thickness, openings, levels, elevations, or final engineering geometry.

## Ambiguity and NO-SAFE-BOX
If structural evidence exists but class or tight visible boundary cannot be defended, use QA/review metadata equivalent to `NO-SAFE-BOX` rather than inventing a box.
`NO-SAFE-BOX`, unresolved candidates, unreviewed regions, and missing annotations MUST NOT be treated as background or negative training evidence.

## Mandatory completeness pass
Before a page may be described as `annotation-complete` or eligible for human approval:
- scan the full applicable plan region again;
- reconcile repeated column patterns against annotated column instances;
- reconcile repeated beam patterns against annotated beam instances, including the one-column-end rule;
- re-check all visible structural-wall candidates;
- ensure excluded/ambiguous regions are not silently converted to negatives;
- ensure every accepted instance is an independent tight box;
- record that the completeness pass was performed.

A page that has only a sparse first-pass subset MUST remain `candidate-pending-human-qa` / incomplete.

## Human-QA promotion
LLM-assisted annotations, detector predictions, and reviewer scaffolds are candidates only.
Only explicit human QA under the active annotation specification may promote exact reviewed boxes to approved training/evaluation evidence.
Human approval of page selection, contact sheets, or review workflow MUST NOT be interpreted as approval of unseen boxes.

## Regression requirement
GPT-7 tests/CI MUST preserve these invariants. Future edits that remove the column-pattern completeness rule, the one-column-end beam review rule, `NO-SAFE-BOX` non-negative semantics, source-page tight boxes, mandatory completeness pass, or human-QA promotion gate are regressions.

## Historical QA compatibility
This contract codifies the established GPT-7 QA practice used before and during the approved reference examples. It prevents future annotation passes from reverting to generic conservative detection that omits supported repeated instances.
