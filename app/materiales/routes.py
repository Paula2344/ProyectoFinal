from flask import redirect, render_template, request,jsonify
import os
from werkzeug.utils import secure_filename
import app
from . import materiales_blueprint
from random import sample

# Directorio donde se guardarán las imágenes
UPLOAD_FOLDER = 'static/imagenes_material'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@materiales_blueprint.route('/agregar', methods=['GET', 'POST'])
def agregar_material():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        cantidad_stock = request.form['cantidad_stock']
        unidad_medida = request.form['unidad_medida']
        color = request.form['color']
        
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                nuevoNombreFile = recibeFoto(file)
                material = app.models.Material(nombre_material=nombre, imagen_material=nuevoNombreFile, descripcion=descripcion, precio=precio,
                            cantidad_stock=cantidad_stock, unidad_medida=unidad_medida, color=color)
                app.db.session.add(material)
                app.db.session.commit()
                return redirect('/materiales/listar')
    
    return render_template('agregar_material.html')

#Definir rutas
@materiales_blueprint.route('/listar')
def listar_materiales():
    materiales = app.models.Material.query.all()
    return render_template('listar_materiales.html', materiales=materiales)



# Ruta para editar un material (UPDATE)

@materiales_blueprint.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_material(id):
    material = app.models.Material.query.get(id)
    
    if request.method == 'POST':
        material.nombre_material = request.form['nombre']
        material.descripcion = request.form['descripcion']
        material.precio = request.form['precio']
        material.cantidad_stock = request.form['cantidad_stock']
        material.unidad_medida = request.form['unidad_medida']
        material.color = request.form['color']
        
        if 'imagen_material' in request.files:
            file = request.files['imagen_material']
            if file:
                filename = secure_filename(file.filename)
                if filename:
                    basepath = os.path.dirname(__file__)  # La ruta donde se encuentra el archivo actual
                    nuevoNombreFile = recibeFoto(file)
                    material.imagen_material = nuevoNombreFile

        app.db.session.commit()
        
        return redirect('/materiales/listar')
    
    return render_template('editar_material.html', material=material)


# Ruta para eliminar un material (DELETE)
@materiales_blueprint.route('/eliminar/<int:id>')
def eliminar_material(id):
    material = app.models.Material.query.get(id)
    
    if material:
        app.db.session.delete(material)
        app.db.session.commit()
    
    return redirect('/materiales/listar')


def recibeFoto(file):
    basepath = os.path.dirname(__file__)  # La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename)  # Nombre original del archivo

    extension = os.path.splitext(filename)[1]  # Capturando extensión del archivo
    nuevoNombreFile = stringAleatorio() + extension

    upload_path = os.path.join(basepath, './../' + UPLOAD_FOLDER, nuevoNombreFile)
    file.save(upload_path)

    return nuevoNombreFile

def stringAleatorio():
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud = 20
    secuencia = string_aleatorio.upper()
    resultado_aleatorio = sample(secuencia, longitud)
    string_aleatorio = "".join(resultado_aleatorio)
    return string_aleatorio