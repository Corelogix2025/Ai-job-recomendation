from flask import Flask, render_template, request
import os

from ai_modules.resume_reader import read_resume
from ai_modules.skill_extractor import extract_skills
from ai_modules.semantic_matcher import find_best_jobs
from ai_modules.explanation_engine import analyze_resume, generate_explanation

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["resume"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    resume_text = read_resume(path)
    extracted_skills = extract_skills(resume_text)

    # ✅ Resume-based analysis
    overall_score, overall_suggestions = analyze_resume(
        resume_text, extracted_skills
    )

    # ✅ Job matching
    jobs = find_best_jobs(resume_text)

    # Inject resume score + explanation into each job
    for job in jobs:
        job["resume_score"] = overall_score
        job["explanation"] = generate_explanation(job["job_match"])

    return render_template(
        "result.html",
        overall_score=overall_score,
        overall_suggestions=overall_suggestions,
        jobs=jobs[:5]
    )


if __name__ == "__main__":
    app.run(debug=True)
