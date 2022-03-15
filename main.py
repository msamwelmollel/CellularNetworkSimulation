# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 19:26:48 2022

@author: msamw
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial.distance import cdist
from tqdm import tqdm
import statsmodels.api as sm




from sight_prob import  ray2sel, plot_curves                         # import dominating signal
from bs_deploy import bs_generator, plot_bs_distribution             # import function to generate BS
from ue_deploy import static_user_position, random_user_position, mobile_user_position, plot_user_bs  # import user function
from connection_UE_BS import association_rule, plot_association_rule   # association rule 
from channel_state_information import path_loss,received_signal, signal_2_noise, signal_2_interferecen, signal_2_InterplusNoise, plot_netStatus #, signal_2_interference

# Constant 
lambda0 = 20  # number of BS densisty  

#%%    BS Deployment


bs_position = bs_generator(lambda0)    # get the position of BS 

n_bs = bs_position.shape[0]                # get number of BS deployed
# plot_bs_distribution(lambda0)   # uncomment to see the BS distribution



#%% UE deployment   https://github.com/panisson/pymobility

ue = mobile_user_position(n_user=1, velocity_min=0.1, velocity_max=1.0, wt_max=1.0)   # mobile_user_position(n_user, velocity_min=0.1, velocity_max=1.0, wt_max=1.0)

ue_position0 = next(ue.next_pos)    # extract user position

# plot_user_bs(ue_position0, bs_position)   # plot the BS along UE

ue_position = next(ue.next_pos)    # extract user position next position


# plot_user_bs(np.concatenate((ue_position0, ue_position), axis=1), bs_position)    # movement and velocity effect 


#%%   plot signal sistribution based on https://ieeexplore.ieee.org/document/6834753

# plot_curves()     # uncomment to view the distribuition of signal either LOS, NLOS or OUTAGE

#%%       # Association rule ---> Connection between BS and UE

distances, idx = association_rule(ue_position, bs_position)

#plot_association_rule(ue_position, bs_position)

#%%    Channel state information 
idx = idx # the BS connected to UE  

#%%     Constant Value

#   link https://ieeexplore.ieee.org/document/6834753
# constant parameter  based on "Millimeter Wave Channel Modeling and Cellular Capacity Evaluation"
ptx = 30   #dbm

gtx = grx = 24.5    # dBi

B = 2*10**9  # 2GHz is the band used for the simualation

k = 1.38064852*(10**-23)   # Boltzmann Constant

T = 290  # ° Kelvin   to calculate noise KTB

#%% pathloss

#path_loss(distances[idx], average= False)

#%% Power received

#received_signal(distances, idx, ptx, gtx, grx, average = False)

#%%  Signal to Noise ratio  

#signal_2_noise(distances, idx, ptx, gtx, grx, B, average = True)

#%%  Signal to Interference

# signal_2_interferecen(distances, idx, ptx, gtx, grx, B, ue_position, bs_position, average = True)

#%% Signal to Noise + Interference ratio

# signal_2_InterplusNoise(distances, idx, ptx, gtx, grx, B, ue_position, bs_position, average = True)

#%%   NETWORK STATUS

#plot_netStatus(distances, idx, ptx, gtx, grx, B, ue_position, bs_position, average = True)  # uncomment

#%%   APPLICATIONS




#%% COVERAGE PROBABILITY  P[SNR>T]
#vary BS ratio

def cov_prob(BSR):
    number_simulation = 20
    user = 5
    #BSR = 40
    x = []
    y = []
    
    for j in tqdm(range(1,50)):
        SNR_bag = []
    
        for i in range(number_simulation):
            lambda0 = BSR  # number of BS densisty 
            bs_position = bs_generator(lambda0)
            
            for u in range(user):
    
                ue_position = random_user_position(1)
                distances, idx = association_rule(ue_position, bs_position)
            
                prx, SIR, SNR, SINR = signal_2_InterplusNoise(distances, idx, ptx, gtx, grx, B, ue_position, bs_position, average = True)
                SNR_bag.append(SNR)
        
         
        x.append(j)
        y.append(len([i for i in SNR_bag if i!= 'No active link' and i>=j])/len(SNR_bag))
    
    plt.plot(x,y)
    y_lowess = sm.nonparametric.lowess(y, x, frac = 0.30)  # 30 % lowess smoothing
    plt.plot(y_lowess[:, 0], y_lowess[:, 1], label='BS_dens ='+str(BSR))
    plt.xlabel("SNR Threshold"); plt.ylabel("Prob")
    plt.axis([0, 50, 0, 1])
    plt.legend()
    
    return None

# cov_prob(10)
# cov_prob(30)
# cov_prob(50)

#%% User  trajectory)

ue = mobile_user_position(n_user=1, velocity_min=5, velocity_max=10.0, wt_max=1.0)   # mobile_user_position(n_user, velocity_min=0.1, velocity_max=1.0, wt_max=1.0)

ue_position = next(ue.next_pos)    # extract user position



# create the figure and axes objects


def plot_trajectory(end=100):

    plt.figure(3)
    
    plt.scatter(bs_position[:, 0],bs_position[:,1], edgecolor='b', facecolor='none', alpha=0.5 )


    
    for i in range(end):
        ue_position = next(ue.next_pos)
        if i == 0:
            plt.text(ue_position[0][0]-0.015, ue_position[0][1]+0.25, "Start")
        if i== end-1:
            plt.text(ue_position[0][0]-0.015, ue_position[0][1]+0.25, "End")


        plt.scatter(ue_position[:, 0],ue_position[:,1], edgecolor='r', facecolor='none', alpha=0.9 )

        


    plt.xlabel("x"); plt.ylabel("y")
    plt.axis([0, 1000, 0, 1000])
    
    return None

end = 200 # number of step
#plot_trajectory(end)


#%% Experienced SNR  mean (SNR per trajectory)

ue = mobile_user_position(n_user=1, velocity_min=5, velocity_max=10.0, wt_max=1.0)   # mobile_user_position(n_user, velocity_min=0.1, velocity_max=1.0, wt_max=1.0)

ue_position = next(ue.next_pos)    # extract user position



# create the figure and axes objects


def plot_trajectory(end, lambda0):
    
    bs_position = bs_generator(lambda0)    # get the position of BS 
    
    
    plt.figure(4)
    plt.scatter(bs_position[:, 0],bs_position[:,1], edgecolor='b', facecolor='none', alpha=0.5 )


    SNR_bag = []
    for i in range(end):
        ue_position = next(ue.next_pos)
        if i == 0:
            plt.text(ue_position[0][0]-0.015, ue_position[0][1]+0.25, "Start")
        if i== end-1:
            plt.text(ue_position[0][0]-0.015, ue_position[0][1]+0.25, "End")
            
            
        distances, idx = association_rule(ue_position, bs_position) 
        
        interBS = list(distances)
        interBS = map(ray2sel, interBS)
        interBS = list(interBS)
        BS_Inter = [x for x,y in enumerate(interBS) if y !='pOUT' and x != idx]
        BS_OUT = [x for x,y in enumerate(interBS) if y !='pOUT']
        
        if len(BS_OUT) == 0:
            SNR = 'No active link'
            
        elif len(BS_Inter) == 0:
            prx, SIR, SNR, SINR = signal_2_InterplusNoise(distances, idx, ptx, gtx, grx, B, ue_position, bs_position, average = True)
            SNR_bag.append(SNR)
            
        elif len(BS_Inter) >= 0:
            prx, SIR, SNR, SINR = signal_2_InterplusNoise(distances, idx, ptx, gtx, grx, B, ue_position, bs_position, average = True)
            SNR_bag.append(SNR)
        

        plt.scatter(ue_position[:, 0],ue_position[:,1], edgecolor='r', facecolor='none', alpha=0.9 )

        
    SNR = (sum(SNR_bag) + 10**-20)/end
    plt.text(0, -200, "SNR: " + str(SNR))
    plt.text(600, -200, "T: " + str(B*10*np.log2(1+SNR)/10**9))
    plt.xlabel("x"); plt.ylabel("y")
    plt.axis([0, 1000, 0, 1000])
    
    return None

end = 100 # number of step
lambda0 = 5

plot_trajectory(end, lambda0)




















