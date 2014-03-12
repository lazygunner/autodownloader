from flask import Blueprint, request, redirect, render_template, url_for, g, abort
from flask.views import MethodView
from weibo_sdk import APIClient

APP_KEY = '2516902990'
APP_SECRET = '1a38af944a3018aa9151c01b6eef1894'
SITE_URI = 'http://tv.xdream.info'

AUTH_CALLBACK_URL = SITE_URI + '/weiboapi/auth-callback'
TOKEN_CALLBACK_URL = SITE_URI + '/weiboapi/token-callback'

weiboapi = Blueprint('weiboapi', __name__, template_folder='templates')

class WeiboAuth(MethodView):
    
    def get(self):
    
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=AUTH_CALLBACK_URL)
        url = client.get_authorize_url()

        return redirect(url)

class AuthCallback(MethodView):
    def get(self):
        code = request.args.get('code')
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=TOKEN_CALLBACK_URL)
        r = client.request_access_token(code)
        access_token = r.access_token
        expires = r.expires
	import json
        return json.dumps(r)

class TokenCallback(MethodView):
    def get(self):
	pass

weiboapi.add_url_rule('/auth', view_func=WeiboAuth.as_view('auth'))
weiboapi.add_url_rule('/auth-callback', view_func=AuthCallback.as_view('callback'))
weiboapi.add_url_rule('/token-callback', view_func=TokenCallback.as_view('token-callback'))
