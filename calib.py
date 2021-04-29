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
import datetime
import pickle

calib_meas = []
calib_meas.append((datetime.datetime(2021, 4, 27, 8, 28), (3.9e-9, 3.17)))
calib_meas.append((datetime.datetime(2021, 4, 27, 8, 30), (2.1e-9, 2.85)))
calib_meas.append((datetime.datetime(2021, 4, 27, 10, 46), (1.3e-9, 2.61)))
calib_meas.append((datetime.datetime(2021, 4, 27, 11, 52), (7.5e-10, 2.31)))
calib_meas.append((datetime.datetime(2021, 4, 27, 12, 16), (6.9e-10, 2.27)))
calib_meas.append((datetime.datetime(2021, 4, 27, 13, 26), (8.2e-10, 2.36)))
calib_meas.append((datetime.datetime(2021, 4, 27, 15, 55), (1.2e-9, 2.59)))
calib_meas.append((datetime.datetime(2021, 4, 28, 8, 10), (4.2e-9, 3.20)))
calib_meas.append((datetime.datetime(2021, 4, 28, 8, 17), (2.0e-9, 2.84)))
calib_meas.append((datetime.datetime(2021, 4, 28, 9, 13), (1.5e-9, 2.68)))
calib_meas.append((datetime.datetime(2021, 4, 28, 9, 54), (1.4e-9, 2.66)))
calib_meas.append((datetime.datetime(2021, 4, 29, 7, 59), (7.8e-11, 1.10)))
calib_meas.append((datetime.datetime(2021, 4, 29, 15, 44), (3.7e-10, 1.93)))
calib_meas.append((datetime.datetime(2021, 4, 29, 15, 44), (3.7e-10, 1.93)))
calib_meas.append((datetime.datetime(2021, 4, 29, 15, 44), (3.9e-10, 1.97)))

pickle.dump(calib_meas, open( "calib.p", "wb" ))

data_x = [calib_meas[i][1][1] for i in range(len(calib_meas))]
data_y = [calib_meas[i][1][0] for i in range(len(calib_meas))]

# Assume P(V) strictly monotonous:
data_x.sort()
data_y.sort()

def pfeiffer(v):
    return 10**(v-10.5)

data_pfeiffer = [pfeiffer(data_x[i]) for i in range(len(data_x))]

def fit_fctn(v, a, b, c, d):
    return a * 10 ** (b * v - c) + d

# Guess initial parameters for the fit:
initial_guess = [2.4, 1, 10, 0]
# Set bounds for the fit:
bounds = ([0, 0, 0, -100], [10, 10, 20, 100])
# Perform fit:
popt, pcov = curve_fit(fit_fctn, data_x, data_y, p0=initial_guess, bounds=bounds)
# Calculate one standard deviation error on fits:
perr = np.sqrt(np.diag(pcov))
# Create fitted data with the optimal parameters found by the fit:
data_fitted = [fit_fctn(x, *popt) for x in data_x]

fig = plt.figure()
ax = plt.gca()
ax.scatter(data_x, data_y)
ax.set_yscale('log')
ax.semilogy(data_x, data_fitted, 'b', label='Measurement + Fit')
ax.semilogy(data_x, data_pfeiffer, 'r', label='Pfeiffer')
ax.set_xlabel('Voltage [V]')
ax.set_ylabel('Pressure [mbar]')
ax.legend()
ax.set_title(r'Fit results: $P(V) = %.2f \times 10^{%.2f \times V - %.2f} + %.2f$' % (popt[0], popt[1], popt[2], popt[3]))

def calib_fctn(popt, v):
    return popt[0] * 10 ** (popt[1] * v - popt[2]) + popt[3]

accepted_range = [calib_fctn(i) for i in [0, 3.3]]

v_float = 3.2
