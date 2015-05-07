# -*- coding: utf-8 *-*

import string,random
import datetime

from flask import g,session,jsonify
from peewee import *
import jieba


from web.app import db, auth
from web.util import get_whoosh_ix
from .whoose_schema import InspirationSchema

class Label(db.Model):
    name        = CharField(unique=True)
    count       = IntegerField(default=0)

class Inspiration(db.Model):
    author      = ForeignKeyField(auth.User)
    content     = TextField()

    def make_keyword_index(self):
        ix = get_whoosh_ix("inspiration", InspirationSchema)
        writer = ix.writer()
        writer.add_document(content=self.content, id=self.id)
        writer.commit()


class LabelInspirationRelationShip(db.Model):
    inspiration = ForeignKeyField(Inspiration)
    label       = ForeignKeyField(Label)
    class Meta:
        primary_key = CompositeKey('inspiration', 'label')


class InspirationIndex(db.Model):
    keyword     = CharField()
    inspiration = ForeignKeyField(Inspiration)
    count       = IntegerField(default=1)
    class Meta:
        primary_key = CompositeKey('keyword', 'inspiration')

    def __str__(self):
        return "[%s]: <Inspiration: %s>  ==> %s" %(self.keyword, self.inspiration.id, self.count) 










