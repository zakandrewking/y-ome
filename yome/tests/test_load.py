# -*- coding: utf-8 -*-

from yome.models import (Gene, Synonym, Knowledgebase, KnowledgebaseGene,
                         KnowledgebaseFeature)
from yome.load import load_knowledgebase

import pandas as pd
import numpy as np
import logging

def test_load_knowledgebase(session):
    print('load knowledge base')
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
