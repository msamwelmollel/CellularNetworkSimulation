# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 18:59:53 2022

@author: msamw
"""

import numpy as np 
import scipy.stats
import matplotlib.pyplot as plt

from mobility import random_waypoint


#Simulation window parameters
xMin=0;xMax=1;
yMin=0;yMax=1;
xDelta=xMax-xMin;yDelta=yMax-yMin; #rectangle dimensions

def static_user_position(x,y):
    
    
    return np.concatenate((np.reshape(np.array(x), (1,1)), np.reshape(np.array(y), (1,1))), axis=1)


def random_user_position(n_user):
    
    x = (xDelta*scipy.stats.uniform.rvs(0,1,((n_user,1)))+xMin)   * 1000#x coordinates of Poisson point
    y = (yDelta*scipy.stats.uniform.rvs(0,1,((n_user,1)))+yMin)   * 1000#y coordinates of Poisson point
    

    return np.concatenate((x, y), axis=1)



class mobile_user_position:  # https://github.com/panisson/pymobility
   

    def __init__(self, n_user, velocity_min=0.1, velocity_max=1.0, wt_max=1.0):

        self.next_pos = random_waypoint(n_user, dimensions=(1000, 1000), velocity=(velocity_min, velocity_max), wt_max=wt_max)
   


def plot_user_bs(ue_position, bs_position):
    
    plt.scatter(bs_position[:, 0],bs_position[:,1], edgecolor='b', facecolor='none', alpha=0.5 )
    plt.scatter(ue_position[:, 0],ue_position[:,1], edgecolor='r', facecolor='none', alpha=0.5 )
    plt.xlabel("x"); plt.ylabel("y")
    
    
    return None

