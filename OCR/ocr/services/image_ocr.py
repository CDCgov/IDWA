import numpy as np
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image


class ImageOCR:
    def __init__(self, model="microsoft/trocr-base-printed"):
        self.processor = TrOCRProcessor.from_pretrained(model)
        self.model = VisionEncoderDecoderModel.from_pretrained(model)
    
    def image_to_textfile(image):
        # Assume 'image' is already a PIL Image object
        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-stage1")
        model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-stage1")
        
        # Convert PIL image to model input
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        
        # Perform OCR to extract text
        output = model.generate(pixel_values)
        decoded_text = processor.decode(output[0], skip_special_tokens=True)
        
        return decoded_text


    def image_to_text(self, segments: dict[str, np.ndarray]) -> dict[str, str]:
        digitized: dict[str, str] = {}
        for label, image in segments.items():
            if image is None:
                continue

            pixel_values = self.processor(images=image, return_tensors="pt").pixel_values

            generated_ids = self.model.generate(pixel_values)
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)
            digitized[label] = generated_text[0]

        return digitized
