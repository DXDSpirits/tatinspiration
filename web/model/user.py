# -*- coding: utf-8 *-*

import hashlib
import string,random
import hashlib
import datetime

from flask import g,session,jsonify

from web.app import db
from peewee import *




class User(db.Model):
    email           = CharField()
    password        = CharField()

    create_time     = DateTimeField(default=datetime.datetime.now)













