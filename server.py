#pipenv install flask pymysql flask-bcrypt

from flask_app import app

from flask_app.controllers import users_controller
from flask_app.controllers import manga_controller
from flask_app.controllers import anime_controller
from flask_app.controllers import miscelaneos_controller

if __name__== "__main__":
    app.run(debug=True)


#acambiar todos los models y controller por cada tema
#debo ver como buscar dentro de toda la info que tenga.