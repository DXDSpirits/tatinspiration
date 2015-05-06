from flask import session
from flask_peewee.admin import Admin

from web.app import app, auth

admin = Admin(app, auth)

admin.register(auth.get_user_model())
admin.setup()