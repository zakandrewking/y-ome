from os.path import join, dirname, realpath
import sys
from setuptools import setup

directory = dirname(realpath(__file__))
sys.path.insert(0, join(directory, 'yome'))
version = __import__('version').__version__

setup(
    name='yome',
    version=version,
    packages=['yome'],
)
