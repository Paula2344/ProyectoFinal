from flask import Blueprint

#Definir paquete de productos
catalogo_blueprint = Blueprint ('catalogo_blueprint', __name__, url_prefix ='/catalogo', template_folder = 'templates')

from . import routes

