# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager, login_required
from flask.ext.security import Security, MongoEngineUserDatastore, utils
from flask_mail import Mail
import datetime

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':"shows"}
app.config["SECRET_KEY"] = "kalashinikov"

# flask security
#app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['SECURITY_PASSWORD_SALT'] = 'gunner'
# After 'Create app'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'xdream420'
app.config['MAIL_PASSWORD'] = '17097448ak'
app.config['MAIL_DEBUG'] = False
mail = Mail(app)
db = MongoEngine(app)

def register_blueprints(app):
    from views import shows
    app.register_blueprint(shows)


register_blueprints(app)

from models import User, Role
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)


#@app.before_first_request
def create_user():
    user_datastore.create_user(email='abcd', password=utils.encrypt_password('password'), confirmed_at=datetime.datetime.now(), nick_name='aa')


from update import thread
    thread()


app.debug=True

if __name__ == '__main__':
    app.run()


