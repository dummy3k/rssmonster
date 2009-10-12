from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)

feeds_table = Table('feeds', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100)),
    Column('url', String(255)),
    Column('last_update', DateTime),
)

def upgrade():
    # Upgrade operations go here. Don't create your own engine; use the engine
    # named 'migrate_engine' imported from migrate.
    feeds_table.create()
    pass

def downgrade():
    # Operations to reverse the above upgrade go here.
    feeds_table.drop()
