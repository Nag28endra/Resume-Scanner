import os
import shutil
from typing import Dict, List

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from ..model.inference import build_resume_index, rank_resumes
from ..model.train import build_training_dataset


class ScoreRequest(BaseModel):
    job_description: str
    top_k: int = 5


class ScoreResult(BaseModel):
    file_name: str
    final_score: int
    decision: str
    semantic_score: float
    skill_score: float
    experience_score: float
    reason: str


router = APIRouter(prefix="/api", tags=["screening"])

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data", "raw")

_resume_index = None
_resume_data = None


def get_resume_index(force_reload=False):
    global _resume_index, _resume_data
    if _resume_index is None or force_reload:
        if not os.path.isdir(DATA_DIR):
            os.makedirs(DATA_DIR, exist_ok=True)

        _resume_data = build_training_dataset(DATA_DIR)
        if not _resume_data:
            _resume_index = None
            return None

        _resume_index = build_resume_index(_resume_data)

    return _resume_index


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/upload")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """Upload resume files to the data directory"""
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

    uploaded_files = []
    for file in files:
        if not file.filename:
            continue

        # Validate file extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ['.pdf', '.docx', '.txt']:
            continue

        file_path = os.path.join(DATA_DIR, file.filename)

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(file.filename)

    # Force reload of resume index
    get_resume_index(force_reload=True)

    return {"uploaded": uploaded_files, "total": len(uploaded_files)}


@router.post("/score", response_model=List[ScoreResult])
def score_job_description(request: ScoreRequest):
    resume_index = get_resume_index()
    if resume_index is None:
        raise HTTPException(status_code=404, detail="No resumes available. Please upload some resumes first.")

    scored = rank_resumes(request.job_description, resume_index, top_k=request.top_k)
    return scored
