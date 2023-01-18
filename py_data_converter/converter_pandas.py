# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import pandas as pd
from platform import python_version

def pkl_to_pandas(file):

    try:
        df = pd.read_pickle(file)
        df = df.set_index(df.columns[1])
        return df
    except:
        return None

def convert_pandas_to_csv(file):
    
    try:
        df = pkl_to_pandas(file)
        return df.to_csv()
    except:
        return None
