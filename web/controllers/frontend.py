# -*- coding: utf-8 -*-

from flask import render_template, request

from web.app import app
from web.model import User

@app.route('/')
def main():
    return render_template("main.html")


@app.route('/register')
def user_register():
    username = request.form.get("username")
    password = request.form.get("password")
