from models import *
from flask.ext.login import current_user
from flask_mail import Message
from flask import Blueprint, request, abort
import json
from autodownloader import app, mail
from flask.ext.security.decorators import http_auth_required

download = Blueprint('download', __name__, template_folder='templates')

#curl -X GET 'tv.xdream.info/download/' -d '{"email":"username"}' -H "Content-Type:application/json" -v
@download.route('/download/', methods=['GET'])
@http_auth_required
def get_all_links():
    
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
            "ed2k_link" : episode.ed2k_link,
            "type" : 'ad'
            })

    if count != 0:
        download_links = DownloadLinks.objects()
    for download_link in download_links:
        if count == 0:
            break
        else:
            count -= 1
            download_json.append({
            "ed2k_link" : download_link.ed2k_link,
            "type" : 'dl'
            })


    return json.dumps(download_json)


@download.route('/download/<show_id>', methods=['GET'])
@http_auth_required
def get_update_links(show_id):
    
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

@download.route('/completed/', methods=['POST'])
@http_auth_required
def post_dl_status():
    user_id = current_user.id
    link = request.json['link']
    links = DownloadLinks.objects.get(user_id=user_id, ed2k_link=link)
    links.delete()

    download_notice(link, current_user.email)

    link_array = []
    links = DownloadLinks.objects(user_id=user_id)
                    
    if len(links) > 0:
        link_array = map(lambda xx:xx['ed2k_link'], links)
    return json.dumps(link_array)

@download.route('/download/<show_id>', methods=['POST'])
@http_auth_required
def update_links(show_id):
    if not request.json or not 'l_e' in request.json:
        abort(404)
    data = request.json
    user_id = current_user.id
    follow = Following.objects.get(show_id=show_id, user_id=user_id)
    
    db_index = follow.latest_season * 100 + follow.latest_episode
    up_index = data['l_s'] * 100 + data['l_e']

    if(up_index > db_index):
        follow.update(set__latest_season = data['l_s'])
        follow.update(set__latest_episode = data['l_e'])

        follow.save()
    
    show = Show.objects.get(show_id=show_id)
    download_notice(show.show_name + '\'s S' + data['l_s'] + 'E' + data['l_e'], current_user.email)

    return json.dumps({'status': show_id})

def download_notice(content, rec):
    msg = Message(content + " has been downloaded!", sender='xdream420@gmail.com', recipients=[rec])
    mail.send(msg)
