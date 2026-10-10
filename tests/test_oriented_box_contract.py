import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "contracts/manual-labeling-intake-validation-rules-v0.2.json").read_text())


class OrientedBoxContractTests(unittest.TestCase):
    def test_contract_versions(self):
        self.assertEqual(RULES["contract"], "manual-labeling-intake-v0.2")
        self.assertEqual(RULES["annotation_spec_versions"], ["v0.2", "v0.3"])

    def test_oriented_box_is_optional_and_v03_only(self):
        oriented = RULES["oriented_bbox"]
        self.assertTrue(oriented["optional"])
        self.assertEqual(oriented["requires_annotation_spec_version"], "v0.3")
        self.assertEqual(
            oriented["fields"],
            ["center_x", "center_y", "width", "height", "rotation_deg"],
        )

    def test_oriented_box_geometry_guards(self):
        oriented = RULES["oriented_bbox"]
        self.assertEqual(oriented["rotation_range"], "[-180,180)")
        self.assertTrue(oriented["positive_area"])
        self.assertTrue(oriented["corners_in_page"])
        self.assertTrue(oriented["bbox_tightly_encloses"])

    def test_training_boundary_unchanged(self):
        self.assertFalse(RULES["owner_approval_implies_admission"])
        self.assertFalse(RULES["admission_implies_training_ready"])
        self.assertFalse(RULES["boundary"]["enablesTraining"])
        self.assertFalse(RULES["boundary"]["emitsCanonicalEngineeringGeometry"])


if __name__ == "__main__":
    unittest.main()
