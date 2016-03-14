# -*- coding: utf-8 -*-

from yome.models import Gene, Synonym, Database, DatabaseGene
from yome.load import load_new_database_from_df

import pandas as pd

def test_load_new_database_from_df(test_db, session):
    df = pd.DataFrame([{
        'bnum': 'b0114',
        'name': 'aceE',
        'synonyms': ['ECK0113', 'EG10024'],
        'annotation_quality': 'high',
    }])
    load_new_database_from_df(session, df, 'UniProt')
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
    assert res[0][2].name == 'UniProt'
    assert set([x[1].synonym for x in res]) == set(['ECK0113', 'EG10024'])
