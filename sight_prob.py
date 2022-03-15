# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 20:46:04 2022

@author: msamw
"""

import numpy as np
import matplotlib.pyplot as plt


#constant


def pOUT(d):
    a_out = 1/30
    b_out = 5.2
    
    
    
    return max(0, 1- np.exp(-a_out*d + b_out))

def pLOS(d):
    a_los = 1/67.1
    
    return (1- pOUT(d))*np.exp(-a_los*d)

def pNLOS(d):
    
    return (1-pOUT(d)-pLOS(d))

def ray2sel(d):
    
    raytype = ['pOUT', 'pLOS', 'pNLOS']
    
    val2sel = np.argmax([pOUT(d), pLOS(d), pNLOS(d)])
    
    
    return raytype[val2sel] 

def plot_curves():

    x = [i for i in range(1,200)]
    
    y_los = list(map(pLOS, x))
    
    plt.plot(x,y_los, label='LOS')
    

    
    y_nlos = list(map(pNLOS, x))
    
    plt.plot(x,y_nlos, label='NLOS')
    
    y_out = list(map(pOUT, x))
    
    plt.plot(x,y_out, label='OUT')
    
    plt.xlabel("Distance"); plt.ylabel("Probability")
    
    plt.legend()

    return None




