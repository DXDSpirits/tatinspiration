# -*- coding: utf-8 -*-
import re
from flask import render_template, request, redirect, flash, session
from whoosh import qparser

from web.app import app, auth
from web.model import Label, Inspiration, LabelInspirationRelationShip, InspirationIndex
from web.util import get_whoosh_ix, q

@app.route('/')
def main():
    inspiration_list = Inspiration.select().order_by(Inspiration.id.desc()).limit(20)
    labels = Label.select()
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
        content = request.form.get("content") 

        ## make inspiration
        inspiration = Inspiration.create(author=user.id, content=content)
        ## we can defer this by using message-queue
        q.enqueue(inspiration.make_keyword_index)

        ## make labels
        label_name_set = set(filter(lambda s: len(s.strip()) > 0, request.values.getlist("labels")))
        label_list = [Label.get_or_create(name=label_name)[0] for label_name in label_name_set]

        ## make rs
        for label in label_list:
            LabelInspirationRelationShip.get_or_create(inspiration=inspiration, label=label)
        return redirect("/")

@app.route('/search')
def search():
    from web.model.whoose_schema import InspirationSchema
    ix = get_whoosh_ix("inspiration", InspirationSchema)
    keyword = request.args.get("keyword")
    ### do not consider splitting keyword firstly


    with ix.searcher() as searcher:
        parser = qparser.QueryParser("content", schema=ix.schema, group=qparser.OrGroup)
        search_expression = parser.parse(keyword)

        print "search_expression: %s"%search_expression

        results = searcher.search(search_expression)

        print "results: %s"%results

        inspiration_list = [ Inspiration.select().where(Inspiration.id==r["inspiration_id"]).get() \
                                     for r in results]
        return render_template("search.html",inspiration_list=inspiration_list)

















