# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import re
from py_data_converter.common import *


def parse_csv(file):
    if type(file) == str:
        fields_string = file.split('\n')
        values_string = fields_string[1]
        fields_string = fields_string[0]
    else:
        fields_string = file.readline().decode('utf-8')
        values_string = file.readline().decode('utf-8')
    fields = fields_string.split(',')
    values = values_string.split(',')
    types = find_type(values)


    model = {}
    for i in range(len(fields)):
        model[fields[i]] = {'type': types[i]}

    return model


def convert_csv_to_django_models(model, filename):
    response = {}
    # the class name is guessed via filename
    codes = f"class {filename}(models.Model):\n\tID = models.AutoField(primary_key=True)\n"
    response[filename] = model
    django_code = get_django_model(model)
    codes = codes + django_code
    response['#codes$'] = codes
    return response


def convert_csv_to_flask_models(model, filename):
    response = {}
    # the class name is guessed via filename
    codes = f"class {filename}(db.Model):\n\tID = db.Column(db.Integer, primary_key=True,autoincrement=True)\n"
    response[filename] = model
    django_code = get_flask_model(model)
    codes = codes + django_code
    response['#codes$'] = codes
    return response


def find_type(values):
    numbers = "[0-9]"
    alphabets = "[a-zA-Z]"
    not_number_alphabet = "[^a-zA-Z0-9.]"
    types = []

    for value in values:

        has_number = re.search(numbers, value)
        has_alphabet = re.search(alphabets, value)
        has_extra = re.search(not_number_alphabet, value)
        if value:
            if ' ' not in value:
                if has_number and not has_alphabet:
                    if has_extra:
                        types.append('string')
                    elif '.' in value:
                        types.append('number')
                    else:
                        types.append('integer')
                else:
                    types.append('string')
            else:
                types.append('string')
        else:
            types.append('string')

    return types


if __name__ == '__main__':
    print(convert_csv_to_flask_models(
        "C:/Users/Mahdi/Downloads", "sales.csv"))
