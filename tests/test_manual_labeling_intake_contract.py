import json, math, unittest
from pathlib import Path
R=json.loads((Path(__file__).resolve().parents[1]/"contracts/manual-labeling-intake-validation-rules-v0.1.json").read_text())
def A(m,x,y):
 a,b,c,d,e,f=m; return a*x+c*y+e,b*x+d*y+f
def box(b,w,h):
 v=[b[k] for k in ("xmin","ymin","xmax","ymax")]
 return all(math.isfinite(x) for x in v) and 0<=b["xmin"]<b["xmax"]<=w and 0<=b["ymin"]<b["ymax"]<=h
def tx(t):
 if any(k not in t for k in R["transform"]["fields"]): return False
 if t["transform_validation_state"]!="validated" or t["page_rotation_deg"] not in R["transform"]["rotation"]: return False
 f,i=t["raster_to_source_page_affine"],t["source_page_to_raster_affine"]
 if len(f)!=6 or len(i)!=6:return False
 for p in [(0,0),(t["raster_width_px"],0),(0,t["raster_height_px"]),(t["raster_width_px"],t["raster_height_px"])]:
  q=A(f,*p); z=A(i,*q)
  if max(abs(z[0]-p[0]),abs(z[1]-p[1]))>R["transform"]["round_trip_tolerance"]:return False
 return True
class T(unittest.TestCase):
 def test_classes_invalid(self): self.assertEqual(R["active_classes"],["column","beam","wall"]);self.assertNotIn("shear-wall",R["active_classes"])
 def test_bbox(self):
  self.assertTrue(box({"xmin":1,"ymin":2,"xmax":3,"ymax":4},612,792))
  self.assertFalse(box({"xmin":1,"ymin":2,"xmax":1,"ymax":4},612,792))
  self.assertFalse(box({"xmin":3,"ymin":2,"xmax":1,"ymax":4},612,792))
  self.assertFalse(box({"xmin":1,"ymin":2,"xmax":700,"ymax":4},612,792))
 def test_transform_normal(self):
  t={"effective_page_width_pt":612,"effective_page_height_pt":792,"effective_crop_box_pdf":[0,0,612,792],"page_rotation_deg":0,"raster_width_px":1224,"raster_height_px":1584,"raster_to_source_page_affine":[.5,0,0,.5,0,0],"source_page_to_raster_affine":[2,0,0,2,0,0],"render_version":"x","transform_validation_state":"validated"}
  self.assertTrue(tx(t));self.assertEqual(A(t["raster_to_source_page_affine"],200,400),(100,200))
 def test_transform_rotated(self):
  t={"effective_page_width_pt":612,"effective_page_height_pt":792,"effective_crop_box_pdf":[0,0,612,792],"page_rotation_deg":90,"raster_width_px":1584,"raster_height_px":1224,"raster_to_source_page_affine":[0,-.5,.5,0,0,792],"source_page_to_raster_affine":[0,2,-2,0,1584,0],"render_version":"r","transform_validation_state":"validated"}
  self.assertTrue(tx(t))
 def test_transform_crop_and_missing(self):
  t={"effective_page_width_pt":500,"effective_page_height_pt":700,"effective_crop_box_pdf":[50,40,550,740],"page_rotation_deg":0,"raster_width_px":1000,"raster_height_px":1400,"raster_to_source_page_affine":[.5,0,0,.5,0,0],"source_page_to_raster_affine":[2,0,0,2,0,0],"render_version":"c","transform_validation_state":"validated"}
  self.assertTrue(tx(t));self.assertFalse(tx({"raster_width_px":1}));self.assertFalse(R["transform"]["pixel_only_admissible"])
 def test_provenance_roundtrip_project_group(self):
  p={"candidate_id":"c","source_id":"s","page_id":"p","project_group_id":"g","sha256":"a"*64};self.assertEqual(json.loads(json.dumps(p)),p);self.assertTrue(R["project_group_preserved"])
 def test_history_and_roles(self):
  self.assertTrue(R["history_append_only"]);self.assertFalse(R["employee_may_owner_approve"]);self.assertIn("owner-approved",R["owner_only"])
 def test_invalid_state_transition(self): self.assertNotIn("gpt7-dataset-admission",R["lifecycle"]["candidate"])
 def test_separation(self): self.assertFalse(R["owner_approval_implies_admission"]);self.assertFalse(R["admission_implies_training_ready"]);self.assertFalse(R["boundary"]["enablesTraining"])
 def test_exclusions_duplicates(self): self.assertFalse(R["gpt6_proposal_observed_gt"]);self.assertFalse(R["synthetic_overlay_observed_gt"]);self.assertTrue(R["duplicate_candidates_preserved"])
 def test_legacy(self): self.assertEqual(R["legacy_v0_1"]["accepted"],["column","beam"]);self.assertEqual(R["legacy_v0_1"]["rejected"],["wall"])
if __name__=="__main__":unittest.main()
