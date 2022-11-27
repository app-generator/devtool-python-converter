# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import yaml
from jsonparser import *
from common import *




def Parse_input(input_address, filename):
    source = open(input_address + "/" + filename)
    source = json.load(source)
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

def get_django_model(model_dict):
    codes = ""
    for attribute_name in model_dict:
        if attribute_name == 'ID':
            continue
        codes = codes + f"\t{attribute_name} = "
        attribute = model_dict[attribute_name]
        attribute_type = attribute['type']
        if attribute_type == 'OneToOneField':
            codes = codes + f"models.OneToOneField()({attribute_type}_ID\n"
        elif attribute_type == 'ManyToManyField':
            codes = codes + f"models.ManyToManyField()({attribute_type}_ID\n"
        elif attribute_type == 'ForeignKey':
            codes = codes + f"models.ForeignKey()({attribute_type}_ID\n"
        elif attribute_type in django_fields:
            codes = codes + django_fields[attribute_type]
        else:
            codes = codes + f"models.ForeignKey({attribute_type})\n"
    return codes


def get_flask_model(model_dict):
    codes = ""
    for attribute_name in model_dict:
        if attribute_name == 'ID':
            continue
        codes = codes + f"\t{attribute_name} = "
        attribute = model_dict[attribute_name]
        attribute_type = attribute['type']
        if attribute_type == 'OneToOneField':
            ...
        # to_be_implemented
        elif attribute_type == 'ManyToManyField':
            ...
        # to_be_implemented

        elif attribute_type == 'ForeignKey':
            ...
        # to_be_implemented

        elif attribute_type in flask_fields:
            codes = codes + flask_fields[attribute_type]
        else:
            codes = codes + f"db.column(db.Integer, db.ForeignKey({attribute_type}.ID))\n"

    return codes


def convert_openapi_json_to_django_models(input_address, filename):
    openAPI_schema = Parse_input(input_address, filename)
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

def convert_openapi_yaml_to_django_models(input_address, filename):
    with open(input_address + "/" + filename, 'r') as file:
        configuration = yaml.safe_load(file)
    with open(input_address + "/converted_to_json.json", 'w') as json_file:
        json.dump(configuration, json_file)
    return convert_openapi_json_to_django_models(input_address, "/converted_to_json.json")


def convert_openapi_json_to_flask_models(input_address, filename):
    openAPI_schema = Parse_input(input_address, filename)
    models = openAPI_schema.get_models()
    response = {}
    codes = ""
    for m in models:
        codes = codes + f"class {m}(db.Model):\n\tID = db.Column(db.Integer, primary_key=True,autoincrement=True)\n"
        model = openAPI_schema.get_model_dict(m)
        response[m] = model
        django_code = get_flask_model(model)
        codes = codes + django_code
    response['#codes$'] = codes
    return response


def convert_openapi_yaml_to_flask_models(input_address, filename):
    with open(input_address + "/" + filename, 'r') as file:
        configuration = yaml.safe_load(file)

    with open(input_address + "/converted_to_json.json", 'w') as json_file:
        json.dump(configuration, json_file)
    return convert_openapi_json_to_flask_models(input_address, "/converted_to_json.json")


if __name__ == '__main__':
    print(convert_openapi_json_to_django_models(
        "C:/Users/Mahdi/Desktop/openapi parser/devtool-openapi-parser/io-samples", "products-with-price.json"))
