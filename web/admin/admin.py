from flask import session
from flask.ext.admin import (Admin, BaseView, 
                            AdminIndexView, expose)
from flask.ext.admin.contrib.mongoengine import ModelView

from web.app import app
from web.model import User

class Accessiable():
    def is_accessible(self):
        return True


class UserView(Accessiable, ModelView):
    can_delete = False
    column_filters = ['email']


admin = Admin(app, name='%s Admin'%app.config["SITENAME"])
admin.add_view(UserView(User))
