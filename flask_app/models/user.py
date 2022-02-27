from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import artist
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.artists = []

#========================================================================
#validates the registration entry

    @staticmethod
    def validate_User(user):
        is_valid = True
        if len(user['first_name']) < 5:
            flash("First name must be at least five characters.")
            is_valid = False
            
        if len(user['last_name']) < 5:
            flash("Last name must be at least five characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("That email is invalid.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least eight characters.")
            is_valid = False
        if ( user['confirm_password']!= user['password']):
            flash("Passwords don't match")
            is_valid = False

        return is_valid

#========================================================================

#========================================================================
#Method to save our user

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        results = connectToMySQL("Itunes_schema").query_db(query,data)
        return results
#========================================================================

#========================================================================
#Method to grab user by email

    @classmethod
    def get_by_email(cls,data):
        query= "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("Itunes_schema").query_db(query,data)
        #check to see if there is no email already existing in result
        if len(result) < 1:
            return False
        return cls(result[0])

#========================================================================

#========================================================================
# Method to grab user by id

    @classmethod
    def get_by_id(cls,data):
        query= "SELECT * FROM users WHERE id = %(id)s;"
        user = connectToMySQL("Itunes_schema").query_db(query,data)
        return cls( user[0] )

#========================================================================

#========================================================================
#PARSE THE DATA JOINING THE ARTISTS TO THE USER

    @classmethod
    def user_get_artists(cls,data):
        query = "SELECT * FROM users LEFT JOIN artists ON artists.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('Itunes_schema').query_db( query , data )
        users = cls( results[0] )
        for row_from_db in results:
            artist_data = {
                'id' : row_from_db['artists.id'],
                'name' : row_from_db['name'],
                'genre' : row_from_db['genre'],
                'album' : row_from_db['album'],
                'started' : row_from_db['started'],
                'created_at' : row_from_db['artists.created_at'],
                'updated_at' : row_from_db['artists.updated_at'],
                'user_id' : row_from_db['user_id']
            }
            users.artists.append(artist.Artist(artist_data))
        return users

#========================================================================