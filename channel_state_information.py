# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 21:00:10 2022

@author: msamw
"""

import numpy as np
import matplotlib.pyplot as plt

from sight_prob import  ray2sel


def path_loss(distance, average= False):
    
    type_of_ray = ray2sel(distance)

    
    if type_of_ray == 'pLOS':    # https://leleivre.com/rf_mmwavelink.html duplicate the result set average True
        alpha0 = 61.4
        beta0 = 2
        gamma0 = 5.8
        
        
        mu, sigma = 0, gamma0*gamma0

        if average == True:
            return np.mean(alpha0+10*beta0*np.log10(distance + 10**-20) + np.random.normal(mu, sigma, 100000))
        else:
            return np.mean(alpha0+10*beta0*np.log10(distance + 10**-20) + np.random.normal(mu, sigma, 1))
        
    if type_of_ray == 'pNLOS':
        alpha0 = 72.0
        beta0 = 2.92
        gamma0 = 8.7

        
        mu, sigma = 0, gamma0*gamma0
        
        if average == True:
            return np.mean(alpha0+10*beta0*np.log10(distance + 10**-20) + np.random.normal(mu, sigma, 100000))
        else:
            return np.mean(alpha0+10*beta0*np.log10(distance+ 10**-20) + np.random.normal(mu, sigma, 1))
        
    else:
        return 'OUT'

def received_signal(distance, ptx, gtx, grx, average = False):
    
    try:
        rx = ptx + gtx + grx - path_loss(distance, average)
    except:
        rx = 'OUT'
    
    return rx

def noise_function(B):
    
    k = 1.38064852*(10**-23)   # Boltzmann Constant
    T = 290  # ° Kelvin
    B = B
    
    noise = k * T  * B   # in https://leleivre.com/rf_mmwavelink.html B is assumed to be 2GHz
    
    
    return 10*np.log10(noise) + 30


def signal_2_noise(distances, idx, ptx, gtx, grx, B, average = True):
    
    
    #SNR = rx / noise

    SNR = received_signal(distances[idx], ptx, gtx, grx, average)  - noise_function(B)
    
    
    
    
    return SNR

def signal_2_interferecen(distances, idx, ptx, gtx, grx, B, ue_position, bs_position, average = True):

    interBS = list(distances)
    #print(interBS)
    interBS = map(ray2sel, interBS)
    interBS = list(interBS)
    
    BS_Inter = [x for x,y in enumerate(interBS) if y !='pOUT' and x != idx]
    BS_OUT = [x for x,y in enumerate(interBS) if y !='pOUT']
    
    if len(BS_OUT) == 0:
        # print('SIR', 'No active link')
        # print('distance', distances[idx])
        SIR = 'No active link'
        
    elif len(BS_Inter) == 0:
        # print('SIR', received_signal(distances[idx], ptx, gtx, grx, average = True))
        # print('distance', distances[idx])
        SIR = received_signal(distances[idx], ptx, gtx, grx, average = True)
    
    elif len(BS_Inter) >= 0:
        signal = received_signal(distances[idx], ptx, gtx, grx, average)
        interferefence = sum([received_signal(distances[x], ptx, gtx, grx, average ) for x,y in enumerate(interBS) if y !='pOUT' and x != idx])
        SIR = signal + interferefence
        
    return SIR

def signal_2_InterplusNoise(distances, idx, ptx, gtx, grx, B, ue_position, bs_position, average = True):

    interBS = list(distances)
    interBS = map(ray2sel, interBS)
    interBS = list(interBS)
    
    BS_Inter = [x for x,y in enumerate(interBS) if y !='pOUT' and x != idx]
    BS_OUT = [x for x,y in enumerate(interBS) if y !='pOUT']
    
    if len(BS_OUT) == 0:
        # print('SIR', 'No active link')
        # print('distance', distances[idx])
        SINR = 'No active link'
        prx = 'No active link'
        SIR = 'No active link'
        SNR = 'No active link'
        
    elif len(BS_Inter) == 0:
        # print('SIR', received_signal(distances[idx], ptx, gtx, grx, average = True))
        # print('distance', distances[idx])
        prx = received_signal(distances[idx], ptx, gtx, grx, average)
        SNR = prx - noise_function(B)
        SIR  = prx
        SINR = prx - noise_function(B)
        
    
    elif len(BS_Inter) >= 0:
        #signal = received_signal(distances[idx], ptx, gtx, grx, average)
        prx = received_signal(distances[idx], ptx, gtx, grx, average)
        interferefence = sum([received_signal(distances[x], ptx, gtx, grx, average ) for x,y in enumerate(interBS) if y !='pOUT' and x != idx])
        SNR = prx - noise_function(B)
        SIR = prx + interferefence
        SINR = prx + interferefence  - noise_function(B)

        
    return prx, SIR, SNR, SINR




def plot_netStatus(distances, idx, ptx, gtx, grx, B, ue_position, bs_position, average = True):
    n= 0
    interBS = list(distances)
    interBS = map(ray2sel, interBS)
    interBS = list(interBS)
    
    
    plt.scatter(bs_position[:, 0],bs_position[:,1], edgecolor='b', facecolor='none', alpha=0.5 )
    plt.scatter(ue_position[:, 0],ue_position[:,1], edgecolor='r', facecolor='none', alpha=0.9 )
    
    for x,y in enumerate(interBS):
        
        if (x == idx) and (y != 'pOUT'):

            x_values = [ue_position[0][0], bs_position[x][0]]
            y_values = [ue_position[0][1], bs_position[x][1]]
            plt.plot(x_values, y_values, 'b', linestyle="-")
            n = n+1
            
        elif y == 'pOUT':
            x_values = [ue_position[0][0], bs_position[x][0]]
            y_values = [ue_position[0][1], bs_position[x][1]]
            plt.plot(x_values, y_values, 'r', linestyle="--", alpha=0.1)
            
        elif y == 'pNLOS':
            x_values = [ue_position[0][0], bs_position[x][0]]
            y_values = [ue_position[0][1], bs_position[x][1]]
            plt.plot(x_values, y_values, 'y', linestyle="--")
            n = n+1
            
        elif y == 'pLOS':
            x_values = [ue_position[0][0], bs_position[x][0]]
            y_values = [ue_position[0][1], bs_position[x][1]]
            plt.plot(x_values, y_values, 'g', linestyle="-")
            n = n+1
        plt.xlabel("x"); plt.ylabel("y")
        plt.axis([0, 1000, 0, 1000])

    if n == 0:
        plt.text(0, -200, "Pr: " + 'No Active link connected')
        
        plt.text(600, -200, "SNR: " + 'No Active link connected')
        
        plt.text(0, -300, "SIR: " + 'No Active link connected')
        
        plt.text(600, -300, "SINR: " + 'No Active link connected')
        
    if n > 0: 
        prx, SIR, SNR, SINR = signal_2_InterplusNoise(distances, idx, ptx, gtx, grx, B, ue_position, bs_position, average)
        plt.text(0, -200, "Pr: " + str(prx))
        
        plt.text(600, -200, "SNR: " + str(SNR))
        
        plt.text(0, -300, "SIR: " + str(SIR))
        
        plt.text(600, -300, "SINR: " + str(SINR))

        
    return None

#print(signal_2_noise(10, 30, 24.5, 24.5, 2*10**9, average = True))

#print(noise_function(20*10**6))

#print(path_loss(10, average= True))

#print(received_signal(200, 30, 24.5, 24.5, average = True))

#print(path_loss(50, True))