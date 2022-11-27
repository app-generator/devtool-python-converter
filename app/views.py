# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask import render_template, request
from jinja2 import TemplateNotFound

# App modules
from app import app


# App main route + generic routing
@app.route('/')
def index():
    data = {}

    data['stuff'] = 'whatever'

    return render_template('converter/index.html', **data)


@app.route('/<path>')
def pages(path):
    try:

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template('pages/' + path)

    except TemplateNotFound:
        return render_template('pages/page-404.html'), 404
