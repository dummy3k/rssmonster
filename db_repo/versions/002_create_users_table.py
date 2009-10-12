from sqlalchemy import *
from migrate import *

meta = MetaData(migrate_engine)

users_table = Table('users', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('email', String(100)),
    Column('openid', String(255)),
    Column('banned', Boolean),
    Column('signup', DateTime),
    Column('last_login', DateTime),
)

def upgrade():
    # Upgrade operations go here. Don't create your own engine; use the engine
    # named 'migrate_engine' imported from migrate.
    users_table.create()
    pass

def downgrade():
    # Operations to reverse the above upgrade go here.
    users_table.drop()
