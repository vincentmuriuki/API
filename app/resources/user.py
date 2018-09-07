from flask import Flask
from flask_restful import Resource, reqparse
import re

from app.model import User, is_blank


class Signup(Resource):
    """
    Resource for user registering a new user
    Add Parser for required fields
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True,
                        help='Username cannot be blank', type=str)
    parser.add_argument('email', required=True,
                        help='Email cannot be blank', type=str)
    parser.add_argument('password', required=True,
                        help='Password cannot be blank', type=str)

    def post(self):
        """ Method to register a user """
        args = Signup.parser.parse_args()
        password = args.get('password')
        username = args.get('username')
        email = args.get('email')

        email_format = re.compile(
            r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[a-zA-Z-]+$)")
        username_format = re.compile(r"(^[A-Za-z]+$)")

        if not (re.match(username_format, username)):
            return {'message': 'Invalid username'}, 400
        elif not (re.match(email_format, email)):
            return {'message': 'Invalid email. Ensure email is of the form example@mail.com'}, 400
        if len(username) < 4:
            return {'message': 'Username should be atleast 4 characters'}, 400
        if is_blank(password) or is_blank(username) or is_blank(email):
            return {'message': 'All fields are required'}, 400
        if len(password) < 8:
            return {'message': 'Password should be atleast 8 characters'}, 400

        username_exists = User.get_user_by_username(username=args['username'])
        email_exists = User.get_user_by_email(email=args['email'])

        if username_exists or email_exists:
            return {'message': 'User already exists'}, 203

        user = User(username=args.get('username'),
                    email=args.get('email'), password=password)
        user = user.save()

        return {'message': 'registration successful, now login', 'user': user}, 201


class Login(Resource):
    """ Resource for user login """
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True,
                        help='Username cannot be blank', type=str)
    parser.add_argument('password', required=True,
                        help='Password cannot be blank')

    def post(self):
        """ Method for registered user to login """
        args = Login.parser.parse_args()
        username = args["username"]
        password = args["password"]
        if is_blank(username) or is_blank(password) == '':
            return {'message': 'All fields are required'}, 400

        user = User.get_user_by_username(username)
        if not user:
            return {'message': 'User unavailable'}, 404
        if user.validate_password(password):
            return {"message": "You are successfully logged in", 'user': user.view()}, 200
        return {"message": "Username or password is wrong."}, 401