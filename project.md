# resume-screener

## Project overview

A resume screening pipeline that ingests candidate resumes, cleans and extracts structured information, generates semantic embeddings, and scores resumes against a job description.

## Current repository structure

- `data/`
  - `raw/` — raw resume files stored as PDF, DOCX, or TXT
  - `processed/` — intended for cleaned and normalized resume text
  - `labeled/` — intended for labeled training or evaluation data

- `src/`
  - `ingestion/`
    - `parser.py` — parse PDF, DOCX, and TXT resumes into raw text
    - `resume_loader.py` — load resume files from a directory and normalize them into a common data structure

  - `preprocessing/`
    - `cleaner.py` — clean raw resume text, extract sections, and infer candidate skills
    - `tokenizer.py` — planned tokenizer utilities for further NLP preprocessing (not present in the current repository)

  - `embedding/`
    - `embedder.py` — sentence-transformers based embedding generation
    - `faiss_store.py` — FAISS index wrapper for semantic retrieval and similarity search

  - `scoring/`
    - `scorer.py` — combined resume scoring logic using semantic similarity, skill matching, and experience heuristics
    - `ranker.py` — planned ranking helper for ordering candidates by score (not present in the current repository)

- `tests/` — placeholder for unit and integration tests
- `venv/` — local Python virtual environment, not part of the published library

## Implemented features

1. Resume ingestion
   - `src/ingestion/parser.py` supports PDF, DOCX, and TXT resume parsing.
   - `src/ingestion/resume_loader.py` iterates over files in `data/raw/`, parses content, and returns a resume dataset.

2. Text preprocessing
   - `src/preprocessing/cleaner.py` applies normalization, removes emails/URLs, and extracts resume sections and skills.

3. Semantic embedding
   - `src/embedding/embedder.py` wraps `SentenceTransformer` for normalized sentence embeddings.
   - `src/embedding/faiss_store.py` stores embeddings in a FAISS inner-product index and supports top-k retrieval.

4. Resume scoring
   - `src/scoring/scorer.py` computes a combined score from semantic relevance, skills, and experience.
   - The scorer returns a normalized score, fit decision, and explanation text.

## Planned / remaining work

- Complete missing modules indicated in the original project skeleton:
  - `src/model/` for training, inference, and any fine-tuning logic
  - `src/evaluation/` for metrics, evaluation pipelines, and model validation
  - `src/api/` for serving the scoring pipeline via REST or Web API
  - `src/utils/` for shared logging, configuration, and reusable helpers

- Add and validate `tests/` with unit tests for parser, cleaner, embedder, FAISS store, and scorer.
- Implement a proper tokenizer or NLP preprocessing pipeline in `src/preprocessing/tokenizer.py`.
- Add data pipeline scripts for generating `processed/` and `labeled/` datasets.
- Create `requirements.txt` and/or a modern dependency manifest.
- Add a top-level `README.md` describing usage, installation, and examples.
- Add Docker packaging in `docker/` for reproducible deployment.

## Notes

- The current codebase is focused on core resume parsing, cleaning, embedding, and scoring.
- The project skeleton in `project.md` is now updated to match the actual repository state and the next implementation steps.
