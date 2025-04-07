import os

class Config:
    # Flask Configurations
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking
    JWT_SECRET_KEY = 'jwt-secret-key'  # Secret key for JWT encoding/decoding

    # File upload configurations
    UPLOAD_FOLDER = 'uploads/'  # Folder where files will be uploaded
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit upload size to 16 MB (you can adjust this)

    # Allowed file extensions for uploads
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
    ALLOWED_PHOTO_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

    # If you want to specify max sizes per file type, you can do that as well (optional)
    MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5 MB for photos
    MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50 MB for videos

    # You can also specify other configurations for your app here if needed
    # Example: EMAIL_CONFIG, API_KEYS, etc.



















