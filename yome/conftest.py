# -*- coding: utf-8 -*-

from yome import Session, Base
from yome.models import settings

import pytest
import os
import logging
from sqlalchemy import create_engine

test_db = 'yome_test'

@pytest.fixture(scope='session')
def session(request):
    """Make a session"""
    def teardown():
        Session.close_all()
    request.addfinalizer(teardown)
    return Session()


@pytest.fixture(scope='session')
def test_db_create():
    """Make sure the test database is clean."""
    os.system('dropdb %s' % test_db)
    os.system('createdb %s -U %s' % (test_db, settings['user']))
    logging.info('Dropped and created database %s' % test_db)


@pytest.fixture(scope='session')
def test_db(request, test_db_create):
    test_settings = {k: (test_db if k == 'database' else v)
                     for k, v in settings.items()}
    engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'
                           .format(**settings))
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)
    logging.info('Loaded database schema')
    def teardown():
        # close all sessions. Comment this line out to see if ome functions are
        # closing their sessions properly.
        Session.close_all()
        # clear the db for the next test
        Base.metadata.drop_all(engine)
        logging.info('Dropped database schema')
    request.addfinalizer(teardown)
