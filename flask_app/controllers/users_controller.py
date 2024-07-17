from flask import Flask, render_template, redirect, request, session, flash

from flask_app import app

from flask_app.models.user import User
from flask_app.models.manga import Manga
from flask_app.models.anime import Anime
from flask_app.models.miscelaneos import Miscelaneos

#tenemos encriptacion (no es tan segura) y hashing (mas segura, no se puede revertir y con esto usamos Bcrypt).
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/iniciar")
def iniciar():
    return render_template("iniciar.html")

#ruta que recibe el fomrulario
@app.route("/register", methods=["POST"])
def register():
    #validamos la info
    if not User.validate_user(request.form):
        return redirect("/")
    
    #encriptar contraseña
    pass_hash = bcrypt.generate_password_hash(request.form["password"])

    #creamos un diccionario con toda la info que recibidos del form, pero el passworrd llega haseado con el codigo de arriba
    form = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"], 
        "email": request.form["email"], 
        "password": pass_hash
    }

    id = User.save(form) #recibe el id del nuevo usario
    session["user_id"] = id #guardamos en sesion el id del usuario
    return redirect("/usuario")

@app.route("/usuario", methods=["POST" , "GET"])
def dashboard():
    #verificar la sesion para ingresar
    if "user_id" not in session:
        return redirect("/")
    
    dicc = {"id": session["user_id"]}
    user = User.get_by_id(dicc) #aca obtenemos el objeto user

    return render_template("index2.html", user = user) #envio a dashboard para que sea mostrado


@app.route("/acceso", methods=["POST"])
def login():
    #queremos vericar email y contrasena
    user = User.get_by_email(request.form) #recibo False o recibo un objeto

    if not user: #si user es falso
        flash("E-mail not found", "login")
        return redirect ("/iniciar") 
    
    #si user si es objeto user, debo comprobar las contraseñas
    if not bcrypt.check_password_hash(user.password, request.form["password"]): #password hasheado y pass no hasheado
        flash("Password incorrect", "login")
        return redirect ("/iniciar")

    session["user_id"] = user.id
    return redirect ("/usuario") 

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")