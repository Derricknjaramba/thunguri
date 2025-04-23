from flasgger import swag_from
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import db, Product, Nursery, AboutUs, MillingProcess, AggressionProcess, FarmProgression, HowTo, Announcement, User
from flask import request
from werkzeug.utils import secure_filename
import os
from utils import allowed_photo


# User Resource
class UserResource(Resource):
    @jwt_required()
    @swag_from({
        'tags': ['User'],
        'summary': 'Retrieve user details',
        'description': 'Fetch user details by ID.',
        'parameters': [
            {
                'name': 'user_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the user'
            }
        ],
        'responses': {
            200: {
                'description': 'User details retrieved successfully'
            }
        }
    })
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {'id': user.id, 'username': user.username, 'email': user.email}, 200

    @jwt_required()
    @swag_from({
        'tags': ['User'],
        'summary': 'Update user details',
        'description': 'Update user information by ID.',
        'parameters': [
            {
                'name': 'user_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'username': {'type': 'string'},
                        'email': {'type': 'string'}
                    },
                    'required': ['username', 'email']
                }
            }
        ],
        'responses': {
            200: {'description': 'User updated successfully'}
        }
    })
    def put(self, user_id):
        data = request.get_json()
        user = User.query.get_or_404(user_id)

        user.username = data['username']
        user.email = data['email']
        db.session.commit()

        return {'message': 'User updated successfully'}, 200

    @jwt_required()
    @swag_from({
        'tags': ['User'],
        'summary': 'Delete user',
        'description': 'Delete user by ID.',
        'parameters': [
            {
                'name': 'user_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the user to delete'
            }
        ],
        'responses': {
            200: {'description': 'User deleted successfully'}
        }
    })
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200


#class ProductResource(Resource):
class ProductResource(Resource):
    @swag_from({
        'tags': ['Product'],
        'summary': 'Retrieve product(s)',
        'description': 'Fetch a list of all products or a specific product by ID.',
        'parameters': [
            {
                'name': 'product_id',
                'in': 'path',
                'type': 'integer',
                'required': False,
                'description': 'ID of the product'
            }
        ],
        'responses': {
            200: {
                'description': 'List of products or product details'
            }
        }
    })
    def get(self, product_id=None):
        # If a product ID is provided, fetch the specific product
        if product_id:
            product = Product.query.get_or_404(product_id)
            return {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'image_path': product.image_path}, 200
        
        # If no product ID is provided, fetch all products
        products = Product.query.all()
        return [{'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'image_path': product.image_path} for product in products], 200

    # The rest of the methods (POST, PUT, DELETE) remain secured with JWT authentication
    @jwt_required()
    @swag_from({
        'tags': ['Product'],
        'summary': 'Create product',
        'description': 'Create a new product in the system.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'name': {'type': 'string'},
                        'description': {'type': 'string'},
                        'price': {'type': 'number'}
                    },
                    'required': ['name', 'description', 'price']
                }
            },
            {
                'name': 'image',
                'in': 'formData',
                'type': 'file',
                'required': False,
                'description': 'Product image'
            }
        ],
        'responses': {
            201: {'description': 'Product created'}
        }
    })
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

            return {'message': 'Product created successfully'}, 201
        return {'message': 'Invalid image format'}, 400

    @jwt_required()
    @swag_from({
        'tags': ['Product'],
        'summary': 'Update product',
        'description': 'Update an existing product by their ID.',
        'parameters': [
            {
                'name': 'product_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'name': {'type': 'string'},
                        'description': {'type': 'string'},
                        'price': {'type': 'number'}
                    },
                    'required': ['name', 'description', 'price']
                }
            }
        ],
        'responses': {
            200: {'description': 'Product updated'}
        }
    })
    def put(self, product_id):
        data = request.get_json()
        product = Product.query.get_or_404(product_id)

        product.name = data['name']
        product.description = data['description']
        product.price = data['price']
        db.session.commit()

        return {'message': 'Product updated successfully'}, 200

    @jwt_required()
    @swag_from({
        'tags': ['Product'],
        'summary': 'Delete product',
        'description': 'Delete a product from the system by their ID.',
        'parameters': [
            {
                'name': 'product_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
        'responses': {
            200: {'description': 'Product deleted'}
        }
    })
    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully'}, 200



class NurseryResource(Resource):
    @swag_from({
        'tags': ['Nursery'],
        'summary': 'Retrieve nursery details',
        'description': 'Fetch a list of all nurseries or a specific nursery by ID.',
        'parameters': [
            {
                'name': 'nursery_id',
                'in': 'path',
                'type': 'integer',
                'required': False,
                'description': 'ID of the nursery'
            }
        ],
        'responses': {
            200: {
                'description': 'List of nurseries or nursery details'
            }
        }
    })
    def get(self, nursery_id=None):
        # If a nursery ID is provided, fetch the specific nursery
        if nursery_id:
            nursery = Nursery.query.get_or_404(nursery_id)
            return {'id': nursery.id, 'name': nursery.name, 'location': nursery.location, 'description': nursery.description}, 200
        
        # If no nursery ID is provided, fetch all nurseries
        nurseries = Nursery.query.all()
        return [{'id': nursery.id, 'name': nursery.name, 'location': nursery.location, 'description': nursery.description} for nursery in nurseries], 200

    # The rest of the methods (POST, PUT, DELETE) remain secured with JWT authentication
    @jwt_required()
    @swag_from({
        'tags': ['Nursery'],
        'summary': 'Create nursery',
        'description': 'Create a new nursery.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'name': {'type': 'string'},
                        'location': {'type': 'string'},
                        'description': {'type': 'string'}
                    },
                    'required': ['name', 'location', 'description']
                }
            }
        ],
        'responses': {
            201: {'description': 'Nursery created'}
        }
    })
    def post(self):
        data = request.get_json()

        new_nursery = Nursery(
            name=data['name'],
            location=data['location'],
            description=data['description']
        )
        db.session.add(new_nursery)
        db.session.commit()
        return {'message': 'Nursery created successfully'}, 201

    @jwt_required()
    @swag_from({
        'tags': ['Nursery'],
        'summary': 'Update nursery',
        'description': 'Update an existing nursery by their ID.',
        'parameters': [
            {
                'name': 'nursery_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'name': {'type': 'string'},
                        'location': {'type': 'string'},
                        'description': {'type': 'string'}
                    },
                    'required': ['name', 'location', 'description']
                }
            }
        ],
        'responses': {
            200: {'description': 'Nursery updated'}
        }
    })
    def put(self, nursery_id):
        data = request.get_json()
        nursery = Nursery.query.get_or_404(nursery_id)

        nursery.name = data['name']
        nursery.location = data['location']
        nursery.description = data['description']
        db.session.commit()

        return {'message': 'Nursery updated successfully'}, 200

    @jwt_required()
    @swag_from({
        'tags': ['Nursery'],
        'summary': 'Delete nursery',
        'description': 'Delete a nursery from the system by their ID.',
        'parameters': [
            {
                'name': 'nursery_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
        'responses': {
            200: {'description': 'Nursery deleted'}
        }
    })
    def delete(self, nursery_id):
        nursery = Nursery.query.get_or_404(nursery_id)
        db.session.delete(nursery)
        db.session.commit()
        return {'message': 'Nursery deleted successfully'}, 200


# class AboutUsResource(Resource):
class AboutUsResource(Resource):
    @swag_from({
        'tags': ['About Us'],
        'summary': 'Retrieve About Us details',
        'description': 'Fetch the About Us details.',
        'responses': {
            200: {'description': 'About Us details retrieved successfully'}
        }
    })
    def get(self):
        about_us = AboutUs.query.first()
        return {'id': about_us.id, 'description': about_us.description}, 200

    @jwt_required()
    @swag_from({
        'tags': ['About Us'],
        'summary': 'Update About Us details',
        'description': 'Update About Us information.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'description': {'type': 'string'}
                    },
                    'required': ['description']
                }
            }
        ],
        'responses': {
            200: {'description': 'About Us updated successfully'}
        }
    })
    def put(self):
        data = request.get_json()
        about_us = AboutUs.query.first()

        about_us.description = data['description']
        db.session.commit()

        return {'message': 'About Us updated successfully'}, 200

    @jwt_required()
    @swag_from({
        'tags': ['About Us'],
        'summary': 'Create About Us details',
        'description': 'Create a new About Us record.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'description': {'type': 'string'}
                    },
                    'required': ['description']
                }
            }
        ],
        'responses': {
            201: {'description': 'About Us created successfully'}
        }
    })
    def post(self):
        data = request.get_json()

        new_about_us = AboutUs(
            description=data['description']
        )
        db.session.add(new_about_us)
        db.session.commit()

        return {'message': 'About Us created successfully'}, 201

    @jwt_required()
    @swag_from({
        'tags': ['About Us'],
        'summary': 'Delete About Us details',
        'description': 'Delete the About Us record.',
        'parameters': [
            {
                'name': 'about_us_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the About Us record to delete'
            }
        ],
        'responses': {
            200: {'description': 'About Us deleted successfully'}
        }
    })
    def delete(self):
        about_us = AboutUs.query.first()  # Assuming there's only one AboutUs record
        if about_us:
            db.session.delete(about_us)
            db.session.commit()
            return {'message': 'About Us deleted successfully'}, 200
        else:
            return {'message': 'No About Us record found to delete'}, 404
class MillingProcessResource(Resource):
    @swag_from({
        'tags': ['Milling Process'],
        'summary': 'Retrieve Milling Process details',
        'description': 'Fetch the Milling Process details.',
        'responses': {
            200: {'description': 'Milling Process details retrieved successfully'}
        }
    })
    def get(self):
        milling_process = MillingProcess.query.first()
        if not milling_process:
            return {'message': 'No Milling Process found'}, 404
        return {
            'id': milling_process.id,
            'description': milling_process.description
        }, 200

    @jwt_required()
    @swag_from({
        'tags': ['Milling Process'],
        'summary': 'Update Milling Process details',
        'description': 'Update Milling Process information.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'description': {'type': 'string'}
                    },
                    'required': ['description']
                }
            }
        ],
        'responses': {
            200: {'description': 'Milling Process updated successfully'}
        }
    })
    def put(self):
        data = request.get_json()
        milling_process = MillingProcess.query.first()
        if not milling_process:
            return {'message': 'No Milling Process found to update'}, 404

        milling_process.description = data['description']
        db.session.commit()
        return {'message': 'Milling Process updated successfully'}, 200

    @jwt_required()
    @swag_from({
        'tags': ['Milling Process'],
        'summary': 'Delete Milling Process',
        'description': 'Delete the Milling Process from the system.',
        'responses': {
            200: {'description': 'Milling Process deleted successfully'}
        }
    })
    def delete(self):
        milling_process = MillingProcess.query.first()
        if not milling_process:
            return {'message': 'No Milling Process found to delete'}, 404

        db.session.delete(milling_process)
        db.session.commit()
        return {'message': 'Milling Process deleted successfully'}, 200

    @jwt_required()
    @swag_from({
        'tags': ['Milling Process'],
        'summary': 'Add a new Milling Process',
        'description': 'Create a new Milling Process in the system.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'description': {'type': 'string'}
                    },
                    'required': ['description']
                }
            }
        ],
        'responses': {
            201: {'description': 'Milling Process created successfully'}
        }
    })
    def post(self):
        data = request.get_json()
        new_milling_process = MillingProcess(description=data['description'])
        db.session.add(new_milling_process)
        db.session.commit()
        return {'message': 'Milling Process created successfully'}, 201


#
class AggressionProcessResource(Resource):
    @swag_from({
        'tags': ['Aggression Process'],
        'summary': 'Retrieve Aggression Process details',
        'description': 'Fetch the Aggression Process details.',
        'responses': {
            200: {'description': 'Aggression Process details retrieved successfully'}
        }
    })
    def get(self):
        aggression_process = AggressionProcess.query.first()
        return {'id': aggression_process.id, 'description': aggression_process.description}, 200

    @jwt_required()
    @swag_from({
        'tags': ['Aggression Process'],
        'summary': 'Update Aggression Process details',
        'description': 'Update Aggression Process information.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'description': {'type': 'string'}
                    },
                    'required': ['description']
                }
            }
        ],
        'responses': {
            200: {'description': 'Aggression Process updated successfully'}
        }
    })
    def put(self):
        data = request.get_json()
        aggression_process = AggressionProcess.query.first()

        aggression_process.description = data['description']
        db.session.commit()

        return {'message': 'Aggression Process updated successfully'}, 200

    @jwt_required()
    @swag_from({
        'tags': ['Aggression Process'],
        'summary': 'Add a new Aggression Process',
        'description': 'Create a new Aggression Process in the system.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'description': {'type': 'string'}
                    },
                    'required': ['description']
                }
            }
        ],
        'responses': {
            201: {'description': 'Aggression Process created successfully'}
        }
    })
    def post(self):
        data = request.get_json()

        new_aggression_process = AggressionProcess(
            description=data['description']
        )
        db.session.add(new_aggression_process)
        db.session.commit()

        return {'message': 'Aggression Process created successfully'}, 201

    @jwt_required()
    @swag_from({
        'tags': ['Aggression Process'],
        'summary': 'Delete Aggression Process',
        'description': 'Delete the Aggression Process from the system.',
        'responses': {
            200: {'description': 'Aggression Process deleted successfully'}
        }
    })
    def delete(self):
        aggression_process = AggressionProcess.query.first()
        db.session.delete(aggression_process)
        db.session.commit()
        return {'message': 'Aggression Process deleted successfully'}, 200
    

class FarmProgressionResource(Resource):
    @swag_from({
        'tags': ['Farm Progression'],
        'summary': 'Retrieve Farm Progression details',
        'description': 'Fetch the Farm Progression details.',
        'responses': {
            200: {'description': 'Farm Progression details retrieved successfully'}
        }
    })
    def get(self):
        farm_progression = FarmProgression.query.first()
        return {
            'id': farm_progression.id,
            'description': farm_progression.description
        }, 200

    @jwt_required()
    @swag_from({
        'tags': ['Farm Progression'],
        'summary': 'Update Farm Progression details',
        'description': 'Update Farm Progression information.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'description': {'type': 'string'}
                    },
                    'required': ['description']
                }
            }
        ],
        'responses': {
            200: {'description': 'Farm Progression updated successfully'}
        }
    })
    def put(self):
        data = request.get_json()
        farm_progression = FarmProgression.query.first()

        farm_progression.description = data['description']
        db.session.commit()

        return {'message': 'Farm Progression updated successfully'}, 200

    @jwt_required()
    @swag_from({
        'tags': ['Farm Progression'],
        'summary': 'Delete Farm Progression',
        'description': 'Delete the Farm Progression from the system.',
        'responses': {
            200: {'description': 'Farm Progression deleted successfully'}
        }
    })
    def delete(self):
        farm_progression = FarmProgression.query.first()
        db.session.delete(farm_progression)
        db.session.commit()
        return {'message': 'Farm Progression deleted successfully'}, 200

    @jwt_required()
    @swag_from({
        'tags': ['Farm Progression'],
        'summary': 'Add a new Farm Progression',
        'description': 'Create a new Farm Progression in the system.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'description': {'type': 'string'}
                    },
                    'required': ['description']
                }
            }
        ],
        'responses': {
            201: {'description': 'Farm Progression created successfully'}
        }
    })
    def post(self):
        data = request.get_json()

        new_farm_progression = FarmProgression(
            description=data['description']
        )
        db.session.add(new_farm_progression)
        db.session.commit()

        return {'message': 'Farm Progression created successfully'}, 201



# 
class HowToResource(Resource):
    @swag_from({
        'tags': ['How To'],
        'summary': 'Retrieve How To guide',
        'description': 'Fetch a list of How To guides or a specific guide by ID.',
        'parameters': [
            {
                'name': 'guide_id',
                'in': 'path',
                'type': 'integer',
                'required': False,
                'description': 'ID of the How To guide'
            }
        ],
        'responses': {
            200: {'description': 'How To guides retrieved successfully'}
        }
    })
    def get(self, guide_id=None):
        if guide_id:
            guide = HowTo.query.get_or_404(guide_id)
            return {'id': guide.id, 'title': guide.title, 'content': guide.content}, 200
        guides = HowTo.query.all()
        return [{'id': guide.id, 'title': guide.title, 'content': guide.content} for guide in guides], 200

    @jwt_required()
    @swag_from({
        'tags': ['How To'],
        'summary': 'Create How To guide',
        'description': 'Create a new How To guide.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'title': {'type': 'string'},
                        'content': {'type': 'string'}
                    },
                    'required': ['title', 'content']
                }
            }
        ],
        'responses': {
            201: {'description': 'How To guide created'}
        }
    })
    def post(self):
        data = request.get_json()

        new_guide = HowTo(
            title=data['title'],
            content=data['content']
        )
        db.session.add(new_guide)
        db.session.commit()

        return {'message': 'How To guide created successfully'}, 201

    @jwt_required()
    @swag_from({
        'tags': ['How To'],
        'summary': 'Update How To guide',
        'description': 'Update an existing How To guide by their ID.',
        'parameters': [
            {
                'name': 'guide_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'title': {'type': 'string'},
                        'content': {'type': 'string'}
                    },
                    'required': ['title', 'content']
                }
            }
        ],
        'responses': {
            200: {'description': 'How To guide updated'}
        }
    })
    def put(self, guide_id):
        data = request.get_json()
        guide = HowTo.query.get_or_404(guide_id)

        guide.title = data['title']
        guide.content = data['content']
        db.session.commit()

        return {'message': 'How To guide updated successfully'}, 200

    @jwt_required()
    @swag_from({
        'tags': ['How To'],
        'summary': 'Delete How To guide',
        'description': 'Delete a How To guide by their ID.',
        'parameters': [
            {
                'name': 'guide_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the How To guide'
            }
        ],
        'responses': {
            200: {'description': 'How To guide deleted successfully'}
        }
    })
    def delete(self, guide_id):
        guide = HowTo.query.get_or_404(guide_id)
        db.session.delete(guide)
        db.session.commit()
        return {'message': 'How To guide deleted successfully'}, 200



class AnnouncementResource(Resource):
    @swag_from({
        'tags': ['Announcements'],
        'summary': 'Retrieve Announcements',
        'description': 'Fetch a list of announcements or a specific announcement by ID.',
        'parameters': [
            {
                'name': 'announcement_id',
                'in': 'path',
                'type': 'integer',
                'required': False,
                'description': 'ID of the announcement'
            }
        ],
        'responses': {
            200: {'description': 'Announcements retrieved successfully'}
        }
    })
    def get(self, announcement_id=None):
        if announcement_id:
            announcement = Announcement.query.get_or_404(announcement_id)
            return {'id': announcement.id, 'title': announcement.title, 'content': announcement.content}, 200
        announcements = Announcement.query.all()
        return [{'id': announcement.id, 'title': announcement.title, 'content': announcement.content} for announcement in announcements], 200

    @jwt_required()
    @swag_from({
        'tags': ['Announcements'],
        'summary': 'Create Announcement',
        'description': 'Create a new Announcement.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'title': {'type': 'string'},
                        'content': {'type': 'string'}
                    },
                    'required': ['title', 'content']
                }
            }
        ],
        'responses': {
            201: {'description': 'Announcement created'}
        }
    })
    def post(self):
        data = request.get_json()

        new_announcement = Announcement(
            title=data['title'],
            content=data['content']
        )
        db.session.add(new_announcement)
        db.session.commit()

        return {'message': 'Announcement created successfully'}, 201

    @jwt_required()
    @swag_from({
        'tags': ['Announcements'],
        'summary': 'Update Announcement',
        'description': 'Update an existing Announcement by its ID.',
        'parameters': [
            {
                'name': 'announcement_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'properties': {
                        'title': {'type': 'string'},
                        'content': {'type': 'string'}
                    },
                    'required': ['title', 'content']
                }
            }
        ],
        'responses': {
            200: {'description': 'Announcement updated'}
        }
    })
    def put(self, announcement_id):
        data = request.get_json()
        announcement = Announcement.query.get_or_404(announcement_id)

        announcement.title = data['title']
        announcement.content = data['content']
        db.session.commit()

        return {'message': 'Announcement updated successfully'}, 200

    @jwt_required()
    @swag_from({
        'tags': ['Announcements'],
        'summary': 'Delete Announcement',
        'description': 'Delete an Announcement by its ID.',
        'parameters': [
            {
                'name': 'announcement_id',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
        'responses': {
            200: {'description': 'Announcement deleted'}
        }
    })
    def delete(self, announcement_id):
        announcement = Announcement.query.get_or_404(announcement_id)
        db.session.delete(announcement)
        db.session.commit()
        return {'message': 'Announcement deleted successfully'}, 200
    





