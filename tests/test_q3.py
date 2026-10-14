
import pytest

from src.q3_ocr_validation import (
    classify_confidence,
    process_ocr_text,
)


def test_high_confidence():
    assert classify_confidence(86.5) == "HIGH"


def test_medium_confidence():
    assert classify_confidence(65.0) == "MEDIUM"


def test_low_confidence():
    assert classify_confidence(30.0) == "LOW"


def test_confidence_boundaries():
    assert classify_confidence(80.0) == "HIGH"
    assert classify_confidence(50.0) == "MEDIUM"
    assert classify_confidence(49.9) == "LOW"


def test_original_text_is_preserved():
    original = "  Paracetamol   500 mg  "
    result = process_ocr_text(original, confidence=90.0)

    assert result["original_text"] == original
    assert result["corrected_text"] == "Paracetamol 500 mg"


def test_whitespace_correction_reason():
    result = process_ocr_text("Hello   world", confidence=90.0)

    assert result["corrected_text"] == "Hello world"
    assert "Normalized extra whitespace" in result["correction_reasons"]


def test_known_medicine_is_matched():
    result = process_ocr_text("Paracetamol 500 mg", confidence=90.0)

    assert {
        "text": "Paracetamol",
        "status": "MATCHED_DICTIONARY",
    } in result["medicine_matches"]


def test_medium_confidence_needs_review():
    result = process_ocr_text("Sample text", confidence=65.0)

    assert result["needs_review"] is True


def test_high_confidence_does_not_need_review():
    result = process_ocr_text("Sample text", confidence=90.0)

    assert result["needs_review"] is False
