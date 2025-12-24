from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid

from ai_modules.resume_reader import read_resume
from ai_modules.skill_extractor import extract_skills
from ai_modules.semantic_matcher import find_best_jobs
from ai_modules.explanation_engine import analyze_resume, generate_explanation

app = Flask(__name__)
CORS(app)  # ✅ Allow Netlify frontend to call API

# ---------------------------------
# Upload folder (temporary storage)
# ---------------------------------
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------------
# Health check (important for Render)
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

    # Create unique filename (prevents collision)
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # -----------------------------
    # AI processing pipeline
    # -----------------------------
    resume_text = read_resume(file_path)
    extracted_skills = extract_skills(resume_text)

    overall_score, overall_suggestions = analyze_resume(
        resume_text, extracted_skills
    )

    jobs = find_best_jobs(resume_text)

    for job in jobs:
        job["resume_score"] = overall_score
        job["explanation"] = generate_explanation(job["job_match"])

    # -----------------------------
    # Cleanup (Render has no disk persistence)
    # -----------------------------
    try:
        os.remove(file_path)
    except Exception:
        pass

    # -----------------------------
    # JSON response to frontend
    # -----------------------------
    return jsonify({
        "resume_score": overall_score,
        "suggestions": overall_suggestions,
        "skills": extracted_skills,
        "jobs": jobs[:5]
    })


# ---------------------------------
# Entry point for local testing
# ---------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
