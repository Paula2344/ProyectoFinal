from flask import Blueprint

#Definir paquete de productos
usuario_blueprint = Blueprint ('usuario_blueprint', __name__, url_prefix ='/usuarios', template_folder = 'templates')

from . import routes