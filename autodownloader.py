# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':"shows"}
app.config["SECRET_KEY"] = "kalashinikov"

db = MongoEngine(app)
lm = LoginManager()
lm.init_app(app)

def register_blueprints(app):
    from views import shows
    app.register_blueprint(shows)


register_blueprints(app)

from update import thread
thread()



app.debug=True

if __name__ == '__main__':
    app.run()


