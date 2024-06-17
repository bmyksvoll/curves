import matplotlib.pyplot as plt
import numpy as np


def integral_brs(s,T, a, b,c):
    return(a**2/(T - s + b) - 2*a*c*log(T - s + b) + c**2*s)

def volatility(t, tau, T, a,  b, c):
    upper_integral = integral_brs(tau, T, a,b,c ) 
    lower_integral = integral_brs(t, T, a,b,c ) 
    variance =  (upper_integral - lower_integral)/(tau-t)
    return np.sqrt(variance)