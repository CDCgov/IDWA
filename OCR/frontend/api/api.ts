import { ImageToTextArgs, ImageToTextResponse } from "./types/types";

export const AddFormData = async (args: ImageToTextArgs): Promise<ImageToTextResponse | null> => {

    const { sourceImage, templateImage, fieldNames } = args;
    const form = new FormData();
    form.append("source_image", sourceImage);
    form.append("segmentation_template", templateImage);
    form.append("labels", JSON.stringify(fieldNames));

    try {
        const response = await fetch("http://localhost:8000/image_file_to_text/", {
            "method": "POST",
            "headers": {
              "Content-Type": "multipart/form-data",
            },
            body: form
          })
          return  await response.json() as ImageToTextResponse;
    } catch (error) {
        console.error(error);
        return null;
    }
    
}
