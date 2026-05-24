import os
from typing import List, Dict
from .parser import ResumeParser


class ResumeLoader:

    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def load_resumes(self) -> List[Dict]:
        resumes = []

        for file in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, file)

            if not os.path.isfile(file_path):
                continue

            try:
                text = ResumeParser.parse(file_path)

                resumes.append({
                    "file_name": file,
                    "text": text
                })

            except Exception as e:
                print(f"Error parsing {file}: {e}")

        return resumes