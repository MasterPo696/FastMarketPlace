import magic
import os
from flask import app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class ImageHandler:
    def __init__(self):
        pass

    def allowed_file(self, filename):
        # Check if the file has an extension and it's in allowed extensions
        if '.' not in filename:
            return False
        
        # Get the actual file extension
        extension = filename.rsplit('.', 1)[1].lower()
        
        # Check if it's in allowed extensions
        if extension not in ALLOWED_EXTENSIONS:
            return False
        
        # Additional MIME type validation
        try:
            mime = magic.from_file(filename, mime=True)
            return mime.startswith('image/')
        except ImportError:
            # Fallback if python-magic is not installed
            return extension in ALLOWED_EXTENSIONS

    def handle_image_upload(self, file):
        if not file or file.filename == '':
            return None, "No selected file", 400
            
        if not self.allowed_file(file.filename):
            return None, "Invalid file type. Allowed types are: png, jpg, jpeg, gif", 400
            
        try:
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f'images/{filename}', None, None
        except Exception as e:
            return None, f"Error saving file: {str(e)}", 500