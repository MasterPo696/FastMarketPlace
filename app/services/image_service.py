import os
from werkzeug.utils import secure_filename
import magic
from app.config import app

class ImageService:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    @staticmethod
    def allowed_file(file):
        """Check if file type is allowed"""
        if '.' not in file.filename:
            return False
        
        extension = file.filename.rsplit('.', 1)[1].lower()
        
        if extension not in ImageService.ALLOWED_EXTENSIONS:
            return False
        
        try:
            file_content = file.read(2048)  
            mime = magic.from_buffer(file_content, mime=True)
            file.seek(0)
            return mime.startswith('image/')
        except Exception:
            return extension in ImageService.ALLOWED_EXTENSIONS

    @staticmethod
    def save_image(file, custom_filename=None):
        """Save image file and return path"""
        if not file or file.filename == '':
            return None, "No selected file", 400
            
        if not ImageService.allowed_file(file):
            return None, "Invalid file type. Allowed types are: png, jpg, jpeg, gif", 400
            
        try:
            filename = custom_filename if custom_filename else secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f'images/{filename}', None, None
        except Exception as e:
            return None, f"Error saving file: {str(e)}", 500 