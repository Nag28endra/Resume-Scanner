from typing import List

from ..embedding.embedder import Embedder
from ..embedding.faiss_store import FAISSStore
from ..ingestion.resume_loader import ResumeLoader
from ..preprocessing.cleaner import ResumeCleaner


def build_training_dataset(data_dir: str) -> List[dict]:
    loader = ResumeLoader(data_dir)
    cleaner = ResumeCleaner()

    examples = []
    for item in loader.load_resumes():
        processed = cleaner.process(item["text"])
        examples.append({
            "file_name": item["file_name"],
            "cleaned_text": processed["cleaned_text"],
            "sections": processed["sections"],
            "skills": processed["skills"],
        })

    return examples


def create_semantic_index(resumes: List[dict], model_name: str = "all-MiniLM-L6-v2") -> FAISSStore:
    embedder = Embedder(model_name)
    texts = [resume["cleaned_text"] for resume in resumes]
    embeddings = embedder.encode(texts)
    store = FAISSStore(embeddings.shape[1])
    store.add(embeddings, resumes)
    return store
