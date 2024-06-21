import cv2
import numpy as np


class CheckboxDetector:
    def __init__(self, template_path):
        self.template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if self.template is None:
            raise FileNotFoundError(f"Template image not found at {template_path}")

    def is_checked(self, image_path, threshold=18000):
        checkbox_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if checkbox_image is None:
            raise FileNotFoundError(f"Checkbox image not found at {image_path}")

        diff = cv2.absdiff(self.template, checkbox_image)

        # Calculate difference
        diff_sum = np.sum(diff)
        print(diff_sum)
        print(threshold)

        # Determine if the checkbox is checked based on the threshold
        return diff_sum > threshold
