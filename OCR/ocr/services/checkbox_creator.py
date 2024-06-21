from PIL import Image, ImageDraw


def fill_checkbox(image_path, fill_percents):
    # Load the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    x, y, w, h = 16, 16, 30, 28

    for percent in fill_percents:
        temp_img = img.copy()
        draw = ImageDraw.Draw(temp_img)

        # Calculate height to fill
        fill_height = int(h * (percent / 100.0))

        # Draw rectangle inside checkbox to represent 'filling'
        draw.rectangle([x, y + h - fill_height, x + w, y + h], fill="black")

        # Save or display the image
        temp_img.save(f"checkbox_filled_{percent}percent.png")


fill_percents = [1, 40, 60, 80, 100]
fill_checkbox("/Users/arindamkulshi/IDWA/IDWA/OCR/ocr/services/checkbox_template.png", fill_percents)
