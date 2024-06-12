import numpy as np
import matplotlib.pyplot as plt

def simulate_ou_process(theta, mu, sigma, X0, dt, T, paths):
    """
    Simulates paths of an Ornstein-Uhlenbeck process.

    theta: rate of mean reversion
    mu: long-term mean
    sigma: volatility parameter
    X0: initial value of the process
    dt: time step size
    T: total time of the simulation
    paths: number of paths to simulate
    """
    n_steps = int(T / dt)
    # Initialize the array for the simulated process
    X = np.zeros((n_steps + 1, paths))
    X[0] = X0

    # Generate random numbers for the simulation
    rand = np.random.normal(0, 1, (n_steps, paths))

    # Simulate the paths
    for t in range(1, n_steps + 1):
        X[t] = X[t - 1] + theta * (mu - X[t - 1]) * dt + sigma * np.sqrt(dt) * rand[t - 1]

    return X

# Parameters for the OU process
theta = 0.15  # Rate of mean reversion
mu = 0.05  # Long-term mean
sigma = 0.02  # Volatility parameter
X0 = 0.03  # Initial value of the process
dt = 1/252  # Daily time step
T = 1  # Total time of the simulation in years
paths = 100  # Number of paths to simulate

# Simulate the OU process
ou_paths = simulate_ou_process(theta, mu, sigma, X0, dt, T, paths)

# Plot the simulated paths
plt.figure(figsize=(10, 6))
plt.plot(ou_paths)
plt.title('Simulated Ornstein-Uhlenbeck Paths')
plt.xlabel('Time Steps')
plt.ylabel('Value of the Process')
plt.show()