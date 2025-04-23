import os
from werkzeug.utils import secure_filename
from PIL import Image

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_photo(filename):
    """
    Check if the filename has a valid image extension.

    Args:
        filename (str): Name of the uploaded file.

    Returns:
        bool: True if valid image extension, else False.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_photo(file, upload_folder):
    """
    Save a photo file to the specified upload folder.

    Args:
        file (FileStorage): The image file to be saved.
        upload_folder (str): Directory to save the file.

    Returns:
        str: Path to the saved image or None if invalid.
    """
    if file and allowed_photo(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    return None

def create_thumbnail(file_path, thumbnail_size=(100, 100)):
    """
    Generate a thumbnail from a saved image file.

    Args:
        file_path (str): Full path of the image.
        thumbnail_size (tuple): Size for the thumbnail (width, height).

    Returns:
        str: Path to the saved thumbnail or None on failure.
    """
    try:
        with Image.open(file_path) as img:
            img.thumbnail(thumbnail_size)
            base, ext = os.path.splitext(file_path)
            thumbnail_path = f"{base}_thumbnail{ext}"
            img.save(thumbnail_path)
            return thumbnail_path
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return None











