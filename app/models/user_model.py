# app/models/user_model.py
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def save_to_db(self):
        # Hash the password before saving
        hashed_password = generate_password_hash(self.password)
        user_data = {
            'username': self.username,
            'email': self.email,
            'password': hashed_password
        }
        # Insert the user document into the users collection
        mongo.db.users.insert_one(user_data)

    @staticmethod
    def find_by_email(email):
        # Find user by email
        return mongo.db.users.find_one({'email': email})

    @staticmethod
    def validate_password(user_password, entered_password):
        # Check if the entered password matches the hashed password
        return check_password_hash(user_password, entered_password)
