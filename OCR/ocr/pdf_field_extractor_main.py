from OCR.ocr.services.pdf_field_extractor import PDFFieldExtractor
import os

current_script_dir = os.path.dirname(os.path.abspath(__file__))
file_relative_path = "../tests/assets/fillable.pdf"
file_absolute_path = os.path.join(current_script_dir, file_relative_path)
extractor = PDFFieldExtractor(file_absolute_path)
extractor.initialize_reader()
