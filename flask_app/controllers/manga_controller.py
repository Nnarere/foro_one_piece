from flask import Flask, render_template, redirect, request, session, flash

from flask_app import app

from flask_app.models.manga import Manga
from flask_app.models.anime import Anime
from flask_app.models.miscelaneos import Miscelaneos
from flask_app.models.commet import Comment
from flask_app.models.user import User

@app.route("/created_manga", methods = ["POST"])
def create_post_manga():
    if not Manga.validate_post_manga(request.form):
        return redirect("/usuario")
    
    Manga.save_manga(request.form)
    return redirect("/manga")

@app.route("/manga/delete_post/<int:id>")
def delete(id):
    dicc= {"id": id}
    Manga.delete_manga(dicc)
    return redirect("/manga")

@app.route("/manga")
def manga():
    dicc = {"id": session["user_id"]}
    user = User.get_by_id(dicc) 
    posts = Manga.get_manga()
    return render_template("manga.html", user = user, posts=posts)

@app.route("/manga/<int:post_id>/comments", methods=['POST', 'GET'])
def create_comment_manga(post_id):
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
    return redirect("/manga")

@app.route("/delete_comment_manga/<int:comment_id>", methods=["POST"])
def delete_comment_manga(comment_id):
    if 'user_id' not in session:
        return redirect("/")
    
    data = {"id": comment_id}
    Comment.delete_comment(data)
    return redirect("/manga")