# -*- coding: utf-8 *-*

import string,random
import datetime

from flask import g,session,jsonify
from peewee import *
import jieba


from web.app import db, auth
from web.util import get_whoosh_ix

class Label(db.Model):
    name        = CharField(unique=True)
    count       = IntegerField(default=0)

class Inspiration(db.Model):
    author      = ForeignKeyField(auth.User)
    content     = TextField()

    def make_keyword_index(self):
        from .whoose_schema import InspirationSchema
        ix = get_whoosh_ix("inspiration", InspirationSchema)
        writer = ix.writer()
        writer.add_document(content=self.content, inspiration_id=unicode(self.id))
        writer.commit()

    def remake_keyword_index(self):
        from .whoose_schema import InspirationSchema
        ix = get_whoosh_ix("inspiration", InspirationSchema)
        writer = ix.writer()
        writer.update_document(content=self.content, inspiration_id=unicode(self.id))
        writer.commit()

    @classmethod
    def post(cls, inpiration_kwg=None, label_list=None):
        inpiration_kwg = inpiration_kwg or {}
        label_list = label_list or []
        inspiration = Inspiration.create(**inpiration_kwg)
        for label in label_list:
            LabelInspirationRelationShip.get_or_create(inspiration=inspiration, label=label)
            label.count += 1
            label.save()
        return inspiration

    def modify(self, content="", label_list=None):
        self.content = content
        label_list = label_list or []

        old_label_RS_list = LabelInspirationRelationShip.select(LabelInspirationRelationShip.label)\
                                            .where(LabelInspirationRelationShip.inspiration==self.id)
        for rs in old_label_RS_list:
            if rs.label not in label_list:
                rs.label.count -= 1;
                rs.label.save()
                rs.delete()

        for label in label_list:
            _, created = LabelInspirationRelationShip.get_or_create(inspiration=self, label=label)
            if created:
                label.count += 1
                label.save()
        self.save()

    def to_json(self):
        return {
            "id": self.id,
            "content": self.content,
        }



class LabelInspirationRelationShip(db.Model):
    inspiration = ForeignKeyField(Inspiration)
    label       = ForeignKeyField(Label)
    class Meta:
        primary_key = CompositeKey('inspiration', 'label')










