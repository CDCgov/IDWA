from ocr.services.checkbox_detector_subtraction import CheckboxDetector

import os

path = os.path.dirname(__file__)

checkbox_template = os.path.join(path, "../tests/assets/checkbox_template.png")
checkbox_example_filled = os.path.join(path, "../tests/assets/checkbox_example_filled.png")
checkbox_example_filled_20 = os.path.join(path, "../tests/assets/checkbox_marked_10percent.png")
checkbox_example_filled_1 = os.path.join(path, "../tests/assets/checkbox_filled_1percent.png")
try:
    detector = CheckboxDetector(checkbox_template)
    result = detector.is_checked(checkbox_example_filled_20)
    print("Checkbox is checked:", result)
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print("An error occurred:", e)
