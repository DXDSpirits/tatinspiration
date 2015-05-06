# -*- coding: utf-8 -*-
import re
from flask import render_template, request, redirect, flash, session

from web.app import app, auth
from web.model import Label, Inspiration, LabelInspirationRelationShip

@app.route('/')
def main():
    inspiration_list = Inspiration.select().order_by(Inspiration.id.desc()).limit(20)
    return render_template("main.html",inspiration_list=inspiration_list)


@app.route('/login', methods=["POST"])
def boring_user_login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = auth.authenticate(username, password)
    if user:
        auth.login_user(user)
        session.pop('_flashes', None)
        flash('login successfully')
        return redirect("/write")

    else:
        flash('Incorrect username or password')
        return redirect("/")


@app.route('/write', methods=["GET", "POST"])
@auth.login_required
def write_inspiration():
    if request.method == "GET":
        return render_template("write.html")
    else:
        user = auth.get_logged_in_user()
        content = request.form.get("content") 

        ## make inspiration
        inspiration = Inspiration.create(author=user, content=content)

        ## make labels
        label_str = request.form.get("labels")
        #### use set to avoid duplicate name
        label_name_set = set(re.split(r"\W+", label_str))
        label_list = [Label.get_or_create(name=label_name)[0] for label_name in label_name_set]

        ## make rs
        for label in label_list:
            LabelInspirationRelationShip.get_or_create(inspiration=inspiration, label=label)
        return redirect("/")







