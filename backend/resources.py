
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flasgger import swag_from
import os
from functools import wraps

from models import db, User, Product, Nursery, AboutUs, MillingProcess, AggressionProcess, FarmProgression, HowTo, Announcement

# Helper function to check if the current user is admin
def is_admin(fn):
    """Helper to check if current user is admin."""
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return {'message': 'You do not have permission to perform this action'}, 403
        return fn(self, *args, **kwargs)  # Proceed with the original function if user is admin
    return wrapper

# Helper function to check allowed image types
def allowed_photo(filename):
    return filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))

class Register(Resource):
    def post(self):
        """Register the only admin user (if not already exists)."""
        if User.admin_exists():
            return {'error': 'Admin already exists'}, 400

        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not (username and email and password):
            return {'error': 'Missing fields'}, 400

        hashed_pw = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_pw,
            is_admin=True
        )

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'Admin registered successfully'}, 201

class Login(Resource):
    def post(self):
        """Authenticate user and return JWT token."""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return {'error': 'Invalid email or password'}, 401

        access_token = create_access_token(identity=user.id)
        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin
            }
        }, 200

class UserResource(Resource):
    @jwt_required()
    def get(self):
        """Return info about the currently logged-in user."""
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200


class ProductResource(Resource):
    @jwt_required(optional=True)
    def get(self, product_id=None):
        """Guests and Admins can view a specific product or list all products."""
        if product_id:
            # Fetch a specific product by product_id
            product = Product.query.get_or_404(product_id)
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'image_path': product.image_path
            }
            return product_data, 200
        else:
            # Fetch all products
            products = Product.query.all()
            return [
                {
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'image_path': product.image_path
                } for product in products
            ], 200

    @jwt_required()
    def put(self, product_id):
        """Admin-only: Update a product."""
        if not is_admin():
            return {'error': 'Admin access required'}, 403

        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.image_path = data.get('image_path', product.image_path)
        db.session.commit()
        return {'message': 'Product updated'}, 200

    @jwt_required()
    def delete(self, product_id):
        """Admin-only: Delete a product."""
        if not is_admin():
            return {'error': 'Admin access required'}, 403

        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted'}, 200



class NurseryResource(Resource):
    @swag_from({
        'tags': ['Nursery'],
        'summary': 'Create nursery',
        'description': 'Create a new nursery with name, description, and an image.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'name': {'type': 'string'},
                        'description': {'type': 'string'}
                    },
                    'required': ['name', 'description']
                }
            },
            {
                'name': 'image',
                'in': 'formData',
                'type': 'file',
                'required': True,
                'description': 'Nursery image (JPEG, PNG, GIF formats only)'
            }
        ],
        'responses': {
            201: {'description': 'Nursery created successfully'},
            400: {'description': 'Invalid image format'}
        }
    })
    @jwt_required()
    @is_admin
    def post(self):
        """Create a new nursery."""
        data = request.get_json()
        file = request.files.get('image')

        if file and allowed_photo(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)

            new_nursery = Nursery(
                name=data['name'],
                description=data['description'],
                photo_path=file_path
            )

            db.session.add(new_nursery)
            db.session.commit()

            return {'message': 'Nursery created successfully'}, 201
        return {'message': 'Invalid image format'}, 400

    @jwt_required()
    @is_admin
    def put(self, nursery_id):
        """Update an existing nursery."""
        nursery = Nursery.query.get_or_404(nursery_id)
        data = request.get_json()
        nursery.name = data['name']
        nursery.description = data['description']

        file = request.files.get('image')
        if file and allowed_photo(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            nursery.photo_path = file_path

        db.session.commit()
        return {'message': 'Nursery updated successfully'}, 200

    @jwt_required()
    @is_admin
    def delete(self, nursery_id):
        """Delete a nursery."""
        nursery = Nursery.query.get_or_404(nursery_id)
        db.session.delete(nursery)
        db.session.commit()
        return {'message': 'Nursery deleted successfully'}, 200


def is_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        if not user or user.role != 'admin':  # Check if the user is an admin
            return {'message': 'You do not have permission to perform this action'}, 403
        return fn(*args, **kwargs)
    return wrapper

class AboutUsResource(Resource):
    def get(self):
        """View the About Us details (everyone can view)."""
        about_us = AboutUs.query.first()  # Assuming only one record exists
        if about_us:
            return {
                'id': about_us.id,
                'who_we_are': about_us.who_we_are,
                'our_story': about_us.our_story,
                'mission_statement': about_us.mission_statement,
                'vision': about_us.vision,
                'core_values': about_us.core_values,
                'what_we_do': about_us.what_we_do,
                'why_choose_us': about_us.why_choose_us
            }, 200
        return {'message': 'About Us not found'}, 404

    @jwt_required()
    @is_admin
    def post(self):
        """Admin-only: Create a new About Us entry."""
        data = request.get_json()

        new_about_us = AboutUs(
            who_we_are=data.get('who_we_are'),
            our_story=data.get('our_story'),
            mission_statement=data.get('mission_statement'),
            vision=data.get('vision'),
            core_values=data.get('core_values'),
            what_we_do=data.get('what_we_do'),
            why_choose_us=data.get('why_choose_us')
        )

        db.session.add(new_about_us)
        db.session.commit()

        return {'message': 'About Us details created successfully'}, 201

    @jwt_required()
    @is_admin
    def put(self):
        """Admin-only: Update the About Us details."""
        data = request.get_json()

        about_us = AboutUs.query.first()  # Assuming there's only one entry
        if not about_us:
            return {'message': 'About Us entry not found'}, 404

        about_us.who_we_are = data.get('who_we_are', about_us.who_we_are)
        about_us.our_story = data.get('our_story', about_us.our_story)
        about_us.mission_statement = data.get('mission_statement', about_us.mission_statement)
        about_us.vision = data.get('vision', about_us.vision)
        about_us.core_values = data.get('core_values', about_us.core_values)
        about_us.what_we_do = data.get('what_we_do', about_us.what_we_do)
        about_us.why_choose_us = data.get('why_choose_us', about_us.why_choose_us)

        db.session.commit()

        return {'message': 'About Us details updated successfully'}, 200

    @jwt_required()
    @is_admin
    def delete(self):
        """Admin-only: Delete the About Us entry."""
        about_us = AboutUs.query.first()
        if not about_us:
            return {'message': 'About Us entry not found'}, 404

        db.session.delete(about_us)
        db.session.commit()

        return {'message': 'About Us entry deleted successfully'}, 200
    
class MillingProcessResource(Resource):
    @jwt_required(optional=True)
    def get(self):
        """View milling processes."""
        milling_processes = MillingProcess.query.all()
        result = [
            {
                'id': process.id,
                'name': process.name,
                'description': process.description,
                'video_link': process.video_link
            } for process in milling_processes
        ]
        return result, 200

    @jwt_required()
    @is_admin
    def post(self):
        """Admin-only: Add a new milling process."""
        data = request.get_json()

        new_process = MillingProcess(
            name=data['name'],
            description=data.get('description', ''),
            video_link=data.get('video_link')
        )

        db.session.add(new_process)
        db.session.commit()

        return {'message': 'Milling process added successfully'}, 201

    @jwt_required()
    @is_admin
    def put(self, process_id):
        """Admin-only: Update an existing milling process."""
        data = request.get_json()

        milling_process = MillingProcess.query.get_or_404(process_id)
        milling_process.name = data.get('name', milling_process.name)
        milling_process.description = data.get('description', milling_process.description)
        milling_process.video_link = data.get('video_link', milling_process.video_link)

        db.session.commit()
        return {'message': 'Milling process updated successfully'}, 200

    @jwt_required()
    @is_admin
    def delete(self, process_id):
        """Admin-only: Delete a milling process."""
        milling_process = MillingProcess.query.get_or_404(process_id)
        db.session.delete(milling_process)
        db.session.commit()

        return {'message': 'Milling process deleted successfully'}, 200

class AggressionProcessResource(Resource):
    @jwt_required(optional=True)
    def get(self):
        """View aggression processes."""
        aggression_processes = AggressionProcess.query.all()
        result = [
            {
                'id': process.id,
                'name': process.name,
                'description': process.description,
                'video_link': process.video_link
            } for process in aggression_processes
        ]
        return result, 200

    @jwt_required()
    @is_admin
    def post(self):
        """Admin-only: Add a new aggression process."""
        data = request.get_json()

        new_process = AggressionProcess(
            name=data['name'],
            description=data.get('description', ''),
            video_link=data.get('video_link')
        )

        db.session.add(new_process)
        db.session.commit()

        return {'message': 'Aggression process added successfully'}, 201

    @jwt_required()
    @is_admin
    def put(self, process_id):
        """Admin-only: Update an existing aggression process."""
        data = request.get_json()

        aggression_process = AggressionProcess.query.get_or_404(process_id)
        aggression_process.name = data.get('name', aggression_process.name)
        aggression_process.description = data.get('description', aggression_process.description)
        aggression_process.video_link = data.get('video_link', aggression_process.video_link)

        db.session.commit()
        return {'message': 'Aggression process updated successfully'}, 200

    @jwt_required()
    @is_admin
    def delete(self, process_id):
        """Admin-only: Delete an aggression process."""
        aggression_process = AggressionProcess.query.get_or_404(process_id)
        db.session.delete(aggression_process)
        db.session.commit()

        return {'message': 'Aggression process deleted successfully'}, 200


class FarmProgressionResource(Resource):
    @jwt_required(optional=True)
    def get(self):
        """View farm progressions."""
        farm_progressions = FarmProgression.query.all()
        result = [
            {
                'id': progression.id,
                'name': progression.name,
                'description': progression.description,
                'video_link': progression.video_link
            } for progression in farm_progressions
        ]
        return result, 200

    @jwt_required()
    @is_admin
    def post(self):
        """Admin-only: Add a new farm progression."""
        data = request.get_json()

        new_progression = FarmProgression(
            name=data['name'],
            description=data.get('description', ''),
            video_link=data.get('video_link')
        )

        db.session.add(new_progression)
        db.session.commit()

        return {'message': 'Farm progression added successfully'}, 201

    @jwt_required()
    @is_admin
    def put(self, progression_id):
        """Admin-only: Update an existing farm progression."""
        data = request.get_json()

        farm_progression = FarmProgression.query.get_or_404(progression_id)
        farm_progression.name = data.get('name', farm_progression.name)
        farm_progression.description = data.get('description', farm_progression.description)
        farm_progression.video_link = data.get('video_link', farm_progression.video_link)

        db.session.commit()
        return {'message': 'Farm progression updated successfully'}, 200

    @jwt_required()
    @is_admin
    def delete(self, progression_id):
        """Admin-only: Delete a farm progression."""
        farm_progression = FarmProgression.query.get_or_404(progression_id)
        db.session.delete(farm_progression)
        db.session.commit()

        return {'message': 'Farm progression deleted successfully'}, 200


class HowToResource(Resource):
    @jwt_required(optional=True)
    def get(self):
        """View How To guides."""
        how_to_guides = HowTo.query.all()
        result = [
            {
                'id': guide.id,
                'title': guide.title,
                'content': guide.content
            } for guide in how_to_guides
        ]
        return result, 200

    @jwt_required()
    @is_admin
    def post(self):
        """Admin-only: Add a new How To guide."""
        data = request.get_json()

        new_guide = HowTo(
            title=data['title'],
            content=data['content']
        )

        db.session.add(new_guide)
        db.session.commit()

        return {'message': 'How To guide added successfully'}, 201

    @jwt_required()
    @is_admin
    def put(self, guide_id):
        """Admin-only: Update an existing How To guide."""
        data = request.get_json()

        how_to_guide = HowTo.query.get_or_404(guide_id)
        how_to_guide.title = data.get('title', how_to_guide.title)
        how_to_guide.content = data.get('content', how_to_guide.content)

        db.session.commit()
        return {'message': 'How To guide updated successfully'}, 200

    @jwt_required()
    @is_admin
    def delete(self, guide_id):
        """Admin-only: Delete a How To guide."""
        how_to_guide = HowTo.query.get_or_404(guide_id)
        db.session.delete(how_to_guide)
        db.session.commit()

        return {'message': 'How To guide deleted successfully'}, 200


class AnnouncementResource(Resource):
    @jwt_required(optional=True)
    def get(self):
        """View announcements."""
        announcements = Announcement.query.all()
        result = [
            {
                'id': announcement.id,
                'title': announcement.title,
                'content': announcement.content
            } for announcement in announcements
        ]
        return result, 200

    @jwt_required()
    @is_admin
    def post(self):
        """Admin-only: Add a new announcement."""
        data = request.get_json()

        new_announcement = Announcement(
            title=data['title'],
            content=data['content']
        )

        db.session.add(new_announcement)
        db.session.commit()

        return {'message': 'Announcement added successfully'}, 201

    @jwt_required()
    @is_admin
    def put(self, announcement_id):
        """Admin-only: Update an existing announcement."""
        data = request.get_json()

        announcement = Announcement.query.get_or_404(announcement_id)
        announcement.title = data.get('title', announcement.title)
        announcement.content = data.get('content', announcement.content)

        db.session.commit()
        return {'message': 'Announcement updated successfully'}, 200

    @jwt_required()
    @is_admin
    def delete(self, announcement_id):
        """Admin-only: Delete an announcement."""
        announcement = Announcement.query.get_or_404(announcement_id)
        db.session.delete(announcement)
        db.session.commit()

        return {'message': 'Announcement deleted successfully'}, 200
