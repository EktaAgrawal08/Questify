import os # File and path handling, Helps in working with .env files, temp files, and file paths
import fitz  # PyMuPDF, Extracts text from PDFs and detects if PDFs are image-only

# Imports Flask and essential utilities - Enables routing (Flask), rendering HTML (render_template), handling form submissions (request), downloading files (send_file), and error handling (abort, jsonify).
from flask import Flask, render_template, request, send_file, abort, jsonify
from fpdf import FPDF # Generates PDF files from text, Converts generated MCQs and answers into downloadable PDFs
import google.generativeai as genai
from dotenv import load_dotenv
import re
import tempfile # Used for safely storing user uploads and generated PDFs without permanent storage.


# Import functions from our dedicated files
from utils.file_validation import allowed_file, valid_mime_type, valid_file_size
from utils.text_sanitization import sanitize_text, extract_pdf_content, extract_docx_content, extract_txt_content

# Loads the .env file containing the API key for Google AI services.
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Load API Key
api_key = os.getenv("GOOGLE_API_KEY")


# Configure Google AI API
genai.configure(api_key=api_key)

# Error Handling for API Configuration
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API key is missing or invalid! Please check your .env file or environment variables.")
    
    genai.configure(api_key=api_key)
    
    available_models = [m.name for m in genai.list_models()]
    model_name = "models/gemini-1.5-pro-latest"
    
    if model_name not in available_models:
        raise ValueError(f"Model '{model_name}' is unavailable. Check your Google Gemini API setup.")
    
    # Initializes the Gemini model for content generation.
    model = genai.GenerativeModel(model_name)
except ValueError as ve:
    print(f"[ERROR] {ve}")
    exit(1)
except Exception as e:
    print(f"[ERROR] Unexpected error during model configuration: {e}")
    exit(1)


# Flask App Initialization
app = Flask(__name__, template_folder="templates")

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Text Extraction from Uploaded Files
def extract_text(filepath):
    ext = filepath.rsplit('.', 1)[1].lower()

    with open(filepath, 'rb') as file:
        if ext == "pdf":
            text = extract_pdf_content(file)
        elif ext == "docx":
            text = extract_docx_content(file)
        elif ext == "txt":
            text = extract_txt_content(file)
        else:
            text = ""

    return text or ""

# MCQ Generation
def generate_mcqs(text, num_questions):
    if not text.strip():
        return [], []

    prompt = f"Generate {num_questions} multiple-choice questions from the following text. Format each question as:\n\n\
              'Q1) Question\nA) Option1\nB) Option2\nC) Option3\nD) Option4\nCorrect Answer: Option'\n\n{text}"

    try:
        # Calls the model and extracts text from response.
        response = model.generate_content(prompt)
        mcq_text = response.text if hasattr(response, 'text') else ""

        if not mcq_text.strip(): # for empty responses
            return [], []

        # Validates that content is not empty, Cleans and formats each MCQ, adds numbering if missing.
        mcqs = []
        for i, q in enumerate(mcq_text.split("\n\n")):
            if re.match(r'^Q\d+\)', q.strip()):  # Already numbered
                mcqs.append(q.strip())
            else:
                mcqs.append(f"Q{i+1}) {q.strip().replace('**', '')}")

        # Extracts the correct answers for each MCQ.
        answers = [q.split("Correct Answer:")[1].strip() for q in mcqs if "Correct Answer:" in q]
        return mcqs, answers
    except Exception as e:
        return [f"⚠️ Error generating MCQs: {e}"], []


# PDF Creation (MCQs and Answers)
def save_as_pdf(content_list, filename):
    pdf = FPDF() # Initializes a new PDF document
    pdf.set_auto_page_break(auto=True, margin=15) # Automatically adds new page if content overflows
    pdf.add_page() # Adds the first page
    pdf.set_font("Arial", size=12)

    for item in content_list:
        pdf.multi_cell(0, 10, item.encode('latin-1', 'ignore').decode('latin-1'))
        pdf.ln(5)  # Adds spacing after each item

    # Use temp directory instead of UPLOADED_FILES_FOLDER
    temp_dir = tempfile.gettempdir()  # Gets system’s temporary directory
    filepath = os.path.join(temp_dir, filename) # Full path where PDF will be saved
    pdf.output(filepath, "F") # Saves the PDF to the temporary path
    return filepath  # Return full path instead of filename


# Flask Routes
@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/upload')
def upload_page():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    # Checks if files are uploaded
    if 'files' not in request.files:
        return render_template('results.html', mcqs=[], error_msg="⚠️ No files uploaded.", image_files=[])

    # Gets uploaded files and number of MCQs to generate.
    files = request.files.getlist('files')
    num_questions = int(request.form.get('num_questions', 5)) # Gets all uploaded files and number of MCQs (defaults to 5 if not given).

    extracted_texts = [] # To store valid extracted texts
    image_only_files = []  # Track image-only PDFs
    temp_files = []  # Keep track of temporary paths

    try:
        for file in files:
            if file and allowed_file(file.filename):  # Check file extension
                if not valid_file_size(file):  # Check file size
                    return render_template('results.html', mcqs=[], error_msg="⚠️ File size exceeds 10MB limit.", image_files=[])

                if not valid_mime_type(file):
                    return render_template('results.html', mcqs=[], error_msg="⚠️ Invalid file type. Only PDF, DOCX, and TXT files are allowed.", image_files=[])

                # Temporary File Creation
                temp = tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.rsplit('.', 1)[1].lower()}")
                temp.write(file.read())
                temp.close()
                temp_files.append(temp.name)

                text = extract_text(temp.name)
                if text == "IMAGE_ONLY":
                    image_only_files.append(file.filename)
                else:
                    extracted_texts.append(text)

        if image_only_files:
            return render_template('results.html', mcqs=[], error_msg="⚠️ Image-only documents are not supported.", image_files=image_only_files)

        if not extracted_texts:
            return render_template('results.html', mcqs=[], error_msg="⚠️ No valid text found in uploaded documents.", image_files=[])

        # Combines all text and uses Gemini model to create MCQs and answers.
        full_text = "\n".join(extracted_texts)
        mcqs, answers = generate_mcqs(full_text, num_questions)

        # Save MCQs and Answers as Temporary PDFs
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as mcq_pdf:
            save_as_pdf(mcqs, mcq_pdf.name)
            mcq_pdf_path = mcq_pdf.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as ans_pdf:
            save_as_pdf(answers, ans_pdf.name)
            ans_pdf_path = ans_pdf.name

        # Shows generated MCQs and provides links to download PDFs.
        return render_template(
            'results.html',
            mcqs=mcqs,
            pdf_path=os.path.basename(mcq_pdf_path),
            answers_pdf_path=os.path.basename(ans_pdf_path)
        )

    except Exception as e:
        return render_template('results.html', mcqs=[], error_msg=f"⚠️ Error generating content: {e}", image_files=[])
    
    finally:
        # Delete all temp input files
        for temp_path in temp_files:
            if os.path.exists(temp_path):
                os.remove(temp_path)


@app.route('/download/<filename>')
def download_file(filename):
    # Looks for the file in the system's temporary directory.
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    if not os.path.exists(file_path):
        abort(404)

    response = send_file(file_path, as_attachment=True)

    # Delete the file after sending
    @response.call_on_close
    def cleanup():
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"⚠️ Failed to delete {file_path}: {e}")

    return response

@app.errorhandler(400)
def bad_request_error(e):
    return jsonify({"error": "Bad Request", "message": str(e)}), 400

@app.errorhandler(404)
def not_found_error(e):
    return jsonify({"error": "Not Found", "message": "Requested resource not found."}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal Server Error", "message": "Something went wrong on our end."}), 500


# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
