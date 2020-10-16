#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 18:20:24 2020

@author: jp
"""

from tkinter import *
from tkinter import ttk
import platform
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import pandas as pd

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

df = import_data()


def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

root = Tk()
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding="3 3 12 12")

mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind("<Return>", calculate)

root.mainloop()


















# root = tkinter.Tk()
# root.wm_title("Embedding in Tk")

# fig = Figure(figsize=(5, 5), dpi=100)
# x_interv = round(len(df)/8)
# a = df['AnalogIn0'].to_numpy(dtype=float)
# fig.add_subplot(111, title='AnalogIn0', xlabel='Timestamp', ylabel='Voltage [V]', xticks=df.index[::x_interv], xticklabels=df['Time'].to_numpy(dtype=str)[::x_interv]).plot(a)

# os_info = platform.system()
# if os_info in {'Windows', 'Darwin'}:
#     os_attr = '-fullscreen'
# elif os_info == 'Linux':
#     os_attr = '-zoomed'
# root.attributes(os_attr, 'true')
# fullScreenState = False

# canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# canvas.draw()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate

# tkinter.mainloop()
# # If you put root.destroy() here, it will cause an error if the window is
# # closed with the window manager.






