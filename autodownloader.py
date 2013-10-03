# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.mongoengine import MongoEngine
import threading

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':"shows"}
app.config["SECRET_KEY"] = "kalashinikov"

db = MongoEngine(app)

def register_blueprints(app):
    from views import shows
    app.register_blueprint(shows)

def thread():
    from update import update_thread
    threading.Thread(target = update_thread, args = (), name = 'update_thread').start()
 

register_blueprints(app)
thread()
   
app.debug=True

if __name__ == '__main__':
    app.run()


