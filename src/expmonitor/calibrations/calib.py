#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 08:36:14 2021

@author: jp
"""
# %%

import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import datetime
import pickle
import os


class Calibrator:

    def __init__(self):
        self.object_descr = 'Pfeiffer TPG 300'
        self.measurement_descr = 'sc_vac'

        # Set floating value of input pin on Arduino:
        self.v_float = 3.2

        """ First calibration """
        # Create new calib file if one doesn't exist already, else load:
        if not os.path.isfile(os.getcwd() + '/calib.p'):
            self.calib_meas = []
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 27, 8, 28), (3.9e-9, 3.17)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 27, 8, 30), (2.1e-9, 2.85)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 27, 10, 46), (1.3e-9, 2.61)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 27, 11, 52), (7.5e-10, 2.31)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 27, 12, 16), (6.9e-10, 2.27)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 27, 13, 26), (8.2e-10, 2.36)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 27, 15, 55), (1.2e-9, 2.59)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 28, 8, 10), (4.2e-9, 3.20)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 28, 8, 17), (2.0e-9, 2.84)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 28, 9, 13), (1.5e-9, 2.68)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 28, 9, 54), (1.4e-9, 2.66)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 29, 7, 59), (7.8e-11, 1.10)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 29, 15, 44), (3.7e-10, 1.93)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 29, 15, 44), (3.7e-10, 1.93)))
            self.calib_meas.append(
                (datetime.datetime(2021, 4, 29, 15, 44), (3.9e-10, 1.97)))
            # pickle.dump(self.calib_meas, open('calib.p', 'wb' ))
        else:
            self.calib_meas = pickle.load(open('calib.p', 'rb'))

    # Interface for use in experiment monitoring:
    def calib_fctn(self, v):
        if not hasattr(self, 'popt'):
            self.calibrate(show=False)
        return (self.popt[0] * 10 ** (self.popt[1] * v - self.popt[2])
                + self.popt[3])

    def calibrate(self, show=True):
        self.data_x = [
            self.calib_meas[i][1][1] for i in range(len(self.calib_meas))]
        self.data_y = [
            self.calib_meas[i][1][0] for i in range(len(self.calib_meas))]

        # Assume strict monotony:
        self.data_x.sort()
        self.data_y.sort()

        # Compare with Pfeiffer calibration:
        def pfeiffer(v):
            return 10**(v-10.5)
        self.data_pfeiffer = [
            pfeiffer(self.data_x[i]) for i in range(len(self.data_x))]

        # Define fitting function:
        def fit_fctn(v, a, b, c, d):
            return a * 10 ** (b * v - c) + d

        # Guess initial parameters for the fit:
        initial_guess = [2.4, 1, 10, 0]

        # Set bounds for the fit:
        bounds = ([0, 0, 0, -100], [10, 10, 20, 100])

        # Perform fit:
        self.popt, self.pcov = curve_fit(
            fit_fctn, self.data_x, self.data_y,
            p0=initial_guess, bounds=bounds)

        # Calculate one standard deviation error on fits:
        self.perr = np.sqrt(np.diag(self.pcov))

        # Create fitted data with the optimal parameters found by the fit:
        self.data_fitted = [fit_fctn(x, *self.popt) for x in self.data_x]

        # Plot calibration result:
        if show is True:
            plt.figure()
            ax = plt.gca()
            ax.scatter(self.data_x, self.data_y)
            ax.set_yscale('log')
            ax.semilogy(
                self.data_x, self.data_fitted, 'b', label='Measurement + Fit')
            ax.semilogy(self.data_x, self.data_pfeiffer, 'r', label='Pfeiffer')
            ax.set_xlabel('Voltage [V]')
            ax.set_ylabel('Pressure [mbar]')
            ax.legend()
            ax.set_title(
                r'Fit results: $P(V) = %.2f \times 10^{%.2f \times V - %.2f}'
                r' + %.2f$' % (
                    self.popt[0], self.popt[1], self.popt[2], self.popt[3]))
            plt.show()

        # Set range of accessible values for monitoring:
        if not hasattr(self, 'accepted_range'):
            self.accepted_range = [self.calib_fctn(i) for i in [0, 3.3]]

    # Add datapoints to calibration:
    def append_calib(self):
        print('\nAdd data points for the %s to improve its calibration.\n'
              % self.object_descr)
        datetime_id = datetime.datetime.today()
        meas_input = input('Enter measured pressure in mbar (e.g. 1.1e-10):\n')
        voltage_input = input('Enter measured voltage in V (e.g. 2.9):\n')
        print('Recalibrating ...')
        self.calib_meas.append(
            (datetime_id, (float(meas_input), float(voltage_input))))
        self.calibrate()
        save_input = input('Save changes? (y/n)\n')
        if save_input == 'y':
            pickle.dump(self.calib_meas, open('calib.p', 'wb'))
            print('Changes saved.')


""" MAIN """

if __name__ == '__main__':

    calibration = Calibrator()
    calibration.append_calib()
