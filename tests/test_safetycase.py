import unittest
from safetycase import validate
class SafetyCaseTests(unittest.TestCase):
    def test_valid_case(self):
        case={"claims":[{"id":"C","supports":["E"]}],"evidence":[{"id":"E"}]}
        self.assertTrue(validate(case)["ok"])
    def test_missing_and_orphan(self):
        report=validate({"claims":[{"id":"C","supports":["X"]}],"evidence":[{"id":"E"}]})
        self.assertFalse(report["ok"]); self.assertTrue(any("missing" in x for x in report["issues"])); self.assertTrue(any("orphan" in x for x in report["issues"]))
if __name__=="__main__": unittest.main()
