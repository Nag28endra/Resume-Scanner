from typing import Dict, List, Optional

from ..embedding.embedder import Embedder
from ..embedding.faiss_store import FAISSStore
from ..scoring.scorer import ResumeScorer


def build_resume_index(resumes: List[Dict], model_name: str = "all-MiniLM-L6-v2") -> FAISSStore:
    embedder = Embedder(model_name)
    embeddings = embedder.encode([resume["cleaned_text"] for resume in resumes])
    store = FAISSStore(embeddings.shape[1])
    store.add(embeddings, resumes)
    return store


def rank_resumes(
    job_description: str,
    resume_index: FAISSStore,
    scorer: Optional[ResumeScorer] = None,
    top_k: int = 5
) -> List[Dict]:
    if scorer is None:
        scorer = ResumeScorer()

    embedder = Embedder()
    query_embedding = embedder.encode(job_description)

    candidates = resume_index.search(query_embedding, top_k=top_k)
    scored = []

    for hit in candidates:
        resume = hit["data"]
        semantic_score = hit["score"]
        result = scorer.compute_score(semantic_score, resume, job_description)
        result["file_name"] = resume.get("file_name")
        result["matched_resume"] = resume
        scored.append(result)

    return scored
