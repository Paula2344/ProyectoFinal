from flask import Blueprint, render_template, redirect, url_for, flash,request

from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
#from flask_mail import Mail, Message
import random
import string
from datetime import datetime, timedelta
import app
#from app.models import Material
from . import usuario_blueprint
from flask import flash, url_for, render_template
#from flask_bcrypt import generate_password_hash


@usuario_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('usuario_blueprint.dashboard'))

    if request.method == 'POST':
        correo_electronico = request.form['correo']
        contrasena = request.form['contrasena']
        usuario = app.models.Usuario.query.filter_by(correo_electronico=correo_electronico).first()

        if usuario and usuario.contrasena == contrasena:
            login_user(usuario)
            return redirect(url_for('usuario_blueprint.dashboard'))
        else:
            flash('Credenciales incorrectas', 'danger')  # Mensaje de error

    return render_template('login.html')


@usuario_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('usuario_blueprint.login'))


def generar_token_verificacion():
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(30))

def enviar_correo_verificacion(usuario):
    token = usuario.token_verificacion
    mensaje = Message('Verifica tu correo electrónico', sender='tu_correo@gmail.com', recipients=[usuario.correo_electronico])
    mensaje.body = f'Por favor, haz clic en el siguiente enlace para verificar tu correo electrónico: {url_for("usuario_blueprint.verificar_correo", token=token, _external=True)}'
    app.mail.send(mensaje)
@usuario_blueprint.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        direccion = request.form['direccion']
        contrasena = request.form['contrasena']

        # Verificar si el correo ya está en uso
        usuario_existente = app.models.Usuario.query.filter_by(correo_electronico=correo).first()

        if usuario_existente:
            flash('El correo electrónico ya está registrado. Por favor, utiliza otro correo.', 'danger')
            

        nuevo_usuario = app.models.Usuario(nombre=nombre, apellido=apellido, telefono=telefono,
                                 correo_electronico=correo, direccion=direccion, contrasena=contrasena, rol_id=1)
        app.db.session.add(nuevo_usuario)
        app.db.session.commit()
        flash('Registrado correctamente', 'success')
        return redirect(url_for('usuario_blueprint.login'))

    return render_template('registro.html')




@usuario_blueprint.route('/dashboard')
@login_required
def dashboard():
    if current_user.rol.nombre_rol == 'admin':
        return render_template('admin_dashboar.html')
    elif current_user.rol.nombre_rol == 'cliente':
        return render_template('user_dashboard.html')
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

    
@usuario_blueprint.route('/perfil/<int:usuario_id>', methods=['GET', 'POST'])
def perfil(usuario_id):
    usuario = app.models.Usuario.query.get(usuario_id)

    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nuevo_apellido = request.form['apellido']
        nuevo_correo = request.form['correo']
        nueva_direccion = request.form['direccion']
        nueva_contrasena = request.form['contrasena']

        resultado, mensaje = actualizar_perfil(usuario_id,nuevo_nombre, nuevo_apellido, nuevo_correo, nueva_direccion, nueva_contrasena)

        if resultado:
            return "Informacion actualizada correctamente"
            
        else:
            return "error"

    return render_template('perfil.html',usuario_id=usuario_id)







@usuario_blueprint.route('/verificar/<token>')
def verificar_correo(token):
    # Verificar la validez del token
    if es_token_valido(token):
        # Marcar la cuenta como verificada en la base de datos
        usuario = app.models.Usuario.query.filter_by(token_verificacion=token).first()
        if usuario:
            usuario.cuenta_verificada = True
            usuario.token_verificacion = None  # Opcional: borrar el token de verificación después de usarlo
            app.db.session.commit()

            flash('Tu correo electrónico ha sido verificado con éxito. Puedes iniciar sesión ahora.', 'success')
            return redirect(url_for('usuario_blueprint.login'))  # Reemplaza 'usuarios.login' con la ruta real de inicio de sesión
        else:
            flash('No se encontró ningún usuario asociado a este token de verificación.', 'danger')
            return redirect(url_for('usuario_blueprint.login'))  # Reemplaza 'usuarios.login' con la ruta real de inicio de sesión
    else:
        flash('El token de verificación es inválido o ha expirado. Por favor, solicita un nuevo correo de verificación.', 'danger')
        return redirect(url_for('usuario_blueprint.login'))
    


