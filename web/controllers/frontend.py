# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash, session

from web.app import app, auth
from web.model import User

@app.route('/')
def main():
    return render_template("main.html")


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


@app.route('/write')
def write_inspiration():
    return render_template("main.html")


