# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import pandas as pd
def convert_pandas_to_csv(file):
    try:
        df = pd.read_pickle(file)
    except ValueError:
        import pickle5
        df = pickle5.load(file)
    df = df.set_index(df.columns[1])
    file1 = df.to_csv()
    return file1


