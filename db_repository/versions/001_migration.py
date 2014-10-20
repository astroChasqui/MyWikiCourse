from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
chapter = Table('chapter', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=64)),
    Column('course_id', Integer),
)

course = Table('course', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=64)),
    Column('timestamp', DATETIME),
    Column('created_on', DATETIME),
    Column('last_update', DATETIME),
    Column('user_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['chapter'].create()
    pre_meta.tables['course'].columns['created_on'].drop()
    pre_meta.tables['course'].columns['last_update'].drop()
    pre_meta.tables['course'].columns['timestamp'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['chapter'].drop()
    pre_meta.tables['course'].columns['created_on'].create()
    pre_meta.tables['course'].columns['last_update'].create()
    pre_meta.tables['course'].columns['timestamp'].create()
