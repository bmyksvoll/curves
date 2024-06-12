import numpy as np
import matplotlib.pyplot as plt

def simulate_clewlow_strickland(theta, mu, sigma, F0, dt, T, paths):
    """
    Simulates paths of the Clewlow-Strickland one-factor model.

    theta: rate of mean reversion
    mu: long-term mean (assumed to be constant for simplicity)
    sigma: volatility parameter (assumed to be constant for simplicity)
    F0: initial forward price
    dt: time step size
    T: total time of the simulation
    paths: number of paths to simulate
    """
    n_steps = int(T / dt)
    # Initialize the array for the simulated forward prices
    F = np.zeros((n_steps + 1, paths))
    F[0] = F0

    # Generate random numbers for the simulation
    rand = np.random.normal(0, 1, (n_steps, paths))

    # Simulate the paths
    for t in range(1, n_steps + 1):
        F[t] = F[t - 1] + theta * (mu - F[t - 1]) * dt + sigma * np.sqrt(dt) * rand[t - 1]

    return F

def simulate_clewlow_strickland_vectorized(theta, mu, sigma, F0, dt, T, paths):
    """
    Vectorized simulation of the Clewlow-Strickland one-factor model.

    theta: rate of mean reversion
    mu: long-term mean (assumed to be constant for simplicity)
    sigma: volatility parameter (assumed to be constant for simplicity)
    F0: initial forward price
    dt: time step size
    T: total time of the simulation
    paths: number of paths to simulate
    """
    n_steps = int(T / dt)
    dt_array = np.full((n_steps, paths), dt)
    theta_dt = theta * dt_array
    sqrt_dt = np.sqrt(dt_array)
    
    # Generate random numbers for the simulation
    rand = np.random.normal(0, 1, (n_steps, paths))
    
    # Calculate the percentage changes
    changes = theta_dt * (mu - F0) + sigma * sqrt_dt * rand
    
    # Cumulatively apply the changes to the initial price
    F = np.vstack([np.full(paths, F0), F0 + np.cumsum(changes, axis=0)])
    
    return F


# Parameters for the Clewlow-Strickland one-factor model
theta = 0.15  # Rate of mean reversion
mu = 0.5  # Long-term mean
sigma = 0.002  # Volatility parameter
F0 = 0.03  # Initial forward price
dt = 1/12  # Daily time step
T = 20  # Total time of the simulation in years
paths = 100  # Number of paths to simulate

# Simulate the Clewlow-Strickland one-factor model
cs_paths = simulate_clewlow_strickland(theta, mu, sigma, F0, dt, T, paths)

# Simulate the Clewlow-Strickland one-factor model
#cs_paths_vectorized = simulate_clewlow_strickland_vectorized(theta, mu, sigma, F0, dt, T, paths)


# Check 1: Mean Reversion Level (Long-Term Mean)
mean_of_paths = np.mean(cs_paths[-1])

print(f"Expected long-term mean (mu): {mu}")
print(f"Mean of simulated paths: {mean_of_paths}")

# Check 2: Volatility
simulated_volatility = np.std(cs_paths[-1]) / np.sqrt(dt)
print(f"Expected annualized volatility (sigma): {sigma}")
print(f"Estimated annualized volatility from paths: {simulated_volatility}")

# Check 3: Mean Reversion Rate (Theta)
# Calculate the first-order autocorrelation of the changes in the simulated paths
changes = np.diff(cs_paths, axis=0)
autocorrelation = np.corrcoef(changes[:-1].flatten(), changes[1:].flatten())[0, 1]
print(f"First-order autocorrelation of changes: {autocorrelation}")
print(f"Expected decay in autocorrelation due to theta: {np.exp(-theta * dt)}")



# Plot the simulated paths
plt.figure(figsize=(10, 6))
plt.plot(cs_paths)
plt.title('Simulated Clewlow-Strickland One-Factor Model Paths')
plt.xlabel('Time Steps')
plt.ylabel('Forward Price')
plt.show()