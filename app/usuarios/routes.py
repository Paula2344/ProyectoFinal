from flask import Blueprint, jsonify, render_template, redirect, url_for, flash,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
import random
import string
from datetime import datetime, timedelta
import app
#from app.models import Material
from . import usuario_blueprint
from flask import flash, url_for, render_template
from app.utils import is_logged_in


#from flask_bcrypt import generate_password_hash



@usuario_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('usuario_blueprint.dashboard'))

    if request.method == 'POST':
        correo_electronico = request.form['correo']
        contrasena = request.form['contrasena']
        usuario = app.models.Usuario.query.filter_by(correo_electronico=correo_electronico).first()

        if usuario.contrasena == contrasena or usuario.contraseña_provisional == contrasena:
            login_user(usuario)
            return jsonify({'status': 'success', 'message': 'Inicio de sesión exitoso'})
        else:
            return jsonify({'status': 'error', 'message': 'Credenciales incorrectas'})

    return render_template('login.html')

@usuario_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('usuario_blueprint.login'))

@usuario_blueprint.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        confirmar_correo = request.form['confirmar_correo']
        direccion = request.form['direccion']
        contrasena = request.form['contrasena']

        # Verificar la longitud y la presencia de al menos una letra mayúscula en la contraseña
        if len(contrasena) < 6 or not any(c.isupper() for c in contrasena):
            mensaje = 'La contraseña debe tener al menos 6 caracteres y contener al menos una letra mayúscula.'
            return jsonify({'status': 'danger', 'message': mensaje})

        # Genera un código de verificación aleatorio
        codigo_verificacion = str(random.randint(1000, 9999))

        # Verificar si el correo ya está en uso
        usuario_existente = app.models.Usuario.query.filter_by(correo_electronico=correo).first()

        if usuario_existente:
            mensaje = 'El correo que intentas registrar ya está registrado por otro usuario, intenta de nuevo con otra dirección de correo.'
            return jsonify({'status': 'danger', 'message': mensaje})

        elif correo != confirmar_correo:
            mensaje = 'Los correos electrónicos no coinciden, revísalos y vuelve a intentar.'
            return jsonify({'status': 'danger', 'message': mensaje})

        else:
            nuevo_usuario = app.models.Usuario(nombre=nombre, apellido=apellido, telefono=telefono,
                                               correo_electronico=correo, direccion=direccion, contrasena=contrasena, rol_id=1, codigo_verificacion=codigo_verificacion)
            app.db.session.add(nuevo_usuario)
            app.db.session.commit()

            # Envía el código de verificación por correo electrónico
            message = Message('Código de Verificación', sender='tu_correo@tudominio.com', recipients=[correo])
            message.body = f'Tu código de verificación es: {codigo_verificacion}'
            app.mail.send(message)

            mensaje = '¡Registro exitoso! Tu código de verificación ha sido enviado a tu correo electrónico.'
            return jsonify({'status': 'success', 'message': mensaje})

    return render_template('registro.html')



@usuario_blueprint.route('/verificar', methods=['GET', 'POST'])
def verificar():
    if request.method == 'POST':
        correo = request.form['correo']
        codigo_ingresado = request.form['codigo_verificacion']
        usuario_actual = app.models.Usuario.query.filter_by(correo_electronico=correo).first()

        if usuario_actual and codigo_ingresado == usuario_actual.codigo_verificacion:
            usuario_actual.correo_verificado = True
            app.db.session.commit()
            return jsonify({'status': 'success', 'message': 'El código de verificación fue validado, ¡Bienvenido!'})
        else:
            resultado = f'Código de verificación incorrecto para el correo electrónico {correo}. Inténtalo nuevamente.'
            return jsonify({'status': 'danger', 'message': resultado})

    return render_template('verificar.html')


@usuario_blueprint.route('/dashboard')
def dashboard():
    if not is_logged_in():
        flash('Error: tienes que acceder al sistema para realizar esta acción.', 'error')
        return render_template("error.html", message="Error: tienes que acceder al sistema para realizar esta acción.")
    usuarios = app.models.Usuario.query.all()
    materialFk = app.models.Material.query.all()
    if current_user.rol.nombre_rol == 'admin':
        return render_template('admin_dashboar.html',materialFk=materialFk,usuarios=current_user)
    elif current_user.rol.nombre_rol == 'cliente':
        return render_template('user_dashboard.html',materialFk=materialFk,usuarios=current_user)
    else:
        return "Rol no válido para el dashboard"



    

def actualizar_perfil(usuario_id, nombre, apellido, correo, direccion,contrasena):
    # Buscar el usuario por su ID
    usuario = app.models.Usuario.query.get(usuario_id)

    if usuario:
        # Actualizar los campos del perfil
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.correo_electronico = correo
        usuario.direccion = direccion
        usuario.contrasena = contrasena
        # Guardar los cambios en la base de datos
        app.db.session.commit()
        return True, "Perfil actualizado exitosamente."
    else:
        return False, "Usuario no encontrado."

    
@usuario_blueprint.route('/perfil/<int:id>', methods=['GET', 'POST'])
def perfil(id):
    if not is_logged_in():
        flash('Error: tienes que acceder al sistema para realizar esta acción.', 'error')
        return render_template("error.html", message="Error: tienes que acceder al sistema para realizar esta acción.")
    usuario = app.models.Usuario.query.get(id)

    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nuevo_apellido = request.form['apellido']
        nuevo_correo = request.form['correo']
        nueva_direccion = request.form['direccion']
        nueva_contrasena = request.form['contrasena']

        resultado, mensaje = actualizar_perfil(id,nuevo_nombre, nuevo_apellido, nuevo_correo, nueva_direccion, nueva_contrasena)

        if resultado:
            return "Informacion actualizada correctamente"
            
        else:
            return "error"

    return render_template('perfil.html',usuario=usuario)

@usuario_blueprint.route('/perfil-actualizar/<int:id>', methods=['GET', 'POST'])
def perfil_actualizar(id):
    if not is_logged_in():
        flash('Error: tienes que acceder al sistema para realizar esta acción.', 'error')
        return render_template("error.html", message="Error: Tienes que acceder al sistema para realizar esta acción.")
    usuario = app.models.Usuario.query.get(id)

    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nuevo_apellido = request.form['apellido']
        nuevo_correo = request.form['correo']
        nueva_direccion = request.form['direccion']
        nueva_contrasena = request.form['contrasena']

        # Verificar la longitud de la contraseña
        if len(nueva_contrasena) < 6:
            mensaje = 'La contraseña debe tener al menos 6 caracteres.'
            return jsonify({'status': 'error', 'message': mensaje})

        # Verificar la cantidad de mayúsculas en la contraseña
        if sum(1 for c in nueva_contrasena if c.isupper()) < 2:
            mensaje = 'La contraseña debe tener al menos dos mayúsculas.'
            return jsonify({'status': 'error', 'message': mensaje})

        # Resto de tu lógica para actualizar el perfil
        resultado, mensaje = actualizar_perfil(id, nuevo_nombre, nuevo_apellido, nuevo_correo, nueva_direccion, nueva_contrasena)

        if resultado:
            return jsonify({'status': 'success', 'message': 'Información actualizada correctamente'})
        else:
            return jsonify({'status': 'error', 'message': 'Error al actualizar la información'})

    return render_template('perfilActualizar.html', usuario=usuario)


def generar_contraseña_aleatoria(longitud=8):
    caracteres = string.ascii_letters + string.digits
    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña

@usuario_blueprint.route('/olvidaste_contraseña', methods=['GET', 'POST'])
def olvidaste_contraseña():
    if request.method == 'POST':
        correo_electronico = request.form.get('email')
        if correo_electronico:
            # Genera una contraseña provisional
            contraseña_provisional = generar_contraseña_aleatoria()

            # Almacena la contraseña provisional en la base de datos del usuario
            usuario = app.models.Usuario.query.filter_by(correo_electronico=correo_electronico).first()
            if usuario:
                usuario.contraseña_provisional = contraseña_provisional
                app.db.session.commit()

                # Envía el correo electrónico
                mensaje = Message('Restablecimiento de contraseña', recipients=[correo_electronico])
                mensaje.body = f"Tu nueva contraseña es: {contraseña_provisional}"

                try:
                    app.mail.send(mensaje)
                    flash('Se ha enviado una contraseña provisional a tu correo electrónico.', 'success')
                    return redirect(url_for('usuario_blueprint.olvidaste_contraseña'))  # Redirige a la misma página
                except Exception as e:
                    flash('No se pudo enviar la contraseña provisional. Verifica tu dirección de correo electrónico.', 'danger')
            else:
                flash('No se encontró un usuario con este correo electrónico.', 'danger')

    return render_template('olvidaste_contraseña.html')


@usuario_blueprint.route('/registerAdmin', methods=['GET', 'POST'])
def registroAdmin():
    if not is_logged_in():
        flash('Error: tienes que acceder al sistema para realizar esta acción.', 'error')
        return render_template("error.html", message="Error: Tienes que acceder al sistema para realizar esta acción.")
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        direccion = request.form['direccion']
        contrasena = request.form['contrasena']

        # Genera un código de verificación aleatorio
        codigo_verificacion = str(random.randint(1000, 9999))

        # Verificar si el correo ya está en uso
        usuario_existente = app.models.Usuario.query.filter_by(correo_electronico=correo).first()

        if usuario_existente:
            flash('El correo electrónico ya está registrado. Por favor, utiliza otro correo.', 'danger')
            
        else:
            nuevo_usuario = app.models.Usuario(nombre=nombre, apellido=apellido, telefono=telefono,
                                 correo_electronico=correo, direccion=direccion, contrasena=contrasena, rol_id=1,codigo_verificacion=codigo_verificacion)
            app.db.session.add(nuevo_usuario)
            app.db.session.commit()

    
        return redirect(url_for('usuario_blueprint.dashboard'))

    return render_template('registrarAdmin.html')



class LoginForm(FlaskForm):
    id = IntegerField('ID')
    submit = SubmitField('Submit')