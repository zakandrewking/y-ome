# -*- coding: utf-8 -*-

import logging

from yome import Session
from yome.models import Base, Gene, DatabaseGene, Database

def create_session():
    session = Session()
    return session

def make_tables():
    logging.info('Creating tables')
    Base.metadata.create_all()

def load_new_database_from_df(session, df, database_name,
                              locus_id_column='bnum',
                              primary_name_column='name',
                              synonyms_column='synonyms'):
    """Load a new database.

    Arguments
    ---------

    session:

    df:

    synonyms_column: The column with synonyms in it. Must be None or a list of
    strings.

    """

    db = Database(name=database_name)

    for row in df.iterrows():
        new_db_gene = DatabaseGene(...)

    session.commit()
