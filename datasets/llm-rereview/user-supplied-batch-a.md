# LLM review ledger — user supplied batch A

Decision basis: actual package sheet identity/content, not keyword-only selection. Cover/3D sheets are excluded.

| Project | Reviewed package | Admit as structural plan | Admit as elevation/section | Reject |
|---|---|---|---|---|
| P2025-151 R2 | 5 pages | Mx101 Anchor Plan; Mx401 Roof Plan | Mx501 Elevations; Mx502 Elevation + Wall Section | Mx001 3D/cover |
| P2025-182 | 5 pages | EsMx201 Mezzanine Plan; EsMx401 Roof Plan | EsMx501 Elevations; EsMx502 Elevation + Wall Section | EsMx001 3D/cover; detail-only sheet if present |
| P2026-010 | 5 pages | EsMx201 Mezzanine Plan; EsMx401 Roof Plan | EsMx501 Elevations; EsMx502 Elevation + Wall Section/Schedules | EsMx001 3D/cover |
| P2026-014 | 3-page supplied package | EsMx401 Roof & Mezzanine Plan | EsMx501/EsMx502 only if actually present in supplied pages; sheet list alone is not admission | EsMx001 3D/cover |
| P2026-017 | 5 pages | EsMx401 Roof Plan line 1-9; EsMx402 Roof Plan line 9-17 | EsMx501 Elevations; EsMx502 Elevation + Wall Section/Schedules | EsMx001 3D/cover |
| P2026-024 | 4 pages | EsMx401 Roof Plan | EsMx501 Elevations; EsMx502 Elevation + Wall Section/Schedules | EsMx001 3D/cover |
| P2026-031 | 4 pages | EsMx401 Roof Plan | EsMx501 Elevations; EsMx502 Elevation + Wall Section/Schedules | EsMx001 3D/cover |
| P2026-021 BLDG 1 | 3 pages | supplied structural plan sheets to be admitted only by actual page identity | supplied elevation sheets only if present | EsMx001 3D/cover |
| P2026-022 upload | 3 pages | IMPORTANT: package text identifies P2026-021 Vars Development BLDG 2, not P2026-022; treat by internal project identity and do not create a false P2026-022 project | same rule | filename identity rejected where it conflicts with drawing title block |

Notes:
- P2025-177 R2/R3 remain one building; latest reviewed revision should be preferred for dataset use unless a prior revision contains uniquely needed source evidence.
- Sheet-list references do not by themselves prove the corresponding sheet exists in a shortened supplied PDF.
- No title-block masking is authorized until the exact admitted page is visually checked for its title-block boundary.


## Legacy web-sourced audit — projects 001–005

These findings supersede the old auto-selected page pairs.

- project-001 — Big Lake City Council agenda attachment: **REJECT from structural-building training set in current form.** The source is primarily a council workshop/WWTF 30% design agenda package and explicitly says only Section G drawings are attached. The legacy `plan_page=25 / elevation_page=13` selection is not accepted as a verified building structural plan/elevation pair.
- project-002 — Tulsa Public Schools Maintenance Facility: source sheet index confirms S101 Foundation Plan, S102 Roof Framing Plan, A201 Building Elevations and A211 Building Sections. **Legacy pages 3/1 rejected.** Correct target sheets are S101 + S102 for structural plans and A201/A211 for vertical context.
- project-003 — Hamilton Builders / Dashwood Trails 4-story 98-unit building: **legacy page 1/page 1 rejected** (cover/index content, not a valid plan/elevation pair). Retain project as candidate; exact S-series structural sheets and exterior-elevation sheets must be selected from the actual indexed set before admission.
- project-004 — City of Dawson URL: **REJECT source entirely.** Fetch resolves to a 2021 special council meeting / remuneration bylaw package, not the claimed structural-building drawing source. Old page 40/page 40 is invalid.
- project-005 — UofU CVRTI bid drawings: **legacy page 2/page 2 rejected.** Project remains candidate, but exact structural/elevation sheet identities must be visually/index-verified before admission; same-page plan/elevation inference is invalid.

### Systemic QA observation
The audit confirms two separate failure classes: (1) wrong sheet selection inside otherwise useful construction sets, and (2) completely wrong source documents admitted as projects. Both must be checked before any PDF is copied into the validated dataset.


## Legacy web-sourced audit — projects 006–012

- project-006 — DDC Teslin structural drawings: **legacy page 1/page 1 rejected pending direct visual/index verification.** Source fetch timed out in this audit, so no unsupported replacement sheet is asserted.
- project-007 — Kirkland permit set: **legacy pages 7/20 not admitted yet.** Source fetch timed out in this audit. Keep candidate only until the actual sheet identities are verified from the drawing set.
- project-008 — HGTC Building 500 Exterior Renovation: source index confirms **S1.01 Foundation Plan** and **A2.02 Proposed Exterior Elevations**; A3.01/A3.02 are Building Sections. The legacy page 1/page 1 pair is rejected. Correct target identities are S1.01 + A2.02 (with A3.01/A3.02 optional vertical context).
- project-009 — Bronx Park Community Centre / Good Neighbours Senior Centre: the URL is a City of Winnipeg bid-opportunity/specification package. The fetched material does not establish legacy PDF pages 31/30 as the required structural plan/elevation pair. **Reject legacy selection; candidate requires drawing-specific verification before admission.**
- project-010 — City of Bondurant Public Works Facility: source index confirms **S100 Foundation Plan**, **S200 Framing Plan**, **A300 Exterior Elevations**, **A400 Building Sections**. The legacy page 1/page 1 selection is rejected. Correct targets: S100 + S200 for structural plans and A300/A400 for vertical context.
- project-011 — Tuscaloosa County DHR: source index confirms **S2.01 Floor and Foundation Plan**, **S2.02 Roof Framing Plan**, **A4.01 Exterior Elevations**, and **S3.01/S3.02 Sections**. Legacy page 2/page 2 is rejected. Correct targets are S2.01 + S2.02 and A4.01 (S3.01/S3.02 optional vertical structural context).
- project-012 — Sanibel Fire & Rescue Station 172: source index confirms structural plans **S100 Foundation and Apparatus Floor Plan**, **S101 First Floor Plan**, **S121 Second Floor and Low Roof Framing Plan**, **S131 Main Roof and Tower Roof Framing Plans**; architectural vertical context is **A201/A202 Exterior Elevations** and A301–A305 Building Sections. Legacy page 1/page 1 is rejected.

### Audit status after project-012
Projects 001–012 have now been re-reviewed at source/sheet-index level. No legacy auto-selected page pair should be considered validated merely because clean/original PDFs exist in `curated-100-projects`. The validated set must be rebuilt from explicit sheet identities after source verification.
