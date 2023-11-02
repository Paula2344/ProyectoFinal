# En el blueprint de "cotizaciones"
from flask import render_template, redirect, url_for, request, flash, send_file
from . import cotizacion_blueprint
from flask_mail import Message  # Importa Flask-Mail para enviar correos
from reportlab.pdfgen import canvas
from io import BytesIO
import app

@cotizacion_blueprint.route('/generar_cotizacion/<int:id>', methods=['GET', 'POST'])
def generar_cotizacion(id):
    orden_servicio = app.models.OrdenServicio.query.get(id)

    if orden_servicio is None:
        flash('La orden de servicio no se encontró', 'error')
        return render_template('error.html')  # Reemplaza 'nombre_de_la_ruta_de_error' con la ruta de manejo de errores adecuada

    if request.method == 'POST':
        # Procesa los datos del formulario de cotización
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        correo_electronico = request.form.get('correo_electronico')
        detalles_adicionales = request.form.get('detallesAdicionales')
        materialFK = request.form.get('materialFk')

        # Genera el PDF de la cotización
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer)

        c.drawString(100, 750, f'Nombre: {nombre}')
        c.drawString(100, 730, f'Teléfono: {telefono}')
        c.drawString(100, 710, f'Correo Electrónico: {correo_electronico}')
        c.drawString(100, 690, f'Detalles Adicionales: {detalles_adicionales}')
        c.drawString(100, 690, f'Material: {materialFK}')
        # Puedes agregar más contenido al PDF según tus necesidades

        c.showPage()
        c.save()

        pdf_buffer.seek(0)
        return send_file(pdf_buffer, as_attachment=True, download_name=f'cotizacion_{orden_servicio.id}.pdf', mimetype='application/pdf')

    return render_template('generar_cotizacion.html', orden_servicio=orden_servicio)
