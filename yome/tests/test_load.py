# -*- coding: utf-8 -*-

from yome.models import (Gene, Synonym, Knowledgebase, KnowledgebaseGene,
                         KnowledgebaseFeature, Dataset, DatasetGeneValue,
                         DatasetGeneFeature)
from yome.load import load_knowledgebase, load_dataset

import pandas as pd
import numpy as np
import logging

def test_load_knowledgebase(session):
    df = pd.DataFrame([{
        'bnum': 'b0114',
        'name': 'aceE',
        'synonyms': ['ECK0113', 'EG10024', 'b0114'],
        'annotation_quality': 'high',
        'description': 'desc',
        'summary': 'sum',
        'missing': np.nan,
    }])
    load_knowledgebase(session, df, 'UniProt',
                       feature_columns=['description', 'summary', 'missing'])
    res = (
        session
        .query(Gene, Synonym, Knowledgebase)
        .join(KnowledgebaseGene)
        .join(Synonym, Synonym.ref_id == KnowledgebaseGene.id)
        .join(Knowledgebase)
        .filter(Gene.locus_id == 'b0114')
        .all()
    )
    assert res[0][0].locus_id == 'b0114'
    assert set([x[1].synonym for x in res]) == set(['ECK0113', 'EG10024', 'b0114', 'aceE'])
    assert res[0][2].name == 'UniProt'
    res = (
        session
        .query(KnowledgebaseFeature)
        .join(KnowledgebaseGene)
        .join(Gene)
        .filter(Gene.locus_id == 'b0114')
        .all()
    )
    feature_dict = {x.feature_type: x.feature for x in res}
    assert feature_dict['description'] == 'desc'
    assert feature_dict['summary'] == 'sum'

def test_load_dataset(session):
    df = pd.DataFrame([{
        'bnum': 'b0114',
        'expr': 103.4,
        'pval': 1.1e-4,
        'expr_t2': np.nan,
        'signif': 't',
    }])
    load_dataset(session, df, 'expr_abc', value_columns=['expr', 'pval', 'expr_t2'],
                 feature_columns=['signif'])
    res = (
        session
        .query(DatasetGeneValue, Dataset, Gene)
        .join(Dataset)
        .join(Gene)
        .filter(DatasetGeneValue.value_type == 'expr')
        .first()
    )
    assert res[0].value_type == 'expr'
    assert res[0].value == 103.4
    assert res[1].name == 'expr_abc'
    assert res[2].locus_id == 'b0114'

    res = (
        session
        .query(DatasetGeneFeature, Dataset, Gene)
        .join(Dataset)
        .join(Gene)
        .first()
    )
    assert res[0].feature_type == 'signif'
    assert res[0].feature == 't'
    assert res[1].name == 'expr_abc'
    assert res[2].locus_id == 'b0114'
