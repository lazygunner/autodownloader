from models import *
from flask.ext.login import current_user
from flask import Blueprint
import json
from autodownloader import app

download = Blueprint('download', __name__, template_folder='templates')


@download.route('/<show_id>')
@login_required
def get_update_links(show_id):
    follow = Following.objects.get(show_id=show_id, user_id=current_user.id)
    new_index = int(follow.latest_season) * 100 + int(follow.latest_episode)
    episodes = Episode.objects(show_id=show_id,format=follow.show_format, index__gt=new_index)
    download_json = []
    for episode in episodes:
        download_json.append({
        "show_id" : show_id,
        "index" : episode.index,
        "ed2k_link" : episode.ed2k_link
        })
    return json.dumps(download_json)
