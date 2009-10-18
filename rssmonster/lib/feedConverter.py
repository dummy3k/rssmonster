import feedparser
import datetime, PyRSS2Gen
import db
import logging

from helper import *

log = logging.getLogger('bayesRSS.' + __name__)

class feedConverter:
    def __init__(self, url, templateGroup):
        self.sourceFeed = feedparser.parse(url)
        self.templateGroup = templateGroup

        connection = db.openConnection(settings['dbFilename'])
        cursor = connection.cursor()

        updateTitleTmpl = self.templateGroup.getInstanceOf("updateOrReplace")
        updateTitleTmpl['table'] = 'Feeds'
        updateTitleTmpl['values'] = 'Title'
        updateTitleTmpl['conditions'] = 'FeedHash'
        log.debug(str(updateTitleTmpl))
#        cursor.execute(str(updateTitleTmpl), (self.sourceFeed['feed']['title'],
#                                              quickHash(url)))

        for entry in self.sourceFeed['entries']:
            #summary = unicode(entry['summary']).encode("utf-8")         
            
            relevant = strip_ml_tags(entry['title'])
            
            if 'summary' in entry.keys():
                relevant += ' '
                relevant += strip_ml_tags(entry['summary'])
            else:
                entry['summary'] = ""
                
            relevant = unicode(relevant).encode("utf-8")         
            entry['relevant'] = relevant
            #entry['uid'] = mem.setSummary(relevant)
            entry['uid'] = quickHash(relevant)
            
            

            insertTmpl = self.templateGroup.getInstanceOf("insertOrReplace")
            insertTmpl['table'] = 'Entries'
            insertTmpl['fields'] = ['Hash', 'Title', 'Summary']
            cursor.execute(str(insertTmpl), (entry['uid'], 
                                             entry['title'],
                                             entry['summary']))

            entry['EntryId'] = cursor.lastrowid
        connection.commit()
            
                

    def to_xml(self):
        myItems = []
        #print "self.sourceFeed: %s" % self.sourceFeed['feed'].keys()
        for entry in self.sourceFeed['entries']:
            newItem = PyRSS2Gen.RSSItem(
                title = entry['title'],
                link = entry['link'],
                description = entry['summary'],
                #guid = PyRSS2Gen.Guid(entry['summary']),
                #guid = entry['uid'],
                guid = PyRSS2Gen.Guid(entry['id'], entry['guidislink']),
                pubDate = entry['updated'])
            
            myItems.append(newItem)
    
        rss = PyRSS2Gen.RSS2(
            title = self.sourceFeed['feed']['title'],
            link = self.sourceFeed['feed']['link'],
            description = self.sourceFeed['feed']['subtitle'],
            lastBuildDate = datetime.datetime.now(),
            items = myItems)

        return rss.to_xml()

