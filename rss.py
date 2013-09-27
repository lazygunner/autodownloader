#-*- coding:utf-8 -*-
import urllib2
import feedparser
from datetime import datetime
from time import mktime

def get_updates(format):
    format = 'HR-HDTV'
    query = u"?channel=tv&format=" + format
    # query = u"all"
    query = query.strip()
    rss_url = 'http://www.yyets.com/rss/feed/'
    url_doc = feedparser.parse(rss_url + query)

    update_items = []
    for item in url_doc['entries']:
        update_item = {}
        update_item['date'] = datetime.fromtimestamp(mktime(item['published_parsed']))
        update_item['id'] = item['id'][len(item['id']) - 5:]
        update_item['format'] = item['summary_detail']['value'][1:3]
        if update_item['format'] != format[:2]:
            continue
        update_items.append(update_item)

    return update_items

