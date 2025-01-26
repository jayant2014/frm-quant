import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

NUM_OF_SIMULATIONS = 1000
NUM_OF_POINTS = 200

class BondPricing:

    def __init__(self, x0, r0, kappa, theta, sigma):
        self.x0 = x0
        self.r0 = r0
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma

    def monte_carlo_simulation(self, x, r0, kappa, theta, sigma, T=1):
        dt = T/float(NUM_OF_POINTS)
        result = []

        for _ in range(NUM_OF_SIMULATIONS):
            rates = [r0]
            for _ in range(NUM_OF_POINTS):
                dr = kappa * (theta - rates[-1]) * dt + sigma * np.sqrt(dt) * np.random.normal()
                rates.append(rates[-1] + dr)

            result.append(rates)

        simulation_data = pd.DataFrame(result)
        simulation_data = simulation_data.T

        # calculate the integral of the r(t) based on the simulated paths
        integral_sum = simulation_data.sum() * dt
        # present value of a future cash flow
        present_integral_sum = np.exp(-integral_sum)
        # mean because the integral is the average
        bond_price = x * np.mean(present_integral_sum)

        print('Bond price based on Monte-Carlo simulation: $%.2f' % bond_price)


if __name__ == '__main__':

    x = 10000
    r0 = 0.1
    kappa = 0.3
    theta = 0.3
    sigma = 0.03
    bp = BondPricing(x, r0, kappa, theta, sigma)
    bp.monte_carlo_simulation(x, r0, kappa, theta, sigma)
