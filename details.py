from models import *
from flask.views import MethodView
from flask import Blueprint, render_template, request, redirect
from flask.ext.login import current_user

details = Blueprint('details', __name__, template_folder='templates')

class DetailView(MethodView):
    
    def get(self, show_id, format='HR-HDTV'):
        show = Show.objects.get(show_id=show_id)
        follow = 'anonymous'
        latest_index = 0
        if current_user.is_anonymous():
            follow = 'anonymous'
        else:

            followings = Following.objects(user_id=current_user.id, show_id=show_id)
            if len(followings) > 0:
                follow = 'unfollow'
                latest_index = followings[0].latest_season * 100 +  followings[0].latest_episode
            else:
                follow = 'follow'
                
        episodes_array = []
        for i in range(1, show.latest_season + 1):
            episodes = Episode.objects(show_id = show_id, format=format, season=i).order_by('+index')
            if len(episodes) > 0:
                episodes_array.append(episodes)
        return render_template('detail.html', show=show, episodes_array = episodes_array, follow=follow, latest_index=latest_index)
    
    def post(self, show_id):
        post_data = request.form
        print show_id
        follow = Following.objects(show_id=show_id, user_id=current_user.id)    
        if len(follow) > 0:
            follow[0].update(set__latest_season = post_data['latest_season'])
            follow[0].update(set__latest_episode = post_data['latest_episode'])
            follow[0].save()
        else:
            follow = Following()
            follow.show_id = show_id
            follow.user_id = current_user.id
            follow.latest_season = post_data['latest_season']
            follow.latest_episode = post_data['latest_episode']
            #following.show_format
            follow.save()

        return redirect(request.path)




details.add_url_rule('/details/<show_id>/', view_func=DetailView.as_view('details'))
