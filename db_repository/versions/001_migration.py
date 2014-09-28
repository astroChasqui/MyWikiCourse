from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('firstname', String(length=32)),
    Column('lastname', String(length=32)),
    Column('email', String(length=64)),
    Column('pwdhash', String(length=54)),
    Column('registered_on', DateTime),
    Column('last_login', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['last_login'].create()
    post_meta.tables['user'].columns['registered_on'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['last_login'].drop()
    post_meta.tables['user'].columns['registered_on'].drop()
