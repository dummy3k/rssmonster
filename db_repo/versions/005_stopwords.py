from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)

feeds_table = Table('feeds', meta.metadata,
    Column('id', Integer, primary_key=True),
)

users_table = Table('users', meta.metadata,
    Column('id', Integer, primary_key=True),
)

stopwords_table = Table('stopwords', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('feed_id', Integer, ForeignKey('feeds.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('word', String(50), unique=True),
)

def upgrade():
    stopwords_table.create()

def downgrade():
    stopwords_table.drop()
