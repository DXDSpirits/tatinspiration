# -*- coding: utf-8 *-*

import hashlib
import string,random
import hashlib
import datetime

from flask import g,session,jsonify

from web.util.db import db




class UserInfo(db.EmbeddedDocument):
    # 512 * 512, this is url
    avatar          = db.StringField(default="/static/pic/default-avatar.png") 

class UserSetting(db.EmbeddedDocument):
    theme           = db.StringField(default="default")

class User(db.Document):
    email           = db.StringField(required=True)
    password        = db.StringField(required=True)

    info            = db.EmbeddedDocumentField("UserInfo")
    setting         = db.EmbeddedDocumentField("UserSetting")
    create_time     = db.DateTimeField(default=datetime.datetime.now)

    permissions     = db.ListField(db.StringField()) # manage, db_admin
    
    meta = {
        'allow_inheritance': False,
        'index_types': False,
        'indexes': [
            {'fields': ['email'], 'unique': True},
        ]
    }

    @classmethod
    def get_user_by_id(cls, _id=None):
        if _id:
            return cls.objects(id=_id).first()

    @classmethod
    def get_user_by_email(cls, email=None):
        return cls.objects(email=email).first()

    @classmethod
    def register(cls,email=None, password=None):
        password = User.encode_password(password)
        return cls(email=email, 
                   password=password,
                   info=UserInfo(), 
                   setting=UserSetting()).save()

   

    @classmethod
    def is_valid(cls,email=None,password=None):
        password = User.encode_password(password)
        return cls.objects(email=email, 
                           password=password).first() is not None

    @classmethod
    def validate_user(cls, email=None, password=None):
        password = User.encode_password(password)
        return cls.objects(email=email,
                           password=password).first()

    @classmethod
    def get_users_by_username_startswith(cls, word=None, limit=15):
        return cls.objects(username__startswith=word)[:limit]

    @staticmethod
    def encode_password(password=""):
        password = hashlib.sha512(password)
        password.update("somethingreallysecret")
        return password.hexdigest()

    def to_dict(self):
        return {"id":str(self.id),
                "email":self.email
        }

class UserStarSentence(db.Document):
    user            = db.ReferenceField("User")
    sentence        = db.ReferenceField("Sentence")

    @classmethod
    def is_user_stared_this_week(cls, user=None):
        pass

    @classmethod
    def get_star_count_by_sentence(cls, sentence=None):
        pass














