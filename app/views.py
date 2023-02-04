# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import io
import os

# from Google import Create_Service
import pandas as pd
import requests
from app.util import *

# Flask modules
from flask import jsonify, send_from_directory
from flask import render_template, request, Response
from werkzeug.utils import secure_filename
# App modules
from app import app
from py_data_converter.converter_csv import convert_csv_to_django_models, convert_csv_to_flask_models, parse_csv
from py_data_converter.converter_openapi import convert_openapi_json_to_django_models, \
    convert_openapi_json_to_flask_models, \
    parse_yaml, parse_json
from py_data_converter.converter_pandas import convert_pandas_to_csv, pkl_to_pandas
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import random
import string


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_tables(db):
    db.load_models()
    tables = db.get_tables_name()
    return tables


def connect_to_sqlite(url):
    url = url + '?raw=true'
    r = requests.get(url)
    file = r.content
    if len(file) < app.config['INPUT_LIMIT']:
        name = app.config['TEMP_FILE_DIRECTORY'] + f'{get_random_string(10)}.sqlite3'
        temp = open(name, 'wb')
        temp.write(file)
        temp.close()
        db = DbWrapper()
        db.driver = COMMON.DB_SQLITE
        db.db_name = name
        db.connect()
        return db, name


def connect_to_db(db_driver, db_name, user, password, host, port):
    db = DbWrapper()
    if db_driver == 'DB_SQLITE':
        db.driver = COMMON.DB_SQLITE
    elif db_driver == 'DB_MYSQL':
        db.driver = COMMON.DB_MYSQL
    elif db_driver == 'DB_PGSQL':
        db.driver = COMMON.DB_PGSQL
    else:
        return None
    db.db_name = db_name
    db.db_user = user
    db.db_pass = password
    db.db_host = host
    db.db_port = port
    db.connect()
    return db


def get_csv_table(db, name):
    db.load_models()
    model = db.dump_model_data(name)
    return model


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


def error_message(message, code=400):
    error = {'message': message}
    return Response(response=json.dumps(error), status=code, mimetype='application/json')


def handle_output(input_file, input_type, output_type, filename):
    if output_type == 'Flask':
        if input_type == 'csv':
            model = parse_csv(input_file)
            flask_response = convert_csv_to_flask_models(model, filename)
        elif input_type == 'pkl':
            input_file = convert_pandas_to_csv(input_file)
            model = parse_csv(input_file)
            flask_response = convert_csv_to_flask_models(model, filename)
        elif input_type == 'json':
            openapi_schema = parse_json(input_file)
            flask_response = convert_openapi_json_to_flask_models(openapi_schema)
        elif input_type == 'yaml':
            openapi_schema = parse_yaml(input_file)
            flask_response = convert_openapi_json_to_flask_models(openapi_schema)
        else:
            return error_message('the combination of input file and output desired is not supported!')
        return {'flask': flask_response}

    elif output_type == 'Django':
        if input_type == 'csv':
            model = parse_csv(input_file)
            django_response = convert_csv_to_django_models(model, filename)
        elif input_type == 'pkl':
            input_file = convert_pandas_to_csv(input_file)
            model = parse_csv(input_file)
            django_response = convert_csv_to_django_models(model, filename)
        elif input_type == 'json':
            openapi_schema = parse_json(input_file)
            django_response = convert_openapi_json_to_django_models(openapi_schema)
        elif input_type == 'yaml':
            openapi_schema = parse_yaml(input_file)
            django_response = convert_openapi_json_to_django_models(openapi_schema)
        else:
            return error_message('the combination of input file and output desired is not supported!')
        return {'django': django_response}
    elif output_type == 'DataTable':
        if input_type == 'csv':
            csv_file = pd.read_csv(input_file, index_col=0)
        elif input_type == 'pkl':
            csv_file = pkl_to_pandas(input_file)
        elif input_type == 'pandas':
            csv_file = input_file
        else:
            return error_message('the input file is not supported!')
        headings = [row for row in csv_file.head()]
        return render_template('datatb/datatb.html', **{
            'model_name': 'model_name',
            'headings': headings,
            'data': [[val for val in record[1]] for record in csv_file.iterrows()],
        })
    elif output_type == 'Charts':
        if input_type == 'csv':
            csv_file = pd.read_csv(input_file, index_col=0)
        elif input_type == 'pkl':
            csv_file = pkl_to_pandas(input_file)
        elif input_type == 'pandas':
            csv_file = input_file
        else:
            return error_message('the input file is not supported!')
        response = jsonify(jsonify_csv(csv_file))
        return response
    else:
        if input_type == 'pandas':
            file = input_file.to_csv()
            response = handle_output(file, 'csv', 'Flask', filename)
            response.update(handle_output(file, 'csv', 'Django', filename))
            return response
        else:
            if input_type == 'csv':
                model = parse_csv(input_file)
                flask_response = convert_csv_to_flask_models(model, filename)
                django_response = convert_csv_to_django_models(model, filename)
            elif input_type == 'pkl':
                input_file = convert_pandas_to_csv(input_file)
                model = parse_csv(input_file)
                flask_response = convert_csv_to_flask_models(model, filename)
                django_response = convert_csv_to_django_models(model, filename)
            elif input_type == 'json':
                openapi_schema = parse_json(input_file)
                flask_response = convert_openapi_json_to_flask_models(openapi_schema)
                django_response = convert_openapi_json_to_django_models(openapi_schema)
            elif input_type == 'yaml':
                openapi_schema = parse_yaml(input_file)
                flask_response = convert_openapi_json_to_flask_models(openapi_schema)
                django_response = convert_openapi_json_to_django_models(openapi_schema)
            elif input_type == 'pandas':
                file = input_file.to_csv()
                return handle_output(file, 'csv', output_type, filename)
            else:
                return error_message('the combination of input file and output desired is not supported!')
        return {'django': django_response, 'flask': flask_response}


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
            if size >= app.config['INPUT_LIMIT']:
                return error_message(
                    f"Sorry your file is too big it must have less than {app.config['INPUT_LIMIT']} char", 400)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                output_desired = data['output']
                input_type = get_type(filename)
                return handle_output(file, input_type, output_desired, file.filename[:-4])

        elif post_type == 'url':
            url = data['url']

            if url.count('google') > 0:
                service = build('sheets', 'v4', developerKey=app.config['GOOGLE_API_KEY'])
                try:
                    sheet = service.spreadsheets()
                    spreadsheet_id = url.split('/')[-2]
                    sheet_metadata = sheet.get(spreadsheetId=spreadsheet_id).execute()
                    sheet_name = sheet_metadata['properties']['title']
                    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
                    sheet_data = result['values'][1:]
                    columns_names = result['values'][0]
                    df = pd.DataFrame(sheet_data, columns=columns_names)
                except HttpError as e:
                    return error_message('Could not get the csv file from google api.'.format(e.error_details))

                if df.shape[0] * df.shape[1] < app.config['INPUT_LIMIT']:
                    return handle_output(df, 'pandas', data['output'], sheet_name)
                else:
                    return error_message(
                        f"the input file exceeds memory policy:the input file's size must be less than {app.config['INPUT_LIMIT']}")
            elif url.count('github') > 0 and url.count('.csv') > 0:
                url1 = url + '?raw=true'
                r = requests.get(url1)
                file = r.content
                file = file.decode('utf-8')
                if len(file) < app.config['INPUT_LIMIT']:
                    filename = extract_filename(url)
                    output_desired = data['output']
                    csv_file = pd.read_csv(io.StringIO(file), index_col=0)
                    return handle_output(csv_file, 'pandas', output_desired, filename)
            else:
                return error_message('the url is not supported!')

        elif post_type == 'dbms':
            ip = data['ip']
            db_driver = data['db-driver']
            if db_driver == 'DB_SQLITE':
                # try:
                db, file_name = connect_to_sqlite(ip)
                tables = get_tables(db)
                db.close()
                os.remove(file_name)
                return jsonify(tables)
                # except Exception:
                #     return error_message('Could not connect to the DBMS!')
            else:
                dbname = data['dbname']
                port = data['port']
                user = data['user']
                password = data['password']
                # try:
                db = connect_to_db(db_driver, dbname, user, password, ip, int(port))
                tables = get_tables(db)
                return jsonify(tables)
                # except Exception:
                #     return error_message('Could not connect to the DBMS!')

        elif post_type == 'dbms-table':
            ip = data['ip']
            db_driver = data['db-driver']
            table_name = data['table-name']
            if db_driver == 'DB_SQLITE':
                try:
                    db, file_name = connect_to_sqlite(ip)
                    csv_table = get_csv_table(db, table_name)
                    output_desired = data['output']
                    if csv_table is None:
                        return error_message('The table is empty.')
                    csv_file = pd.read_csv(io.StringIO(csv_table), index_col=0)
                    db.close()
                    os.remove(file_name)
                    return handle_output(csv_file, 'pandas', output_desired, table_name)
                except Exception:
                    return error_message('Could not connect to the DBMS!')
            else:
                dbname = data['dbname']
                port = data['port']
                user = data['user']
                password = data['password']
                try:
                    db = connect_to_db(db_driver, dbname, user, password, ip, int(port))
                    csv_table = get_csv_table(db, table_name)
                    output_desired = data['output']
                    if csv_table is None:
                        return error_message('The table is empty.')
                    csv_file = pd.read_csv(io.StringIO(csv_table), index_col=0)
                    return handle_output(csv_file, 'pandas', output_desired, table_name)
                except Exception:
                    return error_message('Could not connect to the DBMS!')


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
