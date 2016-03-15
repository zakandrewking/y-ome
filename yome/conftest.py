# -*- coding: utf-8 -*-

from yome import Session, Base
from yome.models import settings

import pytest
import os
import logging
from sqlalchemy import create_engine

@pytest.fixture(scope='session')
def test_db(request):
    test_db = 'yome_test'
    os.system('dropdb %s' % test_db)
    os.system('createdb %s -U %s' % (test_db, settings['user']))
    test_settings = {k: (test_db if k == 'database' else v)
                     for k, v in settings.items()}
    engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'
                           .format(**test_settings))
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

@pytest.fixture(scope='session')
def session(request, test_db):
    """Make a session"""
    def teardown():
        Session.close_all()
    request.addfinalizer(teardown)
    return Session()
