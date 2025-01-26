import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

NUM_OF_SIMULATIONS = 1000
N = 252

class StockPriceMonteCarlo:
    def __init__(self, S0, mu, sigma):
        self.S0 = S0
        self.mu = mu
        self.sigma = sigma

    def stock_monte_carlo(self):

        result = []

        for _ in range(NUM_OF_SIMULATIONS):
            prices = [S0]
            for _ in range(N):
                stock_price = prices[-1] * np.exp((self.mu - 0.5 * self.sigma ** 2) + sigma * np.random.normal())
                prices.append(stock_price)

            result.append(prices)

        simulation_data = pd.DataFrame(result)
        simulation_data = simulation_data.T

        simulation_data['mean'] = simulation_data.mean(axis=1)

        plt.plot(simulation_data['mean'])
        plt.show()

        print('Future stock price: %.2f' % float(simulation_data['mean'].iloc[0]))


if __name__ == '__main__':

    S0 = 850
    mu = 0.0002
    sigma = 0.01
    sp_montecarlo = StockPriceMonteCarlo(S0, mu, sigma)
    sp_montecarlo.stock_monte_carlo()
