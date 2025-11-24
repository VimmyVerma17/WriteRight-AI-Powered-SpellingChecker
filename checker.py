import re
from spellchecker import SpellChecker
from io import BytesIO
from PyPDF2 import PdfReader
import language_tool_python

# Initialize spell checker and language tool
spell = SpellChecker()
tool = language_tool_python.LanguageTool('en-US')


def extract_text_from_pdf_bytes(raw_bytes):
    try:
        reader = PdfReader(BytesIO(raw_bytes))
        pages = [p.extract_text() for p in reader.pages if p.extract_text()]
        return "\n\n".join(pages)
    except Exception:
        return ""


def get_spelling_mistakes(text):
    words = re.findall(r"\b\w+\b", text)
    mistakes = [w for w in words if w.lower() not in spell]
    return list(dict.fromkeys(mistakes))


def correct_text(text):
    if not text.strip():
        return text
    matches = tool.check(text)
    corrected = language_tool_python.utils.correct(text, matches)
    return corrected


def process_text(text):
    spelling_mistakes = get_spelling_mistakes(text)
    corrected_text = correct_text(text)
    grammar_issues = [str(m) for m in tool.check(text)]
    return corrected_text, spelling_mistakes, grammar_issues
