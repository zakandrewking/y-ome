# -*- coding: utf-8 -*-

from yome.models import (Base, config, Session, Gene, Synonym, Knowledgebase,
                         KnowledgebaseGene, Dataset, DatasetGeneValue,
                         DatasetGeneFeature)

import pytest

def test_config():
    assert config.get('DATABASE', 'user')

def test_session(session):
    pass

@pytest.fixture(scope='session')
def test_load_gene(request, session):
    gene = Gene(locus_id='b1779')
    session.add(gene)
    session.commit()
    assert session.query(Gene).get(gene.id).locus_id == 'b1779'
    return gene.id

@pytest.fixture(scope='session')
def test_load_knowledgbase(request, session):
    kb = Knowledgebase(name='EcoCyc')
    session.add(kb)
    session.commit()
    session.query(Knowledgebase).get(kb.id).name == 'EcoCyc'
    return kb.id

@pytest.fixture(scope='session')
def test_load_knowledgbase_gene(request, session, test_load_gene, test_load_knowledgbase):
    kb_gene = KnowledgebaseGene(gene_id=test_load_gene,
                                knowledgebase_id=test_load_knowledgbase,
                                primary_name='gapA',
                                annotation_quality='high')
    session.add(kb_gene)
    session.commit()
    session.query(KnowledgebaseGene).get(kb_gene.id).primary_name == 'gapA'
    return kb_gene.id

def test_load_synonym(request, session, test_load_knowledgbase_gene):
    synonym = Synonym(synonym='gad',
                      ref_id=test_load_knowledgbase_gene,
                      ref_type='knowledgebase_gene')
    session.add(synonym)
    session.commit()
    res = (
        session
        .query(Gene, Synonym)
        .join(KnowledgebaseGene)
        .join(Synonym, Synonym.ref_id == KnowledgebaseGene.id)
        .filter(Gene.locus_id == 'b1779')
        .first()
    )
    assert res[0].locus_id == 'b1779'
    assert res[1].synonym == 'gad'

@pytest.fixture(scope='session')
def test_load_dataset(request, session):
    dataset = Dataset(name='express1')
    session.add(dataset)
    session.commit()
    assert session.query(Dataset).get(dataset.id).name == 'express1'
    return dataset.id

def test_load_dataset_gene_value(request, session, test_load_dataset, test_load_gene):
    dataset_gene_value = DatasetGeneValue(
        dataset_id=test_load_dataset,
        gene_id=test_load_gene,
        value_type='reads',
        value=103.4,
    )
    session.add(dataset_gene_value)
    session.commit()
    assert session.query(DatasetGeneValue).get(dataset_gene_value.id).value == 103.4

def test_load_dataset_gene_feature(request, session, test_load_dataset, test_load_gene):
    dataset_gene_feature = DatasetGeneFeature(
        dataset_id=test_load_dataset,
        gene_id=test_load_gene,
        feature_type='on_off',
        feature='on',
    )
    session.add(dataset_gene_feature)
    session.commit()
    assert session.query(DatasetGeneFeature).get(dataset_gene_feature.id).feature == 'on'
