from ocr.services.image_segmenter import ImageSegmenter
from ocr.services.image_ocr import ImageOCR
from docopt import docopt

usage = """

Manual Data Entry's OCR CLI

usage: 
    main.py (--segment-template) (SEGMENT-TEMPLATE-PATH) (--input-image) (INPUT-IMAGE-PATH) (--labels) (LABELS-PATH)

Arguments:
   SEGMENT-IMAGE       An image template that's already segmented
   INPUT-IMAGE         The working image that needs data extracted from
   LABELS              The json file that coordinates each segment

"""


def main():
    args = docopt(usage)
    segmentation_template = args["SEGMENT-TEMPLATE-PATH"]
    input_image = args["INPUT-IMAGE-PATH"]
    labels_path = args["LABELS-PATH"]

    segmenter = ImageSegmenter()
    segments = segmenter.load_and_segment(input_image, segmentation_template, labels_path)

    print("{:<20} {:<20}".format("Label", "Segment shape"))
    for label, segment in segments.items():
        segment_shape = segment.shape if segment is not None else "INVALID"
        print("{:<20} {:<20}".format(f"{segment_shape}", label))
        # cv.imwrite(f"{label}_segment.png", segment)

    ocr = ImageOCR()
    values = ocr.image_to_text(segments=segments)

    print("{:<20} {:<20} {:<20}".format("Label", "Text", "Confidence"))
    for label, (text, confidence) in values.items():
        print("{:<20} {:<20} {:<20.2f}".format(label, text, confidence))


if __name__ == "__main__":
    main()
