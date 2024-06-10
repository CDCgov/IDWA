from pdf2image import convert_from_path

def convert_pdf_to_images(pdf_path):
    # Convert PDF to a list of images at 300 dpi
    images = convert_from_path(pdf_path, dpi=300)
    return images