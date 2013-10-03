# coding:utf-8

from flask.ext.mongoengine.wtf import model_form
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from models import * 
import re
from update import find_show
from urllib import quote

shows = Blueprint('posts', __name__, template_folder='templates')

class ListView(MethodView):

	def get(self):
		shows = Show.objects()
		return render_template('list.html', shows=shows)
	def post(self):
		ori_name = request.form['show_name'].encode('utf-8')
		url_encode = quote(ori_name)
		print url_encode
		if url_encode != '':
			find_show(url_encode)
			return redirect('/')
		return redirect('/')

shows.add_url_rule('/', view_func=ListView.as_view('list'))
#posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
