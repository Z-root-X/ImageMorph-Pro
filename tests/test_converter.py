import os

import pytest
from PIL import Image

from src.core.converter import convert_image


@pytest.fixture
def create_dummy_image(tmp_path):
    def _create_dummy_image(filename, mode="RGB", size=(100, 100), color="blue"):
        img = Image.new(mode, size, color)
        path = tmp_path / filename
        img.save(path)
        return str(path)
    return _create_dummy_image

def test_convert_image_png_to_jpg(create_dummy_image, tmp_path):
    input_path = create_dummy_image("test.png", mode="RGBA")
    output_path = tmp_path / "output.jpg"
    success, message = convert_image(str(input_path), "JPG", str(output_path))
    assert success is True
    assert os.path.exists(output_path)
    assert Image.open(output_path).mode == "RGB"

def test_convert_image_unsupported_format(create_dummy_image, tmp_path):
    input_path = create_dummy_image("test.png")
    output_path = tmp_path / "output.xyz"
    success, message = convert_image(str(input_path), "XYZ", str(output_path))
    assert success is False
    assert "Unsupported output format" in message

def test_convert_image_file_not_found(tmp_path):
    output_path = tmp_path / "output.jpg"
    success, message = convert_image("non_existent_file.png", "JPG", str(output_path))
    assert success is False
    assert "Input file not found" in message

def test_convert_image_invalid_image(tmp_path):
    invalid_image_path = tmp_path / "invalid.png"
    with open(invalid_image_path, "w") as f:
        f.write("This is not an image")
    output_path = tmp_path / "output.jpg"
    success, message = convert_image(str(invalid_image_path), "JPG", str(output_path))
    assert success is False
    assert "Cannot identify image file" in message
