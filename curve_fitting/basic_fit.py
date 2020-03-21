# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:14:20 2020

@author: Komp
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


data = pd.read_excel('C:\\Users\\Komp\\Desktop\\Covid_Polska.xlsx', sheet_name='Arkusz1', skiprows=7, usecols='B:C', names=['days', 'infected'])
data = data.dropna()

days = data['days']
infected = data['infected']


# basic curve fitting
# Root Mean Square Error (RMS)

x_sq = np.square(days)
x_sq_sum = x_sq.sum()
x_sum = days.sum()
n = days.count()

xy = days * infected
xy_sum = xy.sum()
y_sum = infected.sum()

matrix_a = np.array([[x_sq_sum, x_sum], [x_sum, n]])
matrix_b = np.array([xy_sum, y_sum])

a, b = np.linalg.solve(matrix_a, matrix_b)


def calc_y(a, b, x):
    if isinstance(x, (float, int)):
        return a*x + b
    else:
        v = np.vectorize(calc_y)
        return v(a, b, x)

trend_line = calc_y(a, b, days) 
   

plt.close('all')
plt.figure(1)
plt.xlabel('days')
plt.ylabel('infected')
plt.scatter(days, infected)
plt.plot(days, trend_line)



