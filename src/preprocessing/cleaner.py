import re
from typing import Dict, List

from .tokenizer import SimpleTokenizer


class ResumeCleaner:

    def __init__(self):
        # Common section headers
        self.section_patterns = {
            "skills": r"(skills|technical skills|core competencies)",
            "experience": r"(experience|work experience|professional experience)",
            "education": r"(education|academic background)"
        }
        self.tokenizer = SimpleTokenizer()

    # -------------------------
    # BASIC CLEANING
    # -------------------------
    def basic_clean(self, text: str) -> str:
        text = text.lower()

        # Remove emails
        text = re.sub(r'\S+@\S+', ' ', text)

        # Remove URLs
        text = re.sub(r'http\S+|www\S+', ' ', text)

        # Remove special characters
        text = re.sub(r'[^a-z0-9\s]', ' ', text)

        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    # -------------------------
    # SECTION SPLITTING
    # -------------------------
    def extract_sections(self, text: str) -> Dict[str, str]:
        sections = {
            "skills": "",
            "experience": "",
            "education": ""
        }

        # Split by lines for better control
        lines = text.split("\n")

        current_section = None

        for line in lines:
            line_lower = line.lower()

            for section, pattern in self.section_patterns.items():
                if re.search(pattern, line_lower):
                    current_section = section
                    break

            if current_section:
                sections[current_section] += line + " "

        return sections

    # -------------------------
    # SKILLS EXTRACTION (Simple)
    # -------------------------
    def extract_skills(self, text: str) -> List[str]:
        # Basic keyword-based extraction using normalized tokens
        skills_db = [
            "python", "java", "c++", "sql", "machine learning",
            "deep learning", "nlp", "react", "node", "aws",
            "docker", "kubernetes"
        ]

        tokens = self.tokenizer.tokenize(text)
        normalized_text = " ".join(tokens)

        found = []
        for skill in skills_db:
            if skill in normalized_text:
                found.append(skill)

        return list(set(found))

    # -------------------------
    # FULL PIPELINE
    # -------------------------
    def process(self, raw_text: str) -> Dict:
        cleaned_text = self.basic_clean(raw_text)

        sections = self.extract_sections(raw_text)

        skills = self.extract_skills(cleaned_text)

        return {
            "cleaned_text": cleaned_text,
            "sections": sections,
            "skills": skills
        }