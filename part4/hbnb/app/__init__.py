from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

#-----------------------------------importing namespaces-----------------------------------

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protected import api as protected_ns

#-----------------------------------create_app function (to create application)-----------------------------------

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False
    CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API',
              security='Bearer', authorizations={
                  'Bearer': {
                      'type': 'apiKey',
                      'in': 'header',
                      'name': 'Authorization',
                      'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
                  }
              })
    

#-----------------------------------adding namespaces to the application-----------------------------------

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(protected_ns, path='/api/v1/protected')

#-----------------------------------initializing the application-----------------------------------

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

#-----------------------------------creating all tables-----------------------------------

    with app.app_context():
        db.create_all()

#-----------------------------------returning the application-----------------------------------

    return app