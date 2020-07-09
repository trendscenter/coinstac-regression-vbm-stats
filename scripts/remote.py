# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 15:47:32 2020

@author: Fatemeh
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import statsmodels.api as sm
import sys
import json
from regression import calculate_regression, regression_plot
from rw_utils import read_file
from remote_ancillary import concat_local_outputs, SZ_HC_seperate, json_to_df

def regression_(args, covariates, y, quantity, mode):
    "calculates regression and plot R^2 and MSE"
    result_df = calculate_regression(covariates, y, quantity)
    labels = result_df.index
    regression_plot(args, result_df, 'R squared', labels, quantity, mode, 'c')
    regression_plot(args, result_df, 'MSE', labels, quantity, mode, 'blue')
    return result_df

def regression_HC_SZ(args, covariates, y, quantity):
    X_HC, y_HC, X_SZ, y_SZ = SZ_HC_seperate(covariates, y)
    result_HC = regression_(args, X_HC, y_HC, quantity, 'HC')
    result_SZ = regression_(args, X_SZ, y_SZ, quantity, 'SZ')
    return result_HC, result_SZ

if __name__ == '__main__':
    """remote computation that calculates regression and plot the results"""
    args = json.loads(sys.stdin.read())
    input_list = args["input"] #['average', 'median', 'upper quartile', 'lower quartile']
    userID = list(args["input"])[0]
    quantity_list = input_list[userID]["list of quantities"]
    for quantity in quantity_list:
        covariates, y = concat_local_outputs(args, quantity)
        result_df = regression_(args, covariates, y, quantity, 'HC&SZ')
        result_HC, result_SZ = regression_HC_SZ(args, covariates, y, quantity)
    output_dict = {
        "R squared": result_df['R squared'].to_json(orient='split'),
        "MSE": result_df['MSE'].to_json(orient='split'),
        "R squared_HC": result_HC['R squared'].to_json(orient='split'),
        "MSE_HC": result_HC['MSE'].to_json(orient='split'),
        "R squared_SZ": result_SZ['R squared'].to_json(orient='split'),
        "MSE_SZ": result_SZ['MSE'].to_json(orient='split'),
    }
    computation_output = {"output": output_dict, "success": True}
    #computation_output = {"output": {"id": result_df.to_json(orient='split')}, "success": True}
    sys.stdout.write(json.dumps(computation_output))
