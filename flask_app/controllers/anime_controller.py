from flask import Flask, render_template, redirect, request, session, flash

from flask_app import app

from flask_app.models.manga import Manga
from flask_app.models.anime import Anime
from flask_app.models.miscelaneos import Miscelaneos
from flask_app.models.commet import Comment
from flask_app.models.user import User

@app.route("/created_anime", methods = ["POST"])
def create_post_anime():
    if not Anime.validate_post_anime(request.form):
        return redirect("/usuario")
    
    Anime.save_anime(request.form)
    return redirect("/anime")

@app.route("/delete_post/<int:id>")
def delete_anime(id):
    dicc= {"id": id}
    Anime.delete_anime(dicc)
    return redirect("/anime")

@app.route("/anime")
def anime():
    dicc = {"id": session["user_id"]}
    user = User.get_by_id(dicc)
    posts = Anime.get_anime()
    return render_template("anime.html", user = user, posts=posts)

@app.route("/anime/<int:post_id>/comments", methods=['POST', 'GET'])
def create_comment_anime(post_id):
    if 'user_id' not in session:
        return redirect(request.url)

    if not Comment.validate_comment(request.form):
        return redirect(request.url)

    data = {
        'content': request.form['content'],
        'post_id': post_id,  # Obtener post_id de la ruta
        'user_id': session['user_id']
    }

    Comment.save(data)
    return redirect("/anime")

@app.route("/delete_comment_anime/<int:comment_id>", methods=["POST"])
def delete_comment_anime(comment_id):
    if 'user_id' not in session:
        return redirect("/")
    
    data = {"id": comment_id}
    Comment.delete_comment(data)
    return redirect("/anime")