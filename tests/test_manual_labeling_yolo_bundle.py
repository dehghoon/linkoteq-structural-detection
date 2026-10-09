import hashlib
import json
import pathlib
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_manual_labeling_yolo_bundle.py"


def write_png(path, width, height):
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    raw = b"".join(b"\x00" + b"\xff\xff\xff" * width for _ in range(height))
    payload = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )
    path.write_bytes(payload)


def payload(source_hash):
    return {
        "schema_version": "manual-labeling-intake-v0.1",
        "candidate_id": "candidate-001",
        "source_id": "source-001",
        "page_id": "page-001",
        "project_group_id": "project-001",
        "source_sha256": source_hash,
        "preserved_artifact": True,
        "coordinate_space": "source-page",
        "unit": "pdf-point",
        "workflow_state": "owner-approved",
        "owner_disposition": "owner-approved",
        "dataset_admission": "gpt7-admitted",
        "dataset_split": "train",
        "training_ready": False,
        "boundary": {"enablesTraining": False},
        "transform": {
            "transform_validation_state": "validated",
            "raster_width_px": 100,
            "raster_height_px": 50,
            "source_page_to_raster_affine": [2, 0, 0, 2, 0, 0],
            "rendering_version": "test-v1",
        },
        "annotations": [{
            "annotation_id": "ann-001",
            "class": "column",
            "bbox": {"xmin": 10, "ymin": 5, "xmax": 20, "ymax": 15},
            "annotation_spec_version": "v0.2",
            "flags": {},
        }],
    }


class BundleTests(unittest.TestCase):
    def test_complete_bundle_and_training_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "drawing.pdf"
            source.write_bytes(b"%PDF-1.4\nprivate-test\n")
            raster = root / "page.png"
            write_png(raster, 100, 50)
            intake = root / "intake.json"
            intake.write_text(json.dumps(payload(hashlib.sha256(source.read_bytes()).hexdigest())), encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(SCRIPT),
                "--intake", str(intake),
                "--source-pdf", str(source),
                "--raster-png", str(raster),
                "--output-root", str(root / "out"),
                "--target-repository", "dehghoon/private-structural-dataset",
                "--target-visibility", "private",
            ], check=True, capture_output=True, text=True)
            bundle = pathlib.Path(result.stdout.strip())
            self.assertTrue((bundle / "source" / "original.pdf").exists())
            self.assertTrue((bundle / "images" / "candidate-001.png").exists())
            self.assertEqual(
                (bundle / "labels" / "candidate-001.txt").read_text(encoding="utf-8").strip(),
                "0 0.30000000 0.40000000 0.20000000 0.40000000",
            )
            manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
            self.assertFalse(manifest["training_ready"])
            self.assertFalse(manifest["training_enabled"])
            self.assertFalse(manifest["enablesTraining"])

    def test_public_repository_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "drawing.pdf"
            source.write_bytes(b"%PDF-1.4\nprivate-test\n")
            raster = root / "page.png"
            write_png(raster, 100, 50)
            intake = root / "intake.json"
            intake.write_text(json.dumps(payload(hashlib.sha256(source.read_bytes()).hexdigest())), encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(SCRIPT),
                "--intake", str(intake),
                "--source-pdf", str(source),
                "--raster-png", str(raster),
                "--output-root", str(root / "out"),
                "--target-repository", "dehghoon/linkoteq-structural-detection",
                "--target-visibility", "public",
            ], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("private_github_repository_required", result.stderr)


if __name__ == "__main__":
    unittest.main()
