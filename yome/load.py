# -*- coding: utf-8 -*-

import logging

from yome.models import Base

def make_tables():
    logging.info('Creating tables')
    Base.metadata.create_all()
