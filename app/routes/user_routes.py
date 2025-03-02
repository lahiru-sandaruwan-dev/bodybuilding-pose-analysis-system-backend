# # app/routes/user_routes.py
from flask import Blueprint, request, jsonify
from app.models.user_model import User
from bson import ObjectId, errors
from app import mongo

user_routes = Blueprint('user_routes', __name__)

def response(status, success, message, data=None):
    return jsonify({"status": status, "isSuccessful": success, "message": message, "data": data}), status

@user_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if User.find_by_email(data.get('email')):
        return response(400, False, "User already exists")

    User(data['username'], data['email'], data['password']).save_to_db()
    return response(201, True, "User created successfully!", {"username": data['username'], "email": data['email']})

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_by_email(data.get('email'))

    if not user or not User.validate_password(user['password'], data.get('password')):
        return response(400, False, "Invalid credentials")

    return response(200, True, "Login successful!", {"user_id": str(user['_id']), "email": data['email']})

@user_routes.route('/profile', methods=['GET'])
def profile():
    try:
        users = [{"_id": str(u["_id"]), "username": u.get("username"), "email": u.get("email"), "full_name": u.get("full_name")} 
                 for u in mongo.db.users.find()]
        return response(200, True, "Users retrieved successfully", users)
    except Exception as e:
        return response(500, False, "An error occurred", str(e))

@user_routes.route('/profile/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return response(404, False, "User not found")

        return response(200, True, "User retrieved successfully", {
            "_id": str(user["_id"]), "username": user.get("username"), "email": user.get("email"), "full_name": user.get("full_name")
        })
    except errors.InvalidId:
        return response(400, False, "Invalid user ID format")
    except Exception as e:
        return response(500, False, "An error occurred", str(e))
