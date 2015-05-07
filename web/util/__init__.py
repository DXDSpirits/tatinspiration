# -*- coding: utf-8 -*-
import os
from functools import wraps

from flask import session, request, redirect, url_for
import whoosh.index
from whoosh.filedb.filestore import FileStorage

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
        if ix.get(schemaName) is None:
            # we index per model.
            wi = os.path.join(web.config.conf.WHOOSH_BASE, schemaName)
            if whoosh.index.exists_in(wi):
                ix[schemaName] = whoosh.index.open_dir(wi)
            else:
                if not os.path.exists(wi):
                    os.makedirs(wi)
                ix[schemaName] = whoosh.index.create_in(wi, schema)
        return ix.get(schemaName)

    return _

get_whoosh_ix = _get_whoosh_ix()




