import os
import logging

from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask_peewee.auth import Auth
from flask_peewee.db import Database
import config.conf as conf

app = Flask(__name__)

app.config.from_object("web.config.conf")

### config log
@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

db = Database(app)
# needed for authentication
auth = Auth(app, db)

# assets = Environment(app)
# assets.versions = 'hash:32'
# main_js = Bundle("main_bundle.js", 
#                  output='dist/main_bundle.%(version)s.js')
# assets.register('js_all', main_js)

# all_css = Bundle("style.css", 
#                  output='dist/main.%(version)s.css')
# assets.register('css_all', all_css)



@app.before_request
def something_before_request():
    pass

import controllers
import web.admin


# app.jinja_env.filters['markdown']  = markdown_text
