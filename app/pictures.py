import magic
import os
from app.config import app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class ImageHandler:
    def __init__(self):
        pass

    def allowed_file(self, file):
        if '.' not in file.filename:
            return False
        
        extension = file.filename.rsplit('.', 1)[1].lower()
        
        if extension not in ALLOWED_EXTENSIONS:
            return False
        
        try:
            file_content = file.read(2048)  
            mime = magic.from_buffer(file_content, mime=True)
            file.seek(0)
            return mime.startswith('image/')
        except Exception as e:
            return extension in ALLOWED_EXTENSIONS

    def handle_image_upload(self, file, custom_filename=None):
        if not file or file.filename == '':
            return None, "No selected file", 400
            
        if not self.allowed_file(file):
            return None, "Invalid file type. Allowed types are: png, jpg, jpeg, gif", 400
            
        try:
            filename = custom_filename if custom_filename else secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f'images/{filename}', None, None
        except Exception as e:
            return None, f"Error saving file: {str(e)}", 500