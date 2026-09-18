import unittest
from tools.validate_annotations import validate_record

BASE={
 "annotation_id":"ann-001","source_id":"src-001","page_id":"p01",
 "project_group_id":"prj-001","class_name":"beam",
 "box":{"xmin":10,"ymin":20,"xmax":30,"ymax":40},
 "coordinate_space":"source-page","spec_version":"0.1","qa_state":"approved","flags":[]
}

class AnnotationValidationTests(unittest.TestCase):
    def test_valid(self): self.assertEqual(validate_record(BASE,100,100),[])
    def test_bad_class(self):
        r={**BASE,"class_name":"wall"}
        self.assertTrue(validate_record(r))
    def test_nonpositive_box(self):
        r={**BASE,"box":{"xmin":30,"ymin":20,"xmax":30,"ymax":40}}
        self.assertTrue(validate_record(r))
    def test_page_bounds(self):
        r={**BASE,"box":{"xmin":10,"ymin":20,"xmax":130,"ymax":40}}
        self.assertTrue(validate_record(r,100,100))
    def test_blocking_flag_on_approved(self):
        r={**BASE,"flags":["ambiguous-class"]}
        self.assertTrue(validate_record(r))

if __name__=="__main__": unittest.main()
