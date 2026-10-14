
import json
import re
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator


class MedicalRecord(BaseModel):
    """Validated structure for extracted medication information."""

    medicine_name: Optional[str] = None
    strength: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None

    warnings: list[str] = Field(default_factory=list)
    needs_review: bool = False

    @field_validator("medicine_name", "strength", "frequency", "duration")
    @classmethod
    def strip_text(cls, value):
        if value is None:
            return value
        value = value.strip()
        return value or None


def extract_medical_data(text: str) -> dict:
    """
    Extract basic medication fields from simple text.

    This is a rule-based demonstration, not a clinical-grade
    prescription parser. Ambiguous information is flagged.
    """
    warnings = []

    medicine_match = re.search(
        r"\b(?:medicine|drug)\s*:\s*([A-Za-z][A-Za-z -]*)",
        text,
        re.IGNORECASE,
    )

    strength_match = re.search(
        r"\b(\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|IU))\b",
        text,
        re.IGNORECASE,
    )

    frequency_match = re.search(
        r"\b(once daily|twice daily|three times daily|"
        r"once a day|twice a day|every \d+ hours)\b",
        text,
        re.IGNORECASE,
    )

    duration_match = re.search(
        r"\b(?:for\s+)?(\d+)\s*(days?|weeks?)\b",
        text,
        re.IGNORECASE,
    )

    medicine_name = (
        medicine_match.group(1).strip()
        if medicine_match else None
    )
    strength = (
        strength_match.group(1).strip()
        if strength_match else None
    )
    frequency = (
        frequency_match.group(1).strip()
        if frequency_match else None
    )

    duration = None
    if duration_match:
        number = duration_match.group(1)
        unit = duration_match.group(2).lower()
        duration = f"{number} {unit}"

    # Do not invent missing values.
    fields = {
        "medicine_name": medicine_name,
        "strength": strength,
        "frequency": frequency,
        "duration": duration,
    }

    for field_name, value in fields.items():
        if value is None:
            warnings.append(f"Missing or unrecognized field: {field_name}")

    # Flag possible confusion when a strength is present but frequency
    # is absent, or when the text contains an unsupported schedule.
    if strength and not frequency:
        warnings.append(
            "Strength found, but frequency is missing or unrecognized"
        )

    if re.search(r"\b(?:mg|mcg|ml)\s*/\s*day\b", text, re.IGNORECASE):
        warnings.append(
            "Possible strength/frequency ambiguity; manual review required"
        )

    try:
        record = MedicalRecord(
            **fields,
            warnings=warnings,
            needs_review=bool(warnings),
        )
    except ValidationError as exc:
        return {
            "valid": False,
            "errors": exc.errors(),
            "json": None,
        }

    return {
        "valid": True,
        "errors": [],
        "json": record.model_dump(),
    }


if __name__ == "__main__":
    sample_text = (
        "Medicine: Paracetamol, strength 500 mg, "
        "twice daily for 3 days"
    )

    result = extract_medical_data(sample_text)

    print("MEDICAL DATA EXTRACTION")
    print("=" * 50)
    print(json.dumps(result, indent=4))
