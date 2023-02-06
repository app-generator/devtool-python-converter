# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = (os.getenv('DEBUG', 'False') == 'True')

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')

    # App Config - the minimal footprint
    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_9999')

    # Google Apikey
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', None)

    # temp directory for sqlite_dbms
    TEMP_FILE_DIRECTORY = 'app\\temp\\'

    # Input file limit
    INPUT_LIMIT = 500000

    # App Valid INPUTs
    ALLOWED_EXTENSIONS = {'json', 'yaml', 'csv', 'pkl'}
    