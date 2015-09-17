# -*- coding: utf-8 -*-
from topanga.__init__ import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    description='Topanga: A Python library to create a grouping of docker containers.',
    author='Nik Ridder',
    url='http(s)://the-destro.github.io/topanga',
    download_url='http://github.com/the-destro/topanga',
    author_email='francis[dot]ridder[at]gmail[dot]com',
    version=__version__,
    install_requires=[
        'docker-py>=1.4.0'
    ],
    extras_require={
        'testing': [
            'pytest>=2.7.0',
            'mock>=1.0.1',
            'tox>=1.9.2'
        ],
    },
    packages=['topanga'],
    scripts=[],
    name='topanga',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
