import magic  # For MIME (media type) detection - Reads actual binary content to detect file type
from werkzeug.utils import secure_filename  # Ensures safe file naming

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'} # Acts as a whitelist to restrict file types and prevent malicious uploads (like .exe, .js, etc.).
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB Limit

# Mapping for stricter extension-MIME consistency
MIME_TYPE_MAP = {
    'pdf': 'application/pdf',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'txt': 'text/plain'
}

def allowed_file(filename): # First-level check to block obviously unsupported files
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def valid_mime_type(file): # Confirms file content matches extension, for security
#     """Verify the uploaded file’s MIME type matches its extension."""
#     mime = magic.Magic(mime=True)  # Create a MIME detector
#     file.seek(0)  # Go to beginning of file
#     detected_mime = mime.from_buffer(file.read(2048))  # Read first 2KB of file to detect MIME type
#     file.seek(0) # Reset pointer back to start

#     # Check both MIME type and file extension
#     ext = file.filename.rsplit('.', 1)[1].lower()
#     return detected_mime == MIME_TYPE_MAP.get(ext)


def valid_mime_type(file):
    mime = magic.Magic(mime=True)
    file.seek(0)
    detected_mime = mime.from_buffer(file.read(2048))
    file.seek(0)

    ext = file.filename.rsplit('.', 1)[1].lower()
    expected_mime = MIME_TYPE_MAP.get(ext)

    # Special handling for docx: allow 'application/zip'
    if ext == 'docx' and detected_mime == 'application/zip':
        return True

    print(f"[DEBUG] {file.filename}: Detected MIME = {detected_mime}, Expected = {expected_mime}")
    return detected_mime == expected_mime

def valid_file_size(file): # Ensures uploaded files are under 10MB
    """Ensure the file size is under 10MB."""
    file.seek(0, 2)  # Move pointer to end
    file_size = file.tell() # Get the current position = file size
    file.seek(0)  # Reset pointer
    return file_size <= MAX_FILE_SIZE

