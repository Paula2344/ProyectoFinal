from flask import render_template, request, flash
from flask_mail import Message
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
import app
from . import cotizacion_blueprint
from reportlab.platypus import PageTemplate, Frame, Image

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
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=landscape(letter),
            leftMargin=50,
            rightMargin=50,
            topMargin=50,
            bottomMargin=50
        )

        # Crear un Story para agregar elementos al PDF
        story = []

        # Agrega la imagen al inicio del PDF centrada
        image_path = 'app/static/assets/img/title.png'
        pdf_image = ImageReader(image_path)
        image_width, image_height = pdf_image.getSize()

        # Ajusta el tamaño de la imagen según tus preferencias
        nuevo_ancho = 200
        nueva_altura = 100

        image = Image(image_path, width=nuevo_ancho, height=nueva_altura)

        # Puedes ajustar la posición de la imagen si es necesario
        image.drawHeight = nueva_altura
        image.drawWidth = nuevo_ancho

        story.append(Spacer(1, 12))  # Espacio en blanco
        story.append(image)
        story.append(Spacer(1, 12))  # Espacio en blanco


        # Crear estilos de párrafo
        estilo_izquierda = ParagraphStyle(
            'izquierda',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=25,
            textColor=colors.black,
            fontName='Times-Bold',
            leftIndent=50,
            fontWeight='bold',
            spaceAfter=5,
            backColor=colors.white,
        )

        estilo_derecha = ParagraphStyle(
            'derecha',
            parent=getSampleStyleSheet()['BodyText'],
            fontSize=25,
            textColor=colors.black,
            fontName='Times-Bold',
            rightIndent=50,
            fontWeight='bold',
            spaceAfter=5,
            backColor=colors.white,
        )

        # Agrega los datos como párrafos al Story con espaciadores horizontales
        data = [
            ["Datos Solicitados", "Datos de la cotizacion"],
            ["Nombre:", nombre],
            ["Teléfono:", telefono],
            ["Correo Electrónico:", correo_electronico],
            ["Detalles Adicionales:", detalles_adicionales],
            ["Material:", nombre_material],
            ["Tipo de Servicio:", tipoServicio],
            ["¿Qué incluye?:", incluye],
            ["Precio Total:", precioTotal],
        ]

        # Agrega la tabla al Story con fondo transparente
        table = Table(data, colWidths=[200, 480], rowHeights=40)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'), 
            ('RIGHTPADDING', (1, 0), (1, -1), 25),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.Color(1, 1, 1, alpha=0)),
        ]))
        story.append(table)

        # Agrega la imagen de fondo a todas las páginas del PDF
        image_path = 'app/static/assets/img/fondoPdf2.png'
        pdf_image = ImageReader(image_path)
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        template = PageTemplate(id='test', frames=[frame], onPage=lambda canvas, doc, pdf_image=pdf_image: canvas.drawImage(pdf_image, 0, 0, width=doc.pagesize[0], height=doc.pagesize[1]))
        doc.addPageTemplates([template])

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
