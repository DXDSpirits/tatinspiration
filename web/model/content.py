# -*- coding: utf-8 *-*

import string,random
import datetime

from flask import g,session,jsonify
from peewee import *

from web.app import db, auth


class Label(db.Model):
    name        = CharField(unique=True)
    count       = IntegerField(default=0)

class Inspiration(db.Model):
    author      = ForeignKeyField(auth.User)
    content     = TextField()

class LabelInspirationRelationShip(db.Model):
    inspiration = ForeignKeyField(Inspiration)
    label       = ForeignKeyField(Label)
    class Meta:
        primary_key = CompositeKey('inspiration', 'label')










