#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 08:07:18 2022

@author: michaeltown
"""

import pandas as pd
import numpy as np
import os as os
import matplotlib.pyplot as plt
import datetime as dt


def velCalc(del_t,vi,a):
    
    return a*del_t+vi;



def posCalc(del_t,xi,vi,a):
    
    return 1/2*a*del_t**2+vi*del_t+xi;


def myxyPlotFunc(x,y,clr,xll,xul,yll,yul,title,xlab,ylab,fileloc,filename):

    fig1 = plt.figure();
    plt.plot(x,y,clr,alpha = 0.5)
    plt.xlim([xll,xul])
    plt.ylim([yll,yul])
    plt.grid();
    plt.title(title)
    plt.xlabel(xlab)
    plt.xticks(rotation=30)
    plt.ylabel(ylab)
    os.chdir(fileloc)
    fig1.savefig(filename+'.jpg')
    
    
# load the data file
#fileLoc = '/home/michaeltown/work/projects/lyteProbe/data/banner_summit_03-18-2021/';
fileLoc = '/home/michaeltown/work/projects/lyteProbe/data/tester_stick_02-21-2022/';
figureLoc = '/home/michaeltown/work/projects/lyteProbe/figures/';
#dataFileName = '2021-03-18--132430.csv'

os.chdir(fileLoc)
dataFileNames = os.listdir('./')
dataFileNames = [d for d in dataFileNames if '.csv' in d]

# initialize all models - this might have to be part of the loop eventually
# assumptions of linear trajectory
x0 = 0;         # m
v0 = 0;         # m/s
g = 9.81;       # m/s2 (will change this based on location)
del_t = 1/16000;   # the delta-time for the data set


for d in dataFileNames:
    lpDF = pd.read_csv(fileLoc+d,header = 7);
    
    
    
    # create time vector in seconds
    lpDF['time'] = np.arange(0,del_t*len(lpDF.acceleration),del_t)
    
    # new acceleration vector from IMU in m/s2
#    lpDF['accel_ms2'] = g*(lpDF.acceleration.shift(periods=1)+1);
    lpDF['accel_ms2'] = g*(lpDF.acceleration+.97);
    
    
    # velocity calc
    
    lpDF['del_vel'] = lpDF.accel_ms2*del_t;
    lpDF['vel'] = lpDF['del_vel'].cumsum()+v0;
    
    
    
    # position calc
    
    lpDF['del_x'] = 0.5*lpDF.accel_ms2*del_t**2+lpDF.vel.shift(periods=1)*del_t;
    lpDF['x'] = lpDF['del_x'].cumsum()+x0;
 
    # check of position calc
    lpDF['del_x2'] = 0.5*(lpDF.vel+lpDF.vel.shift(periods=1))*del_t;
    lpDF['x2'] = lpDF['del_x2'].cumsum()+x0;
    
    
    # plot the position, velocity, and acceleration as a function of time
    
    fig = plt.figure()
    plt.subplot(411)
    plt.plot(lpDF.time,lpDF.x,'k')
    plt.plot(lpDF.time,-lpDF.depth/100,'k--',alpha=0.5)
    plt.grid()
    plt.title('lyte probe depth diag: ' + d[:-4]);
    plt.xlabel('time (s)')
    plt.legend(['accel','baro'],loc = 'upper left')
    plt.ylabel('depth (m)')
    plt.ylim([-0.1, 2.2])
    
    plt.subplot(412)
    plt.plot(lpDF.time,lpDF.vel,'b');
    plt.grid();
    plt.xlabel('time (s)')
    plt.ylabel('velocity (m/s)')
    plt.ylim([-0.1, 3])
    
    # plt.subplot(413)
    # plt.plot(lpDF.time,lpDF.del_vel,'r');
    # plt.grid();
    # plt.xlabel('time (s)')
    # plt.ylabel('del-vel (m/s)')
    
    plt.subplot(413)
    plt.plot(lpDF.time,lpDF.accel_ms2,'r');
    plt.grid();
    plt.xlabel('time (s)')
    plt.ylabel('accel (m/s2)')
    plt.ylim([-25, 10])    

    # plot the measurements from the 'sensors' as a function of time
    plt.subplot(414)
    plt.plot(lpDF.time,lpDF.Sensor1,'k');
    plt.grid();
    plt.xlabel('time (s)')
    plt.ylabel('Raw NIR (S1)')
    fig.savefig(figureLoc+'probeAnalysis_TS_'+d[:-4]+'.jpg')
        
    # plot the depth measurements against each other
    fig = plt.figure()
    plt.plot(-lpDF.depth/100,lpDF.x,'k');
    plt.plot(np.arange(0,3),np.arange(0,3),'r--',alpha = 0.5)
    plt.grid();
    plt.title('lyte probe depth diag: ' + d[:-4])
    plt.xlabel('depth_baro (cm)')
    plt.ylabel('depth_accel (m)')
    fig.savefig(figureLoc+'probeAnalysis_dvsd_'+d[:-4]+'.jpg')

    
    # plot the measurements from the 'sensors' as a function of depth
    fig = plt.figure()
    plt.plot(lpDF.Sensor1,-lpDF.x,'k');
    plt.plot(lpDF.Sensor1,lpDF.depth/100,'k--',alpha = 0.5)
    plt.grid();
    plt.title('lyte probe depth diag: ' + d[:-4])
    plt.xlabel('Raw NIR (sensor 1)')
    plt.ylabel('depth (m)')
    plt.legend(['accel','baro'],loc = 'upper right')
    plt.ylim([-2, 0.1])
    fig.savefig(figureLoc+'probeAnalysis_NIRvsd_'+d[:-4]+'.jpg')
    
    # plot the measurements from the 'sensors' as a function of depth
    fig = plt.figure()
    plt.plot(lpDF.time,lpDF.accel_ms2,'r');
    plt.grid();
    plt.xlabel('time (s)')
    plt.ylabel('accel (m/s2)')
    plt.title('accel: '+ d[:-4])
    plt.ylim([-40, 10])
    fig.savefig(figureLoc+'probeAnalysis_accel_'+d[:-4]+'.jpg')
    
    


