# -*- coding: utf-8 -*-

from sqlalchemy import (create_engine, Integer, String, Sequence, Column)
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from ConfigParser import SafeConfigParser
from os.path import join, dirname, realpath

# get settings
config = SafeConfigParser()
directory = dirname(realpath(__file__))
config.read(join(directory, '..', 'settings.ini'))
database_keys = ['user', 'password', 'host', 'port', 'database']
settings = {k: config.get('DATABASE', k) for k in database_keys}

engine = create_engine(('postgresql://{user}:{password}@{host}:{port}/{database}'
                        .format(**settings)))
Base = declarative_base(bind=engine)

class Gene(Base):
    __tablename__ = 'gene'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    locus_id = Column(String)

    __table_args__ = (
        UniqueConstraint(locus_id),
    )
