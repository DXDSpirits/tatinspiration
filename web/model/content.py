# -*- coding: utf-8 *-*

import string,random
import datetime

from flask import g,session,jsonify

from web.app import db


# class Section(db.Document):
#     name        = db.StringField(required=True)
#     count       = db.IntField()


# class Sentence(db.Document):
#     content     = db.StringField()
#     author      = db.ReferenceField("User")

#     def post_to_section(self, section=None):
#         if not section:
#             return ;

#         section.count += 1
#         section.save()
#         self.save()










