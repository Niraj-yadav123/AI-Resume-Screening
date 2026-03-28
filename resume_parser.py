"""from PyPDF2 import PdfReader 

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text 
from PyPDF2 import PdfReader
import re

def extract_name(text):
    lines = text.split("\n")

    # assume name is in first few lines
    for line in lines[:5]:
        line = line.strip()

        # simple name pattern
        if re.match(r"^[A-Za-z ]{3,40}$", line):
            return line

    return "Unknown Candidate"

def extract_text_from_pdf(pdf_path):
    text = ""

    try:
        reader = PdfReader(pdf_path)

        for page in reader.pages:
            page_text = page.extract_text()

            # ✅ prevent None problem
            if page_text:
                text += page_text

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

    return text
from PyPDF2 import PdfReader
import re


# ---------------- EXTRACT NAME ----------------
def extract_name(text):
    lines = text.split("\n")

    # assume name is in first few lines
    for line in lines[:5]:
        line = line.strip()

        # simple name pattern
        if re.match(r"^[A-Za-z ]{3,40}$", line):
            return line

    return "Unknown Candidate"


# ---------------- EXTRACT TEXT FROM PDF ----------------

def extract_text_from_pdf(pdf_path):
    text = ""

    try:
        reader = PdfReader(pdf_path)

        for page in reader.pages:
            page_text = page.extract_text()

            # prevent None error
            if page_text:
                text += page_text

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

    return text"""
from PyPDF2 import PdfReader
from docx import Document
import re

# -------- TEXT EXTRACTION --------
def extract_text(file_path):

    text = ""

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text


# -------- NAME EXTRACTION --------
def extract_name(text):

    lines = text.split("\n")

    for line in lines[:6]:
        line = line.strip()
        if re.match(r"^[A-Za-z ]{3,40}$", line):
            return line.title()

    return "Unknown Candidate"


# -------- PHONE EXTRACTION --------
def extract_phone(text):

    pattern = r'(\+91[\-\s]?)?[6-9]\d{9}'
    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"