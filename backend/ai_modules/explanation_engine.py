import re


def analyze_resume(resume_text: str, extracted_skills: list):
    """
    Analyze resume quality and generate score + improvement suggestions
    """

    score = 0
    suggestions = []

    # -----------------------------
    # 1️⃣ Resume Length (25 points)
    # -----------------------------
    word_count = len(resume_text.split())

    if word_count >= 300:
        score += 25
    elif word_count >= 200:
        score += 18
        suggestions.append(
            "Add more detailed descriptions of your experience or projects."
        )
    else:
        score += 10
        suggestions.append(
            "Increase resume length with meaningful experience, projects, or achievements."
        )

    # -----------------------------
    # 2️⃣ Skills Count (25 points)
    # -----------------------------
    skill_count = len(set(extracted_skills))

    if skill_count >= 10:
        score += 25
    elif skill_count >= 6:
        score += 18
        suggestions.append(
            "Add more relevant technical or domain-specific skills."
        )
    else:
        score += 10
        suggestions.append(
            "Your resume lists very few technical skills. Consider adding more."
        )

    # --------------------------------
    # 3️⃣ Section Completeness (30 pts)
    # --------------------------------
    sections = ["experience", "education", "projects", "skills"]
    found_sections = 0

    for section in sections:
        if re.search(rf"\b{section}\b", resume_text, re.IGNORECASE):
            found_sections += 1
        else:
            suggestions.append(
                f"Include a clearly labeled '{section.capitalize()}' section."
            )

    score += (found_sections / len(sections)) * 30

    # -----------------------------
    # 4️⃣ Action Verbs (20 points)
    # -----------------------------
    action_verbs = [
        "developed", "designed", "implemented", "built",
        "created", "optimized", "analyzed", "automated",
        "engineered", "deployed", "maintained"
    ]

    if any(verb in resume_text.lower() for verb in action_verbs):
        score += 20
    else:
        score += 10
        suggestions.append(
            "Use strong action verbs (e.g., developed, implemented, optimized)."
        )

    # -----------------------------
    # Final Score (Cap at 100)
    # -----------------------------
    final_score = round(min(score, 100), 2)

    if not suggestions:
        suggestions.append(
            "Your resume is strong. Consider tailoring it to specific job roles."
        )

    return final_score, suggestions


def generate_explanation(score: float):
    """
    Generate human-readable explanation for resume score
    """

    if score >= 80:
        return "Strong resume with good structure, skills, and clarity."
    elif score >= 60:
        return "Average resume quality. Some improvements are recommended."
    else:
        return "Weak resume. Significant improvements are required."
