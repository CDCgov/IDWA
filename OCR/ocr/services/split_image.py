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


from PIL import Image


# Load the image containing the 9 checkboxes
img_path = "/Users/arindamkulshi/IDWA/IDWA/OCR/ocr/services/1.png"
img = Image.open(img_path)

# Define the dimensions for splitting
# Assuming there are 3x3 grid of images
img_width, img_height = img.size
single_width = img_width // 3
single_height = img_height // 3

# Create a list to hold the images
images = []

# Split the image
for i in range(3):
    for j in range(3):
        left = j * single_width
        upper = i * single_height
        right = left + single_width
        lower = upper + single_height
        # Crop the image and append to the list
        images.append(img.crop((left, upper, right, lower)))

# Save the cropped images
output_paths = []
for index, image in enumerate(images):
    output_file = f"{index + 1}.png"
    image.save(output_file)
    output_paths.append(output_file)

output_paths
