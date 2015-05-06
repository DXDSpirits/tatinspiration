from flask import session
from flask_peewee.admin import Admin

from web.app import app, auth
from web.model import Label, Inspiration, LabelInspirationRelationShip

admin = Admin(app, auth)

register_class = [Label, Inspiration, LabelInspirationRelationShip, auth.User]

for klass in register_class:
    admin.register(klass)
admin.setup()