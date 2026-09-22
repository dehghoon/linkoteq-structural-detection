import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class PolicyTests(unittest.TestCase):
 def test_policy(self):
  s=(ROOT/"contracts/dataset-training-input-policy-v0.1.md").read_text()
  for x in ["StructuralDetectionEvidence v0.2","`column`, `beam`, `wall`","`source-page`","independent source-evidence/adjudication process","MUST NOT be reprocessed through GPT-7","`enablesTraining` remains `false`"]:
   self.assertIn(x,s)
 def test_status(self):
  s=json.loads((ROOT/"project-status.json").read_text())
  self.assertEqual(s["activeClasses"],["column","beam","wall"])
  self.assertEqual(s["coordinateSpace"],"source-page")
  self.assertFalse(s["boundary"]["enablesTraining"])
  self.assertFalse(s["boundary"]["emitsCanonicalEngineeringGeometry"])
  self.assertTrue(s["boundary"]["legacyV0_1Compatibility"])
  self.assertTrue(s["boundary"]["v0_1WallRejection"])
if __name__=="__main__": unittest.main()
