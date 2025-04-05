import os
import magic  # For MIME type detection
from werkzeug.utils import secure_filename  # Ensures safe file naming

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB Limit

# Mapping for stricter extension-MIME consistency
MIME_TYPE_MAP = {
    'pdf': 'application/pdf',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'txt': 'text/plain'
}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def valid_mime_type(file):
    """Verify the uploaded file’s MIME type matches its extension."""
    mime = magic.Magic(mime=True)
    file.seek(0)
    detected_mime = mime.from_buffer(file.read(2048))
    file.seek(0)

    # Check both MIME type and file extension
    ext = file.filename.rsplit('.', 1)[1].lower()
    return detected_mime == MIME_TYPE_MAP.get(ext)

def valid_file_size(file):
    """Ensure the file size is under 10MB."""
    file.seek(0, 2)  # Move pointer to end
    file_size = file.tell()
    file.seek(0)  # Reset pointer
    return file_size <= MAX_FILE_SIZE

def get_secure_filename(filename):
    """Return a sanitized filename for safer storage."""
    return secure_filename(filename)
