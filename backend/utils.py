import os
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from models import User
from flask import jsonify, g, abort

# Admin access required decorator
def admin_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        # Get the current user's ID from the JWT identity
        current_user_id = get_jwt_identity()

        # If the current_user_id is None, the JWT identity is invalid or expired
        if current_user_id is None:
            return jsonify({
                'status': 'error',
                'message': 'User not found in JWT identity'
            }), 401

        # Query the User model using the user ID
        user = User.query.get(current_user_id)

        # If the user does not exist in the database, return 404
        if user is None:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        # Check if the user has admin privileges
        if not user.is_admin:
            return jsonify({
                'status': 'error',
                'message': 'Admin access required'
            }), 403

        # Store the user object in `g` for later use in other parts of the application (optional)
        g.current_user = user

        # Proceed to the wrapped view function
        return fn(*args, **kwargs)
    
    return decorated_view


# File type validation functions
ALLOWED_PHOTO_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mkv', 'avi'}

def allowed_photo(filename):
    """
    Check if the file is a valid photo type based on the file extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PHOTO_EXTENSIONS

def allowed_video(filename):
    """
    Check if the file is a valid video type based on the file extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS







