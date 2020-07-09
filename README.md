# coinstac_regression_vbm_stats
Coinstac code for decentralized regression on statistics extracted from VBM dataset. The statistics include average, median, and
average of lower and upper quartile of ROIs masked from NIfTI files.

The code plots R^2 and MSE values for each quantity separately.  

Tools: Python 3.6.5, coinstac-simulator 4.2.0

Steps to run: \
1- sudo npm i -g coinstac-simulator@4.2.0 \
2- git clone  https://github.com/trendscenter/coinstac-regression-vbm-stats.git \
3- cd coinstac-regression-vbm-stats \
4- docker build -t regression-vbm-stats . \
5- coinstac-simulator
