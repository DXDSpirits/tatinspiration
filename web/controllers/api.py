# -*- coding: utf-8 -*-
from flask_peewee.rest import RestAPI, RestResource, UserAuthentication
from web.app import app, auth
from web.model import Label, Inspiration, LabelInspirationRelationShip, InspirationIndex


user_auth = UserAuthentication(auth)

api = RestAPI(app, default_auth=user_auth)


# setup user
register_class = [Label, Inspiration, LabelInspirationRelationShip, auth.User, InspirationIndex]
for klass in register_class:
    api.register(klass)



api.setup()