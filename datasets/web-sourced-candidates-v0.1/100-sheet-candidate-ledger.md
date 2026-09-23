# Web Structural Drawing Intake — 100-sheet target

Search-backed candidate inventory for structural detector dataset preparation. Counts below include plan-type sheets useful for column / beam / wall detection and grid context; detail-only sheets are not counted unless needed later.

## Candidate sheet inventory

| Source package | Candidate plan sheets | Count |
|---|---|---:|
| Hamilton Builders issue set | S200, S201, S300, S300A, S301, S301A, S400, S401, S500, S501, S600, S601 | 12 |
| Eastern Engineering plan-room package | S-11, S-11A, S-11B, S-11C, S-12, S-12A, S-12B, S-21, S-21A, S-21B, S-21C | 11 |
| Dawson City structural package | S1.0, S1.1, S1.2, S1.3 | 4 |
| Oswegatchie Fire Station | S100, S101, S102 | 3 |
| BFES Station 201 IFC | S201, S202, S203 | 3 |
| HCFCD MTSC Distribution Center | S201, S202, S203 | 3 |
| University of Utah CVRTI | SB101, SF101, SF102, SF103 | 4 |
| Teslin Community Centre | S2.1-S2.5, S2.1A-S2.5A, S2.2B-S2.5B | 14 |
| 1302 Market Street approved structural set | S200, S201, S201A, S202, S203 | 5 |
| Hamilton General Hospital structural set | 0324-S201 through 0324-S210 | 10 |
| New Orchard Station user-provided structural package | selected plan/framing sheets from source package | 9 |
| LIGO Hanford structural drawings | OSB foundation plan + Beam Tube Enclosure foundation plan | 2 |
| HGTC Building 500 canopy shelter | A1.03 First Floor Structural Framing / Foundation Plan | 1 |
| Cottage Grove plan packet | Foundation + Second Floor Framing + Roof Framing | 3 |
| City of Winnipeg package | S-2.0, S-3.0, S-4.0 | 3 |
| S21 sample engineering set | S100, S200, S201, S300, S301 | 5 |
| Gandy Residence structural set | S101, S102, S201, S202, S203, S301 | 6 |
| 330 Progress Ave structural package | structural framing-plan candidates already identified in intake | 1 |
| Chuck Bailey Recreation Centre | S200 Foundation & Level P1 Framing Plan candidate already identified | 1 |

**Current search-backed candidate total: 100 sheets.**

## Source URLs

- Hamilton Builders: https://www.hamilton-builders.com/wp-content/uploads/2025/01/4809-Issue-Dwgs-24Oct25-compressed.pdf
- Eastern Engineering plan room: https://distribution.easternengineering.com/view/ViewJob.aspx?job_id=30234&view=vp
- Dawson City: https://cityofdawson.ca/Home/DownloadMeeting/5845cbcc-1500-4045-859b-000d97200f28?isEnglish=True
- Oswegatchie Fire Station: https://govtribe.com/file/government-file/general-drawings-dot-pdf-1
- BFES Station 201: https://mjdixon.ca/wp-content/uploads/2021/10/21-07_Struc-IFC-Set.pdf
- HCFCD MTSC: https://govtribe.com/file/government-file/18-drawings-dot-pdf-5
- University of Utah CVRTI: https://www.gramoll.com/wp-content/uploads/2018/10/UofU-CVRTI_BID-DRAWINGS_22-01-31.pdf
- Teslin Community Centre: https://ddc-teslin.com/wp-content/uploads/2024/12/Structural-Drawings-250131.pdf
- 1302 Market Street: https://permits.kirklandwa.gov/WebDocs/2018060177/c6288449-587a-445a-97b7-7249e80c06ba.pdf
- Hamilton General Hospital contract/drawing list: https://www.infrastructureontario.ca/48e235/contentassets/b541356aa36b4c019a46c00ea61f010b/hamilton-general-hospital_guaranteed-price-contract_en.pdf
- LIGO Hanford OSB: https://dcc.ligo.org/LIGO-D960296/public
- LIGO Beam Tube Enclosure: https://dcc.ligo.org/LIGO-D960742/public
- HGTC Building 500: https://www.hgtc.edu/documents/procurement/h59-n269-cb-drawings.pdf
- Cottage Grove packet: https://www.vi.cottagegrove.wi.gov/AgendaCenter/ViewFile/Agenda/_03112026-2313?packet=true
- City of Winnipeg: https://legacy.winnipeg.ca/finance/findata/matmgt/documents/2007/832-2007/832-2007_Bid_Opportunity.pdf
- S21 sample engineering: https://fliphtml5.com/edaky/huqm/S21-Sample_Engineering/
- BFES alternate structural set listing: https://mjdixon.ca/wp-content/uploads/2021/10/T21059_Structural-Drawings.pdf

## Processing status

This is a candidate/source ledger, not a claim that all 100 binary sheets have already been copied into GitHub.

For each admitted sheet:
1. preserve source/package/page provenance;
2. extract the plan sheet from the package;
3. work on a copy;
4. mask/crop the title block without removing structural geometry;
5. retain grid/OCR context;
6. prepare labels for active classes: column, beam, wall.
