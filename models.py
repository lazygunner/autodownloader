import datetime
from flask import url_for
from  autodownloader import db

class Show(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    show_name = db.StringField(max_length=255, required=True)
    show_id = db.StringField(max_length=255, required=True)
    show_format = db.StringField(default='HR-HDTV', required=True)
    latest_season = db.IntField(default=0)
    latest_episode = db.IntField(default=0)
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





