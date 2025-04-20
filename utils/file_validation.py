from werkzeug.utils import secure_filename  # Ensures safe file naming, It removes dangerous characters (like ../../ or ;) that could be used in attacks.

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB Limit

# First, early check before processing
def allowed_file(filename):
    """
    First-level check to ensure the file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS # Then it splits the name by the last dot and checks if the extension is in your allowed set.

# Redundant safety check in later stages, is a simplified MIME-type check, but still based on the extension. It could be improved using actual MIME inspection.
def valid_mime_type(file):
    """
    Simplified MIME(Multipurpose Internet Mail Extensions) type check based on file extension only.
    """
    ext = file.filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS # It’s a lightweight backup check, though a real MIME check would inspect the file’s content type

def valid_file_size(file):
    """
    Ensure the file size is under 10MB.
    """
    file.seek(0, 2)  # Move pointer to end
    file_size = file.tell() # tell() gets the byte position, i.e., the file size.
    file.seek(0)  # Reset pointer
    return file_size <= MAX_FILE_SIZE

