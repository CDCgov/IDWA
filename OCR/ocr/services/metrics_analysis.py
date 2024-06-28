import json

import csv
import Levenshtein


class OCRMetrics:
    """
    A class to calculate and manage OCR metrics.

    """

    def __init__(self, ocr_json_path, ground_truth_json_path):
        """
        Parameters:
        ocr_json (dict): The JSON data extracted from OCR.
        ground_truth_json (dict): The JSON data containing ground truth.
        """
        self.ocr_json = self.load_json_file(ocr_json_path)
        self.ground_truth_json = self.load_json_file(ground_truth_json_path)

    def load_json_file(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    @staticmethod
    def normalize(text):
        if text is None:
            return ""
        return " ".join(text.strip().lower().replace(":", "").replace("#", "").replace(" ", "").split())

    @staticmethod
    def raw_distance(ocr_text, ground_truth):
        return len(ground_truth) - len(ocr_text)

    @staticmethod
    def hamming_distance(ocr_text, ground_truth):
        if len(ocr_text) != len(ground_truth):
            raise ValueError("Strings must be of the same length to calculate Hamming distance.")
        return Levenshtein.hamming(ocr_text, ground_truth)

    @staticmethod
    def levenshtein_distance(ocr_text, ground_truth):
        return Levenshtein.distance(ocr_text, ground_truth)

    def extract_values_from_json(self, json_data):
        extracted_values = {}
        for item in json_data:
            if isinstance(item, dict) and "key" in item and "value" in item:
                key = self.normalize(item["key"])
                value = self.normalize(item["value"])
                extracted_values[key] = value
            else:
                raise ValueError("Invalid JSON format")
        return extracted_values

    def calculate_metrics(self):
        ocr_values = self.extract_values_from_json(self.ocr_json)
        ground_truth_values = self.extract_values_from_json(self.ground_truth_json)

        metrics = []
        for key in ground_truth_values:
            ocr_text = ocr_values.get(key, "")
            ground_truth = ground_truth_values[key]
            raw_dist = self.raw_distance(ocr_text, ground_truth)
            try:
                ham_dist = self.hamming_distance(ocr_text, ground_truth)
            except ValueError as e:
                ham_dist = str(e)
            lev_dist = self.levenshtein_distance(ocr_text, ground_truth)
            metrics.append(
                {
                    "key": key,
                    "ocr_text": ocr_text,
                    "ground_truth": ground_truth,
                    "raw_distance": raw_dist,
                    "hamming_distance": ham_dist,
                    "levenshtein_distance": lev_dist,
                }
            )
        return metrics

    def total_metrics(self, metrics):
        raw_dist_sum = sum(m["raw_distance"] for m in metrics if isinstance(m["raw_distance"], int))
        ham_dist_sum = sum(m["hamming_distance"] for m in metrics if isinstance(m["hamming_distance"], int))
        lev_dist_sum = sum(m["levenshtein_distance"] for m in metrics)

        count_raw = sum(1 for m in metrics if isinstance(m["raw_distance"], int))
        count_ham = sum(1 for m in metrics if isinstance(m["hamming_distance"], int))
        count_lev = len(metrics)

        avg_raw_dist = raw_dist_sum / count_raw if count_raw else 0
        avg_ham_dist = ham_dist_sum / count_ham if count_ham else 0
        avg_lev_dist = lev_dist_sum / count_lev if count_lev else 0

        return {
            "average_raw_distance": avg_raw_dist,
            "average_hamming_distance": avg_ham_dist,
            "average_levenshtein_distance": avg_lev_dist,
        }

    @staticmethod
    def save_metrics_to_csv(metrics, file_path):
        """
        Parameters:
        metrics (list): A list of dictionaries containing individual metrics.
        file_path (str): The path to the CSV file
        """
        keys = metrics[0].keys()
        with open(file_path, "w", newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(metrics)
