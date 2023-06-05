
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import post 
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt


class User:
    db = "dojo_wall_db" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added her for class association?
        self.posts = []



    # Create Users Models
    @classmethod
    def create_user(cls, data):
        #if the data isn't valid, returns false and will redirect in our controller to register form again
        if not cls.validate_user_registration(data):
            return False
        data = cls.parse_registration_data(data)
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query, data)
        #set session id and name to be used while logged in
        session['user_id'] = user_id
        session['user_fullname'] = f"{data['first_name']} {data['last_name']}"
        #return true so we can instantly log them in on successful registration
        return True



    # Read Users Models
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email }
        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            #if there was a user found by that email, make the result a class instance of it
            result = cls(result[0])
        #returns falsy if email was not found in db
        return result
    

    # Update Users Models



    # Delete Users Models

    #Validate Users
    @staticmethod
    def validate_user_registration(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[\W_]).+$')
        is_valid = True
        if len(data['first_name']) < 2:
            is_valid = False
            flash("Hold up! Your name can't be one letter!")
        if len(data['last_name']) < 2:
            is_valid = False
            flash("Hold up! Your name can't be one letter!")
        if User.get_user_by_email(data['email'].lower().strip()):
            is_valid = False
            flash('Nice try! That email is already in use...')
        if not EMAIL_REGEX.match(data['email']):
            if data['email'] == '':
                is_valid = False
                flash("Email can't be blank")
            else:
                is_valid = False
                flash("Invalid email address. Please enter a valid email.")
        if not re.match(PASSWORD_REGEX, data['password']):
            is_valid = False
            flash("Password requires at least 1 number and special character")
        if len(data['password']) < 8: 
            is_valid = False
            flash("Password must be longer than 8 characters!")
        if data['password'] != data['confirm_password']:
            is_valid = False
            flash('Passwords did not match...')
        if data['conditions'] != 'on':
            is_valid = False
            flash('You must accept the terms and conditions')
        return is_valid
    
    #Validate Login
    @staticmethod
    def validate_login(data):
        this_user = User.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['user_fullname'] = f"{this_user.first_name} {this_user.last_name}"
                return True
        flash('Sorry that login was incorrect, try again!')
        return False

    #Parse Registration Data
    @staticmethod
    def parse_registration_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['email'] = data['email'].lower().strip()
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data
