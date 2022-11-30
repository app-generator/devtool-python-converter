# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
import math
import os
import sys
import logging
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
from py_data_converter.converter_pandas import convert_pandas_to_flask_models, convert_pandas_to_django_models


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_type(filename):
    return filename.rsplit('.', 1)[1].lower()


# App main route + generic
# routing

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        # front

        data = request.form
        post_type = data['type']
        if post_type == 'file':
            # check if the post request has the file part
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                output_desired = data['output']
                # front
                flask_response = ''
                django_response = ''
                input_type = get_type(filename)
                print(output_desired)
                if output_desired == 'Flask':
                    if input_type == 'csv':
                        flask_response = convert_csv_to_flask_models(app.config['UPLOAD_FOLDER'], filename)
                    elif input_type == 'json':
                        flask_response = convert_openapi_json_to_flask_models(app.config['UPLOAD_FOLDER'], filename)
                    elif input_type == 'yaml':
                        flask_response = convert_openapi_yaml_to_flask_models(app.config['UPLOAD_FOLDER'], filename)
                    elif input_type == 'pkl':
                        flask_response = convert_pandas_to_flask_models(app.config['UPLOAD_FOLDER'], filename)
                    data = {'flask': flask_response}
                    os.remove(app.config['UPLOAD_FOLDER'] + "\\" + filename)

                    return data
                elif output_desired == 'Django':
                    if input_type == 'csv':
                        django_response = convert_csv_to_django_models(app.config['UPLOAD_FOLDER'], filename)
                    elif input_type == 'json':
                        django_response = convert_openapi_json_to_django_models(app.config['UPLOAD_FOLDER'], filename)
                    elif input_type == 'yaml':
                        django_response = convert_openapi_yaml_to_django_models(app.config['UPLOAD_FOLDER'], filename)
                    elif input_type == 'pkl':
                        django_response = convert_pandas_to_flask_models(app.config['UPLOAD_FOLDER'], filename)
                    data = {'django': django_response}
                    os.remove(app.config['UPLOAD_FOLDER'] + "\\" + filename)
                    return data
                else:
                    if input_type == 'csv':
                        django_response = convert_csv_to_django_models(app.config['UPLOAD_FOLDER'], filename)
                        flask_response = convert_csv_to_flask_models(app.config['UPLOAD_FOLDER'], filename)
                    elif input_type == 'json':
                        django_response = convert_openapi_json_to_django_models(app.config['UPLOAD_FOLDER'],
                                                                                filename)
                        flask_response = convert_openapi_json_to_flask_models(app.config['UPLOAD_FOLDER'], filename)
                    elif input_type == 'yaml':
                        django_response = convert_openapi_yaml_to_django_models(app.config['UPLOAD_FOLDER'],
                                                                                filename)
                        flask_response = convert_openapi_yaml_to_flask_models(app.config['UPLOAD_FOLDER'], filename)
                    elif input_type == 'pkl':
                        flask_response = convert_pandas_to_flask_models(app.config['UPLOAD_FOLDER'], filename)
                        django_response = convert_pandas_to_django_models(app.config['UPLOAD_FOLDER'], filename)
                    os.remove(app.config['UPLOAD_FOLDER'] + "\\" + filename)
                    data = {'django': django_response, 'flask': flask_response}
                    return data
        elif post_type == 'update':
            data_recieved = data['update']
            request_django = data_recieved['django']
            request_flask = data_recieved['flask']
            flask_codes = ""
            for class_name in request_flask:
                flask_codes = flask_codes + f"class {class_name}(db.Model):\n\tID = db.Column(db.Integer, primary_key=True,autoincrement=True)\n"
                flask_code = get_flask_model(request_flask[class_name])
                flask_codes = flask_codes + flask_code
            request_flask['#codes$'] = flask_codes
            django_codes = ""
            for class_name in request_django:
                django_codes = django_codes + f"class {class_name}(models.Model):\n\tID = models.AutoField(primary_key=True)\n"
                django_code = get_django_model(request_flask[class_name])
                django_codes = django_codes + django_code
            request_django['#codes$'] = django_codes
            data = {'django': request_django, 'flask': request_flask}
            # front
            return data

    elif request.method == 'GET':
        # front
        return render_template('Converter/index.html')


import pandas as pd


@app.route('/datatb')
def dynamic_datatb():
    csv_file = pd.read_csv('sales.csv')
    headings = [row for row in csv_file.head()]

    return render_template('datatb/datatb.html', **{
        'model_name': 'model_name',
        'headings': headings,
        'data': [[val for val in record[1]] for record in csv_file.iterrows()],
    })
