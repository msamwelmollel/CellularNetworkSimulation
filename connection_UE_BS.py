# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 20:15:59 2022

@author: msamw
"""
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt

# function for association rule 
# Associate UE to closest BS

def association_rule(ue_position, bs_position):
    
    d = cdist(ue_position,bs_position)
    
    idx = np.argmin(d)
    # print(d.shape)
    # print(idx)

    
    return min(d),  idx 

def plot_association_rule(ue_position, bs_position):
    
    d = cdist(ue_position,bs_position)
    
    idx = np.argmin(d)
    
    # print(bs_position[idx][1])
    # print(ue_position[0][0])
    
    
    
    
    plt.scatter(bs_position[:, 0],bs_position[:,1], edgecolor='b', facecolor='none', alpha=0.5 )
    plt.scatter(ue_position[:, 0],ue_position[:,1], edgecolor='r', facecolor='none', alpha=0.5 )
    
    x_values = [ue_position[0][0], bs_position[idx][0]]
    y_values = [ue_position[0][1], bs_position[idx][1]]
    plt.plot(x_values, y_values, 'b', linestyle="--")
    
    plt.text(ue_position[0][0]-0.015, ue_position[0][1]+0.25, "UE")
    plt.text(bs_position[idx][0]-0.050, bs_position[idx][1]-0.25, "BS")
    
    # plt.plot(ue_position, bs_position[idx])
    plt.xlabel("x"); plt.ylabel("y")
    
    
    
    return None