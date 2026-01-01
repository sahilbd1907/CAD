from typing import List

from PyPDF2 import PdfReader


def extract_pdf_text(path: str) -> str:
    """Extracts concatenated text from a PDF file path.

    Returns a best-effort plain text string. If pages lack text, they are skipped.
    """
    text_parts: List[str] = []
    reader = PdfReader(path)
    for page in reader.pages:
        try:
            t = page.extract_text() or ""
        except Exception:
            t = ""
        if t:
            text_parts.append(t)
    return "\n\n".join(text_parts)





