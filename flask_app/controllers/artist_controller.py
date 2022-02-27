from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.artist import Artist

#===================================================
#ROUTE THE RENDERS ADD PAGE

@app.route('/add_artist')
def add_artist():
    if "user_id" not in session:
        flash("please login/ register before entering the site!")
        return redirect("/")

    data = {
        "id" : session["user_id"]
    }
    user = User.get_by_id(data)
    return render_template("add_artist.html", user = user)

#===================================================

#===================================================
#ROUTE THAT PROCESSES THE POST METHOD TO ADD ARTIST

@app.route('/adding_artist', methods = ['POST'])
def adding_artist():

    data = {
        'name' : request.form['name'],
        'genre' : request.form['genre'],
        'album' : request.form['album'],
        'started' : request.form['started'],
        'user_id' : session['user_id']
    }
    if Artist.validate_Artist(request.form):
        Artist.save_Artist(data)
        return redirect("/dashboard")

    return redirect('/add_artist')

#===================================================

#===================================================
#ROUTE TO RENDER THE UPDATE PAGE

@app.route("/edit/<int:id>")
def edit_artist(id):
    if "user_id" not in session:
        flash("please login/ register before entering the site!")
        return redirect("/")

    data = {
        "id" : id,
    }

    artist = Artist.one_Artist(data)
    return render_template("edit_artist.html", artist = artist)

#===================================================

#===================================================
#ROUTE PROCESSING THE EDIT POST METHOD

@app.route('/editing/<int:id>', methods=['POST'])
def editing_artist(id):
    data ={
        'id' : id,
        'name' : request.form['name'],
        'genre' : request.form['genre'],
        'album' : request.form['album'],
        'started' : request.form['started'],
        'user_id' : session['user_id']
    }
    if Artist.validate_Artist(request.form):
        Artist.update_artist(data)
        return redirect("/dashboard")
    
    return redirect('/edit/%(id)s')

#===================================================

#===================================================

#ROUTE THAT RENDERS ONE ARTIST PAGE

@app.route('/artist/<int:id>')
def show_artist(id):
    if "user_id" not in session:
        flash("please login/ register before entering the site!")
        return redirect("/")
    data = {
        'id' : id
    }
    artist = Artist.one_Artist(data)
    return render_template("one_artist.html", artist = artist)
#===================================================

#===================================================
#DELETE ARTIST
@app.route("/artist/<int:id>/delete")
def delete_artist(id):
    data = {
        "id" : id
    }
    Artist.delete(data)
    return redirect('/dashboard')
#===================================================

