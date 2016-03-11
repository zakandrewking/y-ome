# -*- coding: utf-8 -*-

from yome.models import Base, config

def test_config():
    assert config.get('DATABASE', 'user')
