from flask.ext.mongoengine.wtf import model_form
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from models import * 
import re

shows = Blueprint('posts', __name__, template_folder='templates')

class ListView(MethodView):

    def get(self):
        shows = Show.objects()
        return render_template('list.html', shows=shows)

	

shows.add_url_rule('/', view_func=ListView.as_view('list'))
#posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
