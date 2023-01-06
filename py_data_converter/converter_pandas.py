# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import pandas as pd
from platform import python_version

def pkl_to_pandas(file):
    if python_version() > '3.8':
        df = pd.read_pickle(file)
    else:
        import pickle5
        df = pickle5.load(file)
    df = df.set_index(df.columns[1])
    return df


def convert_pandas_to_csv(file):
    df = pkl_to_pandas(file)
    return df.to_csv()
