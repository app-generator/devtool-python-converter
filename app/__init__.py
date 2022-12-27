# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# import Flask 
from flask import Flask
from flask_cors import CORS

from .config import Config

# Inject Flask magic
app = Flask(__name__)

CORS(app)

# load Configuration
app.config.from_object( Config ) 

# App Config - the minimal footprint
#app.config['TESTING'] = True
#app.config['SECRET_KEY'] = 'S#perS3crEt_JamesBond'
#app.config['UPLOAD_FOLDER'] = app.root_path
app.config['INPUT_LIMIT'] = 50000


# Import routing to render the pages
from app import views
