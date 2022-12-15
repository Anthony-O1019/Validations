from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
    
    #set up the registration for the user
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        return connectToMySQL('users_passwords').query_db(query, data)

    @classmethod
    def single_user(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        result = connectToMySQL('users_passwords').query_db(query,data)

        return cls(result[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        result = connectToMySQL('users_passwords').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def validate_user(cls, user):
        valid = True
        if len(user['first_name']) < 2:
            flash("Invalid First Name", "register")
            valid = False
        if len(user['last_name']) < 2:
            flash("Invalid Last Name", "register")
            valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            valid = False
        if len(user["email"]) < 8:
            flash("Invalid Email", "register")
            valid = False
        if len(user["password"]) < 8:
            flash("invalid Password", "register")
            valid = False
        return valid
