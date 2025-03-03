# from flask import Flask
# from flask_pymongo import PyMongo
# from flask_cors import CORS
# from config import Config

# # Initialize PyMongo without app
# mongo = PyMongo()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # Enable CORS for all routes
#     CORS(app, resources={r"/api/*": {"origins": "*"}})  

#     # Validate and Initialize MongoDB
#     mongo_uri = app.config.get("MONGO_URI")
#     if not mongo_uri:
#         raise ValueError("MONGO_URI is missing in configuration.")
    
#     mongo.init_app(app)

#     try:
#         mongo.db.command("ping")  # Check MongoDB connection
#         print("MongoDB connection successful")
#     except Exception as e:
#         print("MongoDB connection failed:", e)
#         raise e

#     # Import and register blueprints
#     from app.routes.user_routes import user_routes
#     from app.routes.pose_routes import pose_bp
#     from app.routes.side_chest_pose_routes import side_chest_pose_bp

#     app.register_blueprint(user_routes, url_prefix='/api')
#     app.register_blueprint(pose_bp, url_prefix='/api')
#     app.register_blueprint(side_chest_pose_bp, url_prefix='/api')

#     return app

from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_socketio import SocketIO
from config import Config

# Initialize PyMongo without app
mongo = PyMongo()

# Initialize Flask-SocketIO
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})  

    # Validate and Initialize MongoDB
    mongo_uri = app.config.get("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI is missing in configuration.")
    
    mongo.init_app(app)

    try:
        mongo.db.command("ping")  # Check MongoDB connection
        print("MongoDB connection successful")
    except Exception as e:
        print("MongoDB connection failed:", e)
        raise e

    # Initialize SocketIO with the Flask app
    socketio.init_app(app)

    # Import and register blueprints
    from app.routes.user_routes import user_routes
    from app.routes.pose_routes import pose_bp
    from app.routes.side_chest_pose_routes import side_chest_pose_bp

    app.register_blueprint(user_routes, url_prefix='/api')
    app.register_blueprint(pose_bp, url_prefix='/api')
    app.register_blueprint(side_chest_pose_bp, url_prefix='/api')

    return app


