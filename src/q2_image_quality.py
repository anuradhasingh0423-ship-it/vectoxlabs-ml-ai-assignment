from pathlib import Path
import cv2
import numpy as np


def assess_image_quality(
    image_path,
    blur_threshold=100.0,
    dark_threshold=60.0,
):
    """
    Assess image quality using blur and brightness.

    Args:
        image_path: Path to the image file.
        blur_threshold: Minimum Laplacian variance for sharpness.
        dark_threshold: Minimum average grayscale brightness.

    Returns:
        dict: Image name, blur score, brightness score,
              status, and detected issues.

    Note:
        If an image is too dark, blur assessment is skipped
        because low brightness can make blur detection unreliable.
    """
    image_path = Path(image_path)

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Unable to read image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Higher Laplacian variance generally indicates sharper details.
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())

    # Average grayscale brightness ranges from 0 to 255.
    brightness_score = float(np.mean(gray))

    issues = []

    # Check brightness first.
    if brightness_score < dark_threshold:
        issues.append("DARK")
    else:
        # Assess blur only when brightness is sufficient.
        if blur_score < blur_threshold:
            issues.append("BLURRY")

    status = "REVIEW" if issues else "ACCEPT"

    return {
        "image": image_path.name,
        "blur_score": round(blur_score, 2),
        "brightness_score": round(brightness_score, 2),
        "status": status,
        "issues": issues,
    }


def create_sample_images(output_dir="data/sample_images"):
    """Create synthetic clear, blurred, and dark images for testing."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Clear image with visible edges and texture.
    clear = np.full((300, 300, 3), 220, dtype=np.uint8)

    cv2.rectangle(clear, (40, 40), (260, 260), (0, 0, 0), 5)
    cv2.circle(clear, (150, 150), 65, (0, 0, 255), -1)

    cv2.putText(
        clear,
        "CLEAR",
        (75, 285),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 0),
        2,
    )

    # 2. Blurred version of the clear image.
    blurred = cv2.GaussianBlur(clear, (51, 51), 0)

    # 3. Uniformly dark image.
    dark = np.full((300, 300, 3), 15, dtype=np.uint8)

    # Save all sample images.
    cv2.imwrite(str(output_dir / "clear.png"), clear)
    cv2.imwrite(str(output_dir / "blurred.png"), blurred)
    cv2.imwrite(str(output_dir / "dark.png"), dark)

    return output_dir


if __name__ == "__main__":
    sample_dir = create_sample_images()

    print("IMAGE QUALITY ASSESSMENT")
    print("=" * 60)

    for filename in ["clear.png", "blurred.png", "dark.png"]:
        result = assess_image_quality(sample_dir / filename)
        print(result)

    print("=" * 60)
    print("Assessment completed.")
