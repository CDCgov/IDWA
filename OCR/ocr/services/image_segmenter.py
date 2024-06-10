import cv2 as cv
import numpy as np
import json
import os


def crop_zeros(image):
    # argwhere will give you the coordinates of every non-zero point
    true_points = np.argwhere(image)

    if len(true_points) == 0:
        return None

    # take the smallest points and use them as the top left of your crop
    top_left = true_points.min(axis=0)
    # take the largest points and use them as the bottom right of your crop
    bottom_right = true_points.max(axis=0)
    return image[
        top_left[0] : bottom_right[0] + 1,  # plus 1 because slice isn't
        top_left[1] : bottom_right[1] + 1,
    ]  # inclusive


def segment_by_mask_then_crop(self) -> dict[str, np.ndarray]:
    segments = {}

    with open(self.labels, "r") as f:
        labels = json.load(f)
    # iterate over the labels
    for color, label in labels.items():
        raw_image = np.array(self.raw_image, copy=True)
        segmentation_template = np.array(self.segmentation_template, copy=True)
        color = tuple(map(int, reversed(color.split(","))))
        # create a mask for that color
        mask = np.all(segmentation_template == color, axis=2).astype(int)

        # add a third dimension to the mask
        mask = mask[:, :, np.newaxis]

        # multiply the original image with the mask then crop it
        segments[label] = crop_zeros(raw_image * mask)

        if self.debug is True:
            print(f"label: {label}")
            print(f"color {color}")
            print("mask.shape", mask.shape)
            mask[mask >= 1] = 255
            cv.imwrite(f"{label}_mask.png", mask)
            if segments[label] is not None:
                print("segment.shape", segments[label].shape)
                cv.imwrite(f"{label}.png", segments[label])
            print("====")

    return segments


def segment_by_color_bounding_box(self) -> dict[str, np.ndarray]:
    segments = {}
    with open(self.labels, "r") as f:
        labels = json.load(f)
    # iterate over the labels
    for color, label in labels.items():
        # we are reversing from RGB in the label to BGR used by the openCV
        color = tuple(map(int, reversed(color.split(","))))
        # find indices of the color in the segmentation template where the color matches the expected colors
        indices = np.where(np.all(self.segmentation_template == color, axis=-1))
        # if there are matching pixels
        if indices[0].size > 0:
            # Find the x-y coordinates
            y_min, y_max = indices[0].min(), indices[0].max()
            x_min, x_max = indices[1].min(), indices[1].max()
            # crop the area and store the image in the dict
            segments[label] = self.raw_image[y_min : y_max + 1, x_min : x_max + 1]
        else:
            segments[label] = None
    return segments


class ImageSegmenter:
    def __init__(
        self,
        raw_image,
        segmentation_template,
        labels,
        segmentation_function=segment_by_mask_then_crop,
        debug=False,
    ):
        self.debug = debug
        self.segmentation_function = segmentation_function

        if not os.path.isfile(raw_image) or not os.path.isfile(segmentation_template):
            raise FileNotFoundError("One or more input files do not exist.")

        self.raw_image = cv.imread(raw_image)
        if self.raw_image is None:
            raise ValueError(f"Failed to open image file: {raw_image}")

        self.segmentation_template = cv.imread(segmentation_template)
        if self.segmentation_template is None:
            raise ValueError(f"Failed to open image file: {segmentation_template}")

        self.labels = labels

        if self.debug is True:
            print(f"raw_image shape: {self.raw_image.shape}")
            print(f"segmentation_template shape: {self.segmentation_template.shape}")

    def segment(self) -> dict[str, np.ndarray]:
        return self.segmentation_function(self)
    
    def update_segment(self, label, new_value):
        segments = self.segment()
        if label in segments:
            segments[label] = new_value
        return segments

    def save_segments(self, segments, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for label, segment in segments.items():
            if segment is not None:
                cv.imwrite(os.path.join(output_dir, f"{label}_segment.png"), segment)
            else:
                print(f"Segment for {label} is None and cannot be saved.")
