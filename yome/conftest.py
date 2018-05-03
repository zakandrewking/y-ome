from yome import Session, Base

import pytest
import os
import logging
from sqlalchemy import create_engine
from os.path import join, dirname, realpath

directory = dirname(realpath(__file__))
test_db_filepath = join(directory, '..', 'yome_test.db')

@pytest.fixture(scope='session')
def test_db(request):
    os.remove(test_db_filepath)
    engine = create_engine(f'sqlite:///{test_db_filepath}')
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

@pytest.fixture(scope='session')
def session(request, test_db):
    """Make a session"""
    def teardown():
        Session.close_all()
    request.addfinalizer(teardown)
    return Session()
