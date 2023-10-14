from flask import redirect, render_template, request
import app
#from app.models import Material
from . import materiales_blueprint

#Definir rutas
@materiales_blueprint.route('/listar')
def listar_materiales():
    materiales = app.models.Material.query.all()
    return render_template('listar_materiales.html', materiales=materiales)

# Ruta para agregar un nuevo material (CREATE)
@materiales_blueprint.route('/agregar', methods=['GET', 'POST'])
def agregar_material():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        cantidad_stock = request.form['cantidad_stock']
        unidad_medida = request.form['unidad_medida']
        color = request.form['color']
        material = app.models.Material(nombre_material=nombre, descripcion=descripcion, precio=precio,
                            cantidad_stock=cantidad_stock, unidad_medida=unidad_medida,color=color)
        
        app.db.session.add(material)
        app.db.session.commit()
        return redirect('/materiales/listar')
    
    return render_template('agregar_material.html')

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

