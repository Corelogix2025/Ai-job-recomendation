from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from db.db_config import get_connection
import pymysql

model = SentenceTransformer("all-MiniLM-L6-v2")


def fetch_jobs():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return jobs


def find_best_jobs(resume_text):
    resume_emb = model.encode(resume_text)
    jobs = fetch_jobs()

    results = []

    for job in jobs:
        job_text = f"{job['title']} {job['skills']}"
        job_emb = model.encode(job_text)

        similarity = cosine_similarity(
            [resume_emb], [job_emb]
        )[0][0]

        job_match = round(similarity * 100, 2)

        results.append({
            "title": job["title"],
            "job_match": job_match,
            "link": job["apply_link"]
        })

    return sorted(results, key=lambda x: x["job_match"], reverse=True)
