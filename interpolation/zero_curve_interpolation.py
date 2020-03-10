# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 18:11:39 2020

@author: Komp
"""


#Python 3

import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import scipy.interpolate

#market rates
years = np.arange(1, 11, 1)
market_rates = np.array([0.75, 1.00, 1.25, 1.5, 1.75, 2.00, 2.10, 2.25, 2.25, 2.30 ])


def calc_df(r, qdf):
    '''
    Parameters
    ----------
    r : float, represents rate
    qdf : cumulative sum of dicount factors        
    Returns: floats, discount factors, function assums annual payment of rates!
    '''
    return(1 - qdf * r/100)/(1 + r/100)

def calc_zc(df, t):
    ''' 
    Parameters
    ----------
    df : float, discount factor
    t : float, time in years

    Returns
    -------
    float, zero coupon rate, continous compounding

    '''
    return (np.log(1/df)*1/t)*100

def calc_fwdrate(z1, z2, t1, t2, df=True):
    '''
    Parameters
    ----------
    z1 : float, discount factor or continouosly compounded zero rate of time t1
    z2 : float, discount factor or continouosly compounded zero rate of time t2
         t1 < t2
    t1 : float, time 1
    t2 : float, time 2
    df : boolean, True if dicount factors provided, False for zero coupon rate
    Returns
    -------
    float, forward rate
    ''' 
    if not df:
        z1 = np.exp(-z1/100*t1)
        z2 = np.exp(-z2/100*t2)        
    return (z1/z2-1)*1/(t2-t1)*100

# calculation of zero coupon rates and discount factors from market rates

# discount factors
dfactors = np.array([])
for r in market_rates:
    dfactors = np.append(dfactors, calc_df(r, dfactors.sum()))
    
# zero rates
zrates = np.array([])
for y, df in enumerate(dfactors):
    zrates = np.append(zrates, calc_zc(df, y+1))

# *** INTERPOLATION AND FORWARD RATES ***
# 1) linear interpolation of zero rates
# 2) linear interpolation of logarithm of dicount factors
# 3) cubic spline of logarithm of discount factor
# 4) monotone cubic spline of logarithm of discount factor

quarters = np.arange(1, 10.25, 0.25)

# ad.1a) linear interpolation of zerocoupon curves
fzcr_linear = sp.interpolate.interp1d(years, zrates, kind='linear')
zcr_linear = fzcr_linear(quarters)
 
# ad.1b) forward rates from lineary interpolated zero rates
fr_of_zclin = np.array([])
for i in range(len(quarters)-1):
    fr_of_zclin = np.append(fr_of_zclin, calc_fwdrate(zcr_linear[i], zcr_linear[i+1], quarters[i], quarters[i+1], False))

# ad.2a) linear interpolation of log of discount factor
log_dfactors = np.log(dfactors)

flog_df_linear = sp.interpolate.interp1d(years, log_dfactors, kind='linear')
log_df_linear = flog_df_linear(quarters)
df_loglinear = np.exp(log_df_linear)

# ad.2b) forward rates from log linear interpolation of dicount factors
fr_of_dfloglin = np.array([])
for i in range(len(quarters)-1):
    fr_of_dfloglin = np.append(fr_of_dfloglin, calc_fwdrate(df_loglinear[i], df_loglinear[i+1], quarters[i], quarters[i+1], True))

# ad.3a) cubic spline interpolation of log of discount factor
flog_df_cubic = sp.interpolate.interp1d(years, log_dfactors, kind='cubic')
log_df_cubic = flog_df_cubic(quarters)
df_logcubic = np.exp(log_df_cubic)

# ad.3b) forward rates from log cubic interpolation of dicount factors
fr_of_dflogcubic = np.array([])
for i in range(len(quarters)-1):
    fr_of_dflogcubic = np.append(fr_of_dflogcubic, calc_fwdrate(df_logcubic[i], df_logcubic[i+1], quarters[i], quarters[i+1], True))

# ad.4a) monotone cubic spline interpolation of log of discount factor
flog_df_monotone_cubic = sp.interpolate.PchipInterpolator(years, log_dfactors)
log_df_monotone_cubic = flog_df_monotone_cubic(quarters)
df_log_monotone_cubic = np.exp(log_df_monotone_cubic)

# ad.4b) forward rates from log monotone cubic interpolation of dicount factors
fr_of_dflogmonotonecubic = np.array([])
for i in range(len(quarters)-1):
    fr_of_dflogmonotonecubic = np.append(fr_of_dflogmonotonecubic, calc_fwdrate(df_log_monotone_cubic[i], df_log_monotone_cubic[i+1], quarters[i], quarters[i+1], True))


#plot
plt.close('all')
plt.figure(1)
plt.grid(axis='both', which='major', linestyle='-', linewidth=2)
plt.grid(axis='both', which='minor', linestyle='-', linewidth=1)
plt.tick_params(axis='both', colors='red')
plt.minorticks_on()
plt.xlabel('years')
plt.ylabel('rate')
plt.xticks(years)
plt.title('Yield term structure 1')
plt.scatter(years, market_rates, label='market rates')
plt.scatter(years, zrates, label='zero rates cnt.cmpd')
plt.plot(quarters, zcr_linear, label='zero coupon rates linear')
plt.plot(quarters[:-1], fr_of_zclin, label='fwd rates from linear interp.of zero coupon rates')
plt.plot(quarters[:-1], fr_of_dfloglin, label='fwd rates from linear interp. of log of discount factors')
plt.plot(quarters[:-1], fr_of_dflogcubic, label='fwd rates from cubic interp. of log of discount factors')
plt.plot(quarters[:-1], fr_of_dflogmonotonecubic, label='fwd rates from monotone cubic interp. of log of discount factors')
plt.legend(loc='lower left')

plt.figure(2)
plt.grid(axis='both', which='major', linestyle='-', linewidth=2)
plt.grid(axis='both', which='minor', linestyle='-', linewidth=1)
plt.minorticks_on()
plt.xlabel('years')
plt.ylabel('discount factor')
plt.xticks(years)
plt.title('Discount factor')
plt.scatter(years, dfactors, label='discount factor')
plt.plot(quarters, df_loglinear, label='linear interpolated log of DF')
plt.plot(quarters, df_logcubic, label='cubic interpolated log of DF')
plt.plot(quarters, df_log_monotone_cubic, label='monotone cubic interpolated log of DF')
plt.legend(loc='lower left')






