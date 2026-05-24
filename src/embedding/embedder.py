from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        """
        texts: List[str] or str
        returns: numpy array embeddings
        """
        if isinstance(texts, str):
            texts = [texts]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True  # IMPORTANT for cosine similarity
        )

        return embeddings