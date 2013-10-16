import datetime
from flask import url_for
from autodownloader import db
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required 
from flask.ext.login import make_secure_token
from mongoengine import signals

class Show(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = db.DateTimeField()
    show_name = db.StringField(max_length=255, required=True)
    show_id = db.StringField(max_length=255, required=True)
    show_format = db.StringField(default='HR-HDTV', required=True)
    latest_season = db.IntField(default=0)
    latest_episode = db.IntField(default=0)
    poster = db.StringField(max_length=255)
#    episodes = db.ListField(db.EmbeddedDocumentField('Episode'))

    meta = {
        'allow_inheritance': True,
        'indexes': ['-show_id'],
        'ordering': ['-latest_season','-latest_episode']
    }

class Episode(db.Document):
    updated_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    format = db.StringField(max_length=255, required=True)
#    type = db.StringField(max_length=255)#HR-HDTV include hr_mkv,mp4_mkv,ori_mkv,ori_mp4 4 types
    index = db.IntField()
    show_id = db.StringField(max_length=10, required=True)
    season = db.IntField()
    episode = db.IntField()
    ed2k_link = db.StringField()

    meta = {
        'allow_inheritance': True,
        'indexes':['format', '-season', '-episode'],
        'ordering': ['-index']
    }

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document):
#    user_id = db.StringField(max_length=255)
    password = db.StringField(verbose_name="Password", max_length=255, required=True)
    nick_name = db.StringField(max_length=20, unique=True)
    email = db.StringField(max_length=255, required=True, unique=True)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    current_login_at = db.DateTimeField()
    current_login_ip = db.StringField()
    last_login_at = db.DateTimeField()
    last_login_ip = db.StringField()
    login_count = db.IntField()
    following = db.ListField(db.EmbeddedDocumentField('Following'))
    
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return True
    def is_active(self):
        return self.active
    def get_id(self):
        return unicode(self.id)
    def get_auth_token(self):
        return make_secure_token(self.user_id, self.password)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Following(db.EmbeddedDocument):
    show_id = db.StringField(max_length=255, required=True)
    show_format = db.StringField(default='HR-HDTV', required=True)
    latest_season = db.IntField(default=0)
    latest_episode = db.IntField(default=0)

