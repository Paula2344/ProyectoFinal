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