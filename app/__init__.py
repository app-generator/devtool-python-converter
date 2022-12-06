# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# import Flask 
from flask import Flask
from flask_cors import CORS

# Inject Flask magic
app = Flask(__name__)

CORS(app)

# App Config - the minimal footprint
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'S#perS3crEt_JamesBond'
app.config['UPLOAD_FOLDER'] = app.root_path
ALLOWED_EXTENSIONS = {'json', 'yaml', 'csv', 'pkl'}

# Import routing to render the pages
from app import views
