# -*- coding: utf-8 -*-

from yome.models import (Base, config, Session, Gene, Synonym, Database,
                         DatabaseGene)

import pytest

def test_config():
    assert config.get('DATABASE', 'user')

def test_session(session):
    pass

@pytest.fixture(scope='function')
def test_load_gene(test_db, session):
    gene = Gene(locus_id='b1779')
    session.add(gene)
    session.commit()
    assert session.query(Gene).first().locus_id == 'b1779'
    return gene.id

def test_load_synonym(test_db, session, test_load_gene):
    db = Database(name='EcoCyc')
    session.add(db)
    session.flush()
    db_gene = DatabaseGene(gene_id=test_load_gene,
                           database_id=db.id,
                           primary_name='gapA',
                           annotation_quality='high')
    session.add(db_gene)
    session.flush()
    synonym = Synonym(synonym='gad',
                      ref_id=db_gene.id,
                      ref_type='database_gene')
    session.add(synonym)
    session.commit()
    res = (
        session
        .query(Gene, Synonym)
        .join(DatabaseGene)
        .join(Synonym, Synonym.ref_id == DatabaseGene.id)
        .filter(Gene.locus_id == 'b1779')
        .first()
    )
    assert res[0].locus_id == 'b1779'
    assert res[1].synonym == 'gad'
