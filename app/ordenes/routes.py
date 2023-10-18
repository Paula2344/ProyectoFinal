from datetime import datetime
from flask import redirect, render_template, request
from . import ordenes_blueprint
import app 

@ordenes_blueprint.route('/listar')
def listar_ordenes():
    ordenes = app.models.OrdenServicio.query.all()
    return render_template('listar_ordenes.html', ordenes=ordenes)

# Ruta para agregar una nueva orden de servicio (CREATE)

@ordenes_blueprint.route('/agregar', methods=['GET', 'POST'])
def agregar_orden():
    if request.method == 'POST':
        fecha_orden_servicio = datetime.strptime(request.form['fecha_orden_servicio'], '%Y-%m-%d')
        usuario_id = request.form['usuario_id']
        
        orden = app.models.OrdenServicio(fecha_orden_servicio=fecha_orden_servicio, usuario_id=usuario_id)
        
        app.db.session.add(orden)
        app.db.session.commit()
        
        return redirect('/ordenes/listar')
    
    usuarios = app.models.Usuario.query.all()
    return render_template('agregar_orden.html', usuarios=usuarios)

# Ruta para editar una orden de servicio (UPDATE)
@ordenes_blueprint.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_orden(id):
    orden = app.models.OrdenServicio.query.get(id)
    
    if request.method == 'POST':
        orden.fecha_orden_servicio = datetime.strptime(request.form['fecha_orden_servicio'], '%Y-%m-%d')
        orden.usuario_id = request.form['usuario_id']
        
        app.db.session.commit()
        
        return redirect('/ordenes/listar')
    
    usuarios = app.models.Usuario.query.all()
    return render_template('editar_orden.html', orden=orden, usuarios=usuarios)

# Ruta para eliminar una orden de servicio (DELETE)
@ordenes_blueprint.route('/eliminar/<int:id>')
def eliminar_orden(id):
    orden = app.models.OrdenServicio.query.get(id)
    
    if orden:
        app.db.session.delete(orden)
        app.db.session.commit()
    
    return redirect('/ordenes/listar')
