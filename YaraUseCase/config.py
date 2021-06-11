"""
Module that describes different configurations

Created By: Jettin Joy
Created On: 06/12/2021
"""


import os


class Config:
    """Configurations for DataBase"""
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    db = os.environ.get('POSTGRES_DB')
    host = os.environ.get('DB_SERVICE')
    port = os.environ.get('DB_PORT')
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               or
                        f"postgresql://{user}:{password}@{host}:{host}/{db}")
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = os.environ.get('SERECT_KEY')


class TestConfig:
    """Configurations for TEST"""

    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    db = os.environ.get('POSTGRES_DB')
    host = os.environ.get('DB_SERVICE')
    port = os.environ.get('DB_PORT')
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               or
                        f"postgresql://{user}:{password}@{host}:{host}/{db}")
    SQLALCHEMY_TRACK_MODIFICATION = False
    SECRET_KEY = os.environ.get('SERECT_KEY')
