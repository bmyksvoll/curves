
# https://quant.stackexchange.com/questions/70515/interesting-finding-adjusted-kirks-and-bjerksund-stensland-are-exactly-t

"""
Bjerksund-Stensland spread option model

callput has to be 1 call or -1 put
modifications made to input a leg2 weight (positive) for example: heat rate option
spreads are assumed to be +leg1 -leg2

"""
from math import sqrt, erf, log, exp
import numpy as np

def SpreadBJS(F1, F2, vol1, vol2, K, T, IR, corr, leg2_weight_ratio, callput):

    a = (F2*leg2_weight_ratio) + K
    b = (F2*leg2_weight_ratio) / (F2*leg2_weight_ratio + K)
    spreadvol = sqrt(vol1*vol1 - 2*b * corr * vol1 * vol2 + b*b * vol2*vol2)
    d1 = (log(F1 / a) + (0.5 * vol1*vol1 - b* corr * vol1 * vol2 + 0.5 * b*b * vol2*vol2 ) * T) / (spreadvol * sqrt(T))
    d2 = (log(F1 / a) + (- 0.5 * vol1*vol1 + corr * vol1 * vol2 + 0.5 * b*b * vol2*vol2 - b * vol2*vol2) * T) / (spreadvol * sqrt(T))
    d3 = (log(F1 / a) + (-0.5 * vol1*vol1 + 0.5 * b*b * vol2*vol2) * T) / (spreadvol * sqrt(T))
    return exp(-IR * T) * (callput * F1 * normcdf(callput * d1) - callput * (F2*leg2_weight_ratio) * normcdf(callput * d2) - callput * K * normcdf(callput * d3))

"""
Modified Kirk's supposed to be more accurate than Kirk's https://arxiv.org/ftp/arxiv/papers/1812/1812.04272.pdf
MOST RESULTS MATCH Bjerksund-Stensland within 1e-7, guessing it's really the same formula...

"""
def SpreadKirkMod(F1, F2, vol1, vol2, K, T, IR, corr, leg2_weight_ratio, callput):
    
    F2 = F2*leg2_weight_ratio
    a_kirk = sqrt(vol1**2-2*corr*vol1*vol2*(F2/(F2+K))+vol2**2*((F2/(F2+K))**2))
    xt = log(F1)
    xstart = log(F2+K) 
    ihatt = sqrt(a_kirk**2) + 0.5 *(((vol2 * F2/(F2+K)) - corr*vol1)**2 ) * (1/((sqrt(a_kirk**2))**3)) * (vol2**2) * ((F2*K)/((F2+K)**2)) * (xt - xstart)
    S = F1/(F2+K)
    d1 = (log(S)+ 0.5 *(ihatt**2)*T) / (ihatt * (sqrt(T)))
    d2 = d1 - ihatt * sqrt(T)
    return exp(-IR*T) * ((callput * F1 * normcdf(callput * d1)) - callput * ((F2+K) * normcdf(callput * d2)))

# fast norm cdf function
def normcdf(x):
    return (1+erf(x/sqrt(2)))/2


F1 = np.arange(10,100,5)
F2 = np.arange(10,46,2)
vol2 = np.arange(0.95,0.05,-0.05)
vol1 = np.arange(0.05,0.95,0.05)
corr = np.arange(-0.9,0.9,0.1)

for i in range(F1.shape[0]):
    print(SpreadBJS(F1[i],F2[i],vol1[i],vol2[i],0,0.05,0.5,corr[i],1,1)-SpreadKirkMod(F1[i],F2[i],vol1[i],vol2[i],0,0.05,0.5,corr[i],1,1))

for i in range(F1.shape[0]):
    print(SpreadBJS(F1[i],F2[i],vol1[i],vol2[i],0,0.05,0.5,corr[i],1,-1)-SpreadKirkMod(F1[i],F2[i],vol1[i],vol2[i],0,0.05,0.5,corr[i],1,-1))
