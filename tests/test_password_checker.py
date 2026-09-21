import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "tsg-cybersec-p01-muhammad-ali-kashif-password-checker.py"
SPEC = importlib.util.spec_from_file_location("password_checker", MODULE_PATH)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class PasswordCheckerTests(unittest.TestCase):
    def test_empty_input_is_handled_by_scoring_function(self):
        result = checker.check_password("")
        self.assertEqual(result["score"], 30)
        self.assertEqual(result["risk"], "HIGH")

    def test_common_password_is_always_high_risk(self):
        result = checker.check_password("password")
        self.assertTrue(result["common"])
        self.assertEqual(result["risk"], "HIGH")

    def test_strong_test_password_scores_low_risk(self):
        result = checker.check_password("N7!vQ2@rL9#xP4$z")
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["risk"], "LOW")

    def test_predictable_patterns_reduce_score(self):
        result = checker.check_password("Abcd1234!!!!!!")
        self.assertGreaterEqual(len(result["predictability"]), 2)
        self.assertEqual(result["risk"], "HIGH")

    def test_very_long_input_does_not_fail(self):
        result = checker.check_password("A1!" + "x" * 10000)
        self.assertEqual(result["length"], 10003)
        self.assertTrue(0 <= result["score"] <= 100)


if __name__ == "__main__":
    unittest.main()
