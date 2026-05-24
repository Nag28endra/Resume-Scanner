from src.preprocessing.cleaner import ResumeCleaner
from src.preprocessing.tokenizer import SimpleTokenizer


def test_tokenizer_handles_text():
    tokens = SimpleTokenizer.tokenize("Python, C++ and machine-learning")
    assert "python" in tokens
    assert "c++" in tokens
    assert "machine" in tokens


def test_resume_cleaner_extracts_skills():
    cleaner = ResumeCleaner()
    skills = cleaner.extract_skills("Experienced with python, docker and aws.")
    assert "python" in skills
    assert "docker" in skills
    assert "aws" in skills
