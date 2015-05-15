from flask.ext.script import Manager
from web.app import app, auth

manager = Manager(app)

@manager.command
def make_admin(username, password):
    ''' make admin '''
    admin = auth.User(username=username, email=username, admin=True, active=True)
    admin.set_password(password)
    admin.save()
    print "cool"

@manager.command
def make_user(username, password):
    ''' make user '''
    user = auth.User(username=username, email=username, admin=False, active=True)
    user.set_password(password)
    user.save()
    print "cool"

@manager.command
def reindex():
    '''this command will reindex search index'''
    from web.model import Inspiration
    from web.util import _redis, q

    ## delete the redis key
    _redis.delete("RedisStore:inspiration")

    ##
    for inspiration in Inspiration.select():
        q.enqueue(inspiration.make_keyword_index, inspiration.labels)
    print "workers are working on reindexing, type`rqinfo` to check progress"

@manager.command
def recount():
    '''this command will recount label'''
    from web.util import  q
    from web.model import Label, LabelInspirationRelationShip
    labels = Label.select()
    for label in labels:
        # label.count = LabelInspirationRelationShip.
        q.enqueue(label.recount)
    print "workers are working on recount, type`rqinfo` to check progress"



if __name__ == "__main__":
    manager.run()






