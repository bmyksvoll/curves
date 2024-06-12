import numpy as np
import matplotlib.pyplot as plt

def simulate_gbm(S0, mu, sigma, T, dt, paths):
    """
    S0: initial stock price
    mu: expected return
    sigma: volatility
    T: time to maturity
    dt: time step size
    paths: number of paths to simulate
    """
    n_steps = int(T / dt)
    dt_array = np.full((n_steps, paths), dt)
    mu_dt = (mu - 0.5 * sigma**2) * dt_array
    sigma_dt = sigma * np.sqrt(dt_array)
    z = np.random.standard_normal((n_steps, paths))
    
    # Calculate the percentage changes
    percentage_changes = np.exp(mu_dt + sigma_dt * z)
    
    # Cumulatively apply the percentage changes to the initial price
    prices = np.vstack([np.full(paths, S0), S0 * np.cumprod(percentage_changes, axis=0)])
    
    return prices

# Parameters for the GBM
S0 = 100  # Initial stock price
mu = 0.05  # Expected return
sigma = 0.2  # Volatility
T = 1  # Time to maturity in years
dt = 1/252  # Daily time step
paths = 10000  # Number of paths to simulate

# Simulate the price paths
price_paths = simulate_gbm(S0, mu, sigma, T, dt, paths)

# Plot a few of the simulated paths
plt.figure(figsize=(10, 6))
plt.plot(price_paths)
plt.title('Simulated GBM Paths for Stock Price')
plt.xlabel('Time Steps')
plt.ylabel('Stock Price')
plt.show()