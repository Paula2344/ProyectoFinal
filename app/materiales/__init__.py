#Dependencia para hacer un blueprint/paquete
from flask import Blueprint

#Definir paquete de productos
materiales_blueprint = Blueprint ('materiales_blueprint', __name__, url_prefix ='/materiales', template_folder = 'templates')

from . import routes