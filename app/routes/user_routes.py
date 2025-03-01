# app/routes/user_routes.py
from flask import Blueprint, request, jsonify
from app.models.user_model import User
from bson import ObjectId
from bson.errors import InvalidId
from app import mongo
import bcrypt

user_routes = Blueprint('user_routes', __name__)

# Registration Route (POST)
@user_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Extract details from the request
    username = data['username']
    email = data['email']
    password = data['password']
    
    # Check if user already exists
    if User.find_by_email(email):
        return jsonify({"message": "User already exists"}), 400
    
    # Create new user and save to DB
    user = User(username, email, password)
    user.save_to_db()
    
    return jsonify({"message": "User created successfully!"}), 201

# Login Route (POST)
@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data['email']
    password = data['password']
    
    # Check if user exists
    user_data = User.find_by_email(email)
    if not user_data:
        return jsonify({"message": "User not found"}), 404
    
    # Validate password
    if not User.validate_password(user_data['password'], password):
        return jsonify({"message": "Incorrect password"}), 400
    
    # Successful login
    return jsonify({"message": "Login successful!"}), 200

# Profile Route (GET)
@user_routes.route('/profile', methods=['GET'])
def profile():
    try:
        # Query the 'users' collection to get all users
        users = mongo.db.users.find()  # You can adjust the query to fit your needs (e.g., filter by user ID)

        # Convert the cursor result into a list of dictionaries
        user_list = []
        for user in users:
            user_data = {
                "_id": str(user.get("_id")),
                "username": user.get("username"),
                "email": user.get("email"),
                "full_name": user.get("full_name"),  # Add more fields as needed
            }
            user_list.append(user_data)

        # Return the list of users as a JSON response
        return jsonify(user_list), 200

    except Exception as e:
        # Handle any errors (e.g., DB connection issues)
        return jsonify({"error": str(e)}), 500
    
@user_routes.route('/profile/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        # Try to convert the user_id to ObjectId
        try:
            user_object_id = ObjectId(user_id)
        except InvalidId:
            # If invalid ObjectId format, return a 400 error
            return jsonify({"error": "Invalid user ID format"}), 400
        
        # Query the 'users' collection for the specific user
        user = mongo.db.users.find_one({"_id": user_object_id})
        
        if user is None:
            # If no user is found with the given _id, return a 404 error
            return jsonify({"error": "User not found"}), 404
        
        # Prepare user data for response
        user_data = {
            "_id": str(user["_id"]),  # Convert ObjectId to string
            "username": user.get("username"),
            "email": user.get("email"),
            "full_name": user.get("full_name"),  # Add more fields as needed
        }
        
        # Return the user data as a JSON response
        return jsonify(user_data), 200

    except Exception as e:
        # Handle any other unexpected errors
        return jsonify({"error": str(e)}), 500  
