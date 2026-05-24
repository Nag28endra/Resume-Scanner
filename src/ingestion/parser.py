import pdfplumber
import docx
import os


class ResumeParser:

    @staticmethod
    def parse_pdf(file_path: str) -> str:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text.strip()

    @staticmethod
    def parse_docx(file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()

    @staticmethod
    def parse_txt(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    @staticmethod
    def parse(file_path: str) -> str:
        ext = os.path.splitext(file_path)[-1].lower()

        if ext == ".pdf":
            return ResumeParser.parse_pdf(file_path)
        elif ext == ".docx":
            return ResumeParser.parse_docx(file_path)
        elif ext == ".txt":
            return ResumeParser.parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")