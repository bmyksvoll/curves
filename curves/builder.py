import numpy as np
import numpy.matlib as npm
from numpy.polynomial import Polynomial
from scipy.linalg import block_diag
from datetime import datetime

#  spline knot j = 1, ..., n − 1 and contract i = 1, ..., m
def calc_H(tau_b, tau_e):
    return np.matrix([
        [(144 / 5) * (tau_e**5 - tau_b**5),    18 * (tau_e**4 - tau_b**4),    8 * (tau_e**3 - tau_b**3), 0, 0],
        [       18 * (tau_e**4 - tau_b**4),    12 * (tau_e**3 - tau_b**3),    6 * (tau_e**2 - tau_b**2), 0, 0],
        [        8 * (tau_e**3 - tau_b**3),     6 * (tau_e**2 - tau_b**2),    4 * (tau_e**1 - tau_b**1), 0, 0],
        [                   0,                0,               0, 0, 0],
        [                   0,                0,               0, 0, 0],
    ])


#The block diagonal matrix H has dimensions (5n × 5n) and ∆j = t_j+1 − tj
def calc_big_H(knots):
    n = len(knots)- 1 
    h_matrices = []
    for i in range(0, n):
        h_matrices.append(calc_H(knots[i], knots[i+1]))
    return block_diag(*h_matrices)

def calc_integral_constraint(tau_b, tau_e):
    return np.matrix([(tau_e**5 - tau_b**5) / 5, (tau_e**4 - tau_b**4) / 4, (tau_e**3 - tau_b**3) / 3, (tau_e**2 - tau_b**2) / 2, tau_e - tau_b])

def calc_knot_constraints(u_j):
    # Using the four contraints: connectivity, continuous, smooth and maintaining the average.
    # Excluding the requirement for the line to be zero at the end.
    return np.matrix([
        [     u_j**4,     u_j**3,     u_j**2, u_j**1,   1],
        [ 4 * u_j**3, 3 * u_j**2, 2 * u_j**1,      1,   0],
        [12 * u_j**2, 6 * u_j**1,          2,      0,   0]
    ])

# A is a (3n + m − 2 × 5n) matrix 
def calc_big_A(knots, taus):

    m = len(taus)
    n = len(knots)- 1 

    A = npm.zeros((3 * n + m - 2, 5 * n))
    inner_knots = knots[1:-1]
    for i, knot in enumerate(inner_knots):
        c1 = calc_knot_constraints(knot)
        A[(3 * i):(3 * i + 3), (5 * i):(5 * i + 5)] = c1
        A[(3 * i):(3 * i + 3), (5 * i + 5):(5 * i + 10)] = - c1

    # End constraint last knot.
    A[3*(n-1), -5:] =[ 4 *knots[-1]**3, 3 * knots[-1]**2, 2 * knots[-1],  1,  0]

    # No-arbitrage constraints.
    for j, tau in enumerate(taus):
        tau_b, tau_e = tau
        c2 = calc_integral_constraint(tau_b, tau_e)
        A[(3*(n-1) + 1 + j), (5 * (j+1)):(5 * (j+1) + 5)] = c2
    
    return A

# B is a (3n + m − 2 × 1) vector.
def calc_B(prices, knots, taus ):
    m = len(taus)
    n = len(knots)- 1     
    
    B = npm.zeros(3 * n + m- 2 )
    for i in range(0, len(taus) ):
        tau_b, tau_e = taus[i]
        B[:, 3*(n-1) + 1 + i] = prices[i] * (tau_e - tau_b)
    return B.T

# Solves the linear equation and return only the x values (scraps lambda).
# By default it splits the x-matrix into a list of numpy arrays, each containing
# the a, b, c, d and e variables for each line segment.
def solve_lineq(H, A, B, split=True, num_params=5):
    top = np.concatenate((2 * H, A.T), axis=1)
    btm = np.concatenate((A, np.zeros((A.shape[0], A.T.shape[1]))), axis=1)
    A_merged = np.concatenate((top, btm), axis=0)
    B_merged = np.concatenate(
        (
            npm.zeros(top.shape[1] - B.shape[0]).T,
            B
        ), axis=0)
    X = np.squeeze(np.array(np.linalg.solve(A_merged,B_merged)[:A.shape[1]]))
    if split:
        if X.shape[0] % num_params != 0:
            raise ValueError('The split of the x-matrix is not even. Set "num_params" to the correct value to fix this')
        return np.split(X, np.arange(num_params, X.shape[0], num_params))
    else:
        return X

def smfc(u, params):
    return params[0] * u**4 + params[1] * u**3 + params[2] * u**2 + params[3] * u + params[4]

def calc_smfc(taus, prices, flatten=True):
    knots = [0] + sorted(set(item for sublist in taus for item in sublist))
    H = calc_big_H(taus)
    A = calc_big_A(knots, taus)
    B = calc_B(prices, taus)
    X = solve_lineq(H, A, B)
    return X

def calc_price(spline_params, knots, start, end):
    """
    Integrates the spline function over a given time period.

    :param spline_params: List of spline coefficients for each segment.
    :param knots: List of knots where the spline segments change.
    :param start: Start of the integration period.
    :param end: End of the integration period.
    :return: The integral of the spline over the specified period.
    """
    # Ensure the integration bounds are within the range of the knots
    if start < knots[0] or end > knots[-1]:
        raise ValueError("Integration bounds are outside the range of the spline.")

    total_integral = 0
    for i, params in enumerate(spline_params):
        # Find the segment where the start of the integration period lies
        if start >= knots[i] and start < knots[i + 1]:
            # Find the segment where the end of the integration period lies
            while end > knots[i + 1]:
                # Integrate over the current segment up to the next knot
                total_integral += integrate_polynomial(params, start, knots[i + 1])
                start = knots[i + 1]
                i += 1
                if i >= len(spline_params):
                    raise ValueError("Integration bounds are outside the range of the spline.")
            # Integrate over the last segment up to the end of the integration period
            total_integral += integrate_polynomial(params, start, end)
            break

    return total_integral / (end-start)

def integrate_polynomial(params, start, end):
    """
    Integrates a polynomial defined by its coefficients over a given interval.

    :param params: Coefficients of the polynomial.
    :param start: Start of the integration interval.
    :param end: End of the integration interval.
    :return: The integral of the polynomial over the interval.
    """
    # Reverse the coefficients to create a Polynomial object
    p = Polynomial(params[::-1])
    # Integrate the polynomial and evaluate it at the bounds
    integral = p.integ()
    return integral(end) - integral(start)