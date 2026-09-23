# Dataset pairing policy — plans + elevations (GPT-6 context)

Updated requirement from dataset owner:

- Prefer project packages that contain both structural plan/framing sheets and at least one building or structural elevation.
- For each selected structure, target at minimum:
  - >=1 useful structural plan (foundation/floor/roof framing), and
  - >=1 elevation suitable for vertical/storey context.
- Keep plan/elevation sheets linked by project_id/building_id and source provenance.
- Elevations are primarily downstream GPT-6 reconstruction context for storey/level inference; GPT-7 active detector classes remain column, beam, wall unless separately versioned.
- Do not split sheets from the same project/building across train/validation/test.

## Search-confirmed paired candidates

1. Two-storey tuition block package
   - Architectural: ground/first floor plans, south/north/east/west elevations, longitudinal/transverse sections.
   - Structural: S-01 Foundation & Column Layout; S-02 First-Floor Framing Plan.
   - https://ru.scribd.com/document/1064487180/Two-Storey-Tuition-Block-Drawings-and-BoQ-v2-1-F

2. Residential compound drawing set
   - Architectural: ground/second floor plans, front elevation, section, roof plan.
   - Structural: S-05 Foundation Plan; S-06 2nd Floor Framing; S-07 Roof Framing.
   - https://www.scribd.com/document/357121945/a1-pdf

3. Agricultural Science Building set
   - Architectural: ground/second/third floor plans, front/rear/side elevations, cross section.
   - Structural: ground and second-floor framing plans plus structural framing/foundation content.
   - https://ru.scribd.com/document/370083745/Agricultural-Science-Building-1

4. Brooklyn structural set
   - Structural: foundation; 1st-6th floor framing; roof; bulkhead; steel framing elevations.
   - https://www.scribd.com/doc/151476584/Structural-Drawings-Brooklyn-NY

5. North Branford Fonda Pavilion
   - S-1 foundation + roof framing; elevation-bearing structural notes/sections useful as supplemental vertical context.
   - https://www.northbranfordct.gov/DocumentCenter/View/772

## Curation priority

Future 100-sheet curation should be project-paired rather than 100 unrelated plan sheets. A preferred unit is a project/building bundle containing plan(s) + elevation(s), with level names/elevations retained for GPT-6.
