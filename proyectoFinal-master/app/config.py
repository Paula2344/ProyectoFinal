class Config:
    #definir 'cadena de conexion'(connectionString)
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/proyectos'
    SQLALCHEMY_TRACK_NOTIFICATIONS = False
    SECRET_KEY = 'PGLO_MANITO'
    MAIL_SERVER = 'smtp.gmail.com'  # Reemplaza con tu servidor de correo
    MAIL_PORT = 587
    MAIL_USERNAME = 'tu_correo@gmail.com'  # Reemplaza con tu correo
    MAIL_PASSWORD = 'tu_contraseña'  # Reemplaza con tu contraseña['MAIL_USE_TLS'] = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'tucorreo@gmail.com'
    MAIL_USE_TLS = True



    

