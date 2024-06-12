from numpy import sqrt, log


def sigma_bs(t, a= 0.9, b = 0.6, c= 0.1):
    return a / (t + b) + c

def var_bs_integral(t, a= 0.9, b = 0.6, c= 0.1):
    return -a**2/(b + t) + 2*a*c*log(b + t) + c**2*t


def var_bs_F1(t, a= 0.9, b = 0.6):
    return -a**2/(b + t)
    
def var_bs_F2(t, a= 0.9, b = 0.6, c = 0.1):
    return 2*a*c*log(b + t)

def var_bs_F3(t, c = 0.1):
    return c**2*t


# f2 = sqrt((2*a*c)/(t+b))
# f3 = c

t = 1
a= 0.9
b = 0.6
c= 0.1
    
    

#Test Function equivalence
#print("Test Function equivalence:")
print(var_bs_integral(t, a,b,c)/1)
print(var_bs_F1(t, a,b)+var_bs_F2(t, a,b,c)+var_bs_F3(t, c))



#
# 
# 
# 
# print("Test Integral equivalence:")

print(var_bs_F1(t, a,b))
print(var_bs_F2(t, a,b,c))
print(var_bs_F3(t, c))






