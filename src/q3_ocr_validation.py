
from pathlib import Path
import re

import pytesseract
from PIL import Image, ImageOps, ImageEnhance


# Optional: If Tesseract is installed but not in PATH on Windows,
# uncomment and edit the following line:
# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )

# Demonstration dictionary only. Expand it using a verified source
# before using this system for real medical documents.
MEDICINE_DICTIONARY = {
    "paracetamol",
    "ibuprofen",
    "amoxicillin",
    "cetirizine",
    "metformin",
    "omeprazole",
}


def classify_confidence(confidence):
    """Classify OCR confidence as HIGH, MEDIUM, or LOW."""
    if confidence >= 80:
        return "HIGH"
    elif confidence >= 50:
        return "MEDIUM"
    return "LOW"


def clean_ocr_text(original_text):
    """
    Apply conservative formatting cleanup.
    Never silently change medicine names or numeric values.
    """
    corrected_text = re.sub(r"[ \t]+", " ", original_text)
    corrected_text = re.sub(r"\n{3,}", "\n\n", corrected_text)
    corrected_text = corrected_text.strip()

    reasons = []

    if corrected_text != original_text:
        reasons.append("Normalized extra whitespace")

    return corrected_text, reasons


def validate_medicine_names(text):
    """
    Find medicine-like words and flag names that are not in the
    demonstration dictionary. This is not a medical spell-checker.
    """
    words = re.findall(r"\b[A-Za-z][A-Za-z-]*\b", text)

    findings = []

    for word in words:
        if word.lower() in MEDICINE_DICTIONARY:
            findings.append({
                "text": word,
                "status": "MATCHED_DICTIONARY",
            })

    return findings


def process_ocr_text(original_text, confidence=0.0):
    """
    Process already-extracted OCR text.

    Original text is preserved independently from cleaned text.
    """
    corrected_text, reasons = clean_ocr_text(original_text)

    confidence_label = classify_confidence(confidence)

    medicine_matches = validate_medicine_names(corrected_text)

    return {
        "original_text": original_text,
        "corrected_text": corrected_text,
        "correction_reasons": reasons,
        "ocr_confidence": float(confidence),
        "confidence_label": confidence_label,
        "medicine_matches": medicine_matches,
        "needs_review": (
            confidence_label == "LOW"
            or confidence_label == "MEDIUM"
        ),
    }


def extract_text_from_image(image_path):
    """
    Extract OCR text and average word confidence from an image.

    Requires the Tesseract OCR application to be installed.
    """
    image_path = Path(image_path)

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    try:
        with Image.open(image_path) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            image = ImageEnhance.Contrast(image).enhance(1.5)

            data = pytesseract.image_to_data(
                image,
                output_type=pytesseract.Output.DICT,
            )

            words = []
            confidences = []

            for word, confidence in zip(
                data["text"], data["conf"]
            ):
                word = word.strip()

                try:
                    confidence = float(confidence)
                except (TypeError, ValueError):
                    continue

                if word and confidence >= 0:
                    words.append(word)
                    confidences.append(confidence)

            original_text = " ".join(words)
            average_confidence = (
                sum(confidences) / len(confidences)
                if confidences else 0.0
            )

            return process_ocr_text(
                original_text,
                average_confidence,
            )

    except pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract OCR was not found. Install the Tesseract "
            "application and add it to PATH, or set "
            "pytesseract.pytesseract.tesseract_cmd in this file."
        ) from exc


if __name__ == "__main__":
    # First demonstrate text processing without needing OCR software.
    sample_text = "  Paracetamol   500 mg\n\n\nTake after food  "

    result = process_ocr_text(sample_text, confidence=86.5)

    print("OCR TEXT PROCESSING DEMO")
    print("=" * 50)

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nTo run OCR on an actual image, call:")
    print("extract_text_from_image('path/to/image.png')")
