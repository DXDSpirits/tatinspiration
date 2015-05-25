# -*- coding: utf-8 -*-
import os
from functools import wraps
from json import dumps
from flask import session, request, redirect, url_for, make_response
import whoosh.index
from whoosh.filedb.filestore import FileStorage
from redis import Redis
from rq import Queue

import web.config.conf

from .whoose_redis_storage import RedisStore
_redis = Redis(**web.config.conf.REDIS)
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

    ix = {}
    def _(schemaName, schema):
        storage = RedisStore(_redis, schemaName)
        # print "ix.get(schemaName):%s"%ix.get(schemaName)
        if ix.get(schemaName) is None:
            # print "_redis.exists(schemaName):%s"%_redis.exists(schemaName) 
            if storage.folder_exists(schemaName): ## problem here
                ix[schemaName] = storage.open_index()
            else:
                # print "create Index"
                ix[schemaName] = storage.create_index(schema)
        return ix.get(schemaName)

    return _
def compress_jsonify(*args, **kwargs):
    response = make_response(dumps(dict(*args, **kwargs), indent=None, sort_keys=False, ensure_ascii=False))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = 200
    return response

q = Queue(connection=_redis)
get_whoosh_ix = _get_whoosh_ix()


