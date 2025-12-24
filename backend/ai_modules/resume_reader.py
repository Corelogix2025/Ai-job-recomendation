import os
from pdfminer.high_level import extract_text


def read_resume(file_path: str) -> str:
    """
    Reads and extracts text from a PDF resume file.
    Works correctly in local + deployed environments.
    """

    if not file_path or not os.path.exists(file_path):
        return ""

    try:
        text = extract_text(file_path)
        return text.strip() if text else ""
    except Exception as e:
        # Optional: log error in production
        print(f"Resume parsing error: {e}")
        return ""
