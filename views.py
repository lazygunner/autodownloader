# coding:utf-8

from flask.ext.mongoengine.wtf import model_form
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators
from flask import Blueprint, request, redirect, render_template, url_for, g
from flask.views import MethodView
from models import * 
import re
from update import find_show
from urllib import quote
#from flask.ext.login import login_user, logout_user, current_user, login_required
from autodownloader import app, lm, db

#@app.before_request
#def before_request():
#    g.user = current_user

shows = Blueprint('posts', __name__, template_folder='templates')

#@app.route('/')
class ListView(MethodView):
    
    @login_required
    def get(self):
        print 'aaaa'
        shows = Show.objects()
        user = 'Sign in'

        return render_template('list.html', shows=shows, user=user)

	def post(self):
		ori_name = request.form['show_name'].encode('utf-8')
		url_encode = quote(ori_name)
		print url_encode
		if url_encode != '':
			find_show(url_encode)
			return redirect('/')
		return redirect('/')

@lm.user_loader
def load_user(load_user_id):
    print load_user_id
    user = User.objects.get(user_id = load_user_id)
    print user.is_anonymous()
    return User.objects.get(user_id = load_user_id)

class LoginForm(Form):
    user_id = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password')

class LoginView(MethodView):
    
    #form = model_form(User, exclude=['nick_name', 'email', 'role', 'following']) 
    def get_context(self):
        form = LoginForm(request.form)
        context = {
            "form": form
        }
        return context

    def get(self):
        #if g.user is not None and g.user.is_authenticated():
        #    return redirect(url_for('/'))

        context = self.get_context()
        return render_template('login.html', **context)

    def post(self):
        if g.user is not None and g.user.is_authenticated():
            return redirect('/')

        context = self.get_context()
        form = context.get("form")
        if form.validate_on_submit():
            #session['remember_me'] = form.remember_me.data
            user = User.objects(user_id = form.user_id.data).first()
            if user == None:
                return redirect('/login')
            else:
                if user.check_password(form.password.data):
                    print 'login success'
                    db.session.add(user)
                    db.session.save()
                    remember_me = False
                    if 'remember_me' in session:
                        remember_me = session['remember_me']
                        session.pop('remember_me', None)
                    login_user(user, remember = remember_me)
                    return redirect('/')
                else:
                    print 'wrong password'
                    return redirect('/login')
        else:
            print 'validate failed'
            return redirect('/login')

        
        
shows.add_url_rule('/', view_func=ListView.as_view('list'))
#shows.add_url_rule('/login', view_func=LoginView.as_view('login'))
#posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
