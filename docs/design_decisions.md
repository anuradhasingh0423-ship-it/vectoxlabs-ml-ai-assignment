# Design Decisions — VectoX Labs ML/AI Assignment

## Q1: Document Record Processing

The implementation removes duplicate records by keeping the record with the latest timestamp. When timestamps are equal, the first record is retained. Records are classified using quality thresholds:

- **ACCEPT:** Quality score greater than or equal to 0.80.
- **REVIEW:** Quality score greater than or equal to 0.50 and below 0.80.
- **RETAKE:** Quality score below 0.50.

## Q2: Image Quality Assessment

OpenCV is used to inspect image quality. Laplacian variance helps estimate blur, while grayscale brightness helps identify dark images. Missing and unreadable image inputs are handled with errors.

## Q3: OCR Validation

OCR output is evaluated using confidence levels:

- **High:** Confidence greater than or equal to 80.
- **Medium:** Confidence greater than or equal to 50 and below 80.
- **Low:** Confidence below 50.

Text cleanup preserves the original text so that changes can be reviewed. Medicine-name matching uses a predefined dictionary and does not replace professional verification.

## Q4: Medical Information Extraction

Rule-based extraction and Pydantic validation are used to identify and validate structured medical fields. Missing information and potentially ambiguous values are flagged for review. Extracted values are not assumed to be clinically correct.

## Q5: End-to-End OCR Pipeline

The pipeline combines image-quality assessment, OCR and text validation. It records processing time and handles common input and processing errors.

## Q6: Knowledge-Base Chatbot

TF-IDF-based retrieval is used to find relevant documents and produce answers with citations. The implementation includes project filtering, user-specific conversation history and handling for questions that cannot be answered from available documents.

The current implementation is a baseline retrieval system, not a fully featured generative AI chatbot. Access controls require additional security review before production use.

## Q7: Legal Conversation Transcription

Faster-Whisper is used for audio transcription, with CPU-based inference as the default configuration. The implementation supports automatic language detection, transcript cleanup, English and Hindi legal keyword filtering, and rule-based extraction of explicit dates, labelled names and legal references.

The original transcript is preserved. Extracted information is flagged for review because keyword filtering and regular expressions cannot guarantee legal accuracy.

## Overall Design Principles

1. Prefer explicit rules and thresholds where they are appropriate.
2. Preserve original input when cleaning or transforming data.
3. Handle missing, invalid and unreadable inputs.
4. Avoid inventing missing medical or legal information.
5. Make uncertain results visible for human review.
6. Use automated tests to check expected behavior.
