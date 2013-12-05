from models import *
from flask.ext.login import current_user
from flask import Blueprint, request, abort
import json
from autodownloader import app
from flask.ext.security.decorators import http_auth_required

download = Blueprint('download', __name__, template_folder='templates')

#curl -X GET 'tv.xdream.info/download/' -d '{"email":"username"}' -H "Content-Type:application/json" -v
@download.route('/', methods=['GET'])
@http_auth_required
def get_all_links():
    if not request.json:
        abort(404)
    data = request.json
    user_id = current_user.id
    follows = Following.objects(user_id=user_id)
    download_json = []
    
    count = 5
    for follow in follows:
        new_index = int(follow.latest_season) * 100 + int(follow.latest_episode)
        episodes = Episode.objects(show_id=follow.show_id,format=follow.show_format, index__gt=new_index)
        for episode in episodes:
            if count == 0:
                break
            else:
                count -= 1
            download_json.append({
            "show_id" : follow.show_id,
            "index" : episode.index,
            "ed2k_link" : episode.ed2k_link
            })
    return json.dumps(download_json)


@download.route('/<show_id>', methods=['GET'])
@http_auth_required
def get_update_links(show_id):
    
    if not request.json:
        abort(404)
    data = request.json
    user_id = current_user.id
    follow = Following.objects.get(show_id=show_id, user_id=user_id)
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

#RESTful API without auth 
@download.route('/<show_id>', methods=['POST'])
@http_auth_required
def update_links(show_id):
    if not request.json or not 'l_e' in request.json:
        abort(404)
    data = request.json
    user_id = current_user.id
    follow = Following.objects.get(show_id=show_id, user_id=user_id)
    
    follow.update(set__latest_season = data['l_s'])
    follow.update(set__latest_episode = data['l_e'])

    follow.save()
    return json.dumps({'status': show_id})

    
