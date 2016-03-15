# -*- coding: utf-8 -*-

from yome.models import Gene, Synonym, Database, DatabaseGene, DatabaseFeature
from yome.load import load_new_database_from_df

import pandas as pd

def test_load_new_database_from_df(test_db, session):
    df = pd.DataFrame([{
        'bnum': 'b0114',
        'name': 'aceE',
        'synonyms': ['ECK0113', 'EG10024', 'b0114'],
        'annotation_quality': 'high',
        'description': 'desc',
        'summary': 'sum',
    }])
    load_new_database_from_df(session, df, 'UniProt',
                              feature_columns=['description', 'summary'])
    res = (
        session
        .query(Gene, Synonym, Database)
        .join(DatabaseGene)
        .join(Synonym, Synonym.ref_id == DatabaseGene.id)
        .join(Database)
        .filter(Gene.locus_id == 'b0114')
        .all()
    )
    assert res[0][0].locus_id == 'b0114'
    assert set([x[1].synonym for x in res]) == set(['ECK0113', 'EG10024', 'b0114', 'aceE'])
    assert res[0][2].name == 'UniProt'
    res = (
        session
        .query(DatabaseFeature)
        .join(DatabaseGene)
        .join(Gene)
        .filter(Gene.locus_id == 'b0114')
        .all()
    )
    feature_dict = {x.feature_type: x.feature for x in res}
    assert feature_dict['description'] == 'desc'
    assert feature_dict['summary'] == 'sum'
