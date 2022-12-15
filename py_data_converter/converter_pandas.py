# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import io

import pandas as pd
import os

from app import app
from py_data_converter.converter_csv import convert_csv_to_django_models, convert_csv_to_flask_models, parse_csv


def convert_pandas_to_csv(file):
    df = pd.read_pickle(file)
    df = df.set_index(df.columns[1])
    file1 = df.to_csv()
    return file1


