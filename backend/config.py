import os

class Config:
    """
    Configuration class for the Flask application.
    """

    # Core Flask settings
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT for authentication
    JWT_SECRET_KEY = 'jwt-secret-key'

    # File upload settings
    UPLOAD_FOLDER = 'uploads/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload limit

    # Allowed extensions
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
    ALLOWED_PHOTO_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

    # Individual file size limits
    MAX_PHOTO_SIZE = 5 * 1024 * 1024      # 5 MB
    MAX_VIDEO_SIZE = 50 * 1024 * 1024     # 50 MB





















