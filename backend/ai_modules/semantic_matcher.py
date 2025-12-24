from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------
# Lazy-load model
# -------------------------------------------------
_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


# ---------------------------------
# Find best matching jobs
# ---------------------------------
def find_best_jobs(resume_text: str, jobs):
    """
    jobs can be:
    - list (Firebase array)
    - dict (Firebase object)
    """

    if not resume_text or not jobs:
        return []

    model = get_model()
    resume_emb = model.encode(resume_text)

    results = []

    # ✅ SAFELY HANDLE BOTH TYPES
    if isinstance(jobs, dict):
        job_iterable = jobs.values()
    elif isinstance(jobs, list):
        job_iterable = jobs
    else:
        return []

    for job in job_iterable:
        if not job:
            continue

        job_text = f"{job.get('title', '')} {job.get('skills', '')}"
        job_emb = model.encode(job_text)

        similarity = cosine_similarity(
            [resume_emb], [job_emb]
        )[0][0]

        results.append({
    "title": job.get("title", "Unknown Role"),
    "job_match": float(round(similarity * 100, 2)),  # 🔥 FIX
    "link": job.get("apply_link", "#")
})
    return sorted(results, key=lambda x: x["job_match"], reverse=True)
