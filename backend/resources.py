import os
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import db, Product, Nursery, AboutUs, MillingProcess, AggressionProcess, FarmProgression, HowTo, Announcement, User
from flask import request
from werkzeug.utils import secure_filename
from utils import allowed_photo, allowed_video


# Admin Resources for User Management
class UserResource(Resource):
    @jwt_required()
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return {'id': user.id, 'username': user.username, 'email': user.email, 'is_admin': user.is_admin}, 200
        users = User.query.all()
        return [{'id': user.id, 'username': user.username, 'email': user.email, 'is_admin': user.is_admin} for user in users], 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],  # Ideally, you should hash the password before saving
            is_admin=data.get('is_admin', False)
        )
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created'}, 201

    @jwt_required()
    def put(self, user_id):
        data = request.get_json()
        user = User.query.get_or_404(user_id)

        user.username = data['username']
        user.email = data['email']
        user.is_admin = data.get('is_admin', user.is_admin)
        db.session.commit()
        return {'message': 'User updated'}, 200

    @jwt_required()
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 200


# Admin Resources for Product
class AdminProductResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        file = request.files.get('image')

        if file and allowed_photo(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)

            new_product = Product(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                image_path=file_path
            )
            db.session.add(new_product)
            db.session.commit()

            return {'message': 'Product added with image'}, 201
        return {'message': 'Invalid image format'}, 400

    @jwt_required()
    def put(self, product_id):
        data = request.get_json()
        product = Product.query.get_or_404(product_id)
        file = request.files.get('image')

        if file and allowed_photo(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            product.image_path = file_path

        product.name = data['name']
        product.description = data['description']
        product.price = data['price']
        db.session.commit()

        return {'message': 'Product updated'}, 200

    @jwt_required()
    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        if product.image_path:
            os.remove(product.image_path)  # Delete image file
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted'}, 200


# Guest Resources for Product
class GuestProductResource(Resource):
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get_or_404(product_id)
            return {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'image_path': product.image_path}, 200
        products = Product.query.all()
        return [{'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'image_path': product.image_path} for product in products], 200


# Admin Resources for Nursery
class AdminNurseryResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        file = request.files.get('photo')

        if file and allowed_photo(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)

            new_nursery = Nursery(
                name=data['name'],
                location=data['location'],
                description=data['description'],
                photo_path=file_path
            )
            db.session.add(new_nursery)
            db.session.commit()

            return {'message': 'Nursery added with photo'}, 201
        return {'message': 'Invalid image format'}, 400

    @jwt_required()
    def put(self, nursery_id):
        data = request.get_json()
        nursery = Nursery.query.get_or_404(nursery_id)
        file = request.files.get('photo')

        if file and allowed_photo(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            nursery.photo_path = file_path

        nursery.name = data['name']
        nursery.location = data['location']
        nursery.description = data['description']
        db.session.commit()

        return {'message': 'Nursery updated'}, 200

    @jwt_required()
    def delete(self, nursery_id):
        nursery = Nursery.query.get_or_404(nursery_id)
        if nursery.photo_path:
            os.remove(nursery.photo_path)  # Delete photo file
        db.session.delete(nursery)
        db.session.commit()
        return {'message': 'Nursery deleted'}, 200


# Guest Resources for Nursery
class GuestNurseryResource(Resource):
    def get(self, nursery_id=None):
        if nursery_id:
            nursery = Nursery.query.get_or_404(nursery_id)
            return {'id': nursery.id, 'name': nursery.name, 'location': nursery.location, 'description': nursery.description, 'photo_path': nursery.photo_path}, 200
        nurseries = Nursery.query.all()
        return [{'id': nursery.id, 'name': nursery.name, 'location': nursery.location, 'description': nursery.description, 'photo_path': nursery.photo_path} for nursery in nurseries], 200


# Admin Resources for About Us
class AdminAboutUsResource(Resource):
    @jwt_required()
    def put(self):
        # Fetch the incoming JSON data
        data = request.get_json()

        # Try to get the first AboutUs entry
        about_us = AboutUs.query.first()

        # If no entry exists, create a new one
        if not about_us:
            about_us = AboutUs()

        # Update the attributes of the AboutUs entry
        about_us.who_we_are = data.get('who_we_are', about_us.who_we_are)
        about_us.our_story = data.get('our_story', about_us.our_story)
        about_us.mission_statement = data.get('mission_statement', about_us.mission_statement)
        about_us.vision = data.get('vision', about_us.vision)
        about_us.core_values = data.get('core_values', about_us.core_values)
        about_us.what_we_do = data.get('what_we_do', about_us.what_we_do)
        about_us.why_choose_us = data.get('why_choose_us', about_us.why_choose_us)

        # Commit the changes to the database
        db.session.add(about_us)
        db.session.commit()

        # Return a success message
        return {'message': 'About Us updated successfully'}, 200


# Guest Resources for About Us
class GuestAboutUsResource(Resource):
    def get(self):
        # Try to get the first AboutUs entry
        about_us = AboutUs.query.first()

        # If no AboutUs entry exists, return a 404 response
        if not about_us:
            return {'message': 'About Us information not found'}, 404
        
        # If the entry exists, return the information
        return {
            'who_we_are': about_us.who_we_are,
            'our_story': about_us.our_story,
            'mission_statement': about_us.mission_statement,
            'vision': about_us.vision,
            'core_values': about_us.core_values,
            'what_we_do': about_us.what_we_do,
            'why_choose_us': about_us.why_choose_us
        }, 200


# Admin Resources for Milling Process
class AdminMillingProcessResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        file = request.files.get('video')

        if file and allowed_video(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)

            new_milling_process = MillingProcess(
                name=data['name'],
                description=data['description'],
                video_path=file_path
            )
            db.session.add(new_milling_process)
            db.session.commit()

            return {'message': 'Milling Process added with video'}, 201
        return {'message': 'Invalid video format'}, 400

    @jwt_required()
    def put(self, milling_process_id):
        data = request.get_json()
        milling_process = MillingProcess.query.get_or_404(milling_process_id)
        file = request.files.get('video')

        if file and allowed_video(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            milling_process.video_path = file_path

        milling_process.name = data['name']
        milling_process.description = data['description']
        db.session.commit()

        return {'message': 'Milling Process updated'}, 200

    @jwt_required()
    def delete(self, milling_process_id):
        milling_process = MillingProcess.query.get_or_404(milling_process_id)
        if milling_process.video_path:
            os.remove(milling_process.video_path)  # Delete video file
        db.session.delete(milling_process)
        db.session.commit()
        return {'message': 'Milling Process deleted'}, 200


# Guest Resources for Milling Process
class GuestMillingProcessResource(Resource):
    def get(self, milling_process_id=None):
        if milling_process_id:
            milling_process = MillingProcess.query.get_or_404(milling_process_id)
            return {'id': milling_process.id, 'name': milling_process.name, 'description': milling_process.description, 'video_path': milling_process.video_path}, 200
        milling_processes = MillingProcess.query.all()
        return [{'id': milling_process.id, 'name': milling_process.name, 'description': milling_process.description, 'video_path': milling_process.video_path} for milling_process in milling_processes], 200


# Admin Resources for Aggression Process
class AdminAggressionProcessResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        file = request.files.get('video')

        if file and allowed_video(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)

            new_aggression_process = AggressionProcess(
                name=data['name'],
                description=data['description'],
                video_path=file_path
            )
            db.session.add(new_aggression_process)
            db.session.commit()

            return {'message': 'Aggression Process added with video'}, 201
        return {'message': 'Invalid video format'}, 400

    @jwt_required()
    def put(self, aggression_process_id):
        data = request.get_json()
        aggression_process = AggressionProcess.query.get_or_404(aggression_process_id)
        file = request.files.get('video')

        if file and allowed_video(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            aggression_process.video_path = file_path

        aggression_process.name = data['name']
        aggression_process.description = data['description']
        db.session.commit()

        return {'message': 'Aggression Process updated'}, 200

    @jwt_required()
    def delete(self, aggression_process_id):
        aggression_process = AggressionProcess.query.get_or_404(aggression_process_id)
        if aggression_process.video_path:
            os.remove(aggression_process.video_path)  # Delete video file
        db.session.delete(aggression_process)
        db.session.commit()
        return {'message': 'Aggression Process deleted'}, 200


# Guest Resources for Aggression Process
class GuestAggressionProcessResource(Resource):
    def get(self, aggression_process_id=None):
        if aggression_process_id:
            aggression_process = AggressionProcess.query.get_or_404(aggression_process_id)
            return {'id': aggression_process.id, 'name': aggression_process.name, 'description': aggression_process.description, 'video_path': aggression_process.video_path}, 200
        aggression_processes = AggressionProcess.query.all()
        return [{'id': aggression_process.id, 'name': aggression_process.name, 'description': aggression_process.description, 'video_path': aggression_process.video_path} for aggression_process in aggression_processes], 200


# Admin Resources for Farm Progression
class AdminFarmProgressionResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        file = request.files.get('photo')

        if file and allowed_photo(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)

            new_farm_progression = FarmProgression(
                name=data['name'],
                description=data['description'],
                photo_path=file_path
            )
            db.session.add(new_farm_progression)
            db.session.commit()

            return {'message': 'Farm Progression added with photo'}, 201
        return {'message': 'Invalid photo format'}, 400

    @jwt_required()
    def put(self, farm_progression_id):
        data = request.get_json()
        farm_progression = FarmProgression.query.get_or_404(farm_progression_id)
        file = request.files.get('photo')

        if file and allowed_photo(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            file.save(file_path)
            farm_progression.photo_path = file_path

        farm_progression.name = data['name']
        farm_progression.description = data['description']
        db.session.commit()

        return {'message': 'Farm Progression updated'}, 200

    @jwt_required()
    def delete(self, farm_progression_id):
        farm_progression = FarmProgression.query.get_or_404(farm_progression_id)
        if farm_progression.photo_path:
            os.remove(farm_progression.photo_path)  # Delete photo file
        db.session.delete(farm_progression)
        db.session.commit()
        return {'message': 'Farm Progression deleted'}, 200


# Guest Resources for Farm Progression
class GuestFarmProgressionResource(Resource):
    def get(self, farm_progression_id=None):
        if farm_progression_id:
            farm_progression = FarmProgression.query.get_or_404(farm_progression_id)
            return {'id': farm_progression.id, 'name': farm_progression.name, 'description': farm_progression.description, 'photo_path': farm_progression.photo_path}, 200
        farm_progressions = FarmProgression.query.all()
        return [{'id': farm_progression.id, 'name': farm_progression.name, 'description': farm_progression.description, 'photo_path': farm_progression.photo_path} for farm_progression in farm_progressions], 200


# Admin Resources for How To
class AdminHowToResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        new_how_to = HowTo(
            title=data['title'],
            description=data['description']
        )
        db.session.add(new_how_to)
        db.session.commit()

        return {'message': 'How To added'}, 201

    @jwt_required()
    def put(self, how_to_id):
        data = request.get_json()
        how_to = HowTo.query.get_or_404(how_to_id)

        how_to.title = data['title']
        how_to.description = data['description']
        db.session.commit()

        return {'message': 'How To updated'}, 200

    @jwt_required()
    def delete(self, how_to_id):
        how_to = HowTo.query.get_or_404(how_to_id)
        db.session.delete(how_to)
        db.session.commit()
        return {'message': 'How To deleted'}, 200


# Guest Resources for How To
class GuestHowToResource(Resource):
    def get(self, how_to_id=None):
        if how_to_id:
            how_to = HowTo.query.get_or_404(how_to_id)
            return {'id': how_to.id, 'title': how_to.title, 'description': how_to.description}, 200
        how_to_list = HowTo.query.all()
        return [{'id': how_to.id, 'title': how_to.title, 'description': how_to.description} for how_to in how_to_list], 200


# Admin Resources for Announcements
class AdminAnnouncementResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        new_announcement = Announcement(
            title=data['title'],
            content=data['content']
        )
        db.session.add(new_announcement)
        db.session.commit()

        return {'message': 'Announcement added'}, 201

    @jwt_required()
    def put(self, announcement_id):
        data = request.get_json()
        announcement = Announcement.query.get_or_404(announcement_id)

        announcement.title = data['title']
        announcement.content = data['content']
        db.session.commit()

        return {'message': 'Announcement updated'}, 200

    @jwt_required()
    def delete(self, announcement_id):
        announcement = Announcement.query.get_or_404(announcement_id)
        db.session.delete(announcement)
        db.session.commit()
        return {'message': 'Announcement deleted'}, 200


# Guest Resources for Announcements
class GuestAnnouncementResource(Resource):
    def get(self, announcement_id=None):
        if announcement_id:
            announcement = Announcement.query.get_or_404(announcement_id)
            return {'id': announcement.id, 'title': announcement.title, 'content': announcement.content}, 200
        announcements = Announcement.query.all()
        return [{'id': announcement.id, 'title': announcement.title, 'content': announcement.content} for announcement in announcements], 200









