__author__ = 'vako'

from setuptools import setup

setup(
    name="django-psql-view",
    url="https://github.com/valentinkozhevnik/django-psql-view",
    author="valentin Kozhevnik",
    author_email="valentinkozhevnik@gmail.com",
    version="0.0.1a",
    packages=[
        'psqlview'
    ],
    install_requires=[
        'django>=1.6',
        'psycopg2>=2.5.4',
    ]
)