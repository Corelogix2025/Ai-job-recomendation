from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from db.db_config import get_connection
import pymysql

# -------------------------------------------------
# Lazy-load model (IMPORTANT for Render / deployment)
# -------------------------------------------------
_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


# ---------------------------------
# Fetch jobs from database
# ---------------------------------
def fetch_jobs():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT title, skills, apply_link FROM jobs")
    jobs = cursor.fetchall()

    cursor.close()
    conn.close()
    return jobs


# ---------------------------------
# Find best matching jobs
# ---------------------------------
def find_best_jobs(resume_text: str):
    if not resume_text:
        return []

    model = get_model()
    resume_emb = model.encode(resume_text)

    jobs = fetch_jobs()
    results = []

    for job in jobs:
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
