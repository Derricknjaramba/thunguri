from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate  # Import Migrate
from models import db
from resources import (
    UserResource,
    GuestMillingProcessResource, AdminMillingProcessResource,
    GuestAggressionProcessResource, AdminAggressionProcessResource,
    GuestFarmProgressionResource, AdminFarmProgressionResource,
    GuestHowToResource, AdminHowToResource,
    GuestAnnouncementResource, AdminAnnouncementResource,
    AdminProductResource, GuestProductResource,
    AdminNurseryResource, GuestNurseryResource,
    AdminAboutUsResource, GuestAboutUsResource
)
from config import Config

app = Flask(__name__)

# Load configurations from the Config class
app.config.from_object(Config)

# Initialize database and JWT manager
db.init_app(app)
jwt = JWTManager(app)

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Initialize Flask-RESTful API
api = Api(app)

# Add user resource (for authentication or user management)
api.add_resource(UserResource, '/users')

# Guest Routes
api.add_resource(GuestMillingProcessResource, '/guest/millingprocesses')
api.add_resource(GuestAggressionProcessResource, '/guest/aggressionprocesses')
api.add_resource(GuestFarmProgressionResource, '/guest/farmprogressions')
api.add_resource(GuestHowToResource, '/guest/howtos')
api.add_resource(GuestAnnouncementResource, '/guest/announcements')

# Admin Routes
api.add_resource(AdminMillingProcessResource, '/admin/millingprocesses', '/admin/millingprocesses/<int:id>')
api.add_resource(AdminAggressionProcessResource, '/admin/aggressionprocesses', '/admin/aggressionprocesses/<int:id>')
api.add_resource(AdminFarmProgressionResource, '/admin/farmprogressions', '/admin/farmprogressions/<int:id>')
api.add_resource(AdminHowToResource, '/admin/howtos', '/admin/howtos/<int:id>')
api.add_resource(AdminAnnouncementResource, '/admin/announcements', '/admin/announcements/<int:id>')

# Admin Routes for Product, Nursery, About Us
api.add_resource(AdminProductResource, '/admin/products', '/admin/products/<int:product_id>')
api.add_resource(AdminNurseryResource, '/admin/nurseries', '/admin/nurseries/<int:nursery_id>')
api.add_resource(AdminAboutUsResource, '/admin/aboutus', '/admin/aboutus/<int:about_us_id>')

# Guest Routes for Product, Nursery, About Us
api.add_resource(GuestProductResource, '/guest/products', '/guest/products/<int:product_id>')
api.add_resource(GuestNurseryResource, '/guest/nurseries', '/guest/nurseries/<int:nursery_id>')
api.add_resource(GuestAboutUsResource, '/guest/aboutus', '/guest/aboutus')

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(debug=True)







