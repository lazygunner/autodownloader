import datetime
from flask import url_for
from  autodownloader import db

class Show(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    updated_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    show_name = db.StringField(max_length=255, required=True)
    show_id = db.StringField(max_length=255, required=True)
    show_format = db.StringField(default='HR-HDTV', required=True)
    latest_season = db.DecimalField(default=0)
    latest_episode = db.DecimalField(default=0)
    episodes = db.ListField(db.EmbeddedDocumentField('Episode'))

    meta = {
        'allow_inheritance': True,
        'indexes': ['-show_id'],
        'ordering': ['-latest_season','-latest_episode']
    }

class Episode(db.EmbeddedDocument):
    updated_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    format = db.StringField(max_length=255, required=True)
    index = db.DecimalField()
    season = db.DecimalField()
    episode = db.DecimalField()
    ed2k_link = db.StringField()

    meta = {
        'allow_inheritance': True,
        'ordering': ['-index']
    }





