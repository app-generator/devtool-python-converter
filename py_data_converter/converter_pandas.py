# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import pandas as pd
import os

from app import app
from py_data_converter.converter_csv import convert_csv_to_django_models, convert_csv_to_flask_models


def convert_pandas_to_django_models(input_address, filename):
    df = pd.read_pickle(input_address +'\\'+ filename)
    df = df.set_index(df.columns[1])
    df.to_csv(input_address +'\\'+ f'{filename[:-4]}.csv')
    return convert_csv_to_django_models(input_address, f'{filename[:-4]}.csv')


def convert_pandas_to_flask_models(input_address, filename):
    df = pd.read_pickle(input_address +'\\'+ filename)
    df = df.set_index(df.columns[1])
    df.to_csv(input_address +'\\'+ f'{filename[:-4]}.csv')
    return convert_csv_to_flask_models(input_address, f'{filename[:-4]}.csv')
