from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Artist:
    def __init__(self,data):
        self.id = data['id']

        self.name = data['name']
        self.genre = data['genre']
        self.album = data['album']
        self.started = data['started']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


        self.user_id = data['user_id']

#=============================================================
#=============================================================

#VALIDATING THE ARTIST INFO

    @staticmethod
    def validate_Artist(artist):
        is_valid = True
        if len(artist['name']) < 1:
            flash("Artist name must be at least one character")
            is_valid = False
        if len(artist['genre']) < 1:
            flash("Genre must be at least one character")
            is_valid = False
        if len(artist['album']) < 1:
            flash("Favorite album's name must be at least one character")
            is_valid = False
        if artist['started'] == "":
            flash("Record when artist started")
            is_valid = False
        return is_valid

#=============================================================

#=============================================================

#SAVE THE CREATED ARTIST

    @classmethod
    def save_Artist(self,data):
        query = "INSERT INTO artists (name, genre, album, started, user_id, created_at) VALUES (%(name)s,%(genre)s,%(album)s,%(started)s,%(user_id)s,NOW());"
        results = connectToMySQL("Itunes_schema").query_db(query,data)
        return results

#=============================================================

#=============================================================
#GET ONE ARTIST
    @classmethod
    def one_Artist(cls,data):
        query = "SELECT * FROM artists WHERE id = %(id)s;"
        results = connectToMySQL("Itunes_schema").query_db(query,data)
        return cls(results[0])

#==============================================================

#==============================================================
#GET ALL THE ARTISTS 
    @classmethod
    def all_artists(self, data):
        query = "SELECT * FROM artists"
        results = connectToMySQL("Itunes_schema").query_db(query, data)
        return results

#=============================================================

#=============================================================
#UPDATE THE ARTIST INFO
    @classmethod
    def update_artist(self,data):
        query = "UPDATE artists SET name = %(name)s,genre = %(genre)s,album = %(album)s, started = %(started)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL("Itunes_schema").query_db(query, data)
#=============================================================

#=============================================================
#DELETES THE ARTIST FROM DB
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM artists WHERE id = %(id)s;"
        clear = connectToMySQL('Itunes_schema').query_db(query, data)
        return

#=============================================================