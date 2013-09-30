from models import *
from rss import get_updates
import re
import urllib2
import json
import time

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
    
    if results == 'false':
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
    else:
        if _debug:
            print 'find the resource ' + show['itemid']\
                    + ' ' + show['title']
    #save show info
    show_item = Show.objects(show_id=show['itemid']).first()
    if show_item == None:
        if _debug:
            print 'New resouece!'
        show_item = Show()
        show_item.show_id = show['itemid']
        show_item.show_name = show['title']
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
            if max_s < episode.season:
                max_s = episode.season            
            if max_e < episode.episode:
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
                print 'insert new episode:S' + new_episode.season + \
                    'E' + new_episode.episode
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
            print 'finding update of show: ' + show['show_name']
        for update in updates:
            #find the update match and time is later then update db
            if show['show_id'] == update['id'] and \
            show['updated_at'] < update['date']:
                update_show(update['id'], update['date'])
                if _debug:
                    print 'found update'
                found = True
                break
        if _debug:
            if found == False: 
                print 'no update'

def update_thread():
    while(True):
       update_routine()
       time.sleep(10)
