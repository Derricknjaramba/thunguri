import os

class Config:
    """
    Configuration class for the Flask application.
    """

    # Core Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # Fetch from environment variable
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')  # Use environment variable for production database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT for authentication
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')  # Fetch from environment variable

    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # This might not be needed now if you're not uploading files
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload limit (still useful for other file uploads)

    # Allowed extensions (for photos, if any)
    ALLOWED_PHOTO_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

    # Individual file size limits (for photos, if needed)
    MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5 MB for photo uploads (optional)

    # You can add more settings related to external services for video URLs (like YouTube, Vimeo API keys, etc.)






















