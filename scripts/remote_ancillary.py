# -*- coding: utf-8 -*-
"""
Created on Thu Jul 2 10:25:20 2020

@author: Fatemeh
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import statsmodels.api as sm
import sys
import json
from rw_utils import read_file

def json_to_df(jsonfile):
    """convert json file to a dataframe"""
    jsonfile = json.loads(jsonfile)
    df_fromjson = pd.DataFrame.from_dict(jsonfile, orient="index")

    col_name = df_fromjson.loc['columns']
    #remove nones
    col_name = list(filter(None.__ne__, col_name))
    indices = df_fromjson.loc['index']
    indices = indices.dropna()
    indices = list(filter(None.__ne__, indices))
    data = pd.DataFrame(df_fromjson.loc['data'])
    data = data.dropna()
    data_df = pd.DataFrame(data['data'].to_list(), columns=col_name)
    data_df.index = indices
    return data_df

def concat_local_outputs(args, which_quantity):
    """concatenates locals' outputs"""
    input_ = args["input"]
    input_dir = args["state"]["baseDirectory"]
    site_list = input_.keys()
    input_list = dict()
    for site in site_list:
        file_name = os.path.join(input_dir, site, 'local_output')
        input_list[site] = read_file(args, "input", file_name)
        covariates_df = json_to_df(input_list[site]['covariates'])
        y = json_to_df(input_list[site][which_quantity])
    covariates_df = covariates_df*1
    #ROIs = list(map(int, quantity_df.columns))
    return covariates_df, y

def SZ_HC_seperate(X, y):
    "seperates control and case"
    X_HC = X.loc[X['isControl'] != 0]
    X_SZ = X.loc[X['isControl'] != 1]
    y_HC = y.reindex(X_HC.index)
    y_SZ = y.reindex(X_SZ.index)
    return X_HC, y_HC, X_SZ, y_SZ
