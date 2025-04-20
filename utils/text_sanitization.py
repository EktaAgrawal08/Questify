import re #  To clean up text — for example, removing excessive spaces or filtering out unwanted characters.
import fitz  # PyMuPDF -  We use it to extract text from PDFs and detect images, helping us differentiate between readable and image-only PDFs.

from docx import Document # To extract all paragraph content from .docx documents in a structured way.


def sanitize_text(text):
    """Cleans and sanitizes text to remove unwanted characters and excessive whitespace."""
    cleaned_text = re.sub(r'\s+', ' ', text.strip())  # Replaces multiple spaces, newlines, tabs with a single space. - Ensures the text is compact and easy to process for NLP tasks.
    cleaned_text = re.sub(r'[^\x20-\x7E\n]', '', cleaned_text)  # Retain newlines for better structure - Ensures clean, readable, and model-friendly text input. Removes special/unreadable characters
    return cleaned_text.strip()

def extract_pdf_content(file):
    """Extracts and sanitizes text from a PDF file. Identifies image-only PDFs."""
    text = '' # will hold the extracted string.
    has_images = False #  boolean to track if the document only contains images without text.


    try:
        with fitz.open(stream=file.read(), filetype='pdf') as doc:
            for page in doc: # Loop through each page in the PDF.
                page_text = page.get_text() or '' # Tries to extract text from the page.
                if not page_text.strip(): # If the page has no text, check if it contains images.
                    has_images = has_images or bool(page.get_images(full=True))  # Improved image detection
                text += page_text.strip() + '\n' # Adds cleaned text from each page to the full text variable.

    except Exception as e:
        print(f"⚠️ Error extracting PDF content: {e}")
        return ''
    
    if not text.strip():
        return "IMAGE_ONLY" if has_images else "" # If no text was found, and images were detected → return "IMAGE_ONLY", If no text and no images → return empty string ("")
    
    return sanitize_text(text) # Returns the final sanitized version of the extracted PDF content.



def extract_docx_content(file):
    """Extracts and sanitizes text from a DOCX file."""
    try:
        doc = Document(file) # Loads the DOCX file into a Document object (paragraph-wise structure).

        text = ' '.join(para.text.strip() for para in doc.paragraphs if para.text.strip()) # Loops through each paragraph in the document. Extracts and joins all non-empty paragraphs.

    except Exception as e:
        print(f"⚠️ Error extracting DOCX content: {e}")
        return ''

    return sanitize_text(text) # Final return after cleaning the extracted DOCX text.

def extract_txt_content(file):
    """Extracts and sanitizes text from a TXT file with encoding fallback."""
    try:
        text = file.read().decode('utf-8', errors='ignore') # Reads the file and decodes it from UTF-8, Ignores any problematic characters that can’t be decoded.


    except Exception as e:
        print(f"⚠️ Error extracting TXT content: {e}")
        return ''

    return sanitize_text(text) # Cleans and returns the final sanitized TXT text.


