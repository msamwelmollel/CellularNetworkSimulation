# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 19:29:39 2022

@author: msamw
"""
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

def bs_generator(n_bs):

    #Simulation window parameters
    xMin=0;xMax=1;
    yMin=0;yMax=1;
    xDelta=xMax-xMin;yDelta=yMax-yMin; #rectangle dimensions
    areaTotal=xDelta*yDelta;
     
    #Point process parameters
    lambda0=n_bs; #intensity (ie mean density) of the Poisson process  #BS per KM2
     
    #Simulate Poisson point process
    numbPoints = scipy.stats.poisson( lambda0*areaTotal ).rvs()#Mean poisson number of points
    xx = xDelta*scipy.stats.uniform.rvs(0,1,((numbPoints,1)))+xMin#x coordinates of Poisson points
    yy = yDelta*scipy.stats.uniform.rvs(0,1,((numbPoints,1)))+yMin#y coordinates of Poisson points
    #Plotting
    
    xx = xx * 1000 # convert to meter
    yy = yy * 1000 # convert to meter
    
    return np.concatenate((xx, yy), axis=1)

def plot_bs_distribution(n_bs):
    
    xx, yy = bs_generator(n_bs)
    

    
    plt.scatter(xx,yy, edgecolor='b', facecolor='none', alpha=0.5 )
    plt.xlabel("x"); plt.ylabel("y")
    
    return None

#plot_bs_distribution(10)