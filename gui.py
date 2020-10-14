#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 14:09:23 2020

@author: jp
"""
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import platform
import numpy as np

class ExpSurvGUI():
        
    def __init__(self, fig_to_plot):
        self.root = tk.Tk()
        self.root.wm_title("Experiment surveillance")        
        self.fig_to_plot = fig_to_plot
        self._set_fullscreen()
        # self.plot_fig()
        self.plot()

    # Set window size to fullscreen:
    def _set_fullscreen(self):
        os_info = platform.system()
        if os_info in {'Windows', 'Darwin'}:
            os_attr = '-fullscreen'
        elif os_info == 'Linux':
            os_attr = '-zoomed'
        self.root.attributes(os_attr, 'true')  
        self.fullScreenState = False
        
    # Plot figure:
    def plot_fig(self):
        
        canvas = FigureCanvasTkAgg(self.fig_to_plot, master=self.root)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row=0, column=0)
        
        figure = plt.Figure(figsize=(16,9), dpi=100)
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, self.root)
        chart_type.get_tk_widget().pack()
        ax.set_title('The Title for your chart')
        
        
    
    def plot (self):
        x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        v= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
        fig = Figure(figsize=(6,6))
        a = fig.add_subplot(111)
        a.scatter(v,x,color='red')
        a.invert_yaxis()

        a.set_title ("Estimation Grid", fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().pack()
        canvas.draw()
