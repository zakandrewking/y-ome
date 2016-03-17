# -*- coding: utf-8 -*-

from yome.models import (Base, Gene, KnowledgebaseGene, Knowledgebase, Synonym,
                         KnowledgebaseFeature, Dataset, DatasetGeneValue,
                         DatasetGeneFeature)
from yome.util import get_or_create

import logging
import numpy as np
import pandas as pd

def _none_for_nan(df):
    """Replace np.nan with None.

    http://stackoverflow.com/questions/14162723/replacing-pandas-or-numpy-nan-with-a-none-to-use-with-mysqldb

    """
    return df.where((pd.notnull(df)), None)

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

    session: An instance of yome.Session.

    df: A pandas DataFrame.

    locus_id_column: The column containing locus IDs that will map to the gene
    table.

    primary_name_column:

    synonyms_column: The column with synonyms in it. Must be None or a list of
    strings.

    feature_columns: A list of columns that contain textual data.

    annotation_quality_column:

    """
    logging.info('Loading knowledgebase %s' % knowledgebase_name)

    for col in [locus_id_column, primary_name_column, synonyms_column,
                annotation_quality_column] + feature_columns:
        if not col in df.columns:
            raise Exception('Could not find column %s' % col)

    df = _none_for_nan(df)

    db = get_or_create(session, Knowledgebase, name=knowledgebase_name)
    # load genes
    for _, row in df.iterrows():
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


def load_dataset(session, df, dataset_name, locus_id_column='bnum',
                 value_columns=[], feature_columns=['description']):
    """Load a new dataset.

    Arguments
    ---------

    session: An instance of yome.Session.

    df: A pandas DataFrame.

    dataset_name: An identifier for the dataset.

    locus_id_column: The column containing locus IDs that will map to the gene
    table.

    value_columns: A list of columns that contain numeric data.

    feature_columns: A list of columns that contain textual data.

    """
    logging.info('Loading dataset %s' % dataset_name)

    for col in [locus_id_column] + value_columns + feature_columns:
        if not col in df.columns:
            raise Exception('Could not find column %s' % col)

    df = _none_for_nan(df)

    ds = get_or_create(session, Dataset, name=dataset_name)

    # probably quicker to get all the genes at once
    gene_dict = {gene.locus_id: gene.id for gene in session.query(Gene)}

    # load values
    for _, row in df.iterrows():
        # load gene and knowledgebase gene
        locus_id = row[locus_id_column]
        gene_id = gene_dict[locus_id]
        for col in value_columns:
            get_or_create(session, DatasetGeneValue,
                          dataset_id=ds.id,
                          gene_id=gene_id,
                          value_type=col,
                          value=row[col])
        for col in feature_columns:
            get_or_create(session, DatasetGeneFeature,
                          dataset_id=ds.id,
                          gene_id=gene_id,
                          feature_type=col,
                          feature=row[col])
    session.commit()

    logging.info('Finished loading dataset %s' % dataset_name)
