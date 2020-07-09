# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 15:40:04 2020

@author: Fatemeh
"""

from parsers import parser
import numpy as np
import pandas as pd
import nibabel as nib
import json
import sys
import os
from rw_utils import write_file


if __name__ == '__main__':
    """local computation that calculates average, median, average of upper and lower quartile for each ROI for nifti images"""
    args = json.loads(sys.stdin.read())
    quantity_list = ['average', 'median', 'upper quartile', 'lower quartile']
    (covariates, avg, median, upper_quartile, lower_quartile) = parser(args)
    ixs = covariates.index.intersection(avg.index)

    if ixs.empty:
        raise Exception('No common covariates and data subjects at ' +args["state"]["clientId"])
    else:
        covariates = covariates.loc[ixs]
        avg = avg.loc[ixs]
        median = median.loc[ixs]
        upper_quartile = upper_quartile.loc[ixs]
        lower_quartile = lower_quartile.loc[ixs]

    output_dict = {
         "covariates": covariates.to_json(orient='split'),
        "average": avg.to_json(orient='split'),
        "median": median.to_json(orient='split'),
        "upper quartile": upper_quartile.to_json(orient='split'),
        "lower quartile": lower_quartile.to_json(orient='split')
    }
    write_file(args, output_dict , 'output', 'local_output')
    computation_output = {"output":{ "list of quantities": quantity_list}}
    sys.stdout.write(json.dumps(computation_output))
