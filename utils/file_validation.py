from werkzeug.utils import secure_filename  # Ensures safe file naming

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB Limit

def allowed_file(filename):
    """
    First-level check to ensure the file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def valid_mime_type(file):
    """
    Simplified MIME type check based on file extension only.
    """
    ext = file.filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def valid_file_size(file):
    """
    Ensure the file size is under 10MB.
    """
    file.seek(0, 2)  # Move pointer to end
    file_size = file.tell()
    file.seek(0)  # Reset pointer
    return file_size <= MAX_FILE_SIZE

