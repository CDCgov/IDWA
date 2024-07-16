import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# Function to convert PDF to images
def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images

# Function to extract text from images using Tesseract
def images_to_text(images):
    text_data = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        text_data += f"Page {i + 1}\n{text}\n\n"
    return text_data

# Function to process a single PDF and save as a text file
def pdf_to_text(pdf_path, txt_path):
    images = pdf_to_images(pdf_path)
    extracted_text = images_to_text(images)
    
    with open(txt_path, 'w') as txt_file:
        txt_file.write(extracted_text)
    
    print(f"Converted {pdf_path} to {txt_path}")

# Main function to process a directory of PDFs
def process_directory(pdf_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(pdf_directory):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)
            txt_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.txt")
            pdf_to_text(pdf_path, txt_path)

# Example usage
pdf_directory = '/Users/kevinnguyen/workspace/IDWA/OCR/ocr/output_pdfs'
output_directory = '/Users/kevinnguyen/workspace/IDWA/OCR/ocr/output_jsons'
process_directory(pdf_directory, output_directory)