from flask_peewee.rest import RestAPI, RestResource, UserAuthentication
from web.app import app, auth


user_auth = UserAuthentication(auth)

api = RestAPI(app, default_auth=user_auth)


# setup user
api.register(auth.get_user_model())




api.setup()