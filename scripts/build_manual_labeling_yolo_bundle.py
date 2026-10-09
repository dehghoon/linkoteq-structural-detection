import argparse
import hashlib
import json
import pathlib
import shutil
import struct

from export_yolo_human_approved import yolo_line

BUNDLE_SCHEMA = "manual-labeling-yolo-artifact-bundle-v0.1"


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_size(path):
    with open(path, "rb") as stream:
        header = stream.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("deterministic_raster_must_be_png")
    return struct.unpack(">II", header[16:24])


def point(coefficients, x, y):
    if len(coefficients) != 6:
        raise ValueError("source_page_to_raster_affine_must_have_six_coefficients")
    a, b, c, d, e, f = [float(value) for value in coefficients]
    return a * x + c * y + e, b * x + d * y + f


def raster_box(source_box, coefficients):
    xmin, ymin, xmax, ymax = [float(source_box[key]) for key in ("xmin", "ymin", "xmax", "ymax")]
    if not (xmin < xmax and ymin < ymax):
        raise ValueError("source_page_bbox_must_have_positive_area")
    corners = (
        point(coefficients, xmin, ymin),
        point(coefficients, xmax, ymin),
        point(coefficients, xmax, ymax),
        point(coefficients, xmin, ymax),
    )
    xs = [item[0] for item in corners]
    ys = [item[1] for item in corners]
    return {"x_min": min(xs), "y_min": min(ys), "x_max": max(xs), "y_max": max(ys)}


def require_text(payload, key):
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"required_field:{key}")
    return value


def validate(payload):
    if payload.get("schema_version") != "manual-labeling-intake-v0.1":
        raise ValueError("unsupported_intake_schema")
    if payload.get("workflow_state") != "owner-approved" or payload.get("owner_disposition") != "owner-approved":
        raise ValueError("owner_approval_required")
    if payload.get("dataset_admission") != "gpt7-admitted":
        raise ValueError("gpt7_dataset_admission_required")
    if payload.get("preserved_artifact") is not True:
        raise ValueError("preserved_source_artifact_required")
    if payload.get("coordinate_space") != "source-page" or payload.get("unit") != "pdf-point":
        raise ValueError("source_page_pdf_point_coordinates_required")
    if payload.get("training_ready") is True or (payload.get("boundary") or {}).get("enablesTraining") is not False:
        raise ValueError("training_must_remain_disabled")
    transform = payload.get("transform")
    if not isinstance(transform, dict) or transform.get("transform_validation_state") != "validated":
        raise ValueError("validated_transform_required")
    for key in ("candidate_id", "source_id", "page_id", "project_group_id", "source_sha256", "dataset_split"):
        require_text(payload, key)
    if payload["dataset_split"] not in {"train", "validation", "test"}:
        raise ValueError("invalid_dataset_split")
    if not payload.get("annotations"):
        raise ValueError("admitted_annotations_required")
    return transform


def build_bundle(intake_path, source_pdf, raster_png, output_root, target_repository, target_visibility):
    if target_visibility != "private":
        raise ValueError("private_github_repository_required_for_website_source_artifacts")

    payload = json.loads(pathlib.Path(intake_path).read_text(encoding="utf-8"))
    transform = validate(payload)
    source_pdf = pathlib.Path(source_pdf)
    raster_png = pathlib.Path(raster_png)

    if sha256_file(source_pdf).lower() != payload["source_sha256"].lower():
        raise ValueError("source_sha256_mismatch")

    width, height = png_size(raster_png)
    if (width, height) != (
        int(round(float(transform["raster_width_px"]))),
        int(round(float(transform["raster_height_px"]))),
    ):
        raise ValueError("raster_dimensions_do_not_match_validated_transform")

    sample_id = payload["candidate_id"]
    root = pathlib.Path(output_root) / sample_id
    (root / "source").mkdir(parents=True, exist_ok=True)
    (root / "images").mkdir(exist_ok=True)
    (root / "labels").mkdir(exist_ok=True)

    source_target = root / "source" / "original.pdf"
    image_target = root / "images" / f"{sample_id}.png"
    label_target = root / "labels" / f"{sample_id}.txt"
    shutil.copyfile(source_pdf, source_target)
    shutil.copyfile(raster_png, image_target)
    (root / "intake.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    coefficients = transform["source_page_to_raster_affine"]
    lines = []
    for annotation in payload["annotations"]:
        if annotation.get("annotation_spec_version") != "v0.2":
            raise ValueError("annotation_spec_v0_2_required")
        lines.append(yolo_line(annotation["class"], raster_box(annotation["bbox"], coefficients), width, height))
    label_target.write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest = {
        "schema_version": BUNDLE_SCHEMA,
        "sample_id": sample_id,
        "candidate_id": sample_id,
        "source_id": payload["source_id"],
        "page_id": payload["page_id"],
        "project_group_id": payload["project_group_id"],
        "owner_qa_state": "owner-approved",
        "dataset_admission": "gpt7-admitted",
        "dataset_split": payload["dataset_split"],
        "class_id_map": {"0": "column", "1": "beam", "2": "wall"},
        "source_pdf": {"path": "source/original.pdf", "sha256": sha256_file(source_target)},
        "deterministic_raster": {
            "path": f"images/{sample_id}.png",
            "sha256": sha256_file(image_target),
            "width_px": width,
            "height_px": height,
            "rendering_version": transform.get("rendering_version"),
            "transform_validation_state": "validated",
        },
        "yolo_label": {
            "path": f"labels/{sample_id}.txt",
            "sha256": sha256_file(label_target),
            "annotation_count": len(lines),
        },
        "github_archive": {"repository": target_repository, "required_visibility": "private"},
        "training_ready": False,
        "training_enabled": False,
        "enablesTraining": False,
    }
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return root


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--source-pdf", required=True)
    parser.add_argument("--raster-png", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--target-repository", required=True)
    parser.add_argument("--target-visibility", choices=["private", "public"], required=True)
    args = parser.parse_args()
    print(build_bundle(
        args.intake,
        args.source_pdf,
        args.raster_png,
        args.output_root,
        args.target_repository,
        args.target_visibility,
    ))


if __name__ == "__main__":
    main()
