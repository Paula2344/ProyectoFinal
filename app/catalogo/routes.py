from flask import redirect, render_template, request
import app
from app import config
#from app.models import cataogo
from . import catalogo_blueprint

#Para subir archivo tipo foto al servidor
import os
from werkzeug.utils import secure_filename 
from random import sample



@catalogo_blueprint.route('/listar')
def listar_catalogo():
    catalogo = app.models.Catalogo.query.all()
    return render_template('listar_catalogo.html', catalogo=catalogo)



@catalogo_blueprint.route('/registrar', methods=['GET','POST'])
def addCatalogo():
    return render_template('agregar_catalogo.html')


@catalogo_blueprint.route('/agregar', methods=['GET', 'POST'])
def agregar_catalogo():
    if request.method == 'POST':
        nombre_catalogo = request.form['nombre_catalogo']

        if(request.files['imagen_catalogo'] !=''):
            file     = request.files['imagen_catalogo'] #recibiendo el archivo
            nuevoNombreFile = recibeFoto(file)
        catalogo = app.models.Catalogo(nombre_catalogo=nombre_catalogo, imagen_catalogo=nuevoNombreFile )
        
        app.db.session.add(catalogo)
        app.db.session.commit()
        return redirect('/catalogo/listar')
    
    return render_template('agregar_catalogo.html')

# Ruta para editar un material (UPDATE)
@catalogo_blueprint.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_catalogo(id):
    catalogo = app.models.Catalogo.query.get(id)

    if request.method == 'POST':
        catalogo.nombre_catalogo = request.form['nombre_catalogo']

        if(request.files['imagen_catalogo'] !=''):
            file     = request.files['imagen_catalogo'] #recibiendo el archivo
            catalogo.imagen_catalogo = recibeFoto(file)
            app.db.session.commit()
        
        
        return redirect('/catalogo/listar')
    
    return render_template('editar_catalogo.html', catalogo=catalogo)

# Ruta para eliminar un material (DELETE)
@catalogo_blueprint.route('/eliminar/<int:id>')
def eliminar_catalgo(id):
    catalogo = app.models.Catalogo.query.get(id)
    
    if catalogo:
        app.db.session.delete(catalogo)
        app.db.session.commit()
    
    return redirect('/catalogo/listar')


        
def recibeFoto(file):
    print(file)
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFile     = stringAleatorio() + extension
    #print(nuevoNombreFile)
        
    upload_path = os.path.join (basepath,'./../static/imagenes_Catalogo', nuevoNombreFile) 
    file.save(upload_path)

    return nuevoNombreFile



def stringAleatorio():
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio
