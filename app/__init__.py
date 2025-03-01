 
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
# from flask import Flask
# from flask_pymongo import PyMongo
# from config import Config

# mongo = PyMongo()  # Initialize PyMongo without app

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
    
#     # Initialize MongoDB with Flask app
#     mongo.init_app(app)

#     # Import and register blueprints
#     from app.routes.user_routes import user_routes
#     from app.routes.pose_routes import pose_bp  # Import your pose blueprint
#     from app.routes.side_chest_pose_routes import side_chest_pose_bp  # Import your pose blueprint

#     # Register Blueprints with appropriate URL prefixes
#     app.register_blueprint(user_routes, url_prefix='/api')  # User-related routes
#     app.register_blueprint(pose_bp, url_prefix='/api')      # Pose-related routes
#     app.register_blueprint(side_chest_pose_bp, url_prefix='/api')      # Pose-related routes

#     return app

from flask import Flask
from flask_pymongo import PyMongo
from config import Config

mongo = PyMongo()  # Initialize PyMongo without app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Test the MongoDB URI
    if not app.config.get("MONGO_URI"):
        raise ValueError("MONGO_URI is missing in configuration.")
    
    # Initialize MongoDB with Flask app
    mongo.init_app(app)
    
    # Test the MongoDB connection
    try:
        # Check if MongoDB is reachable
        mongo.db.command("ping")
        print("MongoDB connection successful")
    except Exception as e:
        print("MongoDB connection failed:", e)
        raise e
    
    # Import and register blueprints
    from app.routes.user_routes import user_routes
    from app.routes.pose_routes import pose_bp
    from app.routes.side_chest_pose_routes import side_chest_pose_bp

    # Register Blueprints with appropriate URL prefixes
    app.register_blueprint(user_routes, url_prefix='/api')
    app.register_blueprint(pose_bp, url_prefix='/api')
    app.register_blueprint(side_chest_pose_bp, url_prefix='/api')

    return app


# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
    
#     # Initialize MongoDB with Flask app
#     mongo.init_app(app)

#     # Test the MongoDB connection
#     try:
#         # Check if MongoDB is reachable
#         mongo.db.command("ping")
#         print("MongoDB connection successful")
#     except Exception as e:
#         print("MongoDB connection failed", e)
#         raise e

#     # Import and register blueprints
#     from app.routes.user_routes import user_routes
#     from app.routes.pose_routes import pose_bp  # Import your pose blueprint
#     from app.routes.side_chest_pose_routes import side_chest_pose_bp  # Import your pose blueprint

#     # Register Blueprints with appropriate URL prefixes
#     app.register_blueprint(user_routes, url_prefix='/api')  # User-related routes
#     app.register_blueprint(pose_bp, url_prefix='/api')      # Pose-related routes
#     app.register_blueprint(side_chest_pose_bp, url_prefix='/api')      # Pose-related routes

#     return app



