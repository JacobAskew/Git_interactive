#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import some things, maybe some more things

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import random

# Creating some data in a way you can optimize or change yourself

freq = np.arange(0, 3000, 3)
data = []
for i in range(1000):
    measurement = ( 1 * (freq[i]/1500) ** (4.4) ) + 0.5 * random.uniform(0, 2)  # Sinusoidal pattern with random variation
    measurement_err = measurement * 0.05 * random.uniform(0, 2)
    data.append((freq[i], measurement, measurement_err))
data = np.asarray(data)

# Define some functions


def powerlaw(xdata, alpha, constant):
    '''
    Hello this is a test comment :)
    xdata: data
    alpha: exponent
    constant: normalisation 

    returns power law with above variables
    '''
    return constant * (xdata/1500)**alpha    


def get_index(xdata=None, ydata=None, yerrdata=None, Plot=True, Filename=None):
    '''
    xdata: data along axis 0 (xaxis) of eventual plot
    ydata: data along axis 1 (yaxis) of eventual plot
    yerrdata: error on ydata
    Plot: boolean, make/don't make plot
    Filename: name under which to save the file, excluding type (e.g. .png), including path from code directory 
    '''
        
    popt, pcov = curve_fit(powerlaw, xdata, ydata)#, sigma=yerrdata)
    
    index = popt[0]
    perr = np.sqrt(np.diag(pcov))
    index_err = perr[0]

    if Plot:
        get_plot(xdata, ydata, yerrdata, Filename)
    return index, index_err


def get_plot(xdata=None, ydata=None, yerrdata=None, Filename=None):
    
    popt, pcov = curve_fit(powerlaw, xdata, ydata)
    
    fig = plt.figure(figsize=(9, 9))
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(xdata, ydata, c='C0', alpha=0.8)
    ax.errorbar(xdata, ydata, yerr=yerrdata, fmt=' ', alpha=0.1)
    ax.plot(xdata, powerlaw(xdata, *popt), 'r-',
             label=r'fit: $\alpha$=%5.3f, C=%5.3f' % tuple(popt))
    ax.set_ylabel(r"Scintillation Bandwidth, $\Delta\nu_D$ (MHz)")
    ax.set_xlabel("Observational Frequency (MHz)")
    ax.legend()
    if Filename:
        ax.savefig(Filename+'.png')
    ax.show()
    ax.close()
    
    return "Plot go brrrrr"



# Call the functions and print/save results

index, index_err = get_index(xdata=data[:, 0], ydata=data[:, 1], yerrdata=data[:, 2], Plot=True, Filename=None)
print("The relationship between observational frequency and scintilation bandwidth, alpha, was found to be: alpha=", index, "+/-", index_err)
