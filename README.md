# VectoX Labs — ML/AI Assignment

## Overview

This repository contains seven Python tasks covering document record processing, image quality assessment, OCR validation, medical information extraction, an end-to-end OCR pipeline, knowledge-base retrieval, and legal conversation transcription.

The project emphasizes input validation, error handling, transparent decision-making, and automated testing.

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
Processes document records, handles duplicate records using timestamps, and assigns quality categories based on configured thresholds.

### Q2 — Image Quality Assessment
Uses OpenCV to estimate image blur and brightness and identify potentially unsuitable images.

### Q3 — OCR Validation
Evaluates OCR confidence, processes extracted text, and checks medicine names against a predefined dictionary.

### Q4 — Medical Information Extraction
Extracts structured medical information and flags missing or potentially ambiguous fields for review.

### Q5 — End-to-End OCR Pipeline
Combines image-quality assessment, OCR, and text validation with error handling and latency measurement.

### Q6 — Knowledge-Base Chatbot
Uses TF-IDF-based retrieval to find relevant information. The implementation includes citation support and user/project-level separation as implemented in the source code.

### Q7 — Legal Conversation Transcription
Uses Faster-Whisper for audio transcription and provides transcript cleanup, legal keyword filtering, and rule-based extraction of explicit information.

## Requirements

- Python 3.10 or a compatible version.
- Python dependencies listed in `requirements.txt`.
- Tesseract OCR installed and configured for tasks that require it.
- Faster-Whisper and the required model files for audio transcription.

Some components may require additional configuration depending on the installed libraries and available hardware.

## Setup

Open a terminal in the project root directory.

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure external dependencies

Install Tesseract OCR separately and ensure its executable is accessible to the application. Configure its path if required by your environment.

For audio transcription, install and configure Faster-Whisper and ensure the selected model is available. Initial model setup may require an internet connection unless the model is already stored locally.

## Run the Tests

Run the full automated test suite:

```bash
python -m pytest -v
```

Run an individual test module, for example:

```bash
python -m pytest tests/test_q7.py -v
```

## Test Results

The previously recorded test run reported the following results:

- **Tests passed:** 44
- **Tests failed:** 0
- **Python version:** 3.10.11
- **Operating system:** Windows
- **Recorded test-suite duration:** 2.54 seconds

These results describe the recorded test run. Rerun the test suite in your current environment to verify the results before final submission.

The reported duration is the test-suite runtime, not the time required to transcribe an audio recording.

## Documentation and Evaluation

- Design decisions: `docs/design_decisions.md`
- Benchmark report: `results/benchmark_report.md`
- Notebook: `main.ipynb`

Performance measurements that have not yet been collected are identified as pending in the benchmark report.

## Limitations

- Passing automated tests does not guarantee correctness for every real-world input.
- OCR results depend on image quality, OCR configuration, and the source text.
- Medical extraction results require human verification and are not clinical advice.
- The knowledge-base implementation is a baseline and requires further security evaluation before production use.
- Legal keyword filtering and rule-based extraction may miss relevant information or produce false positives.
- Transcripts and extracted legal or medical information must be checked against the original sources.
- Performance and resource usage should be evaluated on the target deployment environment.

## Responsible Use

This project is intended for educational and technical evaluation. Do not use its outputs as a substitute for professional medical or legal judgment. Review uncertain outputs and verify extracted information against the original material.

## AI Assistance Disclosure

Complete the following disclosure accurately to reflect the tools actually used during development.

| AI tool | Purpose | Level of assistance |
|---|---|---|
| [Enter the AI tool(s) actually used] | [Describe how each tool assisted with planning, coding, debugging, testing, or documentation] | [Low / Medium / High] |

**Actual time spent using AI assistance:** [Enter your actual estimated or recorded duration, and label it as an estimate if applicable.]

AI assistance was used for the purposes described above. The final disclosure should accurately distinguish AI-generated suggestions from code that was independently written, reviewed, tested, or modified.

## Author

Anuradha Singh
