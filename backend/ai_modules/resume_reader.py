import os
from pdfminer.high_level import extract_text


def read_resume(file_path: str) -> str:
    """
    Extracts text from a PDF resume.
    Safe for local development and cloud deployment (Render).
    """

    # Basic validation
    if not file_path or not os.path.isfile(file_path):
        return ""

    try:
        text = extract_text(file_path)

        if not text:
            return ""

        # Normalize whitespace
        cleaned_text = " ".join(text.split())
        return cleaned_text

    except Exception as e:
        # Render-friendly logging (no crash)
        print(f"[ResumeReader] Failed to parse PDF: {e}")
        return ""
