from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------
# Lazy-load model (IMPORTANT for Render)
# -------------------------------------------------
_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


# ---------------------------------
# Find best matching jobs (Firebase)
# ---------------------------------
def find_best_jobs(resume_text: str, jobs: dict):
    """
    resume_text : extracted resume text
    jobs        : jobs fetched from Firebase (dict)
    """

    if not resume_text or not jobs:
        return []

    model = get_model()
    resume_emb = model.encode(resume_text)

    results = []

    # Firebase returns dict -> iterate values
    for _, job in jobs.items():

        job_text = f"{job['title']} {job['skills']}"
        job_emb = model.encode(job_text)

        similarity = cosine_similarity(
            [resume_emb], [job_emb]
        )[0][0]

        results.append({
            "title": job["title"],
            "job_match": round(similarity * 100, 2),
            "link": job["apply_link"]
        })

    return sorted(results, key=lambda x: x["job_match"], reverse=True)
