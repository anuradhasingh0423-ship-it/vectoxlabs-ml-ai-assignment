
from pathlib import Path

import cv2
import numpy as np
import pytest

from src.q2_image_quality import assess_image_quality


@pytest.fixture
def sample_images(tmp_path):
    clear = np.full((200, 200, 3), 220, dtype=np.uint8)
    cv2.rectangle(clear, (30, 30), (170, 170), (0, 0, 0), 5)

    blurred = cv2.GaussianBlur(clear, (51, 51), 0)
    dark = np.full((200, 200, 3), 15, dtype=np.uint8)

    paths = {}

    for name, image in [
        ("clear.png", clear),
        ("blurred.png", blurred),
        ("dark.png", dark),
    ]:
        path = tmp_path / name
        assert cv2.imwrite(str(path), image)
        paths[name] = path

    return paths


def test_clear_image_is_accepted(sample_images):
    result = assess_image_quality(sample_images["clear.png"])
    assert result["status"] == "ACCEPT"
    assert result["issues"] == []


def test_blurred_image_is_flagged(sample_images):
    result = assess_image_quality(sample_images["blurred.png"])
    assert result["status"] == "REVIEW"
    assert "BLURRY" in result["issues"]


def test_dark_image_is_flagged(sample_images):
    result = assess_image_quality(sample_images["dark.png"])
    assert result["status"] == "REVIEW"
    assert result["issues"] == ["DARK"]


def test_missing_image_raises_error(tmp_path):
    missing_path = tmp_path / "missing.png"

    with pytest.raises(FileNotFoundError):
        assess_image_quality(missing_path)


def test_unreadable_image_raises_error(tmp_path):
    invalid_path = tmp_path / "invalid.png"
    invalid_path.write_text("not a valid image")

    with pytest.raises(ValueError):
        assess_image_quality(invalid_path)
