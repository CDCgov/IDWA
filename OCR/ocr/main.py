import os
from ocr.services.image_segmenter import ImageSegmenter
from ocr.services.image_ocr import ImageOCR
from ocr.services.pdf_to_image import convert_pdf_to_images
from PIL import Image
import pytesseract
import json

path = os.path.dirname(__file__)

    # Function to read a JSON file
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    segmentation_template = os.path.join(path, "../tests/assets/form_segmentation_template_hep_page_1.png")
    raw_image = os.path.join(path, "../tests/assets/form_filled_hep.jpg")
    labels_path = os.path.join(path, "../tests/assets/labels_hep_page1.json")

    segmenter = ImageSegmenter(raw_image, segmentation_template, labels_path)
    segments = segmenter.segment()

    print("{:<20} {:<20}".format("Label", "Segment shape"))
    for label, segment in segments.items():
        segment_shape = segment.shape if segment is not None else "INVALID"
        print("{:<20} {:<20}".format(f"{segment_shape}", label))
        # cv.imwrite(f"{label}_segment.png", segment)

    ocr = ImageOCR()
    values = ocr.image_to_text(segments=segments)

    print("{:<20} {:<20}".format("Label", "Text"))
    for label, text in values.items():
        print("{:<20} {:<20}".format(label, text))
    # segmentation_template = os.path.join(path, "../tests/assets/form_segmentation_template_hep_page_1.png")
    # raw_image = os.path.join(path, "../tests/assets/form_filled_hep.jpg")
    # labels_path = os.path.join(path, "../tests/assets/labels_hep_page1.json")

    # segmenter = ImageSegmenter(raw_image, segmentation_template, labels_path)
    # segments = segmenter.segment()

    # print("{:<20} {:<20}".format("Label", "Segment shape"))
    # for label, segment in segments.items():
    #     segment_shape = segment.shape if segment is not None else "INVALID"
    #     print("{:<20} {:<20}".format(f"{segment_shape}", label))
    #     # cv.imwrite(f"{label}_segment.png", segment)

    # ocr = ImageOCR()
    # values = ocr.image_to_text(segments=segments)

    # print("{:<20} {:<20}".format("Label", "Text"))
    # for label, text in values.items():
    #     print("{:<20} {:<20}".format(label, text))

    # images = convert_pdf_to_images('/Users/kevinnguyen/workspace/IDWA/OCR/ocr/assets/hepatitis_a.pdf')
    # print(images)
    # image_paths = []
    # for i, image in enumerate(images):
    #     image_path = f'/Users/kevinnguyen/workspace/IDWA/OCR/ocr/assets/page_{i + 1}.jpg'
    #     image.save(image_path)
    #     image_paths.append(image_path)

    # # print(image_paths)

    # image = Image.open("/Users/kevinnguyen/workspace/IDWA/OCR/ocr/assets/page_1.jpg")
    # image.show()




    file_path = '/Users/kevinnguyen/workspace/IDWA/OCR/ocr/assets/Glenn0_Conn188_a3223cb0-f83c-097c-2ee4-4a71e6753946.json'  # Replace with your JSON file path
    data = read_json_file(file_path)
    print(data.keys())
    if data.get('attributes'):
        print(data.get('attributes').get('city'))
        print(data.get('attributes').get('address'))
        print(data.get('attributes')['state'])
        print(data.get('attributes')['birth_country'])
        print(data.get('attributes').get('birthdate'))
        print(data.get('attributes').get('name'))
        print(data.get('attributes').get('telecom'))




        # print(data.attributes.city)
        # print(data.attributes.state)
        # print(data.attributes.name)
        # print(data.attributes.phone)



    

    # text_page_1 = pytesseract.image_to_string(Image.open("/Users/kevinnguyen/workspace/IDWA/OCR/ocr/assets/page_1.jpg"))
    # print(text_page_1)

    # image_text = ImageOCR.image_to_textfile(image)
    # print(image_text)



if __name__ == "__main__":
    main()
