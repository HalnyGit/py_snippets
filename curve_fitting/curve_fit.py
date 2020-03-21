# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 17:30:49 2020

@author: Komp
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1, 4, 1)
y = np.array([1.0, 2.0, 3.5])

# =============================================================================
# plt.close('all')
# plt.figure(1)
# plt.grid(axis='both', which='major', linestyle='-', linewidth=1)
# plt.scatter(x, y)
# plt.plot(x, y)
# =============================================================================

xi = 3.25

dif_xi_x = {}

for num in x:
    for i in range(len(x)):
        dif_xi_x.setdefault(num-1, []).append(xi - x[i])

nominators = {}
for k, v in dif_xi_x.items():
    del dif_xi_x[k][k]
    nominators[k] = np.prod(dif_xi_x[k])

dif_x = {}
for num in x:
    for i in range(len(x)):
        if num - x[i] != 0:
            dif_x.setdefault(num, []).append(num - x[i])

denominators = {}
for k, v in dif_x.items():
    denominators[k-1] = np.prod(dif_x[k])
    
coeffs = {}
for i in range(len(x)):
    coeffs[i] = nominators[i]/denominators[i]

yi = 0
for i in range(len(y)):
    yi+=y[i]*coeffs[i]

print(yi)


xis = np.arange(1, 3, 0.1)

class Lag_fit(object):
    
    def __init__(self, x, xs, ys):
        self.x = x
        self.xs = xs
        self.ys = ys
    
    
    
    








