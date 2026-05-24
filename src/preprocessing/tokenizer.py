import re
from typing import List


class SimpleTokenizer:
    TOKEN_PATTERN = re.compile(r"[a-z0-9\+\-]+")

    @staticmethod
    def tokenize(text: str) -> List[str]:
        if not text:
            return []

        normalized = text.lower().replace("-", " ")
        return SimpleTokenizer.TOKEN_PATTERN.findall(normalized)
