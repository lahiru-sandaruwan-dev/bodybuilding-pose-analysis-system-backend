# # app/controllers/user_controller.py

from app.models import User
from flask import jsonify
from flask_pymongo import PyMongo
import bcrypt


# MongoDB Instance
mongo = PyMongo()

# Signup Function
def signup_user(data):
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password:
        return jsonify({"error": "Email and Password are required"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
        "email": email,
        "password": hashed_password,
        "name": name
    }
    
    # Check if user already exists
    existing_user = mongo.db.users.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "User already exists"}), 400
    
    mongo.db.users.insert_one(user)
    return jsonify({"message": "User registered successfully"}), 201

# Login Function
def login_user(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and Password are required"}), 400
    
    user = mongo.db.users.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "user_id": str(user["_id"])}), 200

# Get User Profile
def get_user_profile(user_id):
    user = mongo.db.users.find_one({"_id": user_id})
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "name": user["name"],
        "email": user["email"],
        "user_id": str(user["_id"])
    })
