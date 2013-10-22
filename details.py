from models import *
from flask.views import MethodView
from flask import Blueprint, render_template

details = Blueprint('details', __name__, template_folder='templates')

class DetailView(MethodView):
    
    def get(self, show_id, format='HR-HDTV'):
        show = Show.objects.get(show_id=show_id)
        episodes_array = []
        for i in range(1,100):
            episodes = Episode.objects(show_id = show_id, format=format, season=i).order_by('+index')
            if len(episodes) > 0:
                episodes_array.append(episodes)
            else:
                break
        return render_template('detail.html', show=show, episodes_array = episodes_array)
        



details.add_url_rule('/details/<show_id>/', view_func=DetailView.as_view('detail'))
