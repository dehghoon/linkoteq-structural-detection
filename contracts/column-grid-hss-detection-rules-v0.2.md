# Column grid/HSS detection rules v0.2

Status: candidate detection/annotation QA rule. Does not activate ontology v0.2.

## Purpose
Prevent repeat false negatives for interior or off-main-framing columns, and false positives from dimension/annotation marks.

## Rules

1. Grid intersections are a strong column-location prior and MUST be included in high-recall column candidate generation.

2. A grid intersection is NOT by utself a Ground Truth column. Promotion requires visible source-drawing structural evidence at or near the intersection, such as a column footprint/symbol, structural member connectivity, or a member designation consistent with a column.

3. HSS designation near a grid intersection is strong semantic evidence for a column candidate. It MUST not be ignored during high-recall candidate generation. The HSS text bounding box MUST NOT be used as the column bbox.
4. Column candidates must be searched across the full structural plan, including interior grid intersections, not just the perimeter, main framing lines, or previously annotated regions.

5. Off-grid or eccentric columns remain valid candidates when visible structural evidence supports them. Grid proximity must not become a hard filter.

## Negative gate

Dimension ticks, leader marks, text boxes, grid bubbles, dimension values, and other annotation primitives MUST NOT be promoted to columns merely because they are compact vector geometry near a grid.

## ML regression requirements

- Add a positive regression case: dense plan with multiple interior grid intersections and HHS-labeled columns. Expectation: interior columns are not missed.
- Add a negative regression case: dimension/grid annotation primitives near grids. Expectation: no false column promotion.
- Measure column recall separately for interior grid intersections and perimeter/edge regions.
- Fail the detection regression if a known human-approved interior column is missed or a known dimension/annotation mark is promoted as a column.

## Evidence boundary

This rule governs detection candidate generation and ML regression. It does NOT create canonical GridLines, engineering coordinates, topology, or final engineering geometry. All detection geometry remains source-page.
