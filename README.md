# VectoX Labs — ML/AI Assignment

## Overview

This repository contains seven Python tasks covering document processing, image quality assessment, OCR validation, medical information extraction, an OCR pipeline, knowledge-base retrieval, and legal conversation transcription.

The implementation emphasizes input validation, error handling, transparent rule-based decisions, and automated testing.

## Project Structure

```text
vectoxlabs-ml-ai-assignment/
├── data/
│   └── sample_images/
│       ├── clear.png
│       ├── blurred.png
│       └── dark.png
├── docs/
│   └── design_decisions.md
├── results/
│   └── benchmark_report.md
├── src/
│   ├── q1.py
│   ├── q2_image_quality.py
│   ├── q3_ocr_validation.py
│   ├── q4_medical_extraction.py
│   ├── q5_ocr_pipeline.py
│   ├── q6_knowledge_base.py
│   └── q7_legal_transcription.py
├── tests/
│   ├── test_q1.py
│   ├── test_q2.py
│   ├── test_q3.py
│   ├── test_q4.py
│   ├── test_q5.py
│   ├── test_q6.py
│   └── test_q7.py
├── main.ipynb
├── requirements.txt
└── README.md
```

## Tasks Implemented

### Q1 — Document Record Processing
Deduplicates records using timestamps and assigns quality categories based on configured thresholds.

### Q2 — Image Quality Assessment
Uses OpenCV to estimate image blur and brightness and flag unsuitable images.

### Q3 — OCR Validation
Evaluates OCR confidence, cleans extracted text, and checks medicine names against a predefined dictionary.

### Q4 — Medical Information Extraction
Extracts structured medical information and flags missing or potentially ambiguous fields for review.

### Q5 — End-to-End OCR Pipeline
Combines image-quality assessment, OCR and text validation with error handling and latency measurement.

### Q6 — Knowledge-Base Chatbot
Retrieves relevant documents using TF-IDF, provides citations, separates conversation history by user, and supports project-level filtering.

### Q7 — Legal Conversation Transcription
Uses Faster-Whisper for audio transcription and provides transcript cleanup, English/Hindi legal keyword filtering, and rule-based extraction of explicit information.

## Requirements

- Python 3.10 or compatible version
- Dependencies listed in `requirements.txt`
- Tesseract OCR installed and configured for OCR tasks that require it
- Faster-Whisper and its required model files for audio transcription

Some tasks may require additional setup, depending on the installed libraries and selected inference device.

## Setup

Open a terminal in the project root.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Tests

Run the full automated test suite:

```bash
python -m pytest -v
```

Run an individual question's tests, for example Q7:

```bash
python -m pytest tests/test_q7.py -v
```

## Test Results

The latest recorded full test run reported:

- **44 tests passed**
- **0 tests failed**
- Python 3.10.11
- Windows

The recorded test-suite duration was 2.54 seconds. This is the test-suite runtime, not the audio transcription runtime.

## Documentation and Evaluation

- Design decisions: `docs/design_decisions.md`
- Benchmark and evaluation report: `results/benchmark_report.md`

Performance measurements not yet collected are explicitly marked as pending in the benchmark report.

## Limitations

- Automated tests do not guarantee correctness for every real-world input.
- OCR quality depends on image quality and OCR configuration.
- Medical extractions require human verification and are not clinical advice.
- The knowledge-base implementation is a baseline and needs further security evaluation before production deployment.
- Legal keyword filtering and rule-based extraction may miss information or produce false positives.
- Legal and medical outputs must be verified against their original sources.

## Responsible Use

Do not use this project as a substitute for professional medical or legal judgment. Review uncertain outputs and verify extracted information against the original material.

## AI Assistance Disclosure

Complete this section according to the assignment's disclosure requirements. Identify the AI tools used, their purpose, the extent of assistance, and your actual usage duration. Do not report estimated usage duration as measured fact.

## Author

Anuradha Singh
