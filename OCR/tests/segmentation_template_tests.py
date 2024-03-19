import pytest
import json
import os
from OCR.services.image_segmenter import ImageSegmenter
from dotenv import load_dotenv
import numpy as np


load_dotenv()

segmentation_template = os.getenv('SEGMENTATION_TEMPLATE_PATH')
raw_image = os.getenv('RAW_IMAGE_PATH')
labels_path = os.getenv('LABELS_PATH')

class TestImageSegmenter:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.raw_image = raw_image
        self.segmentation_template = segmentation_template
        self.labels_path = labels_path
        self.segmenter = ImageSegmenter(self.raw_image, self.segmentation_template, self.labels_path)

    def test_segment(self):
        segments = self.segmenter.segment()
        assert isinstance(segments, dict)
        with open(self.labels_path, 'r') as f:
            labels = json.load(f)
        assert set(segments.keys()) == set(labels.values())
        for segment in segments.values():
            assert isinstance(segment, np.ndarray)

    def test_segment_shapes(self):
        segments = self.segmenter.segment()
        for segment in segments.values():
            assert len(segment.shape) == 3
    
    def test_invalid_file_paths(self):
        with pytest.raises(FileNotFoundError):
            ImageSegmenter('invalid_path', 'invalid_path', {})

    def test_invalid_image_files(self):
        with open('empty_file1', 'w'), open('empty_file2', 'w'):
            pass

        with pytest.raises(ValueError):
            ImageSegmenter('empty_file1', 'empty_file2', {})

        os.remove('empty_file1')
        os.remove('empty_file2')
    