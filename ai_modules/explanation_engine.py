import re

def analyze_resume(resume_text, extracted_skills):
    score = 0
    suggestions = []

    word_count = len(resume_text.split())

    # 1️⃣ Resume length (25 points)
    if word_count >= 300:
        score += 25
    elif word_count >= 200:
        score += 18
        suggestions.append("Add more detailed experience or project descriptions.")
    else:
        score += 10
        suggestions.append("Increase resume length with meaningful content.")

    # 2️⃣ Skills count (25 points)
    if len(extracted_skills) >= 10:
        score += 25
    elif len(extracted_skills) >= 6:
        score += 18
        suggestions.append("Add more relevant technical skills.")
    else:
        score += 10
        suggestions.append("Your resume lacks sufficient technical skills.")

    # 3️⃣ Section completeness (30 points)
    sections = ["experience", "education", "projects", "skills"]
    found = 0
    for section in sections:
        if re.search(section, resume_text, re.IGNORECASE):
            found += 1
        else:
            suggestions.append(f"Include a clear '{section.capitalize()}' section.")

    score += (found / len(sections)) * 30

    # 4️⃣ Action verbs (20 points)
    action_verbs = [
        "developed", "designed", "implemented", "built",
        "created", "optimized", "analyzed", "automated"
    ]
    if any(v in resume_text.lower() for v in action_verbs):
        score += 20
    else:
        score += 10
        suggestions.append("Use strong action verbs to describe your work.")

    final_score = round(min(score, 100), 2)

    # Ensure suggestions are never empty
    if not suggestions:
        suggestions.append("Your resume is strong. Consider tailoring it for specific job roles.")

    return final_score, suggestions


def generate_explanation(score):
    if score >= 80:
        return "Strong resume with good alignment."
    elif score >= 60:
        return "Average resume quality. Improvements recommended."
    else:
        return "Weak resume. Significant improvements required."
