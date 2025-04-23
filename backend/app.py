from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db
from flasgger import Swagger
from resources import (
    UserResource,
    ProductResource, NurseryResource, AboutUsResource,
    MillingProcessResource, AggressionProcessResource, FarmProgressionResource,
    HowToResource, AnnouncementResource
)
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
swagger = Swagger(app)

# === Core Resources ===
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(ProductResource, '/product', '/product/<int:product_id>')
api.add_resource(NurseryResource, '/nursery', '/nursery/<int:nursery_id>')
api.add_resource(AboutUsResource, '/about-us')
api.add_resource(MillingProcessResource, '/milling-process', '/milling-process/<int:process_id>')
api.add_resource(AggressionProcessResource, '/aggression-process', '/aggression-process/<int:process_id>')
api.add_resource(FarmProgressionResource, '/farm-progression')
api.add_resource(HowToResource, '/how-to', '/how-to/<int:guide_id>')
api.add_resource(AnnouncementResource, '/announcement', '/announcement/<int:announcement_id>')

if __name__ == '__main__':
    app.run(debug=True)











