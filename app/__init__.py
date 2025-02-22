 
# # app/__init__.py

# from flask import Flask
# from flask_pymongo import PyMongo
# from flask_cors import CORS

# mongo = PyMongo()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('config.Config')
#     mongo.init_app(app)
#     CORS(app)  # Enable Cross-Origin Resource Sharing

#     # Register routes
#     from .routes import pose_routes
#     app.register_blueprint(pose_routes.bp)

#     return app


# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo
from config import Config

mongo = PyMongo()  # Initialize PyMongo without app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize MongoDB with Flask app
    mongo.init_app(app)

    # Import and register blueprints
    from app.routes.user_routes import user_routes
    from app.routes.pose_routes import pose_bp  # Import your pose blueprint

    # Register Blueprints with appropriate URL prefixes
    app.register_blueprint(user_routes, url_prefix='/api')  # User-related routes
    app.register_blueprint(pose_bp, url_prefix='/api')      # Pose-related routes

    return app


