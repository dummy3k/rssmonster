"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from rssmonster.model import meta
from user import User, users_table
from feed import Feed, feeds_table
from feed_entries import FeedEntry, feed_entries_table
from classification import Classification, classifications_table
from stopword import Stopword, stopwords_table
from bayes_feed_setting import BayesFeedSetting, bayes_feed_settings_table

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=engine)
    meta.engine = engine

orm.mapper(User, users_table, properties = {
    'bayes_feed_settings' : orm.relation(BayesFeedSetting),
    })
    
orm.mapper(Feed, feeds_table, properties = {
    'entries' : orm.relation(FeedEntry),
    })

orm.mapper(FeedEntry, feed_entries_table, properties = {
    'feed' : orm.relation(Feed),
    })

orm.mapper(Classification, classifications_table, properties = {
    'user' : orm.relation(User),
    'entry' : orm.relation(FeedEntry),
    })

orm.mapper(Stopword, stopwords_table)
orm.mapper(BayesFeedSetting, bayes_feed_settings_table)

