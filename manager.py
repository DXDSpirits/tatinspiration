from flask.ext.script import Manager
from web.app import app

manager = Manager(app)

@manager.command
def hello():
    return "hello"

@manager.command
def make_demo():
    from web.model import User
    user = User()
    user.register(email="demo",
                  password="demo")
    print "cool"


if __name__ == "__main__":
    manager.run()