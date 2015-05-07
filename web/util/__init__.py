# -*- coding: utf-8 -*-
import os
from functools import wraps

from flask import session, request, redirect, url_for
import whoosh.index
from whoosh.filedb.filestore import FileStorage
from redis import Redis
from rq import Queue

from .whoose_redis_storage import RedisStore
_redis = Redis()
#http://flask.pocoo.org/docs/patterns/viewdecorators/
def login_required(f):
    from web.model import User
    from web.app import app
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = request.path
        if "user" not in session:
            flash("You need to login first!", "danger")
            return redirect(url_for('login', r=r))
        else:
            g.user = User.get_user_by_id(session["user"]["id"])
            if g.user is None:
                return redirect(url_for('login', r=r))
        def inject_user():
            if "user" not in g:
                g.user = User.get_user_by_id(session.get("user", {}).get("id"))
            return dict(cur_user=g.user)
        app.template_context_processors[None].append(inject_user)
        return f(*args, **kwargs)

    return decorated_function

def _get_whoosh_ix():
    # refer to flask-whooshalchemy
    # use FileStorage

    import web.config.conf
    ix = {}
    def _(schemaName, schema):
        storage = RedisStore(_redis, schemaName)
        if ix.get(schemaName) is None:
            # we index per model.
            print 'storage.file_exists(""): %s'%storage.file_exists("")

            # if storage.file_exists(""): ## problem here
            ix[schemaName] = storage.open_index()
            # else:
            #     ix[schemaName] = storage.create_index(schema)
        return ix.get(schemaName)

    return _


q = Queue(connection=_redis)
get_whoosh_ix = _get_whoosh_ix()


