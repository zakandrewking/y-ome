# -*- coding: utf-8 -*-

from yome import Session
from yome.models import Base, Gene, DatabaseGene, Database, Synonym
from yome.util import get_or_create

import logging

def create_session():
    return Session()

def make_tables():
    logging.info('Creating tables')
    Base.metadata.create_all()

def load_new_database_from_df(session, df, database_name,
                              locus_id_column='bnum',
                              primary_name_column='name',
                              synonyms_column='synonyms',
                              annotation_quality_column='annotation_quality'):
    """Load a new database.

    Arguments
    ---------

    session:

    df:

    synonyms_column: The column with synonyms in it. Must be None or a list of
    strings.

    """
    for col in [locus_id_column, primary_name_column, synonyms_column,
                annotation_quality_column]:
        if not col in df.columns:
            raise Exception('Could not find column %s' % col)

    db = get_or_create(session, Database, name=database_name)
    for _, row in df.iterrows():
        gene = get_or_create(session, Gene,
                             locus_id=row[locus_id_column])
        db_gene = get_or_create(session, DatabaseGene,
                                gene_id=gene.id,
                                database_id=db.id,
                                primary_name=row[primary_name_column],
                                annotation_quality=row[annotation_quality_column])
        for synonym in row[synonyms_column]:
            synonym = get_or_create(session, Synonym,
                                    synonym=synonym,
                                    ref_id=db_gene.id,
                                    ref_type='database_gene')
    session.commit()
