# -*- coding: utf-8 -*-
from flask_peewee.rest import RestAPI, RestResource, UserAuthentication
from web.app import app, auth
from web.model import Label, Inspiration, LabelInspirationRelationShip


user_auth = UserAuthentication(auth)

api = RestAPI(app, default_auth=user_auth)

class InspirationResource(RestResource):
    def prepare_data(self, obj, data):
        data["labels"] = [l.to_json() for l in obj.labels]
        return data
api.register(Inspiration, InspirationResource)

class LabelInspirationRelationShipResource(RestResource):
    paginate_by = 200
    def prepare_data(self, obj, data):
        inspiration_id = data["inspiration"]
        inspiration = Inspiration.select().where(Inspiration.id == inspiration_id).first()
        data["inspiration"] = inspiration.to_json()
        return data
api.register(LabelInspirationRelationShip, LabelInspirationRelationShipResource)



# setup user
register_class = [Label, auth.User]
for klass in register_class:
    api.register(klass)


api.setup()

