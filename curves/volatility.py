import matplotlib.pyplot as plt
import numpy as np
from scipy.special import spence

def term_structure(t):
    T_max= t[-1]
    # Define a term structure function that could depend on t
    # Simple sinusoidal term structure for demonstration
    return 100 + 20 * np.cos(2*T_max * np.pi * t /T_max) + np.exp(0.5*t)


def sigma_instantanous(t, T, a= 0.9, b = 0.6, c= 0.1):
    return a / (T - t + b) + c

# Returns the volatility structure from t+tau(?)
def sigma_brs (t, tau, T, a,b,c):
    upper = (a**2/(T - tau + b) - 2*a*c*np.log(T - tau + b) + c**2*tau) 
    lower = (a**2/(T - t + b) - 2*a*c*np.log(T - t + b) + c**2*t) 
    var = (upper-lower)/(tau-t)
    return(np.sqrt(var))

def sigma_factor1(t, tau ,T, a, b):
    upper = (a**2/(T - tau + b))
    lower = (a**2/(T - t + b))
    var = (upper-lower)/(tau-t)
    return(np.sqrt(var))

def sigma_factor2(t, tau,T, a, b,c):
    upper = (- 2*a*c*np.log(T - tau + b))
    lower = (- 2*a*c*np.log(T - t + b))
    var = (upper-lower)/(tau-t)
    return(np.sqrt(var))


def sigma_factor3(t, tau,T,c):
    upper = (c**2*tau)
    lower = (c**2*t)
    var = (upper-lower)/(tau-t)
    return(np.sqrt(var))

def sigma_plugin(t, tau, T1, T2, a, b,c):
    
    def X(s):
        return b + 0.5 * (T2 + T1) - s
   
    def integral1(x):
        int1 = (x+alpha)*(np.log(x+alpha))**2 \
            - 2*(x+alpha)*np.log(x + alpha) * np.log(x - alpha) \
            + 4*alpha*np.log(2*alpha)*np.log((x - alpha)/(2 * alpha)) \
            - 4 * alpha * spence((x + alpha)/(2 * alpha)) \
            + (x-alpha)*(np.log(x-alpha))**2
        return(int1)
    
    def integral2(x):
        int2 = (x+alpha)*np.log(x+alpha) \
            -(x-alpha)*np.log(x-alpha)
        return(int2)

    alpha = 0.5*(T2-T1)
    xu = X(t)
    xl = X(tau)
    
    variance = (a/(T2-T1))**2 * (integral1(xu)-integral1(xl)) \
        + (2*a*c)/(T2-T1) * (integral2(xu)-integral2(xl)) \
           + c**2 *(tau-t) # * integral ds 
    return(np.sqrt(variance/(tau-t)))


