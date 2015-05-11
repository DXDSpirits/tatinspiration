from flask.ext.script import Manager
from web.app import app, auth

manager = Manager(app)

@manager.command
def hello():
    return "hello"

@manager.command
def make_admin(username, password):
    admin = auth.User(username=username, email=username, admin=True, active=True)
    admin.set_password(password)
    admin.save()
    print "cool"

@manager.command
def make_user(username, password):
    user = auth.User(username=username, email=username, admin=False, active=True)
    user.set_password(password)
    user.save()
    print "cool"


if __name__ == "__main__":
    manager.run()