from services.metrics_analysis import OCRMetrics
import os


current_script_dir = os.path.dirname(os.path.abspath(__file__))
file_relative_path_ground_truth = "../tests/assets/ltbi_legacy.json"
file_relative_path_ocr = "../tests/assets/ltbi_legacy_ocr.json"
ground_truth_json_path = os.path.join(current_script_dir, file_relative_path_ground_truth)
ocr_json_path = os.path.join(current_script_dir, file_relative_path_ocr)

ocr_metrics = OCRMetrics(ocr_json_path, ground_truth_json_path)
metrics = ocr_metrics.calculate_metrics()
for m in metrics:
    print(m)
overall_metrics = ocr_metrics.total_metrics(metrics)
print("Overall Metrics:", overall_metrics)
OCRMetrics.save_metrics_to_csv(metrics, "new.csv")
