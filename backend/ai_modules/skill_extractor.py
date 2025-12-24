import spacy

# -------------------------------------------------
# Lazy load spaCy model (IMPORTANT for deployment)
# -------------------------------------------------
_nlp = None


def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


# ---------------------------------
# Skill vocabulary (expanded & modern)
# ---------------------------------
SKILLS = [
    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript", "typescript",

    # Web Technologies
    "html", "css", "react", "angular", "vue",
    "flask", "django", "node", "express",

    # Data & AI
    "machine learning", "deep learning", "data analysis",
    "data science", "artificial intelligence", "nlp",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "firebase",

    # Cloud & DevOps
    "aws", "azure", "gcp", "cloud computing",
    "docker", "kubernetes", "ci/cd",

    # Testing & QA
    "selenium", "automation testing", "manual testing",

    # Tools & Others
    "linux", "git", "github", "excel", "power bi"
]


# ---------------------------------
# Extract skills from resume text
# ---------------------------------
def extract_skills(text: str):
    """
    Extract predefined technical skills from resume text.
    Returns a list of matched skills.
    """

    if not text:
        return []

    text = text.lower()

    # Load spaCy (future-ready, minimal overhead now)
    get_nlp()

    found_skills = set()

    for skill in SKILLS:
        # Phrase-safe matching
        if f" {skill} " in f" {text} ":
            found_skills.add(skill)

    return sorted(found_skills)
