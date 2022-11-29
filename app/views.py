# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
import os

# Flask modules
from jinja2 import TemplateNotFound
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
# App modules
from app import app, ALLOWED_EXTENSIONS
from py_data_converter import *
from py_data_converter.common import get_flask_model, get_django_model
from py_data_converter.converter_csv import convert_csv_to_django_models, convert_csv_to_flask_models
from py_data_converter.converter_openapi import convert_openapi_json_to_django_models, \
    convert_openapi_json_to_flask_models, convert_openapi_yaml_to_django_models, convert_openapi_yaml_to_flask_models
from py_data_converter.converter_pandas import convert_pandas_to_flask_models


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_type(filename):
    return filename.rsplit('.', 1)[1].lower()


# App main route + generic routing
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # front
        return render_template('converter/index.html')


@app.route('/output/<name>', methods=['GET', 'POST'])
def pages(name):
    if request.method == 'GET':
        try:
            type = get_type(name)
            if type == 'csv':
                django_response = convert_csv_to_django_models(
                    app.config['UPLOAD_FOLDER'], name)
                flask_response = convert_csv_to_flask_models(
                    app.config['UPLOAD_FOLDER'], name)
            elif type == 'json':
                django_response = convert_openapi_json_to_django_models(
                    app.config['UPLOAD_FOLDER'], name)
                flask_response = convert_openapi_json_to_flask_models(
                    app.config['UPLOAD_FOLDER'], name)
            elif type == 'yml':
                django_response = convert_openapi_yaml_to_django_models(
                    app.config['UPLOAD_FOLDER'], name)
                flask_response = convert_openapi_yaml_to_flask_models(
                    app.config['UPLOAD_FOLDER'], name)

                data = {'django': django_response, 'flask': flask_response}
                return render_template(output_template, data=json.dumps(data))
        elif post_type == 'update':
            data_recieved = data['update']
            request_django = data_recieved['django']
            request_flask = data_recieved['flask']
            flask_codes = ""
            for class_name in request_flask:
                flask_codes = flask_codes + \
                    f"class {class_name}(db.Model):\n\tID = db.Column(db.Integer, primary_key=True,autoincrement=True)\n"
                flask_code = get_flask_model(request_flask[class_name])
                flask_codes = flask_codes + flask_code
            request_flask['#codes$'] = flask_codes
            django_codes = ""
            for class_name in request_django:
                django_codes = django_codes + \
                    f"class {class_name}(db.Model):\n\tID = db.Column(db.Integer, primary_key=True,autoincrement=True)\n"
                django_code = get_django_model(request_flask[class_name])
                django_codes = django_codes + django_code
            request_django['#codes$'] = django_codes
            data = {'django': request_django, 'flask': request_flask}
            # front
            render_template(output_template, data=data)
    elif request.method == 'GET':
        # front
        return render_template(home_page)
