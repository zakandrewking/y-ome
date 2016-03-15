# -*- coding: utf-8 -*-

from yome.models import (Base, Gene, DatabaseGene, Database, Synonym,
                         DatabaseFeature)
from yome.util import get_or_create

import logging

def make_tables():
    logging.info('Creating tables')
    Base.metadata.create_all()

# TODO add primary name and locus id to synonyms
# TODO add features

def load_new_database_from_df(session, df, database_name,
                              locus_id_column='bnum',
                              primary_name_column='name',
                              synonyms_column='synonyms',
                              feature_columns=['description'],
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
                annotation_quality_column] + feature_columns:
        if not col in df.columns:
            raise Exception('Could not find column %s' % col)

    db = get_or_create(session, Database, name=database_name)
    # load genes
    for _, row in df.iterrows():
        locus_id = row[locus_id_column]
        primary_name = row[primary_name_column]
        gene = get_or_create(session, Gene,
                             locus_id=locus_id)
        db_gene = get_or_create(session, DatabaseGene,
                                gene_id=gene.id,
                                database_id=db.id,
                                primary_name=primary_name,
                                annotation_quality=row[annotation_quality_column])
        # load synonyms
        for synonym in row[synonyms_column] + [locus_id, primary_name]:
            synonym = get_or_create(session, Synonym,
                                    synonym=synonym,
                                    ref_id=db_gene.id,
                                    ref_type='database_gene')
        # load features
        for col in feature_columns:
            get_or_create(session, DatabaseFeature,
                          feature_type=col,
                          feature=row[col],
                          database_gene_id=db_gene.id)
    session.commit()
