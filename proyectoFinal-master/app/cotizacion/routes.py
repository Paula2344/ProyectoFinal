holaaaaaaaaaaaa
from flask import redirect, render_template, request
import app
#from app.models import Material
from . import cotizacion_blueprint

#Definir rutas
@cotizacion_blueprint.route('/listar')
def listar_materiales():
    cotizacion = app.models.Cotizacion.query.all()
    return render_template('listar_cotizacion.html', cotizacion=cotizacion)

# Ruta para agregar un nuevo material (CREATE)
@cotizacion_blueprint.route('/agregar', methods=['GET', 'POST'])
def agregar_cotizacion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        correo_electronico = request.form['correo_electronico']
        ciudad = request.form['ciudad']
        tipoServicio = request.form['tipoServicio']
        detallesAdicionales = request.form['color']
        cotizacion = app.models.Cotizacion(nombre=nombre, telefono=telefono, correo_electronico=correo_electronico,
                            ciudad=ciudad, tipoServicio=tipoServicio,detallesAdicionales=detallesAdicionales)
        
        app.db.session.add(cotizacion)
        app.db.session.commit()
        return redirect('/cotizacion/listar')
    
    return render_template('agregar_cotizacion.html')

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
