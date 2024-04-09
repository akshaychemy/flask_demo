from flask import request, Response, json, Blueprint,jsonify
from src.models.user_model import User
from src import bcrypt, db
from datetime import datetime
import jwt
import os

from src import collection

# user controller blueprint to be registered with api blueprint
users = Blueprint("users", __name__)

# route for signup api/users/signup
@users.route('/signup', methods=["POST"])
def handle_signup():
    try:
        # first validate required user parameters
        data = request.json
        if "firstname" in data and "lastname" in data and "email" in data and "password" in data:
            # validate if the user exists
            user = collection.find_one({"email": data["email"]})
            print("user==>", user)
            # use case if the user doesn't exist
            if not user:
                # creating the user instance to be stored in DB
                user_data = {
                    "firstname": data["firstname"],
                    "lastname": data["lastname"],
                    "email": data["email"],
                    "password": bcrypt.generate_password_hash(data['password'])
                }
                # insert user data into MongoDB
                result = collection.insert_one(user_data)
                print("result==>",result)

                # let's generate a JWT token
                payload = {
                    'iat': datetime.utcnow(),
                    'user_id': str(result.inserted_id),
                    'firstname': user_data["firstname"],
                    'lastname': user_data["lastname"],
                    'email': user_data["email"],
                }
                token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
                return jsonify({'status': "success",
                                "message": "User Sign up Successful",
                                "token": token}), 201
            else:
                # if user already exists
                return jsonify({'status': "failed", "message": "User already exists, kindly use sign in"}), 409
        else:
            # if request parameters are not correct
            return jsonify({'status': "failed", "message": "User parameters Firstname, Lastname, Email, and Password are required"}), 400

    except Exception as e:
        return jsonify({'status': "failed", "message": "Error Occurred", "error": str(e)}), 500

        
# route for login api/users/signin
@users.route('/signin', methods=["POST"])
def handle_login():
    try:
        # first check user parameters
        data = request.json
        if "email" and "password" in data:
            # check the database for user records
            user = collection.find_one({"email": data["email"]})

            # if user record exists, we will check the password
            if user:
                # check user password
                if bcrypt.check_password_hash(user["password"], data["password"]):
                    # user password matched, we will generate a token
                    payload = {
                        'iat': datetime.utcnow(),
                        'user_id': str(user["_id"]),
                        'firstname': user["firstname"],
                        'lastname': user["lastname"],
                        'email': user["email"],
                    }
                    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
                    return jsonify({
                        'status': "success",
                        "message": "User Sign In Successful",
                        "token": token
                    }), 200

                else:
                    return jsonify({
                        'status': "failed",
                        "message": "User Password Mismatched"
                    }), 401
            else:
                # if there is no user record
                return jsonify({
                    'status': "failed",
                    "message": "User Record doesn't exist, kindly register"
                }), 404
        else:
            # if request parameters are not correct
            return jsonify({
                'status': "failed",
                "message": "User Parameters Email and Password are required"
            }), 400

    except Exception as e:
        return jsonify({
            'status': "failed",
            "message": "Error Occurred",
            "error": str(e)
        }), 500

