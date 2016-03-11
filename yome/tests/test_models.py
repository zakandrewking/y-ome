# -*- coding: utf-8 -*-

from yome.models import Base, config, Session, Gene

def test_config():
    assert config.get('DATABASE', 'user')

def test_session():
    session = Session()

def test_load_db(test_db, session):
    assert session.Query(Gene).first() is None
