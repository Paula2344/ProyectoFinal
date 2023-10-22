#dependencia de flask
from flask import Flask
from flask import render_template,url_for,session
from flask_login import LoginManager
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from app.config_mail import MailConfig
import random
import string
#Dependencia de configuracion 
from .config import Config #El punto es para indicarle a python que los archivos estan en el mismo paquete

#dependencia de modelos
from flask_sqlalchemy import SQLAlchemy

#dependencia de las migraciones
from flask_migrate import Migrate

#crear el objeto flask
app = Flask(__name__)

#Configuracion del objeto flask
app.config.from_object(Config)
#Configuracion del objeto email
app.config.from_object(MailConfig)
mail = Mail(app)

#Importar el modulo 
from app.materiales import materiales_blueprint
from app.ordenes import ordenes_blueprint
from app.usuarios import usuario_blueprint
from app.catalogo import catalogo_blueprint

#Vincular submodulos del proyecto
app.register_blueprint(materiales_blueprint)
app.register_blueprint(ordenes_blueprint)
app.register_blueprint(usuario_blueprint)
app.register_blueprint(catalogo_blueprint)

#crear el objeto de modelos:


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'




#crear el obejeto de migracion 
migrate=Migrate(app,db)

@app.route('/')
def index():
    return render_template('index.html' )


from .models import RolUsuario,Usuario,Material,Cotizacion,OrdenServicio

@login_manager.user_loader
def load_user(user_id):
    # Implementa la lógica para cargar un usuario basado en el user_id proporcionado
    try:
        return Usuario.query.get(int(user_id))
    except Exception as e:
        return None 
    