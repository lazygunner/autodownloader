from flask import Blueprint, request, redirect, render_template, url_for, g, abort
from flask.views import MethodView
from weibo_sdk import APIClient

APP_KEY = '2516902990'
APP_SECRET = '1a38af944a3018aa9151c01b6eef1894'
SITE_URI = 'http://tv.xdream.info'


weiboapi = Blueprint('weiboapi', __name__, template_folder='templates')

class WeiboAuth(MethodView):
    
    def get(self):
    
        CALLBACK_URL = 'SITE_URI' + url_for('weiboapi.callback')
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        url = client.get_authorize_url()

        return redirect(url)

class WeiboCallback(MethodView):
    def callback(self):
        code = request
        r = client.request_access_token(code)
        access_token = r.access_token
        expires = r.expires
        print 1 + 'a'

weiboapi.add_url_rule('/auth', view_func=WeiboAuth.as_view('auth'))
weiboapi.add_url_rule('/callback', view_func=WeiboAuth.as_view('callback'))
