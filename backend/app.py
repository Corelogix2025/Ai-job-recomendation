from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid

# AI modules
from ai_modules.resume_reader import read_resume
from ai_modules.skill_extractor import extract_skills
from ai_modules.semantic_matcher import find_best_jobs
from ai_modules.explanation_engine import analyze_resume, generate_explanation

# Firebase DB
from db.db_config import get_jobs   # 🔥 Firebase integration

app = Flask(__name__)
CORS(app)

# ---------------------------------
# Upload folder (temporary storage)
# ---------------------------------
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------------
# Health check (Render requirement)
# ---------------------------------
@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Backend running successfully"})


# ---------------------------------
# Resume upload & analysis API
# ---------------------------------
@app.route("/analyze", methods=["POST"])
def analyze_resume_api():

    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Unique filename
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        # -----------------------------
        # AI Processing Pipeline
        # -----------------------------
        resume_text = read_resume(file_path)
        extracted_skills = extract_skills(resume_text)

        overall_score, overall_suggestions = analyze_resume(
            resume_text, extracted_skills
        )

        # 🔥 Fetch jobs from Firebase
        firebase_jobs = get_jobs()

        # 🔥 AI Job Matching
        jobs = find_best_jobs(resume_text, firebase_jobs)

        # Add explanations
        for job in jobs:
            job["explanation"] = generate_explanation(job["job_match"])

        # -----------------------------
        # JSON response
        # -----------------------------
        return jsonify({
            "resume_score": overall_score,
            "suggestions": overall_suggestions,
            "skills": extracted_skills,
            "jobs": jobs[:5]
        })

    finally:
        # -----------------------------
        # Cleanup (important for Render)
        # -----------------------------
        try:
            os.remove(file_path)
        except Exception:
            pass


# ---------------------------------
# Entry point
# ---------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
