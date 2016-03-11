# -*- coding: utf-8 -*-

from sqlalchemy import (create_engine, Integer, String, Sequence, Column, Enum,
                        ForeignKey)
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ConfigParser import SafeConfigParser
from os.path import join, dirname, realpath

# get settings
config = SafeConfigParser()
directory = dirname(realpath(__file__))
config.read(join(directory, '..', 'settings.ini'))
database_keys = ['user', 'password', 'host', 'port', 'database']
settings = {k: config.get('DATABASE', k) for k in database_keys}

# create the engine, Base, and Session
engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'
                       .format(**settings))
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

# set up some enums
_enum_l = [
    Enum('database_gene', name='synonym_type'),
    Enum('high', 'medium', 'low', name='annotation_quality')
]
enums = {x.name: x for x in _enum_l}


class Gene(Base):
    __tablename__ = 'gene'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    locus_id = Column(String)
    __table_args__ = (
        UniqueConstraint(locus_id),
    )


class Database(Base):
    __tablename__ = 'database'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    name = Column(String)


class DatabaseGene(Base):
    __tablename__ = 'database_gene'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    primary_name = Column(String)
    gene_id = Column(Integer, ForeignKey(Gene.id))
    database_id = Column(Integer, ForeignKey(Database.id))
    annotation_quality = Column(enums['annotation_quality'])
    # TODO any unique constraint for DatabaseGene?
    # __table_args__ = (
    #     UniqueConstraint(),
    # )


class DatabaseFeature(Base):
    __tablename__ = 'database_feature'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    feature_type = Column(String)
    feature = Column(String)
    database_gene_id = Column(Integer, ForeignKey(Database.id))


class Synonym(Base):
    __tablename__ = 'synonym'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    row_id = Column(Integer)
    synonym = Column(String)
    type = Column(enums['synonym_type'])
    __table_args__ = (
        UniqueConstraint('row_id', 'synonym', 'type'),
    )
