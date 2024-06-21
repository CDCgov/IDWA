# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file is derived from:
# https://github.com/jaswanth04/Checkbox_Detection


import cv2
import argparse
from ocr.services.checkbox_image_align import SIFTAligner
from ocr.services.checkbox_detector_image_extractor import MorphDataExtractor


def extract_data(im, aligner, extractor):
    query = cv2.imread(im)
    aligned_sift = aligner.align(query)

    entities = extractor.extract(aligned_sift)

    return entities


def main(args):
    query_image_location = args.query
    template_location = args.template
    roi_json_file = args.roi

    # roi_data = "./Users/arindamkulshi/IDWA/IDWA/OCR/tests/assets/checkbox1.json"

    morph_extractor = MorphDataExtractor(roi_json_file)

    # lifecell_template_path = "./Users/arindamkulshi/IDWA/IDWA/OCR/tests/assets/checkbox_template.png"

    sift_aligner = SIFTAligner(template_location)

    entities = extract_data(im=query_image_location, aligner=sift_aligner, extractor=morph_extractor)

    print(entities)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Parsing arguments for information extraction")

    parser.add_argument("--query", type=str, help="Image from where the data needs to be extracted")

    parser.add_argument("--template", type=str, help="The template document which is used for alignment")

    parser.add_argument("--roi", type=str, help="json file that contains the roi data")

    args = parser.parse_args()

    main(args)
