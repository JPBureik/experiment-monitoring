#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 10:03:16 2021

@author: jp

Exception handling module for the experiment monitoring suite.

Centralizes exception handling by regrouping all output to the specified log
file.
"""

# Standard library imports:
import getpass
from pathlib import Path
import os
import glob
from datetime import date, datetime
import traceback


class ExceptionHandler():

    def __init__(self):
        self.log_dir = Path('/home/' + getpass.getuser() + '/.exp_monitor')
        self._overwrite_log_file = True
        self._log_full_tb = False
        self._verbose = False

    @property
    def overwrite_log_file(self):
        """Boolean to overwrite old log files or not"""
        return self._overwrite_log_file

    @overwrite_log_file.setter
    def overwrite_log_file(self, overwrite_log_file):
        if type(overwrite_log_file) == bool:
            self._overwrite_log_file = overwrite_log_file

    @property
    def log_full_tb(self):
        """Write entire traceback to log file instead of just one line."""
        return self._log_full_tb

    @log_full_tb.setter
    def log_full_tb(self, log_full_tb):
        if type(log_full_tb) == bool:
            self._log_full_tb = log_full_tb

    @property
    def verbose(self):
        """Print full exception traceback to stdout."""
        return self._verbose

    @verbose.setter
    def verbose(self, verbose):
        if type(verbose) == bool:
            self._verbose = verbose

    def create_log_file(self):
        """Check for log file directory and overwrite old log file."""
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)
        if self._overwrite_log_file:
            for f in glob.glob(str(self.log_dir) + '/log_*.txt'): os.remove(f)
            self.log_file = self.log_dir / ('log_'
                                    + date.today().strftime('%Y_%m_%d')
                                    + '.txt')
        else:
            self.log_file = self.log_dir / ('log_'
                                    + datetime.now().strftime(
                                        '%Y_%m_%d_%H_%M_%S') + '.txt')
        self.log_file.touch()

    def log_exception(self, sensor, e):
        """Append exception description to log file."""
        log_str = "Data acquisition failure for {} at {} due to {}: {}.\n".format(
                    sensor.descr,
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    type(e).__name__.strip('<>').split("'")[0],
                    e.args[0]
                    )
        with open(self.log_file, 'a') as logf:
            logf.write(log_str)
            if self._log_full_tb:
                logf.write(traceback.format_exc())
                logf.write('---\n')
        if self._verbose:
            print(log_str.rstrip())
            traceback.print_exc()
