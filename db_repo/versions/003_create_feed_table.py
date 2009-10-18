from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)

feeds_table = Table('feeds', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100)),
    Column('url', String(255)),
    Column('last_fetch', DateTime),
    Column('last_builddate', DateTime),
    Column('updated', DateTime),
    Column('subtitle', String(100)),
    Column('language', String(100)),
    Column('image', String(100)),
    Column('link', String(100)),
)

feed_entries_table = Table('feed_entries', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('feed_id', Integer, ForeignKey('feeds.id')),
    Column('uid', String(100)),
    Column('title', String(100)),
    Column('summary', String(255)),
    Column('link', String(255)),
)

users_table = Table('users', meta.metadata,
    Column('id', Integer, primary_key=True),
)

classifications_table = Table('classifications_entries', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('entry_id', Integer, ForeignKey('feeds.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('pool', String(5)),
)

def upgrade():
    # Upgrade operations go here. Don't create your own engine; use the engine
    # named 'migrate_engine' imported from migrate.
    feeds_table.create()
    feed_entries_table.create()
    classifications_table.create()

def downgrade():
    # Operations to reverse the above upgrade go here.
    feeds_table.drop()
    feed_entries_table.drop()
    classifications_table.drop()
    
