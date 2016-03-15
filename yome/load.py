# -*- coding: utf-8 -*-

from yome.models import (Base, Gene, KnowledgebaseGene, Knowledgebase, Synonym,
                         KnowledgebaseFeature)
from yome.util import get_or_create

import logging
import numpy as np

def make_tables():
    logging.info('Creating tables')
    Base.metadata.create_all()

def load_knowledgebase(session, df, knowledgebase_name, locus_id_column='bnum',
                       primary_name_column='name', synonyms_column='synonyms',
                       feature_columns=['description'],
                       annotation_quality_column='annotation_quality'):
    """Load a new knowledgebase.

    Arguments
    ---------

    session:

    df:

    synonyms_column: The column with synonyms in it. Must be None or a list of
    strings.

    """
    logging.info('Loading knowledgebase %s' % knowledgebase_name)

    for col in [locus_id_column, primary_name_column, synonyms_column,
                annotation_quality_column] + feature_columns:
        if not col in df.columns:
            raise Exception('Could not find column %s' % col)

    db = get_or_create(session, Knowledgebase, name=knowledgebase_name)
    # load genes
    for _, row_in in df.iterrows():
        # check for nan
        row = row_in.map(lambda v: None if type(v) is float and np.isnan(v) else v)
        # load gene and knowledgebase gene
        locus_id = row[locus_id_column]
        primary_name = row[primary_name_column]
        if locus_id is not None:
            gene = get_or_create(session, Gene,
                                 locus_id=locus_id)
            gene_id = gene.id
        else:
            gene_id = None
        db_gene = get_or_create(session, KnowledgebaseGene,
                                gene_id=gene_id,
                                knowledgebase_id=db.id,
                                primary_name=primary_name,
                                annotation_quality=row[annotation_quality_column])
        # load synonyms
        all_synonyms = [primary_name]
        if locus_id is not None:
            all_synonyms += [locus_id]
        if row[synonyms_column] is not None:
            all_synonyms += row[synonyms_column]
        for synonym in all_synonyms:
            synonym = get_or_create(session, Synonym,
                                    synonym=synonym,
                                    ref_id=db_gene.id,
                                    ref_type='knowledgebase_gene')
        # load features
        for col in feature_columns:
            if row[col] is not None:
                get_or_create(session, KnowledgebaseFeature,
                              feature_type=col,
                              feature=row[col],
                              knowledgebase_gene_id=db_gene.id)
    session.commit()

    logging.info('Finished loading knowledgebase %s' % knowledgebase_name)
