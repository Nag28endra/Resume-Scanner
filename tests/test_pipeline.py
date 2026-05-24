from src.ingestion.resume_loader import ResumeLoader
from src.preprocessing.cleaner import ResumeCleaner
from src.scoring.scorer import ResumeScorer


def test_imports():
    assert ResumeLoader is not None
    assert ResumeCleaner is not None
    assert ResumeScorer is not None
