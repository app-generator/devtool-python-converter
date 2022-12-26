# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import csv
import io
import json
import os
# from google import Create_Service
import pandas as pd
import requests

# Flask modules
from werkzeug.datastructures import FileStorage
from flask import jsonify, send_from_directory
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
# App modules
from app import app

from py_data_converter.converter_csv import convert_csv_to_django_models, convert_csv_to_flask_models, parse_csv
from py_data_converter.converter_openapi import convert_openapi_json_to_django_models, \
    convert_openapi_json_to_flask_models, \
    Parse_input, parse_yaml, parse_json
from py_data_converter.converter_pandas import convert_pandas_to_csv


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def jsonify_csv(df):
    values = [[val for val in record[1]] for record in df.iterrows()]
    headings = [row for row in df.head()]
    out = []
    for i in range(len(values)):
        out.append({})
        for j in range(len(values[i])):
            if (pd.isna(values[i][j])):
                out[i][headings[j]] = 'null'
            else:
                out[i][headings[j]] = values[i][j]
    return out


def get_type(filename):
    return filename.rsplit('.', 1)[1].lower()


# App main route + generic
# routing

def extract_filename(url):
    parts = url.split('/')
    return parts[-1][:-4]


def run_batchUpdate_request(service, google_sheet_id, request_body_json):
    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=google_sheet_id,
            body=request_body_json
        ).execute()
        return response
    except Exception as e:
        print(e)
        return None


# def test_google_api():
#     CLIENT_SECRET_FILE = '<Client Secret file path>'
#     API_SERVICE_NAME = 'sheets'
#     API_VERSION = 'v4'
#     SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
#     GOOGLE_SHEET_ID = '1_z9OGyFnVKKvD2OidFNKF8vEXMzoddnLgbBCERLPgG8'
#
#     service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
#
#     """
#     Iterate Worksheets
#     """
#     gsheets = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEET_ID).execute()
#     sheets = gsheets['sheets']
#     print(sheets)

def test_github_api():
    url = 'https://github.com/app-generator/devtool-data-converter/raw/main/samples/data.csv?raw=true?raw=true'
    r = requests.get(url)
    file = r.content
    print(file.decode('utf-8'))


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
            file.stream.seek(0, 2)
            size = file.stream.tell()
            file.stream.seek(0)
            if size >= 50000:
                return 'Sorry your file is too big it must have less than 50000 char', 400
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
                        django_response = convert_openapi_json_to_django_models(openAPI_schema)
                    elif input_type == 'pkl':
                        file = convert_pandas_to_csv(file)
                        model = parse_csv(file)
                        django_response = convert_csv_to_django_models(model, file.filename[:-4])
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
                        django_response = convert_openapi_json_to_django_models(openAPI_schema)
                        flask_response = convert_openapi_json_to_flask_models(openAPI_schema)
                    elif input_type == 'pkl':
                        file1 = convert_pandas_to_csv(file)
                        model = parse_csv(file1)
                        flask_response = convert_csv_to_flask_models(model, file.filename[:-4])
                        django_response = convert_csv_to_django_models(model, file.filename[:-4])
                    data = {'django': django_response, 'flask': flask_response}
                    return data
        elif post_type == 'url':
            url = data['url']
            if url.count('github') > 0:
                url = url + '?raw=true'
                r = requests.get(url)
                file = r.content
                file = file.decode('utf-8')
            else:
                file = "Not implemented"
                ...

            if len(file) < 50000:
                filename = extract_filename(url)
                output_desired = data['output']
                flask_response = ''
                django_response = ''
                input_type = get_type(filename)

                if output_desired == 'DataTable':
                    if input_type == 'csv':
                        csv_file = pd.read_csv(file)
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
                    else:
                        flash('input file is not supported!')
                        return redirect(request.url)
                    response = jsonify(jsonify_csv(csv_file))
                    return response
                else:
                    if input_type == 'csv':
                        model = parse_csv(file)
                        django_response = convert_csv_to_django_models(model, filename)
                        flask_response = convert_csv_to_flask_models(model, filename)
                    data = {'django': django_response, 'flask': flask_response}
                    return data



    elif request.method == 'GET':
        return render_template('converter/index.html')


@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')


@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('./static/common', 'favicon.ico')


@app.route('/googlee35aa2f2fd7b0c5b.html')
def google_hash():
    return send_from_directory('.', 'googlee35aa2f2fd7b0c5b.html')
