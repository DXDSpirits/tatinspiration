# -*- coding: utf-8 -*-
import re
from flask import render_template, request, redirect, flash, session, jsonify
from whoosh import qparser

from web.app import app, auth
from web.model import Label, Inspiration, LabelInspirationRelationShip
from web.util import get_whoosh_ix, q

@app.route('/')
def main():
    inspiration_list = Inspiration.select().order_by(Inspiration.id.desc()).limit(20)
    labels = Label.select().order_by(Label.count.desc())
    return render_template("main.html",inspiration_list=inspiration_list, labels=labels)


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
        labels = Label.select()

        return render_template("write.html", labels=labels)
    else:
        user = auth.get_logged_in_user()
        content = request.form.get("content", "").strip()
        if len(content) < 5:
            flash("no enough words in content area")
            return redirect("/write")
        

        ## make labels
        label_name_set = set(filter(lambda s: len(s.strip()) > 0, request.values.getlist("labels")))
        label_list = [Label.get_or_create(name=label_name)[0] for label_name in label_name_set]
        ## make inspiration
        inspiration = Inspiration.post(inpiration_kwg={"author":user.id, "content":content}, label_list=label_list)
        ## we can defer this by using message-queue
        q.enqueue(inspiration.make_keyword_index, label_list)
        ## make rs
        flash("make inspiration successfully")
        return redirect("/")

@app.route('/inspiration/<int:inspiration_id>/modify', methods=["GET", "POST"])
@auth.login_required
def modify_inspiration(inspiration_id):
    inspiration = Inspiration.select().where(Inspiration.id==inspiration_id).get()
    if request.method == "GET":
        labels = Label.select()
        return render_template("modify.html", 
                               labels=labels,
                               inspiration=inspiration)
    else:
        content = request.form.get("content")
        label_name_set = set(filter(lambda s: len(s.strip()) > 0, request.values.getlist("labels")))
        label_list = [Label.get_or_create(name=label_name)[0] for label_name in label_name_set]
        inspiration.modify(content=content, label_list=label_list)
        q.enqueue(inspiration.remake_keyword_index, label_list)
        flash("modify inspiration successfully")
        return redirect("/")


@app.route('/api/inspiration/<int:inspiration_id>/modify', methods=["POST"])
@auth.login_required
def api_modify_inspiration(inspiration_id):
    inspiration = Inspiration.select().where(Inspiration.id==inspiration_id).get()
    content = request.form.get("content")
    label_name_set = set(filter(lambda s: len(s.strip()) > 0, request.values.getlist("labels")))
    label_list = [Label.get_or_create(name=label_name)[0] for label_name in label_name_set]
    inspiration.modify(content=content, label_list=label_list)
    q.enqueue(inspiration.remake_keyword_index, label_list)
    return jsonify(rcode=200)

@app.route('/api/nolabel-inspiration/')
def nolabel_inspiration():
    LIR = LabelInspirationRelationShip
    LIR_list = LIR.select(LIR.inspiration).distinct()

    inspiration_list = Inspiration.select().where(Inspiration.id.not_in(LIR_list))

    inspiration_json = [inspiration.to_json() for inspiration in inspiration_list]

    return jsonify({"objects": inspiration_json})








