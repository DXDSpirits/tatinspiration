# -*- coding: utf-8 *-*

import string,random
import datetime

from flask import g,session,jsonify
from peewee import *
import jieba


from web.app import db, auth


class Label(db.Model):
    name        = CharField(unique=True)
    count       = IntegerField(default=0)

class Inspiration(db.Model):
    author      = ForeignKeyField(auth.User)
    content     = TextField()

    def make_keyword_index(self):
        keyword_list = jieba.cut_for_search(self.content)
        for keyword in keyword_list:
            ii, created = InspirationIndex.get_or_create(keyword=keyword, inspiration=self)
            if not created:
                ii.count += 1
                ii.save()


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










