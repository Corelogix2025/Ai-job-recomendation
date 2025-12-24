import spacy

# -------------------------------------------------
# Lazy load spaCy model (VERY IMPORTANT for deploy)
# -------------------------------------------------
_nlp = None


def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


# ---------------------------------
# Skill vocabulary
# ---------------------------------
SKILLS = [
    "python", "java", "sql", "machine learning", "deep learning",
    "html", "css", "javascript", "react", "flask", "django",
    "aws", "docker", "linux", "selenium", "testing",
    "excel", "data analysis", "cloud computing"
]


# ---------------------------------
# Extract skills from resume text
# ---------------------------------
def extract_skills(text: str):
    if not text:
        return []

    text = text.lower()

    # Ensure spaCy model is loaded (for future expansion)
    get_nlp()

    found_skills = set()

    for skill in SKILLS:
        if skill in text:
            found_skills.add(skill)

    return list(found_skills)
