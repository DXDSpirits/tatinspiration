# -*- coding: utf-8 -*-

from functools import wraps

from flask import session, request, redirect, url_for


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


