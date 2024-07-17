from flask_app.config.mysqlconnection import connectToMySQL
#es el encargado de mostrar mensajes de error o msj en general

from flask import flash

import re 
#expresiones regulares, empatadar con un patron de texto
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    #metodo de clase crea un nuevo registro
    @classmethod
    def save(cls, form): #este form tendra un diccionario con toda la informacion del usuario
        query = "insert into users (first_name, last_name, email, password) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL("foro_publicaciones").query_db(query, form) #regresa el ID del nuevo registro
    
    #metodo que regresa objeto de usuario en base al email
    @classmethod
    def get_by_email(cls, form):  #este form tendra un diccionario con el email y password. cls es user.
        query = "select * from users where email = %(email)s"
        result = connectToMySQL("foro_publicaciones").query_db(query, form) #regresa lista de diccionario

        if len(result) <1: #revisa que la lista este vacia
            return False
        else:
            #regresa 1 registro
            #result = lista que tiene solo 1 diccionario con id, nombre, apellido, contraseña, etc. Nosotros queremos tener ese diccionario para obtener un objeto
            user = cls(result[0]) #cls por que en esa clase estamos, puede ser cls o user
            return user
        
    #metodo que valide la info que recibimos del form, es un metodo ayudante, no ingresa info
    @staticmethod
    def validate_user(form):
        is_valid = True
        # validamos que el nombre tenga al menos 2 caracteres
        if len(form["first_name"])<2:
            flash("First name must have at least 2 chars", "register") #el register se refiere a la categoria. Un mensaje y una categoria.
            is_valid = False
        
        if len(form["last_name"])<2:
            flash("Last name must have at least 2 chars", "register")
            is_valid = False

        if len(form["password"])<6:
            flash("Password must have at least 6 chars", "register")
            is_valid = False

        #validas que el correo sea unico, revisa si el correo ya esta comparando el tama;o de la lista. 0 es que no existe, sigual o mayor 1 es que esta
        query = "select * from users where email = %(email)s"
        result = connectToMySQL("foro_publicaciones").query_db(query, form)
        if len(result) >=1:
            flash("E-mail already registered", "register")
            is_valid = False

        #verificar las contraseñas
        if form["password"] != form["confirm"]: #aca se toma del name del form
            flash("Password do not match", "register")
            is_valid = False

        if not EMAIL_REGEX.match(form["email"]): #match empata una er con un texto, aca debe seguir el patron de correo
            flash("E-mail not valid", "register")
            is_valid = False

        return is_valid
    
    @classmethod
    def get_by_id(cls, data):  #este form tendra un diccionario con el email y password. cls es user.
        query = "select * from users where id = %(id)s"
        result = connectToMySQL("foro_publicaciones").query_db(query, data) #regresa lista de 1 diccionario, solo existe indice 0
        user = cls(result[0])
        return user



