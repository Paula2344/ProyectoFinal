from flask import render_template, request, flash
from flask_mail import Message
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import app
from . import cotizacion_blueprint
from reportlab.lib import colors


@cotizacion_blueprint.route('/generar_cotizacion/<int:id>', methods=['GET', 'POST'])
def generar_cotizacion(id):
    orden_servicio = app.models.OrdenServicio.query.get(id)

    if orden_servicio is None:
        flash('La orden de servicio no se encontró', 'error')
        return render_template('error.html')

    materiales = app.models.Material.query.all()
    correo_enviado = False  # Variable para indicar si se ha enviado el correo
    material = None
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        correo_electronico = request.form.get('correo_electronico')
        detalles_adicionales = request.form.get('detallesAdicionales')
        materialFk = request.form.get('materialFk')
        tipoServicio = request.form.get('tipoServicio')
        descripcion = request.form.get('descripcion')
        incluye = request.form.get('incluye')
        precioTotal = request.form.get('precioTotal')

        # Consulta la base de datos para obtener el nombre del material
        material = app.models.Material.query.get(materialFk)

        if material:
            nombre_material = material.nombre_material
        else:
            nombre_material = "Material no encontrado"  # Manejo de error si el material no se encuentra en la base de datos

        # Crear un nuevo objeto PDF
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter), leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)

        # Crear un Story para agregar elementos al PDF
        story = []

        # Estilo para el título de la cotización
        estilos = getSampleStyleSheet()
        estilo_titulo = estilos["Title"]
        estilo_titulo.alignment = 1  # Centrar el título
        story.append(Paragraph("<u>Cotización Tapiplas</u>", estilo_titulo))
        story.append(Spacer(1, 12))  # Espacio en blanco

        # Crear una tabla para mostrar los datos
        data = [
            ["Nombre:", nombre],
            ["Teléfono:", telefono],
            ["Correo Electrónico:", correo_electronico],
            ["Detalles Adicionales:", detalles_adicionales],
            ["Material:", nombre_material],
            ["Tipo de Servicio:", tipoServicio],
            ["¿Qué incluye?:", incluye],
            ["Precio Total:", precioTotal]
        ]

        # Configurar la tabla
        table = Table(data, colWidths=[120, 350], style=[('ALIGN', (0, 0), (0, -1), 'RIGHT'), ('ALIGN', (1, 0), (1, -1), 'LEFT')])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(table)

        # Construir el PDF
        doc.build(story)
        pdf_buffer.seek(0)

        # Envía el correo con el PDF adjunto
        msg = Message('Cotización', sender='tu_correo@gmail.com', recipients=[correo_electronico])
        msg.body = 'Hola, esta es tu cotizacion con nuestra empresa Tapiplas. Te esperamos.'
        msg.attach('cotizacion.pdf', 'application/pdf', pdf_buffer.read())
        app.mail.send(msg)

        correo_enviado = True  # Marcar el correo como enviado

    return render_template('generar_cotizacion.html', orden_servicio=orden_servicio, materiales=materiales, correo_enviado=correo_enviado)
