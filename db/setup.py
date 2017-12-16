# -*- coding: utf-8 -*-

from os.path import join, dirname, realpath
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

directory = dirname(realpath(__file__))
sys.path.insert(0, join(directory, 'yome'))
version = __import__('version').__version__

setup(
    name='yome',
    version=version,
    packages=['yome'],
    install_requires=[
        'SQLAlchemy>=1.0.12',
        'psycopg2>=2.6.1',
        'pandas>=0.18.0',
        'pytest>=2.9.0',
        'xlrd>=0.9.4',
        'beautifulsoup4>=4.6.0',
    ],
)
