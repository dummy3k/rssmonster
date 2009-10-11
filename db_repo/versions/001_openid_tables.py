from sqlalchemy import *
from migrate import *
from pylons import config 
from openid.store.sqlstore import SQLiteStore, MySQLStore

def upgrade():
    con = migrate_engine.raw_connection()

#    if config['sqlalchemy.url'].find('mysql:') != -1:
#        store = MySQLStore(con);
#    else:
#        store = SQLiteStore(con);
    store = SQLiteStore(con);
    store.createTables()

def downgrade():
    con = migrate_engine.raw_connection()
    #store = SQLiteStore(con);
    #store.dropTables()
    
    meta = MetaData(migrate_engine)

    associations = Table('oid_associations',meta,
        Column('id',Integer,primary_key=True)
    )
    associations.drop()

    nonces = Table('oid_nonces',meta,
        Column('id',Integer,primary_key=True)
    )
    nonces.drop()

