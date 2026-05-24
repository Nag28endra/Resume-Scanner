import faiss
import numpy as np


class FAISSStore:

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # cosine similarity (with normalized vectors)
        self.metadata = []

    def add(self, embeddings: np.ndarray, data: list):
        """
        embeddings: np.array shape (n, d)
        data: list of metadata (resume info)
        """
        self.index.add(embeddings)
        self.metadata.extend(data)

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            # 🚨 Skip invalid results
            if idx == -1:
                continue

            # 🚨 Skip garbage scores
            if score < 0 or score > 1:
                continue

            results.append({
                "score": float(score),
                "data": self.metadata[idx]
            })

        return results