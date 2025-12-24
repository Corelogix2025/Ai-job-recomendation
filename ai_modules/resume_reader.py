from pdfminer.high_level import extract_text

def read_resume(path):
    try:
        return extract_text(path)
    except:
        return ""
