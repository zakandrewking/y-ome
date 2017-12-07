# -*- coding: utf-8 -*-

from sqlalchemy import (create_engine, Integer, String, Sequence, Column, Enum,
                        ForeignKey, Float)
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from configparser import SafeConfigParser
from os.path import join, dirname, realpath

# Get settings
config = SafeConfigParser()
directory = dirname(realpath(__file__))
config.read(join(directory, '..', 'settings.ini'))
database_keys = ['user', 'password', 'host', 'port', 'database']
settings = {k: config.get('DATABASE', k) for k in database_keys}

# Create the engine, Base, and Session
engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'
                       .format(**settings))
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

# Set up some enums
_enum_l = [
    Enum('knowledgebase_gene', name='synonym_ref_type'),
    Enum('high', 'low', 'tbd', 'excluded', name='annotation_quality')
]
enums = {x.name: x for x in _enum_l}

class Gene(Base):
    __tablename__ = 'gene'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    locus_id = Column(String, nullable=False)
    __table_args__ = (
        UniqueConstraint(locus_id),
    )


class Knowledgebase(Base):
    __tablename__ = 'knowledgebase'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    name = Column(String, nullable=False)


class KnowledgebaseGene(Base):
    __tablename__ = 'knowledgebase_gene'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    primary_name = Column(String, nullable=False)
    gene_id = Column(Integer, ForeignKey(Gene.id, ondelete='CASCADE'), nullable=True)
    knowledgebase_id = Column(Integer, ForeignKey(Knowledgebase.id, ondelete='CASCADE'), nullable=False)
    annotation_quality = Column(enums['annotation_quality'], nullable=False)
    # TODO any unique constraint for KnowledgebaseGene?
    # __table_args__ = (
    #     UniqueConstraint(),
    # )


class KnowledgebaseFeature(Base):
    __tablename__ = 'knowledgebase_feature'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    feature_type = Column(String, nullable=False)
    feature = Column(String, nullable=False)
    knowledgebase_gene_id = Column(Integer, ForeignKey(KnowledgebaseGene.id, ondelete='CASCADE'), nullable=False)


class Synonym(Base):
    __tablename__ = 'synonym'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    synonym = Column(String, nullable=False)
    ref_id = Column(Integer, nullable=False)
    ref_type = Column(enums['synonym_ref_type'], nullable=False)
    __table_args__ = (
        UniqueConstraint('synonym', 'ref_id', 'ref_type'),
    )


class Dataset(Base):
    __tablename__ = 'dataset'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    name = Column(String, nullable=False)
    __table_args__ = (
        UniqueConstraint('name'),
    )


class DatasetGeneValue(Base):
    __tablename__ = 'dataset_gene_value'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    dataset_id = Column(Integer, ForeignKey(Dataset.id, ondelete='CASCADE'), nullable=False)
    gene_id = Column(Integer, ForeignKey(Gene.id, ondelete='CASCADE'), nullable=False)
    value_type = Column(String, nullable=False)
    value = Column(Float, nullable=True)
    # only one of each type currently allowed
    __table_args__ = (
        UniqueConstraint('dataset_id', 'gene_id', 'value_type'),
    )


class DatasetGeneFeature(Base):
    __tablename__ = 'dataset_gene_feature'
    id = Column(Integer, Sequence('wids'), primary_key=True)
    dataset_id = Column(Integer, ForeignKey(Dataset.id, ondelete='CASCADE'), nullable=False)
    gene_id = Column(Integer, ForeignKey(Gene.id, ondelete='CASCADE'), nullable=False)
    feature_type = Column(String, nullable=False)
    feature = Column(String, nullable=True)
    # only one of each type currently allowed
    __table_args__ = (
        UniqueConstraint('dataset_id', 'gene_id', 'feature_type'),
    )
