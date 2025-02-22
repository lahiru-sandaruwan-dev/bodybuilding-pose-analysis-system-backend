# app/routes/user_routes.py
from flask import Blueprint, request, jsonify
from app.models.user_model import User
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
    # Fetch user details from the session or token (just a simple demo here)
    user_data = {"username": "John Doe", "email": "john@example.com"}
    
    return jsonify(user_data), 200
