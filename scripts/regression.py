# -*- coding: utf-8 -*-
"""
This module contains functions to perform regression, calculate R^2 and MSE
and save the plots for R^2 and MSE
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import statsmodels.api as sm
import sys
import json


def regression_ols(X, y):
    """calculate regression for X and y and return R^2 and MSE values as a dataframe"""
    X = sm.add_constant(X) # adding a constant
    model = sm.OLS(y.astype(float), X.astype(float)).fit()
    return model.rsquared, model.mse_total

def calculate_regression(covariates_df, quantity_df, quantity_name):
    ROIs = list(map(int, quantity_df.columns))
    R_squared = []
    MSE_ = []
    for ROI in ROIs:
        y = quantity_df[ROI].values.reshape(-1,1)
        rsquared, mse = regression_ols(covariates_df, y)
        R_squared.append(rsquared)
        MSE_.append(mse)
    result_df = pd.DataFrame(index = ROIs)
    result_df['R squared'] = R_squared
    result_df['MSE'] = MSE_

    return result_df

def regression_plot(args, stats, which_stats, labels, which_quantity, mode, color):
    """plot R^2 and MSE values for ROIS for each quantity seperately in bar plots"""
    width = 0.4
    fig = plt.figure(figsize=(11.69, 8.27))
    plt.rcParams.update({'font.size': 5.5})
    values_toPlot = stats[which_stats]
    for i in range(4): #ploting in 4 slides
        n = len(labels)//4
        ax = fig.add_subplot(2,2,i+1)
        num_of_features = n #including only n regions in each plot
        start = i*n
        end = start + num_of_features
        values_toPlot_ = values_toPlot.iloc[start:end]
        x = np.arange(len(values_toPlot_))  # the label locations
        rects = ax.bar(x, values_toPlot_, width, label=which_stats, color = color)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel('Regions')
        ax.set_title('Linear Regression on '+which_quantity+' of values in each ROI for ' +mode)
        ax.set_xticks(x)
        ax.set_xticklabels(labels[start:end])
        ax.legend(loc='upper right')

        plt.grid(linestyle='--', linewidth = 0.25)
    fig.tight_layout()
    output_dir = args["state"]["transferDirectory"]
    plt.savefig(os.path.join(output_dir, "plot_"+which_stats+"_for_"+which_quantity+"_"+mode+".pdf"))
    plt.clf()
    plt.close('all')
