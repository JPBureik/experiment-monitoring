#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 18:20:24 2020

@author: jp
"""
import csv
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('tkagg')
from matplotlib import pyplot as plt
from gui import ExpSurvGUI


def import_data():

    # Import csv to DataFrame
    with open('exp_surv_test.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                header = row
                df = pd.DataFrame(data=None, columns=header)
                line_count += 1
            else:
                df = df.append(pd.DataFrame([[i for i in row]], columns=header, dtype=float))
                line_count += 1
    df.index = np.arange(0, line_count-1, 1)
    return df

def plot_data(df):
    x_interv = round(len(df)/9)
    a = df['AnalogIn0'].to_numpy(dtype=float)
    fig_to_plot = plt.figure(1)
    plt.plot(a)
    plt.xticks(df.index[::x_interv],labels=df['Time'].to_numpy(dtype=str)[::x_interv])
    plt.xlabel('Timestamp')
    plt.ylabel('Voltage [V]')
    plt.title('AnalogIn0')
    # plt.show()
    return fig_to_plot
    
def main():
    df = import_data()
    # fig_to_plot = plot_data(df['AnalogIn0'])
    program = ExpSurvGUI(df)
    program.root.mainloop()
    
if __name__ == "__main__":
    main()

