import re
import time
from pathlib import Path


# These keywords help identify potentially relevant legal content.
# They are filtering hints, not a legal classification system.
LEGAL_KEYWORDS = {
    "agreement", "contract", "court", "judge", "lawyer",
    "advocate", "police", "complaint", "evidence", "witness",
    "hearing", "petition", "notice", "affidavit", "bail",
    "arrest", "fir", "section", "case", "judgment",
    "अदालत", "न्यायालय", "वकील", "पुलिस", "शिकायत",
    "सबूत", "गवाह", "सुनवाई", "समझौता", "नोटिस",
    "मुकदमा", "धारा", "जमानत", "गिरफ्तार",
    "karar", "police", "shikayat", "saboot", "gawah",
    "sunwai", "vakil", "girftar", "jamanat",
}


def clean_transcript(text):
    """
    Normalize whitespace while preserving the original transcript.
    """
    if not isinstance(text, str):
        raise TypeError("Transcript must be a string.")

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def split_sentences(text):
    """
    Split text using English and Hindi sentence-ending marks.
    Supports ., !, ?, Hindi danda (।), and double danda (॥).
    """
    parts = re.split(r"(?<=[.!?।॥])\s*", text.strip())

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


def filter_legal_content(text):
    """
    Return sentences containing at least one legal keyword.

    Substring matching supports Hindi text more reliably than
    extracting Unicode word tokens with a regular expression.
    The original transcript is retained separately.
    """
    cleaned = clean_transcript(text)

    if not cleaned:
        return []

    relevant = []

    for sentence in split_sentences(cleaned):
        normalized_sentence = sentence.casefold()

        if any(
            keyword.casefold() in normalized_sentence
            for keyword in LEGAL_KEYWORDS
        ):
            relevant.append(sentence)

    return relevant


def extract_legal_information(text):
    """
    Extract only explicit text patterns.

    This function does not infer facts or determine legal validity.
    """
    cleaned = clean_transcript(text)

    # Capture explicit references such as:
    # Section 12, Sec. 12, Section 12 of Example Act.
    section_pattern = re.compile(
        r"\b(?:section|sec\.?)\s+\d+[A-Za-z]?"
        r"(?:\s+of\s+(?:the\s+)?[\w ]+?Act)?"
        r"(?=[,.;:\n]|$)",
        re.IGNORECASE,
    )

    # Capture common date formats as written in the transcript.
    date_pattern = re.compile(
        r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
        r"|\d{4}-\d{2}-\d{2})\b"
    )

    # Extract names only when explicitly labelled.
    # Example: Name: Rahul Sharma
    person_pattern = re.compile(
        r"\b(?:Name|Person|Witness)\s*:\s*"
        r"([A-Za-z][A-Za-z .'-]{1,80})",
        re.IGNORECASE,
    )

    sections = list(dict.fromkeys(
        match.group(0).strip()
        for match in section_pattern.finditer(cleaned)
    ))

    dates = list(dict.fromkeys(
        match.group(0)
        for match in date_pattern.finditer(cleaned)
    ))

    people = list(dict.fromkeys(
        match.group(1).strip()
        for match in person_pattern.finditer(cleaned)
    ))

    return {
        "legal_references": sections,
        "dates": dates,
        "explicitly_labelled_people": people,
        "review_required": True,
        "note": (
            "Rule-based extraction may miss information or extract "
            "incorrectly. Verify all details against the original."
        ),
    }


def process_transcript(text):
    """
    Process an existing transcript without calling an AI model.
    """
    start_time = time.perf_counter()

    # Preserve the exact original input separately.
    original_text = text

    cleaned_text = clean_transcript(text)
    relevant_sentences = filter_legal_content(cleaned_text)
    extracted_information = extract_legal_information(cleaned_text)

    return {
        "original_transcript": original_text,
        "cleaned_transcript": cleaned_text,
        "relevant_sentences": relevant_sentences,
        "extracted_information": extracted_information,
        "processing_latency_seconds": round(
            time.perf_counter() - start_time, 6
        ),
    }


def transcribe_audio(
    audio_path,
    model_size="tiny",
    device="cpu",
    compute_type="int8",
    language=None,
):
    """
    Transcribe an audio file using Faster-Whisper.

    Args:
        audio_path: Path to the audio file.
        model_size: Whisper model size, such as tiny or base.
        device: Inference device, usually cpu or cuda.
        compute_type: Model computation type, such as int8.
        language: Optional language code, such as en or hi.
                  None enables automatic language detection.

    Returns:
        A dictionary containing the transcript, relevant legal
        sentences, extracted information, language details,
        timestamps, and latency measurements.
    """
    start_time = time.perf_counter()
    audio_path = Path(audio_path)

    if not audio_path.is_file():
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError(
            "Faster-Whisper is not installed. Run "
            "'python -m pip install faster-whisper'."
        ) from exc

    model = WhisperModel(
        model_size,
        device=device,
        compute_type=compute_type,
    )

    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=5,
        vad_filter=True,
    )

    segment_results = []
    transcript_parts = []

    # Iterating over segments performs the transcription.
    for segment in segments:
        segment_text = segment.text.strip()

        if segment_text:
            transcript_parts.append(segment_text)

        segment_results.append({
            "start": round(segment.start, 3),
            "end": round(segment.end, 3),
            "text": segment_text,
        })

    transcript = " ".join(transcript_parts).strip()

    result = process_transcript(transcript)

    result["audio_file"] = audio_path.name
    result["detected_language"] = getattr(info, "language", None)
    result["language_probability"] = getattr(
        info, "language_probability", None
    )
    result["segments"] = segment_results
    result["transcription_latency_seconds"] = round(
        time.perf_counter() - start_time, 3
    )

    return result


if __name__ == "__main__":
    sample_transcript = (
        "The agreement was discussed in court on 12/10/2026. "
        "The witness gave evidence. "
        "The parties will meet again tomorrow. "
        "पुलिस ने शिकायत दर्ज की।"
    )

    result = process_transcript(sample_transcript)

    print("Original transcript:")
    print(result["original_transcript"])

    print("\nCleaned transcript:")
    print(result["cleaned_transcript"])

    print("\nRelevant legal sentences:")
    for sentence in result["relevant_sentences"]:
        print("-", sentence)

    print("\nExtracted information:")
    print(result["extracted_information"])

    print(
        "\nProcessing latency:",
        result["processing_latency_seconds"],
        "seconds",
    )
