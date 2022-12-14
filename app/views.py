# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import csv
import io
import json

# Flask modules
from werkzeug.datastructures import FileStorage
from flask import jsonify
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
# App modules
from app import app, ALLOWED_EXTENSIONS

from py_data_converter.converter_csv import convert_csv_to_django_models, convert_csv_to_flask_models, parse_csv
from py_data_converter.converter_openapi import convert_openapi_json_to_django_models, \
    convert_openapi_json_to_flask_models, \
    Parse_input, parse_yaml, parse_json
from py_data_converter.converter_pandas import convert_pandas_to_csv


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def jsonify_csv(df):
    values = [[val for val in record[1]] for record in df.iterrows()]
    headings = [row for row in df.head()]
    out = []
    for i in range(len(values)):
        out.append({})
        for j in range(len(values[i])):
            if(pd.isna(values[i][j])):
                out[i][headings[j]] = 'null'
            else:
                out[i][headings[j]] = values[i][j]
    return out

def get_type(filename):
    return filename.rsplit('.', 1)[1].lower()


# App main route + generic
# routing

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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
                output_desired = data['output']
                flask_response = ''
                django_response = ''
                input_type = get_type(filename)
                if output_desired == 'Flask':
                    if input_type == 'csv':
                        model = parse_csv(file)
                        flask_response = convert_csv_to_flask_models(model, file.filename[:-4])
                    elif input_type == 'json':
                        openAPI_schema = parse_json(file)
                        flask_response = convert_openapi_json_to_flask_models(openAPI_schema)
                    elif input_type == 'yaml':
                        openAPI_schema = parse_yaml(file)
                        flask_response = convert_openapi_json_to_flask_models(openAPI_schema)
                    elif input_type == 'pkl':
                        file = convert_pandas_to_csv(file)
                        model = parse_csv(file)
                        flask_response = convert_csv_to_flask_models(model, file.filename[:-4])
                    data = {'flask': flask_response}
                    return data
                elif output_desired == 'Django':
                    if input_type == 'csv':
                        model = parse_csv(file)
                        django_response = convert_csv_to_django_models(model, file.filename[:-4])
                    elif input_type == 'json':
                        openAPI_schema = parse_json(file)
                        django_response = convert_openapi_json_to_django_models(openAPI_schema)
                    elif input_type == 'yaml':
                        openAPI_schema = parse_yaml(file)
                        django_response = convert_openapi_json_to_flask_models(openAPI_schema)
                    elif input_type == 'pkl':
                        file = convert_pandas_to_csv(file)
                        model = parse_csv(file)
                        django_response = convert_csv_to_flask_models(model, file.filename[:-4])
                    data = {'django': django_response}
                    return data
                elif output_desired == 'DataTable':
                    if input_type == 'csv':
                        csv_file = pd.read_csv(file)
                    elif input_type == 'pkl':
                        csv_file = pd.read_pickle(file)
                    else:
                        flash('input file is not supported!')
                        return redirect(request.url)
                    headings = [row for row in csv_file.head()]

                    return render_template('datatb/datatb.html', **{
                        'model_name': 'model_name',
                        'headings': headings,
                        'data': [[val for val in record[1]] for record in csv_file.iterrows()],
                    })
                elif output_desired == 'Charts':
                    if input_type == 'csv':
                        csv_file = pd.read_csv(file)
                    elif input_type == 'pkl':
                        csv_file = pd.read_pickle(file)

                    else:
                        flash('input file is not supported!')
                        return redirect(request.url)
                    response = jsonify(jsonify_csv(csv_file))
                    return response
                else:
                    if input_type == 'csv':
                        model = parse_csv(file)
                        django_response = convert_csv_to_django_models(model, file.filename[:-4])
                        flask_response = convert_csv_to_flask_models(model, file.filename[:-4])
                    elif input_type == 'json':
                        openAPI_schema = parse_json(file)
                        django_response = convert_openapi_json_to_django_models(openAPI_schema)
                        flask_response = convert_openapi_json_to_flask_models(openAPI_schema)
                    elif input_type == 'yaml':
                        openAPI_schema = parse_yaml(file)
                        django_response = convert_openapi_json_to_flask_models(openAPI_schema)
                        flask_response = convert_openapi_json_to_flask_models(openAPI_schema)
                    elif input_type == 'pkl':
                        file1 = convert_pandas_to_csv(file)
                        model = parse_csv(file1)
                        flask_response = convert_csv_to_flask_models(model, file.filename[:-4])
                        django_response = convert_csv_to_django_models(model, file.filename[:-4])
                    data = {'django': django_response, 'flask': flask_response}
                    return data

    elif request.method == 'GET':
        return render_template('Converter/index.html')


import pandas as pd
