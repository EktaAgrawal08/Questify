import re
import fitz  # PyMuPDF
from docx import Document

def sanitize_text(text):
    """Cleans and sanitizes text to remove unwanted characters and excessive whitespace."""
    cleaned_text = re.sub(r'\s+', ' ', text.strip())  # Remove excessive spaces
    cleaned_text = re.sub(r'[^\x20-\x7E\n]', '', cleaned_text)  # Retain newlines for better structure
    return cleaned_text.strip()

def extract_pdf_content(file):
    """Extracts and sanitizes text from a PDF file. Identifies image-only PDFs."""
    text = ''
    has_images = False

    try:
        with fitz.open(stream=file.read(), filetype='pdf') as doc:
            for page in doc:
                page_text = page.get_text() or ''
                if not page_text.strip():
                    has_images = has_images or bool(page.get_images(full=True))  # Improved image detection
                text += page_text.strip() + '\n'

    except Exception as e:
        print(f"⚠️ Error extracting PDF content: {e}")
        return ''
    
    if not text.strip():
        return "IMAGE_ONLY" if has_images else ""
    
    return sanitize_text(text)

def extract_docx_content(file):
    """Extracts and sanitizes text from a DOCX file."""
    try:
        doc = Document(file)
        text = ' '.join(para.text.strip() for para in doc.paragraphs if para.text.strip())
    except Exception as e:
        print(f"⚠️ Error extracting DOCX content: {e}")
        return ''

    return sanitize_text(text)

def extract_txt_content(file):
    """Extracts and sanitizes text from a TXT file with encoding fallback."""
    try:
        text = file.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"⚠️ Error extracting TXT content: {e}")
        return ''

    return sanitize_text(text)
