import unittest
from safetycase import validate
class SafetyCaseTests(unittest.TestCase):
    def test_valid_case(self):
        case={"claims":[{"id":"C","supports":["E"]}],"evidence":[{"id":"E"}]}
        self.assertTrue(validate(case)["ok"])
    def test_missing_and_orphan(self):
        report=validate({"claims":[{"id":"C","supports":["X"]}],"evidence":[{"id":"E"}]})
        self.assertFalse(report["ok"]); self.assertTrue(any("missing" in x for x in report["issues"])); self.assertTrue(any("orphan" in x for x in report["issues"]))
    def test_duplicate_node_ids_are_rejected(self):
        # References must identify exactly one graph node.  Previously the
        # dictionary comprehensions silently discarded one of these entries.
        report=validate({
            "claims":[{"id":"C","supports":["E"]}],
            "evidence":[{"id":"E"},{"id":"E"}],
        })
        self.assertFalse(report["ok"])
        self.assertIn("duplicate node id E", report["issues"])
    def test_empty_case_is_rejected(self):
        # A truncated or empty case must not pass validation as a complete
        # safety argument.
        report=validate({})
        self.assertFalse(report["ok"])
        self.assertIn("safety case has no claims", report["issues"])
if __name__=="__main__": unittest.main()
