from flask import session
from flask_peewee.admin import Admin

from web.app import app, auth
from web.model import Label, Inspiration, LabelInspirationRelationShip, InspirationIndex

admin = Admin(app, auth)

register_class = [Label, Inspiration, LabelInspirationRelationShip, auth.User, InspirationIndex]

for klass in register_class:
    admin.register(klass)
admin.setup()