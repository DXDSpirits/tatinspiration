# -*- coding: utf-8 -*-

from flask import render_template

from web.app import app
from web.model import User

@app.route('/')
def main():
    return render_template("main.html")

