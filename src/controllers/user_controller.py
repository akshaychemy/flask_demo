from flask import request, Response, json, Blueprint,jsonify
from src.models.user_model import User
from src import bcrypt, db
from datetime import datetime
import jwt
import os

# user controller blueprint to be registered with api blueprint
users = Blueprint("users", __name__)

# Route for signup api/users/signup
@users.route('/signup', methods=["POST"])
def handle_signup():
    try:
        # First validate required user parameters
        data = request.json
        if "firstname" in data and "lastname" in data and "email" in data and "password" in data:
            # Validate if the user exists
            user = User.query.filter_by(email=data["email"]).first()
            # Use case if the user doesn't exist
            if not user:
                # Creating the user instance of User Model to be stored in DB
                user_obj = User(
                    firstname=data["firstname"],
                    lastname=data["lastname"],
                    email=data["email"],
                    # Hashing the password
                    password=bcrypt.generate_password_hash(data['password']).decode('utf-8')
                )
                db.session.add(user_obj)
                db.session.commit()

                # Let's generate JWT token
                payload = {
                    'iat': datetime.utcnow(),
                    'user_id': str(user_obj.id).replace('-', ""),
                    'firstname': user_obj.firstname,
                    'lastname': user_obj.lastname,
                    'email': user_obj.email,
                }
                token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
                return Response(
                    response=json.dumps({'status': "success",
                                         "message": "User Sign up Successful",
                                         "token": token}),
                    status=201,
                    mimetype='application/json'
                )
            else:
                # If user already exists
                return Response(
                    response=json.dumps({'status': "failed", "message": "User already exists. Kindly sign in."}),
                    status=409,
                    mimetype='application/json'
                )
        else:
            # If request parameters are not correct
            return Response(
                response=json.dumps({'status': "failed", "message": "User parameters (Firstname, Lastname, Email, and Password) are required"}),
                status=400,
                mimetype='application/json'
            )

    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed",
                                 "message": "Error occurred",
                                 "error": str(e)}),
            status=500,
            mimetype='application/json'
        )

# route for login api/users/signin
@users.route('/signin', methods = ["POST"])
def handle_login():
    try: 
        # first check user parameters
        data = request.json
        if "email" and "password" in data:
            # check db for user records
            user = User.query.filter_by(email = data["email"]).first()

            # if user records exists we will check user password
            if user:
                # check user password
                if bcrypt.check_password_hash(user.password, data["password"]):
                    # user password matched, we will generate token
                    payload = {
                        'iat': datetime.utcnow(),
                        'user_id': str(user.id).replace('-',""),
                        'firstname': user.firstname,
                        'lastname': user.lastname,
                        'email': user.email,
                        }
                    token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')
                    return Response(
                            response=json.dumps({'status': "success",
                                                "message": "User Sign In Successful",
                                                "token": token}),
                            status=200,
                            mimetype='application/json'
                        )
                
                else:
                    return Response(
                        response=json.dumps({'status': "failed", "message": "User Password Mistmatched"}),
                        status=401,
                        mimetype='application/json'
                    ) 
            # if there is no user record
            else:
                return Response(
                    response=json.dumps({'status': "failed", "message": "User Record doesn't exist, kindly register"}),
                    status=404,
                    mimetype='application/json'
                ) 
        else:
            # if request parameters are not correct 
            return Response(
                response=json.dumps({'status': "failed", "message": "User Parameters Email and Password are required"}),
                status=400,
                mimetype='application/json'
            )
        
    except Exception as e:
        return Response(
                response=json.dumps({'status': "failed", 
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )


# Define a route to find a user by ID
#api/users/find/1
@users.route('find/<int:user_id>', methods=["GET"])
def get_user(user_id):
    try:
        # Query the database for the user with the given ID
        user = User.query.get(user_id)

        # If user is not found, return 404 Not Found response
        if not user:
            return Response(
                response=jsonify({'status': "failed", "message": "User not found"}),
                status=404,
                mimetype='application/json'
            )

        # If user is found, return user details
        user_data = {
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email
        }

        return jsonify({'status': "success", "user": user_data})

    except Exception as e:
        # Return response in case of any error
        return Response(
            response=jsonify({'status': "failed", "message": "Error Occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )