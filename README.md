# Resume Scanner

A lightweight resume screening application that parses resumes, cleans the text, generates semantic embeddings, and scores each resume against a job description.

## What the application does

The application works in four main steps:

1. **Ingest resumes**
   - `src/ingestion/parser.py` reads `.pdf`, `.docx`, and `.txt` files.
   - `src/ingestion/resume_loader.py` loads all files from `data/raw/` and converts them into a simple list of resume records.

2. **Clean and extract resume features**
   - `src/preprocessing/cleaner.py` lowercases text, removes emails/URLs, strips punctuation, and extracts basic sections (`skills`, `experience`, `education`).
   - `src/preprocessing/tokenizer.py` provides a small tokenization helper used by the cleaner.

3. **Create embeddings and search semantically**
   - `src/embedding/embedder.py` uses `SentenceTransformer` (`all-MiniLM-L6-v2`) to create normalized embeddings.
   - `src/embedding/faiss_store.py` stores those embeddings in a FAISS inner-product index.
   - When a job description is provided, the app encodes that text and retrieves the closest resumes from the FAISS index.

4. **Score and rank matches**
   - `src/scoring/scorer.py` computes a weighted score using:
     - **Semantic similarity**: 50%
     - **Skill match**: 30%
     - **Experience match**: 20%
   - A resume is labeled **Fit** when its final score is `>= 50`, otherwise **Not Fit**.
   - The result includes `final_score`, `semantic_score`, `skill_score`, `experience_score`, `decision`, and a short explanation.

## Project structure

- `data/raw/` — resume files to scan
- `demo.py` — simple CLI demo that loads resumes, builds an index, and ranks them
- `serve_ui.py` — serves the browser UI on port `3000`
- `src/api/` — FastAPI server that exposes the resume scanning endpoints
- `src/embedding/` — transformer embeddings and FAISS index
- `src/ingestion/` — resume parsing and loading
- `src/model/` — dataset building and inference helpers
- `src/preprocessing/` — text cleaning and tokenization
- `src/scoring/` — scoring logic
- `src/evaluation/` — evaluation helpers (precision, recall, MRR)
- `src/utils/` — shared config and logging helpers
- `ui/` — HTML, CSS, and JavaScript for the web interface
- `tests/` — current test coverage for cleaning and a basic pipeline import check

## Requirements

- Python 3.8+
- `pip` and internet access for the first model download
- Dependencies from `requirements.txt`

> This repository was verified on Python 3.12.

## Setup

### 1. Create and activate the virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you prefer to use the existing virtual environment in this repository:

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Add resumes

Place `.pdf`, `.docx`, or `.txt` files in `data/raw/`.

The repository already contains a sample resume at `data/raw/Nagendra_Marisetti_AI_Engineer.docx`.

## How to run the application

### Option A: Run the CLI demo

This is the quickest way to test the pipeline end to end.

```powershell
python demo.py
```

What it does:

- Loads all resumes from `data/raw/`
- Cleans and embeds them
- Builds a FAISS index
- Scores the resumes against the built-in job description
- Prints the top 3 matches with scores and explanations

> The first run downloads `sentence-transformers/all-MiniLM-L6-v2`, so it may take a minute.

### Option B: Run the API and the web UI

Use two terminals:

#### Terminal 1 — start the API

```powershell
python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

This exposes:

- `GET /api/health`
- `POST /api/upload`
- `POST /api/score`

#### Terminal 2 — start the UI

```powershell
python serve_ui.py
```

Then open:

- `http://localhost:3000`

The UI lets you:

1. Upload one or more resumes
2. Paste a job description
3. Click **Scan Resumes**
4. Review ranked results with semantic, skill, and experience breakdowns

## API behavior

### `GET /api/health`

Checks whether the API is running.

### `POST /api/upload`

Uploads resume files to `data/raw/`, validates the extension, and forces a reload of the in-memory resume index.

### `POST /api/score`

Accepts a JSON payload like:

```json
{
  "job_description": "Looking for a Python engineer with ML and AWS experience",
  "top_k": 5
}
```

Returns a ranked list of result objects.

## Running tests

```powershell
pytest
```

## Notes about the current codebase

- The current implementation is focused on parsing, cleaning, embedding, and scoring.
- `src/model/finetune_lora.py` is currently a placeholder and not implemented.
- `src/preprocessing/tokenizer.py` is a simple tokenizer, not a full NLP pipeline.
- `src/api/routes.py` keeps the resume index in memory and reloads it after uploads.
- `project.md` contains the original roadmap and planned work items.

## Troubleshooting

- If the demo or API fails on the first run, it is usually because the embedding model is still downloading.
- If you see import issues when running `demo.py`, use the repository root as the working directory and run:

```powershell
python demo.py
```

- If the API is not reachable, confirm that `uvicorn` is running and that the command is using the same Python environment as your `pip install` command.
