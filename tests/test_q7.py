
import pytest

from src.q7_legal_transcription import (
    clean_transcript,
    extract_legal_information,
    filter_legal_content,
    process_transcript,
    transcribe_audio,
)


def test_whitespace_is_cleaned():
    assert clean_transcript("  Hello   world \n\n\nNext ") == (
        "Hello world \n\nNext"
    )


def test_original_transcript_is_preserved():
    original = "  The witness gave evidence.  "
    result = process_transcript(original)

    assert result["original_transcript"] == original
    assert result["cleaned_transcript"] == (
        "The witness gave evidence."
    )


def test_legal_sentence_is_filtered():
    sentences = filter_legal_content(
        "The weather is pleasant. "
        "The witness gave evidence in court."
    )

    assert len(sentences) == 1
    assert "witness" in sentences[0].lower()


def test_hindi_legal_keyword_is_recognized():
    sentences = filter_legal_content(
        "आज मौसम अच्छा है। पुलिस ने शिकायत दर्ज की।"
    )

    assert len(sentences) == 1
    assert "पुलिस" in sentences[0]


def test_explicit_legal_reference_is_extracted():
    result = extract_legal_information(
        "The notice refers to Section 12 of Example Act."
    )

    assert result["legal_references"]
    assert "Section 12 of Example Act" in (
        result["legal_references"][0]
    )


def test_missing_legal_reference_is_not_invented():
    result = extract_legal_information(
        "The parties discussed an agreement."
    )

    assert result["legal_references"] == []
    assert result["review_required"] is True


def test_explicit_date_is_extracted():
    result = extract_legal_information(
        "The hearing took place on 2026-10-12."
    )

    assert "2026-10-12" in result["dates"]


def test_empty_transcript_is_handled():
    result = process_transcript("")

    assert result["cleaned_transcript"] == ""
    assert result["relevant_sentences"] == []
    assert result["extracted_information"]["legal_references"] == []


def test_non_string_transcript_is_rejected():
    with pytest.raises(TypeError):
        clean_transcript(None)


def test_missing_audio_returns_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        transcribe_audio(tmp_path / "missing.wav")
