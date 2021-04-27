#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 08:36:14 2021

@author: jp
"""
#%%

import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

real_p = {'0828': 3.9e-9, '0830': 2.1e-9}
real_v = {'0828': 3.17, '0830': 2.85}
ard_p = {'0828': 5.13247861409858e-9, '0830': 2.1628279468830034e-9}
ard_v = {'0828': 3.2103271484375, '0830': 2.83502197265625}

real_data_x = [real_v['0828'], real_v['0830']]
real_data_y = [real_p['0828'], real_p['0830']]

def fit_fctn(v, a, b, c, d):
    return a * 10 ** (b * v - c) + d

# Guess initial parameters for the fit:
initial_guess = [0.85, 1, 11.56, 0]
# Set bounds for the fit:
bounds = ([0, 0, 0, -100], [10, 10, 20, 100])
# Perform fit:
popt, pcov = curve_fit(fit_fctn, real_data_x, real_data_y, p0=initial_guess, bounds=bounds)
# Calculate one standard deviation error on fits:
perr = np.sqrt(np.diag(pcov))
# Create fitted data with the optimal parameters found by the fit:
data_fitted = [fit_fctn(x, *popt) for x in real_data_x]

fig = plt.figure()
ax = plt.gca()
ax.scatter(real_data_x, real_data_y)
ax.set_yscale('log')
ax.semilogy(real_data_x, data_fitted)
ax.set_title(['%.2f' % elem for elem in popt])

def calib_fctn(v):
    return 0.85 * 10 ** (v - 11.56)

test = [calib_fctn(i) for i in list(ard_v.values())]

ax.scatter(list(ard_v.values()), test, c='r')

accepted_range = [calib_fctn(i) for i in [0, 3.3]]
