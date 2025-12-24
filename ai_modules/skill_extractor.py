import spacy
nlp = spacy.load("en_core_web_sm")

SKILLS = [
    "python","java","sql","machine learning","deep learning",
    "html","css","javascript","react","flask","django",
    "aws","docker","linux","selenium","testing",
    "excel","data analysis","cloud computing"
]

def extract_skills(text):
    text = text.lower()
    return list(set(skill for skill in SKILLS if skill in text))
