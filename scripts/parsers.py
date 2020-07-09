# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 17:44:41 2020

@author: Fatemeh
"""

import os
import nibabel as nib
import glob
import numpy as np
import pandas as pd
import sys

def calculate_stats(roi_data):
    sorted_nifti_data = np.sort(roi_data, kind='quicksort')
    quartiles = np.array_split(roi_data, 4)
    return np.average(roi_data), np.median(roi_data), np.average(quartiles[0]), np.average(quartiles[3])

def apply_mask(mask, nifti_img):
    "apply mask on nifti file and return average, median, average of upper and lower quartile"
    stats = pd.DataFrame(index = range(1, int(np.amax(mask))+1), columns = ['average', 'median', 'lower quartile', 'upper quartile'])
    for i in range(1, int(np.amax(mask))+1):
        roi_masked_data = nifti_img[mask == i]
        stats['average'][i] = np.average(roi_masked_data)
        stats['median'][i] = np.median(roi_masked_data)
        sorted_nifti_data = np.sort(roi_masked_data, kind='quicksort')
        quartiles = np.array_split(roi_masked_data, 4)
        stats['lower quartile'][i] = np.average(quartiles[0])
        stats['upper quartile'][i] = np.average(quartiles[3])
    return stats

def parse_nifti(args, files):
    """read nifiti images, apply the mask and return the quntities for ROIs"""
    try:
        mask_file = nib.load(os.path.join(args["state"]["baseDirectory"],'aal_1.5.nii'))
        mask_data = np.asarray(mask_file.dataobj)
    except FileNotFoundError:
        raise Exception("Missing mask at " + args["state"]["clientId"])
    average_df = pd.DataFrame()
    median_df = pd.DataFrame()
    upper_quartile_df = pd.DataFrame()
    lower_quartile_df = pd.DataFrame()
    for file in files:
        if file:
            try:
                nifti_file = nib.load(os.path.join(args["state"]["baseDirectory"],file))
                nifti_data = np.asarray(nifti_file.dataobj)
                stats = apply_mask(mask_data, nifti_data)
                average_df[file] = stats['average']
                median_df[file] = stats['median']
                upper_quartile_df[file] = stats['upper quartile']
                lower_quartile_df[file] = stats['lower quartile']
            except pd.errors.EmptyDataError:
                continue
            except FileNotFoundError:
                continue
    return average_df.T, median_df.T, upper_quartile_df.T, lower_quartile_df.T

def parser(args):
    input_list = args["input"]
    X_info = input_list["covariates"]
    Y_info = input_list["data"]

    X_data = X_info[0][0]
    Y_data = Y_info[0]

    X_labels = X_info[1]

    X_data = pd.DataFrame.from_records(X_data)
    X_data.columns = X_data.iloc[0]
    X_data = X_data.drop(X_data.index[0])

    X_data.set_index(X_data.columns[0], inplace = True)
    X_ = X_data[X_labels]

    X = X_.apply(pd.to_numeric, errors = 'ignore')
    X = pd.get_dummies(X, drop_first=True)

    average, median, upper_quartile, lower_quartile = parse_nifti(args, Y_data)

    return X, average, median, upper_quartile, lower_quartile
