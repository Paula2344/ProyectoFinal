# utils.py

from flask_login import current_user

def is_logged_in():
    return current_user.is_authenticated
