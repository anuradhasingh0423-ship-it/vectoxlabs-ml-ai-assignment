
import time
from pathlib import Path

import cv2
import pytesseract
from PIL import Image

from src.q2_image_quality import assess_image_quality
from src.q3_ocr_validation import process_ocr_text


def run_ocr_pipeline(image_path):
    """
    Run image quality assessment, OCR, text processing,
    and latency measurement on one image.

    Returns a structured dictionary containing results,
    errors, and processing time.
    """
    start_time = time.perf_counter()
    image_path = Path(image_path)

    result = {
        "image": image_path.name,
        "success": False,
        "image_quality": None,
        "ocr": None,
        "latency_seconds": None,
        "error": None,
    }

    try:
        if not image_path.is_file():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        # Stage 1: Assess image quality.
        quality = assess_image_quality(image_path)
        result["image_quality"] = quality

        # Stage 2: Extract OCR text and word confidence.
        with Image.open(image_path) as image:
            image = image.convert("RGB")

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
            if confidences
            else 0.0
        )

        # Stage 3: Process text without discarding the original.
        ocr_result = process_ocr_text(
            original_text,
            average_confidence,
        )

        ocr_result["word_count"] = len(words)
        result["ocr"] = ocr_result
        result["success"] = True

    except FileNotFoundError as exc:
        result["error"] = str(exc)

    except pytesseract.TesseractNotFoundError:
        result["error"] = (
            "Tesseract OCR application was not found. "
            "Install Tesseract and add it to PATH."
        )

    except Exception as exc:
        result["error"] = (
            f"{type(exc).__name__}: {exc}"
        )

    finally:
        result["latency_seconds"] = round(
            time.perf_counter() - start_time, 4
        )

    return result


if __name__ == "__main__":
    sample_dir = Path("data/sample_images")

    if not sample_dir.exists():
        print(
            "Sample images not found. Run "
            "'python src/q2_image_quality.py' first."
        )
    else:
        for filename in [
            "clear.png",
            "blurred.png",
            "dark.png",
        ]:
            output = run_ocr_pipeline(sample_dir / filename)

            print("\n" + "=" * 60)
            print(f"Pipeline result for {filename}")

            for key, value in output.items():
                print(f"{key}: {value}")
