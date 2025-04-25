from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from models import db
from flasgger import Swagger
from resources import (
    Register, Login, UserResource,  # Import new resources
    ProductResource, NurseryResource, AboutUsResource,
    MillingProcessResource, AggressionProcessResource, FarmProgressionResource,
    HowToResource, AnnouncementResource
)
from config import Config

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from config.py

# Enable CORS for localhost:3000 only
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Initialize extensions
api = Api(app)
db.init_app(app)  # Initialize the database
jwt = JWTManager(app)  # Initialize JWT manager for handling authentication
migrate = Migrate(app, db)  # Initialize Flask-Migrate for DB migrations
swagger = Swagger(app)  # Initialize Flasgger for API documentation

# === Core Resources ===
api.add_resource(Register, '/api/register')  # Register the only admin user
api.add_resource(Login, '/api/login')  # Login for the user and get JWT
api.add_resource(UserResource, '/api/user/<int:user_id>')  # User details

# === CRUD Resources ===
api.add_resource(ProductResource, '/api/products', '/api/products/<int:product_id>')  # CRUD for Products
api.add_resource(NurseryResource, '/api/nurseries', '/api/nurseries/<int:nursery_id>')  # CRUD for Nurseries
api.add_resource(AboutUsResource, '/api/about-us')  # View, Admin-only Create/Update/Delete About Us
api.add_resource(MillingProcessResource, '/api/milling-process', '/api/milling-process/<int:process_id>')  # CRUD for Milling Process
api.add_resource(AggressionProcessResource, '/api/aggression-process', '/api/aggression-process/<int:process_id>')  # CRUD for Aggression Process
api.add_resource(FarmProgressionResource, '/api/farm-progression')  # CRUD for Farm Progression
api.add_resource(HowToResource, '/api/how-to', '/api/how-to/<int:guide_id>')  # CRUD for How-To Guides
api.add_resource(AnnouncementResource, '/api/announcements', '/api/announcements/<int:announcement_id>')  # CRUD for Announcements (Admin Only)

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
















