import unittest
from ocr.services.checkbox_detector_subtraction import CheckboxDetector
import os


class TestCheckboxDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        current_dir = os.path.dirname(__file__)
        cls.checkbox_template = os.path.join(current_dir, "./assets/checkbox_template.png")
        cls.checkbox_filled = os.path.join(current_dir, "./assets/checkbox_filled_100percent.png")
        cls.checkbox_filled_20 = os.path.join(current_dir, "./assets/checkbox_marked_10percent.png")
        cls.checkbox_filled_1 = os.path.join(current_dir, "./assets/checkbox_filled_1percent.png")

    def test_checkbox_full(self):
        detector = CheckboxDetector(self.checkbox_template)
        result = detector.is_checked(self.checkbox_filled)
        self.assertTrue(result, "Fully filled checkbox should be detected as checked.")

    def test_checkbox_20_percent(self):
        detector = CheckboxDetector(self.checkbox_template)
        result = detector.is_checked(self.checkbox_filled_20)
        self.assertTrue(result, "20% filled checkbox should be detected as checked.")

    def test_checkbox_1_percent(self):
        # 1% filled should be detected as not checked
        detector = CheckboxDetector(self.checkbox_template)
        result = detector.is_checked(self.checkbox_filled_1)
        self.assertFalse(result, "1% filled checkbox should not be detected as checked.")
