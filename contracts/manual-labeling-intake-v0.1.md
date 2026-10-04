# Manual Labeling Intake Contract v0.1
Status: Active. Owner: GPT-7. Boundary: Linkoteq Website -> GPT-7 dataset admission.

## Authority
This operational contract does not change ontology v0.2, annotation-spec v0.2, StructuralDetectionEvidence v0.2, source-page semantics, or the GPT-6 reconstruction boundary. Active classes are exactly `column`, `beam`, `wall`. GPT-7 retains ontology, dataset-admission, split, duplicate/leakage, YOLO export/training/evaluation, registry, and evidence authority. Website/Employees cannot create or redefine classes.

## Lifecycle and roles
`candidate -> suitable-for-labeling -> labeling-in-progress -> submitted-for-owner-qa -> owner-approved | owner-rejected | revision-required -> gpt7-dataset-admission`.
Employees may assess suitability, annotate, save, submit, reject suitability with reason, and upload candidates. Employees cannot Owner-approve, admit datasets, change splits, mark training-ready, or train. Only Owner may set owner-approved/owner-rejected/revision-required; rejection/revision requires reason. GPT-7 alone controls gpt7-dataset-admission.
`owner-approved != gpt7-dataset-admitted != training-ready`.

## Minimum payload
Required: `schema_version=manual-labeling-intake-v0.1`; stable `candidate_id`,`source_id`,`page_id`,`project_group_id`; source origin/ref, lowercase SHA-256 content identity, original filename/page identity and preserved-artifact flag; effective page geometry; render/transform metadata when raster/display is used; annotations with stable annotation_id, exact class, bbox, `annotation_spec_version=v0.2`, flags; workflow state; operator identity/timestamps; Owner identity/timestamps/disposition/reasons; append-only adjudication history; annotation tool/version; provenance history.

Source artifacts are immutable/traceable and not destructively overwritten. Duplicates preserve separate candidate/provenance records.

## Annotation and ambiguity
One tight axis-aligned box per visible component under annotation-spec v0.2. Missing/unresolved/ambiguous/`NO-SAFE-BOX` regions are never negative/background evidence. GPT-6 proposals, reconstructed geometry, synthetic overlays, inferred continuation, or generated reconstruction artifacts are excluded from observed detector ground truth. `emitsCanonicalEngineeringGeometry=false`.

## Authoritative coordinates
Admitted annotations MUST use `coordinate_space="source-page"`, `unit="pdf-point"`, effective-page top-left origin, +x right, +y down, finite `xmin,ymin,xmax,ymax`, `xmin<xmax`, `ymin<ymax`, and page bounds.

Website tools may use pixels, but pixel-only evidence cannot pass admission without a deterministic validated reversible mapping to effective source-page PDF points.

### Minimum transform metadata
GPT-3/Website MUST preserve: effective page width/height in PDF points; effective crop box (`x0,y0,x1,y1`) in original PDF coordinates; page rotation (0/90/180/270); raster width/height pixels; display width/height when different; six finite affine coefficients raster->source-page where `x_pt=a*x_px+c*y_px+e`, `y_pt=b*x_px+d*y_px+f`; six-coefficient inverse source-page->raster; rendering/crop identifier/version; `transform_validation_state="validated"`. If stored coordinates are display-space, preserve deterministic display->raster mapping too. Forward/inverse control-point round trips must meet validation tolerance. Missing, singular, inconsistent, or unvalidated transforms block admission. Dimensions alone are insufficient.

## Review history
History is append-only and preserves event_id, actor_id, actor_role, prior/new state, timestamp, and required reason/notes. Operator/Owner decisions cannot be silently edited/deleted. Employee cannot create Owner adjudication. Owner approval cannot create GPT-7 admission.

Permitted rejection dispositions include `unsuitable-for-labeling`, `owner-rejected`, `revision-required`, all with reason.

## Duplicates, splits, admission
Exact/near duplicates remain detectable and traceable; `project_group_id` is preserved. GPT-7 owns project-group isolation and cross-split duplicate/leakage gates.

Owner approval is necessary but insufficient. GPT-7 admission additionally requires valid identities/provenance/SHA-256, preserved source, active class/spec, complete human trail, valid source-page geometry and transform evidence where applicable, no blocking ambiguity, observed-source (not GPT-6/synthetic) evidence, completeness/QA compliance, and duplicate/leakage/project-group compliance. Admission is an explicit GPT-7 decision.

## YOLO/training boundary
An annotation may enter YOLO data only after Owner approval, GPT-7 admission, inclusion in a NEW immutable versioned dataset release, frozen project-group split, duplicate/leakage PASS, and deterministic YOLO export validation. Released baselines are not mutated. Dataset admission does not imply training readiness.

`enablesTraining` remains false until independently required gates pass: frozen training-capable dataset, complete admitted human labels, frozen splits, duplicate/leakage pass, verified deterministic YOLO export, required regression/challenge sets, and versioned run/model-registry identity with applicable approval. This contract does not authorize training.

## Compatibility
StructuralDetectionEvidence v0.2 and GPT-6 boundary are unchanged. Legacy v0.1 accepts `column`,`beam` and rejects `wall`.
