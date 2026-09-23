# Web-sourced structural drawing intake

This folder is the staging location for structural drawing sources selected for GPT-7 detector dataset preparation.

## Sources queued

1. New Orchard Station structural package (user-provided source)
   - selected structural-plan pages: 17-25
   - local preprocessing target: remove title block from copies; preserve source
   - classes of interest: column, beam, wall
   - grid/OCR context retained

2. Chuck Bailey Recreation Centre structural package
   - https://www.surrey.ca/sites/default/files/media/tender_docs/221028_CBRCE_Phase_2_-_Issued_for_Review_-_Structural.pdf

3. 330 Progress Ave Multifunction Station structural package
   - https://anacond.ca/wp-content/uploads/2024/06/300-Progress-Ave-Multifunction-Station-Issued-for-Tender-Structural.pdf

4. PRS Structural Drawings IFC
   - https://mjdixon.ca/wp-content/uploads/2023/07/PRS-32-Structural-Drawings-IFC.pdf

5. Habitat for Humanity Fourplex drawing package
   - https://assets.habitat.ca/southeast-bc/images/C21001-022-Habitat-for-Humanity-Fourplex-New-Concept-For-Building-Permit-Feb-22ND-2022-Copy.pdf

## Processing
- work on copies only
- select structural plan/framing/foundation sheets
- remove title-block regions from training images
- retain source/page provenance
- prepare detector examples for column / beam / wall
