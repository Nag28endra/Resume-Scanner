from src.ingestion.resume_loader import ResumeLoader
from src.preprocessing.cleaner import ResumeCleaner
from src.embedding.embedder import Embedder
from src.embedding.faiss_store import FAISSStore

# Load & clean
loader = ResumeLoader("data/raw")
cleaner = ResumeCleaner()
embedder = Embedder()

resumes = loader.load_resumes()

processed_resumes = []
texts = []

for r in resumes:
    processed = cleaner.process(r["text"])

    texts.append(processed["cleaned_text"])

    processed_resumes.append({
        "file_name": r["file_name"],
        "skills": processed["skills"]
    })

# Generate embeddings
embeddings = embedder.encode(texts)

# Create FAISS index
store = FAISSStore(dimension=embeddings.shape[1])
store.add(embeddings, processed_resumes)

# Query with Job Description
job_description = """
Looking for a AI engineer with 1.5+ years of experience in Python, GenAI, Pytorch, Machine Learning.
"""

jd_embedding = embedder.encode(job_description)

results = store.search(jd_embedding, top_k=3)

from src.scoring.scorer import ResumeScorer

scorer = ResumeScorer()

results = store.search(jd_embedding, top_k=5)

for r in results:
    score_data = scorer.compute_score(
        semantic_score=r["score"],
        resume_data=r["data"],
        jd_text=job_description
    )

    print("\n======================")
    print("Resume:", r["data"]["file_name"])
    print(score_data)

