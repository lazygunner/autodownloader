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
from flask.ext.login import current_user
from autodownloader import app, db

#@app.before_request
#def before_request():
#    g.user = current_user

shows = Blueprint('posts', __name__, template_folder='templates')


class ListView(MethodView):
    
    def get(self):
        shows = Show.objects()
        user = 'Sign in'
        if not current_user.is_anonymous():
            user = current_user.email
        return render_template('list.html', shows=shows, user=user)

	def post(self):
		ori_name = request.form['show_name'].encode('utf-8')
		url_encode = quote(ori_name)
		print url_encode
		if url_encode != '':
			find_show(url_encode)
			return redirect('/')
		return redirect('/')

class IndexView(MethodView):
    
    @login_required
    def get(self):
        shows = []
        followings = Following.objects(user_id = current_user.id)

        for f in followings:
            show = Show.objects(show_id = f.show_id)[0]
            shows.append(show)
        if not current_user.is_anonymous():
            user = current_user.email
        return render_template('index.html', shows=shows, user=user)

	def post(self):
		ori_name = request.form['show_name'].encode('utf-8')
		url_encode = quote(ori_name)
		print url_encode
		if url_encode != '':
			find_show(url_encode)
			return redirect('/')
		return redirect('/')

@app.route('/follow/<follow_show_id>/', methods=['POST'])
@login_required
def follow(follow_show_id):
    following = Following()
    following.show_id = follow_show_id
    following.user_id = current_user.id
    #following.show_format
    following.save()
    return redirect('/')

@app.route('/unfollow/<follow_show_id>/', methods=['POST'])
@login_required
def unfollow(follow_show_id):
    following = Following.objects(show_id = follow_show_id, user_id = current_user.id)
    following.delete()
    return redirect('/index')

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
shows.add_url_rule('/index', view_func=IndexView.as_view('index'))
#shows.add_url_rule('/login', view_func=LoginView.as_view('login'))
#posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
