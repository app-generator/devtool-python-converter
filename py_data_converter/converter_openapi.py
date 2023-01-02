# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


import yaml
from py_data_converter.jsonparser import *
from py_data_converter.common import *


def Parse_input(source):
    allthekeys = [*get_keys(source)]
    alltheValues = [glom(source, item) for item in allthekeys]
    listofRefitem = [item for item in alltheValues if item.find('#') != -1]

    for item in listofRefitem:
        source = dict_replace_value(source, item, item.split('/')[-1])

    template_ = {'$ref': 'type'}
    replacedRefDict = replace_keys(source, template_)

    # OOP Representation
    openAPI_schema = OAJsonParser(replacedRefDict)

    return openAPI_schema


def convert_openapi_json_to_django_models(openAPI_schema):
    models = openAPI_schema.get_models()
    response = {}
    codes = ""
    for m in models:
        codes = codes + f"class {m}(models.Model):\n\tID = models.AutoField(primary_key=True)\n"
        model = openAPI_schema.get_model_dict(m)
        response[m] = model
        django_code = get_django_model(model)
        codes = codes + django_code
    response['#codes$'] = codes
    return response



def convert_openapi_json_to_flask_models(openAPI_schema):
    models = openAPI_schema.get_models()
    response = {}
    codes = ""
    for m in models:
        codes = codes + f"class {m}(db.Model):\n\tID = db.Column(db.Integer, primary_key=True,autoincrement=True)\n"
        model = openAPI_schema.get_model_dict(m)
        response[m] = model
        flask_code = get_flask_model(model)
        codes = codes + flask_code
    response['#codes$'] = codes
    return response


def parse_yaml(file):
    configuration = yaml.safe_load(file)
    file = json.loads(json.dumps(configuration))
    return Parse_input(file)

def parse_json(file):
    source = json.load(file)
    return Parse_input(source)


if __name__ == '__main__':
    print(convert_openapi_json_to_django_models(
        "C:/Users/Mahdi/Desktop/openapi parser/devtool-openapi-parser/io-samples", "products-with-price.json"))
