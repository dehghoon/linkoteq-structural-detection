# Column Source-Semantics Rules v0.2 — Candidate Addendum

## Status and scope
Candidate normative addendum to `contracts/annotation-spec-v0.2.md` for GPT-7 source-page column candidate generation and human QA. It does not activate ontology v0.2 and does not create canonical Core geometry, GridLine, topology, or engineering coordinates.

## Grid-intersection prior
For structural plans with visible structural grids, column candidate generation MUST use visible source-drawing grid intersections as the primary spatial prior. A compact square or rectangular graphic away from a defensible grid intersection MUST NOT be promoted as a column solely from shape, stroke density, or local appearance.

Limited exceptions are permitted where the visible drawing provides defensible structural-column evidence outside the displayed grid network, especially around stairs, elevators, shafts, or comparable local framing conditions. Such exceptions require explicit review evidence.

If a visible structural column or structural wall is defensible but the corresponding grid appears omitted from the source drawing, GPT-7 MUST NOT invent or emit a canonical GridLine. Record `missing-grid-evidence` QA metadata for downstream reconstruction review. Grid reconstruction remains outside GPT-7 ownership.

Grid lines and grid intersections are contextual source-space evidence only and are not `column` annotations.

## Foundation-plan column-in-footing prior
On foundation plans, a column footprint is commonly shown as a smaller square or rectangular structural graphic located within a larger footing or pedestal graphic. The larger footing/pedestal outline MUST NOT be labeled as the column.

When visible and semantically consistent, the combination of:
- a defensible structural grid intersection,
- a smaller inner column footprint, and
- a surrounding larger footing/pedestal graphic

is strong source-space evidence for a column candidate. The annotation box MUST remain tight to the visible column footprint and MUST exclude the surrounding footing/pedestal.

Containment inside a footing/pedestal is a contextual prior, not sufficient evidence by itself. Ambiguous cases MUST be routed to QA rather than promoted automatically.

## Shifted columns and expansion-joint clusters
The grid-intersection rule is a strong spatial prior, but the visibe column footprint is the detection target. A column footprint MAY be locally shifted or ecchentric relative to the nominal grid intersection or to the center of its footing/pedestal. GPT-7 MUST NOT move the detection box back to the grid intersection; the tight box MUST follow the visible source-page column footprint.

Closely spaced column footprints MUST NOT be automatically deduplicated. At a visible or otherwis defensible expansion/separation joint, two nearby columns may be distinct structural instances, including when they are associated with the same or nearby footing/pedestal context. Each visible column footprint MUST remain a separate candidate until review.

Away from a defensible expansion/separation-joint context, very close column candidates are anomalous. As a domain prior from human review, ordinary columns in these plans typically have spacing of about 3 meters or more. This is not a hard geometric or engineering scale constraint: if drawing scale is not already approved by the downstream reconstruction process, GPT-7 MUST NOT convert source-page distances into engineering meters or use a 3 m threshold as a canonical distance. The spacing rule is a QA/candidate-ranking cue only.

## Human-review regression
A reviewer rejection of a candidate because it is not at a defensible grid intersection MUST be preserved in the QA trail. Missing unmarked columns on a reviewed foundation plan MUST prevent page-completeness/background approval until grid-intersection plus footing/pedestal review has been completed.

## Ownership boundary
These rules govern detection candidate generation, annotation QA, and source-page evidence only. They MUST NOT create canonical structural topology, canonical GridLine objects, engineering scale, project/global engineering coordinates, final member geometry, or StructuralModel.
