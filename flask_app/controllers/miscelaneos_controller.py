from flask import Flask, render_template, redirect, request, session, flash

from flask_app import app

#Importamos los modelos
from flask_app.models.manga import Manga
from flask_app.models.anime import Anime
from flask_app.models.miscelaneos import Miscelaneos
from flask_app.models.commet import Comment
from flask_app.models.user import User


@app.route("/created_miscelaneos", methods = ["POST"])
def create_post_miscelaneos():
    if not Miscelaneos.validate_post_miscelaneos(request.form):
        return redirect("/usuario")
    
    Miscelaneos.save_miscelaneos(request.form)
    return redirect("/miscelaneos")

@app.route("/delete_post/<int:id>")
def delete_miscelaneos(id):
    dicc= {"id": id}
    Miscelaneos.delete_miscelaneos(dicc)
    return redirect("/miscelaneos")

@app.route("/miscelaneos")
def miscelaneos():
    dicc = {"id": session["user_id"]}
    user = User.get_by_id(dicc) #aca obtenemos el objeto user
    posts = Miscelaneos.get_miscelaneos()
    return render_template("miscelaneos.html", user = user, posts=posts)

@app.route("/miscelaneos/<int:post_id>/comments", methods=['POST', 'GET'])
def create_comment_miscelaneos(post_id):
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
    return redirect("/miscelaneos")

@app.route("/delete_comment_miscelaneos/<int:comment_id>", methods=["POST"])
def delete_comment_miscelaneos(comment_id):
    if 'user_id' not in session:
        return redirect("/")
    
    data = {"id": comment_id}
    Comment.delete_comment(data)
    return redirect("/miscelaneos")