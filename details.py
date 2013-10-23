from models import *
from flask.views import MethodView
from flask import Blueprint, render_template
from flask.ext.login import current_user

details = Blueprint('details', __name__, template_folder='templates')

class DetailView(MethodView):
    
    def get(self, show_id, format='HR-HDTV'):
        show = Show.objects.get(show_id=show_id)
        follow = 'anonymous'
        if current_user.is_anonymous():
            follow = 'anonymous'
        else:
            followings = len(Following.objects(user_id=current_user.id, show_id=show_id))
            if followings > 0:
                follow = 'unfollow'
            else:
                follow = 'follow'
                
        episodes_array = []
        for i in range(1,100):
            episodes = Episode.objects(show_id = show_id, format=format, season=i).order_by('+index')
            if len(episodes) > 0:
                episodes_array.append(episodes)
            else:
                break
        return render_template('detail.html', show=show, episodes_array = episodes_array, follow=follow)
        



details.add_url_rule('/details/<show_id>/', view_func=DetailView.as_view('details'))
