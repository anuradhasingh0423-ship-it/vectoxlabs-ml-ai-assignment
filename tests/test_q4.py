
from src.q4_medical_extraction import extract_medical_data


def test_extract_complete_medical_record():
    text = (
        "Medicine: Paracetamol, strength 500 mg, "
        "twice daily for 3 days"
    )

    result = extract_medical_data(text)

    assert result["valid"] is True
    record = result["json"]

    assert record["medicine_name"] == "Paracetamol"
    assert record["strength"] == "500 mg"
    assert record["frequency"] == "twice daily"
    assert record["duration"] == "3 days"
    assert record["needs_review"] is False


def test_missing_fields_are_flagged():
    result = extract_medical_data("Medicine: Paracetamol")

    assert result["valid"] is True
    record = result["json"]

    assert record["medicine_name"] == "Paracetamol"
    assert record["strength"] is None
    assert record["needs_review"] is True
    assert any(
        "Missing or unrecognized field" in warning
        for warning in record["warnings"]
    )


def test_duration_is_normalized():
    result = extract_medical_data(
        "Medicine: Paracetamol, 500 mg, twice daily for 5 days"
    )

    assert result["json"]["duration"] == "5 days"


def test_week_duration():
    result = extract_medical_data(
        "Medicine: Paracetamol, 500 mg, twice daily for 2 weeks"
    )

    assert result["json"]["duration"] == "2 weeks"


def test_strength_without_frequency_needs_review():
    result = extract_medical_data(
        "Medicine: Paracetamol, strength 500 mg"
    )

    assert result["json"]["needs_review"] is True
    assert any(
        "frequency" in warning.lower()
        for warning in result["json"]["warnings"]
    )


def test_empty_text_does_not_invent_values():
    result = extract_medical_data("")

    assert result["valid"] is True
    record = result["json"]

    assert record["medicine_name"] is None
    assert record["strength"] is None
    assert record["frequency"] is None
    assert record["duration"] is None
    assert record["needs_review"] is True
