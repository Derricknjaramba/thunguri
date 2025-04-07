import os
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import db, Product, Nursery, AboutUs, MillingProcess, AggressionProcess, FarmProgression, HowTo, Announcement, User, Query, Feedback
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
        data = request.get_json()

        about_us = AboutUs.query.first()

        if not about_us:
            about_us = AboutUs()

        about_us.who_we_are = data.get('who_we_are', about_us.who_we_are)
        about_us.our_story = data.get('our_story', about_us.our_story)
        about_us.mission_statement = data.get('mission_statement', about_us.mission_statement)
        about_us.vision = data.get('vision', about_us.vision)
        about_us.core_values = data.get('core_values', about_us.core_values)
        about_us.what_we_do = data.get('what_we_do', about_us.what_we_do)
        about_us.why_choose_us = data.get('why_choose_us', about_us.why_choose_us)

        db.session.add(about_us)
        db.session.commit()

        return {'message': 'About Us updated successfully'}, 200


# Guest Resources for About Us
class GuestAboutUsResource(Resource):
    def get(self):
        about_us = AboutUs.query.first()

        if not about_us:
            return {'message': 'About Us information not found'}, 404

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
        milling_process = MillingProcess(name=data['name'], description=data['description'])
        db.session.add(milling_process)
        db.session.commit()
        return {'message': 'Milling Process added'}, 201

    @jwt_required()
    def put(self, process_id):
        data = request.get_json()
        process = MillingProcess.query.get_or_404(process_id)
        process.name = data['name']
        process.description = data['description']
        db.session.commit()
        return {'message': 'Milling Process updated'}, 200

    @jwt_required()
    def delete(self, process_id):
        process = MillingProcess.query.get_or_404(process_id)
        db.session.delete(process)
        db.session.commit()
        return {'message': 'Milling Process deleted'}, 200


# Guest Resources for Milling Process
class GuestMillingProcessResource(Resource):
    def get(self, process_id=None):
        if process_id:
            process = MillingProcess.query.get_or_404(process_id)
            return {'id': process.id, 'name': process.name, 'description': process.description}, 200
        processes = MillingProcess.query.all()
        return [{'id': process.id, 'name': process.name, 'description': process.description} for process in processes], 200


# Admin Resources for Aggression Process
class AdminAggressionProcessResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        aggression_process = AggressionProcess(name=data['name'], description=data['description'])
        db.session.add(aggression_process)
        db.session.commit()
        return {'message': 'Aggression Process added'}, 201

    @jwt_required()
    def put(self, process_id):
        data = request.get_json()
        process = AggressionProcess.query.get_or_404(process_id)
        process.name = data['name']
        process.description = data['description']
        db.session.commit()
        return {'message': 'Aggression Process updated'}, 200

    @jwt_required()
    def delete(self, process_id):
        process = AggressionProcess.query.get_or_404(process_id)
        db.session.delete(process)
        db.session.commit()
        return {'message': 'Aggression Process deleted'}, 200


# Guest Resources for Aggression Process
class GuestAggressionProcessResource(Resource):
    def get(self, process_id=None):
        if process_id:
            process = AggressionProcess.query.get_or_404(process_id)
            return {'id': process.id, 'name': process.name, 'description': process.description}, 200
        processes = AggressionProcess.query.all()
        return [{'id': process.id, 'name': process.name, 'description': process.description} for process in processes], 200


# Admin Resources for Farm Progression
class AdminFarmProgressionResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        farm_progression = FarmProgression(name=data['name'], description=data['description'])
        db.session.add(farm_progression)
        db.session.commit()
        return {'message': 'Farm Progression added'}, 201

    @jwt_required()
    def put(self, progression_id):
        data = request.get_json()
        progression = FarmProgression.query.get_or_404(progression_id)
        progression.name = data['name']
        progression.description = data['description']
        db.session.commit()
        return {'message': 'Farm Progression updated'}, 200

    @jwt_required()
    def delete(self, progression_id):
        progression = FarmProgression.query.get_or_404(progression_id)
        db.session.delete(progression)
        db.session.commit()
        return {'message': 'Farm Progression deleted'}, 200


# Guest Resources for Farm Progression
class GuestFarmProgressionResource(Resource):
    def get(self, progression_id=None):
        if progression_id:
            progression = FarmProgression.query.get_or_404(progression_id)
            return {'id': progression.id, 'name': progression.name, 'description': progression.description}, 200
        progressions = FarmProgression.query.all()
        return [{'id': progression.id, 'name': progression.name, 'description': progression.description} for progression in progressions], 200


# Admin Resources for How To
class AdminHowToResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        how_to = HowTo(title=data['title'], content=data['content'])
        db.session.add(how_to)
        db.session.commit()
        return {'message': 'How To guide added'}, 201

    @jwt_required()
    def put(self, guide_id):
        data = request.get_json()
        guide = HowTo.query.get_or_404(guide_id)
        guide.title = data['title']
        guide.content = data['content']
        db.session.commit()
        return {'message': 'How To guide updated'}, 200

    @jwt_required()
    def delete(self, guide_id):
        guide = HowTo.query.get_or_404(guide_id)
        db.session.delete(guide)
        db.session.commit()
        return {'message': 'How To guide deleted'}, 200


# Guest Resources for How To
class GuestHowToResource(Resource):
    def get(self, guide_id=None):
        if guide_id:
            guide = HowTo.query.get_or_404(guide_id)
            return {'id': guide.id, 'title': guide.title, 'content': guide.content}, 200
        guides = HowTo.query.all()
        return [{'id': guide.id, 'title': guide.title, 'content': guide.content} for guide in guides], 200


# Admin Resources for Announcement
class AdminAnnouncementResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        announcement = Announcement(title=data['title'], content=data['content'])
        db.session.add(announcement)
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


# Guest Resources for Announcement
class GuestAnnouncementResource(Resource):
    def get(self, announcement_id=None):
        if announcement_id:
            announcement = Announcement.query.get_or_404(announcement_id)
            return {'id': announcement.id, 'title': announcement.title, 'content': announcement.content}, 200
        announcements = Announcement.query.all()
        return [{'id': announcement.id, 'title': announcement.title, 'content': announcement.content} for announcement in announcements], 200


# Admin Resources for Queries
class AdminQueryResource(Resource):
    @jwt_required()
    def get(self, query_id=None):
        if query_id:
            query = Query.query.get_or_404(query_id)
            return {
                'id': query.id,
                'name': query.name,
                'email': query.email,
                'query': query.query,
                'timestamp': query.timestamp
            }, 200
        queries = Query.query.all()
        return [{'id': query.id, 'name': query.name, 'email': query.email, 'query': query.query, 'timestamp': query.timestamp} for query in queries], 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_query = Query(
            name=data['name'],
            email=data['email'],
            query=data['query']
        )
        db.session.add(new_query)
        db.session.commit()
        return {'message': 'Query submitted'}, 201

    @jwt_required()
    def put(self, query_id):
        data = request.get_json()
        query = Query.query.get_or_404(query_id)
        
        query.name = data['name']
        query.email = data['email']
        query.query = data['query']
        db.session.commit()

        return {'message': 'Query updated'}, 200

    @jwt_required()
    def delete(self, query_id):
        query = Query.query.get_or_404(query_id)
        db.session.delete(query)
        db.session.commit()
        return {'message': 'Query deleted'}, 200


# Admin Resources for Feedback
class AdminFeedbackResource(Resource):
    @jwt_required()
    def get(self, feedback_id=None):
        if feedback_id:
            feedback = Feedback.query.get_or_404(feedback_id)
            return {
                'id': feedback.id,
                'name': feedback.name,
                'email': feedback.email,
                'feedback': feedback.feedback,
                'timestamp': feedback.timestamp
            }, 200
        feedbacks = Feedback.query.all()
        return [{
            'id': feedback.id,
            'name': feedback.name,
            'email': feedback.email,
            'feedback': feedback.feedback,
            'timestamp': feedback.timestamp
        } for feedback in feedbacks], 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_feedback = Feedback(
            name=data['name'],
            email=data['email'],
            feedback=data['feedback']
        )
        db.session.add(new_feedback)
        db.session.commit()
        return {'message': 'Feedback submitted'}, 201

    @jwt_required()
    def put(self, feedback_id):
        data = request.get_json()
        feedback = Feedback.query.get_or_404(feedback_id)

        feedback.name = data['name']
        feedback.email = data['email']
        feedback.feedback = data['feedback']
        db.session.commit()

        return {'message': 'Feedback updated'}, 200

    @jwt_required()
    def delete(self, feedback_id):
        feedback = Feedback.query.get_or_404(feedback_id)
        db.session.delete(feedback)
        db.session.commit()
        return {'message': 'Feedback deleted'}, 200


# Guest Resources for Queries
class GuestQueryResource(Resource):
    def post(self):
        data = request.get_json()
        new_query = Query(
            name=data['name'],
            email=data['email'],
            query=data['query']
        )
        db.session.add(new_query)
        db.session.commit()
        return {'message': 'Query submitted'}, 201


# Guest Resources for Feedback
class GuestFeedbackResource(Resource):
    def post(self):
        data = request.get_json()
        new_feedback = Feedback(
            name=data['name'],
            email=data['email'],
            feedback=data['feedback']
        )
        db.session.add(new_feedback)
        db.session.commit()
        return {'message': 'Feedback submitted'}, 201











