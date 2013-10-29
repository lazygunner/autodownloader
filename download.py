from models import *
from flask.ext.login import current_user
from flask import Blueprint, request
import json
from autodownloader import app

download = Blueprint('download', __name__, template_folder='templates')


@download.route('/', methods=['GET'])
def get_all_links():

    if not request.json or not 'email' in request.json:
        abort(404)
    data = request.json
    user_id = User.objects(email=data['email']).first()['id']
    follows = Following.objects(user_id=user_id)
    download_json = []
    
    for follow in follows:
        new_index = int(follow.latest_season) * 100 + int(follow.latest_episode)
        episodes = Episode.objects(show_id=follow.show_id,format=follow.show_format, index__gt=new_index)
        for episode in episodes:
            download_json.append({
            "show_id" : follow.show_id,
            "index" : episode.index,
            "ed2k_link" : episode.ed2k_link
            })
    return json.dumps(download_json)


@download.route('/<show_id>', methods=['GET'])
def get_update_links(show_id):
    
    if not request.json or not 'email' in request.json:
        abort(404)
    data = request.json
    user_id = User.objects.get(email=data['email'])['id']
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
def update_links(show_id):
    if not request.json or not 'l_e' in request.json:
        abort(404)
    data = request.json
    user_id = User.objects.get(email=data['email'])['id']
    follow = Following.objects.get(show_id=show_id, user_id=user_id)
    
    follow.update(set__latest_season = data['l_s'])
    follow.update(set__latest_episode = data['l_e'])

    follow.save()
    return json.dumps({'status': show_id})

    
