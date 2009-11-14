from sqlalchemy import *
from migrate import *
import migrate.changeset

meta = MetaData(migrate_engine)

feeds_table = Table('feeds', meta.metadata,
    Column('id', Integer, primary_key=True),
)

users_table = Table('users', meta.metadata,
    Column('id', Integer, primary_key=True),
)

feed_entries_table = Table('feed_entries', meta.metadata,
    Column('id', Integer, primary_key=True),
)

bayes_feed_settings_table = Table('bayes_feed_settings', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('feed_id', Integer, ForeignKey('feeds.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('next_report', DateTime),
    Column('last_report', DateTime),
    Column('summarize_at', String(30)),
    UniqueConstraint('feed_id', 'user_id')
)

def upgrade():
    bayes_feed_settings_table.drop()
    bayes_feed_settings_table.create()

def downgrade():
	pass
    #bayes_feed_settings_table.create()

