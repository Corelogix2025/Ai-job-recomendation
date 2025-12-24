import re


def analyze_resume(resume_text: str, extracted_skills: list):
    """
    Analyze resume quality and generate a score (0–100)
    along with improvement suggestions.
    """

    if not resume_text:
        return 0, ["Resume text could not be extracted properly. Try uploading a clearer PDF."]

    text = resume_text.lower()
    score = 0
    suggestions = set()  # avoid duplicates

    # -----------------------------
    # 1️⃣ Resume Length (25 points)
    # -----------------------------
    word_count = len(text.split())

    if word_count >= 300:
        score += 25
    elif word_count >= 200:
        score += 18
        suggestions.add("Add more detailed descriptions of your experience or projects.")
    else:
        score += 10
        suggestions.add("Increase resume length with meaningful experience, projects, or achievements.")

    # -----------------------------
    # 2️⃣ Skills Count (25 points)
    # -----------------------------
    skill_count = len(set(extracted_skills))

    if skill_count >= 10:
        score += 25
    elif skill_count >= 6:
        score += 18
        suggestions.add("Add more relevant technical or domain-specific skills.")
    else:
        score += 10
        suggestions.add("Your resume lists very few technical skills. Consider adding more.")

    # --------------------------------
    # 3️⃣ Section Completeness (30 pts)
    # --------------------------------
    sections = ["experience", "education", "projects", "skills"]
    found_sections = 0

    for section in sections:
        if re.search(rf"\b{section}\b", text):
            found_sections += 1
        else:
            suggestions.add(f"Include a clearly labeled '{section.capitalize()}' section.")

    score += (found_sections / len(sections)) * 30

    # -----------------------------
    # 4️⃣ Action Verbs (20 points)
    # -----------------------------
    action_verbs = [
        "developed", "designed", "implemented", "built",
        "created", "optimized", "analyzed", "automated",
        "engineered", "deployed", "maintained"
    ]

    if any(verb in text for verb in action_verbs):
        score += 20
    else:
        score += 10
        suggestions.add("Use strong action verbs (e.g., developed, implemented, optimized).")

    # -----------------------------
    # Final Score (Cap at 100)
    # -----------------------------
    final_score = round(min(score, 100), 2)

    if not suggestions:
        suggestions.add("Your resume is strong. Consider tailoring it to specific job roles.")

    return final_score, list(suggestions)


def generate_explanation(score: float):
    """
    Generate a human-readable explanation for job match score.
    """

    if score >= 80:
        return "Excellent match. Your skills and experience strongly align with this role."
    elif score >= 60:
        return "Good match. You meet most requirements, with room for improvement."
    elif score >= 40:
        return "Partial match. Some skills align, but gaps exist."
    else:
        return "Low match. Significant skill or experience gaps for this role."
