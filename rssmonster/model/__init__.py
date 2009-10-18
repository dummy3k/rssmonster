"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from rssmonster.model import meta
from user import User, users_table
from feed import Feed, feeds_table
from feed_entries import FeedEntry, feed_entries_table
from classification import Classification, classifications_table

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

orm.mapper(User, users_table)
orm.mapper(Feed, feeds_table)

orm.mapper(FeedEntry, feed_entries_table, properties = {
    'feed' : orm.relation(Feed),
    })

orm.mapper(Classification, classifications_table, properties = {
    'user' : orm.relation(User),
    'entry' : orm.relation(FeedEntry),
    })

