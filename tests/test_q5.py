
from pathlib import Path

import cv2
import numpy as np

from src.q5_ocr_pipeline import run_ocr_pipeline


def test_missing_image_returns_error(tmp_path):
    result = run_ocr_pipeline(tmp_path / "missing.png")

    assert result["success"] is False
    assert "Image not found" in result["error"]
    assert result["latency_seconds"] >= 0


def test_pipeline_returns_quality_for_valid_image(tmp_path):
    image = np.full((200, 200, 3), 220, dtype=np.uint8)
    cv2.rectangle(image, (30, 30), (170, 170), (0, 0, 0), 5)

    image_path = tmp_path / "clear.png"
    assert cv2.imwrite(str(image_path), image)

    result = run_ocr_pipeline(image_path)

    assert result["image_quality"] is not None
    assert result["latency_seconds"] >= 0

    # OCR may succeed or report a missing Tesseract installation.
    if result["success"]:
        assert result["ocr"] is not None
        assert "original_text" in result["ocr"]
        assert "corrected_text" in result["ocr"]
    else:
        assert result["error"] is not None


def test_unreadable_image_is_handled(tmp_path):
    image_path = tmp_path / "invalid.png"
    image_path.write_text("not a valid image")

    result = run_ocr_pipeline(image_path)

    assert result["success"] is False
    assert result["error"] is not None
    assert result["latency_seconds"] >= 0
