
from models import *
from rss import get_updates
import re
import urllib2
import json
import time
from datetime import datetime
from urllib2 import quote
import threading

_debug = True

base_url = 'http://www.yyets.com/resource/'
query_url = 'http://www.yyets.com/search/api?keyword='
def find_episodes(show_id='11005', format='.*?'):
    #get episodes through YYets resource page
    if _debug:
        print 'getting html...'
    try:
        response = urllib2.urlopen(base_url + show_id)
    except:
        print 'Net work error!Please check your network and the city name!'
        return
    html = response.read()
    if _debug:
        print 'parsing html...'
    #parse the episodes info
    p = re.compile(r'<li.*?itemid="(\d*)" format="(' + format + ')">.*?title=".*?\.[sS](\d{2})[eE](\d{2}).*?type="ed2k"\shref="(.*?)".*?</li>')
    episodes = p.findall(html)
    if _debug:
        print 'finished parsing.'
    return episodes

def find_show(name='master of sex', format='HR-HDTV', season=0, episode=0):
    #get the show info through YYets query API
    try:
        response = urllib2.urlopen(query_url+name)
    except:
        print 'Net work error!Please check your network and the city name!'
        return
    html = response.read()

    urldoc = json.loads(html)
    results = urldoc["data"]
    
    if results == False:
        print 'Show name error, cannot find it in YYets'
        return
    show = {}
    for res in results:
        if(res['type'] == 'resource' and res['channel'] == 'tv'):
            show = res
            break
    if len(show) == 0:
        print 'Cannot find TV show according to the name!'
        return
    #else:
        #if _debug:
           # print 'find the resource ' + show['itemid'] + ' ' + show['title']
    #save show info
    show_item = Show.objects(show_id=show['itemid']).first()
    if show_item == None:
	if _debug:
            print 'New resouece!'
	show_item = Show()
	show_item.show_id = show['itemid']
	p = re.compile(r'.*?\)')
	show_item.show_name = p.findall(show['title'])[0]
	show_item.created_at = datetime.fromtimestamp(int(show['pubtime']))
	show_item.updated_at = datetime.fromtimestamp(int(show['uptime']))
        #find episodes according to show_id
        episodes = find_episodes(show_item.show_id)
        if _debug:
            print 'find ' + str(len(episodes)) + ' episodes.' 
        max_s = 0
        max_e = 0
        #save episodes to db
        for item in episodes:
            episode = Episode()
            episode.show_id = show_item.show_id
            episode.index = item[0]
            episode.format = item[1]
            episode.season = item[2]
            episode.episode = item[3]
            episode.ed2k_link = item[4]
            episode.save()
            if episode.season > max_s:
                max_s = episode.season
                max_e = episode.episode
            elif episode.season == max_s:
                if episode.episode > max_e:
                    max_e = episode.episode

                
        #update latest s&e in show info
        show_item.latest_season = max_s
        show_item.latest_episode = max_e
        show_item.save()
    else:
        print show_item.latest_episode
    return

#episode:0-index,1-format,2-season,3-episode,4-ed2k_link
def update_show(update_id, date):
    if _debug:
        print 'update :' + update_id + ' at ' + date.strftime("%A, %d. %B %Y %I:%M%p")
    episodes = find_episodes(update_id)
    #sort by the index, make the latest update on the top of the list
    episodes_sorted = sorted(episodes, key = lambda x:x[0], reverse=True)
    show = Show.objects(show_id=update_id)[0]
    if _debug:
        print 'latest data in db: season:%d episode:%d'\
            %(show['latest_season'], show['latest_episode'])
    i = 0
    for episode in episodes_sorted:
        #insert new episode to db
        if(int(episode[2]) >= show['latest_season'] and \
            int(episode[3]) > show['latest_episode']):
            new_episode = Episode()
            new_episode.show_id = update_id
            new_episode.index = episode[0]
            new_episode.format = episode[1]
            new_episode.season = int(episode[2])
            new_episode.episode = int(episode[3])
            new_episode.ed2k_link = episode[4]
            if _debug:
                print 'insert new episode:S' +str(new_episode.season) + \
                    'E' + str(new_episode.episode)
            new_episode.save()
        #update exist latest episode
        elif(int(episode[2]) == show['latest_season'] and \
             int(episode[3]) == show['latest_episode']):

            if _debug:
                print 'updating exist episode S' + episode[2] + \
                    'E' + episode[3] + ' format: ' + \
                    episode[1]
                print Episode.objects(show_id=update_id,\
                     format=episode[1],season=show['latest_season'], \
                     episode=show['latest_episode'])[0]['ed2k_link']\
                     + '\n --> \n' + \
                     episode[4]

            new_episode = Episode.objects(show_id=update_id,\
                format=episode[1],season=show['latest_season'], \
                episode=show['latest_episode'])[0]\
                .update(set__ed2k_link=episode[4])
        #skip the rest episodes get from the update
        else:
            break

    show.latest_season = int(episodes_sorted[0][2])
    show.latest_episode = int(episodes_sorted[0][3])
    show.updated_at = date
    show.save()
    if _debug:
        print 'update finished.'

def check_update_time(title, updated_time):
    title = quote(title.encode('utf-8'))
    #get the show info through YYets query API
    try:
        response = urllib2.urlopen(query_url+title)
    except:
        print 'Net work error!Please check your network and the city name!'
        return
    html = response.read()

    urldoc = json.loads(html)
    results = urldoc["data"]
    
    if results == False:
        print 'Show name error, cannot find it in YYets'
        return
    show = {}
    for res in results:
        if(res['type'] == 'resource' and res['channel'] == 'tv'):
            show = res
            break
    if len(show) == 0:
        print 'Cannot find TV show according to the name!'
        return
    #else:
        #if _debug:
           # print 'find the resource ' + show['itemid'] + ' ' + show['title']
    new_updated_time = datetime.fromtimestamp(int(show['uptime']))
    if(updated_time < new_updated_time):
	return new_updated_time
    else:
	return None


def update_routine():
    update_format = 'HR-HDTV'
    #get updates from RSS
    updates = get_updates(update_format)    
    shows = Show.objects()
    if len(shows) == 0:
        print 'There is no following shows in the db!'
        return
    found = False
    #match updates in RSS with shows in db
    for show in shows:
        if _debug:
           print 'finding update of show: ' + show['show_id']
       # for update in updates:
            #find the update match then check the update time
       #     if show['show_id'] == update['id']:
        new_update_time = check_update_time(show['show_name'], show['updated_at'])
        if new_update_time!= None:
	    update_show(show['show_id'], new_update_time)
	    if _debug:
	        print 'found update'
	else:
            if _debug:
                print 'no update'

def update_thread():
    while(True):
       print 'update...'
       update_routine()
       time.sleep(60 * 60)
def thread():
    t = threading.Thread(target = update_thread, args = (), name = 'update_thread')
    t.start()
 
