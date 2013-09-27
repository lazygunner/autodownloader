from models import *
from rss import get_updates
import re
import urllib2
import json

_debug = True

base_url = 'http://www.yyets.com/resource/'
query_url = 'http://www.yyets.com/search/api?keyword='
def find_episodes(show_id='11005',format='HR-HDTV', season=0, episode=0):

    try:
        response = urllib2.urlopen(base_url + show_id)
    except:
        print 'Net work error!Please check your network and the city name!'
        return
    html = response.read()

    p = re.compile(r'<li.*?format="' + format + '">.*?title=".*?\.[sS](\d{2})[eE](\d{2}).*?type="ed2k"\shref="(.*?)".*?</li>')
    episodes = p.findall(html)
    return episodes

def find_show(name='s.h.i.e.l.d', format='HR-HDTV', season=0, episode=0):
    
    try:
        response = urllib2.urlopen(query_url+name)
    except:
        print 'Net work error!Please check your network and the city name!'
        return
    html = response.read()

    urldoc = json.loads(html)
    results = urldoc["data"]
    
    if results == 'false':
        print 'Show name error, cannot find it in YYets'
        return
    show = {}
    for res in results:
        if(res['type'] == 'resource' and res['channel'] == 'tv'):
            show = res
            break
    if len(show) == 0:
        print 'Cannot TV show according to the name!'
        return
    else:
        if _debug:
            print 'find the resource ' + show['itemid']\
                    + ' ' + show['title']

    show_item = Show.objects(show_id=show['itemid']).first()
    if show_item == None:
        if _debug:
            print 'New resouece!'
        show_item = Show()
        show_item.show_id = show['itemid']
        show_item.show_name = show['title']
        episodes = find_episodes(show_item.show_id, format, season, episode)
        if _debug:
            print 'find ' + str(len(episodes)) + ' episodes.' 
        for item in episodes:
            episode = Episode()
            episode.format = format
            episode.season = item[0]
            episode.episode = item[1]
            episode.ed2k_link = item[2]
            show_item.episodes.append(episode)
        show_item.save()
    else:
        print show_item.latest_episode
    return

def update_show(update_id):
    if _debug:
        print 'update :' + update_id

def update_routine():
    updates = get_updates('HR-HDTV')    
    shows = Show.objects()
    if len(shows) == 0:
        print 'There is no following shows in the db!'
        return
    found = False
    for show in shows:
        if _debug:
            print 'finding update of show: ' + show['show_name']
        for update in updates:
            if show['show_id'] == update['id'] and \
            show['updated_at'] < update['date']:
                update_show(update['id'])
                if _debug:
                    print 'found update'
                found = True
                break
        if _debug:
            if found == False: 
                print 'no update'
                
            


update_routine()
