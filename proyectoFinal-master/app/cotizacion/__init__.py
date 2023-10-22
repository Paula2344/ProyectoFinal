#Dependencia para hacer un blueprint/paquete
from flask import Blueprint

#Definir paquete de productos
cotizacion_blueprint = Blueprint ('cotizacion_blueprint', __name__, url_prefix ='/cotizacion', template_folder = 'templates')

from . import routes