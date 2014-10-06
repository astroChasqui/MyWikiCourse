from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
section = Table('section', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=64)),
    Column('wiki_title', VARCHAR(length=64)),
    Column('wiki_section', VARCHAR(length=64)),
    Column('position', VARCHAR(length=64)),
    Column('course_id', INTEGER),
)

section = Table('section', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=64)),
    Column('wiki_title', String(length=64)),
    Column('wiki_section', String(length=64)),
    Column('chapter', Integer),
    Column('section', Integer),
    Column('subsection', Integer),
    Column('subsubsection', Integer),
    Column('course_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['section'].columns['position'].drop()
    post_meta.tables['section'].columns['chapter'].create()
    post_meta.tables['section'].columns['section'].create()
    post_meta.tables['section'].columns['subsection'].create()
    post_meta.tables['section'].columns['subsubsection'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['section'].columns['position'].create()
    post_meta.tables['section'].columns['chapter'].drop()
    post_meta.tables['section'].columns['section'].drop()
    post_meta.tables['section'].columns['subsection'].drop()
    post_meta.tables['section'].columns['subsubsection'].drop()
