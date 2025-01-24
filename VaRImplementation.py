import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm

stocks = ['NVDA']

start_date = '2018-01-01'
end_date = '2025-01-01'

def download_data():
    stock_data = {}

    for stock in stocks:
        ticker = yf.Ticker(stock)
        stock_data[stock] = ticker.history(start=start_date, end=end_date)['Close']

    return pd.DataFrame(stock_data)

class ValueAtRiskImplementation:

    def __init__(self, position, mu, sigma, confidence, n, iterations):
        self.position = position
        self.mu = mu
        self.sigma = sigma
        self.confidence = confidence
        self.n = n
        self.iterations = iterations
    
    def calculate_var(self, position, confidence, mu, sigma):
        """
            Calculate VaR tomorrow (n = 1)
        """
        var = position * (mu - sigma * norm.ppf(1-confidence))
        return var

    def calculate_var_ndays(self, position, confidence, mu, sigma, n):
        """
            Calculate VaR for any days in future
        """
        var = position * (mu * n - sigma * np.sqrt(n) * norm.ppf(1-confidence))
        return var

    def montecarlo_simulation_var(self, position, confidence, mu, sigma, n, iterations):
        """
            VaR Calculation with Montecarlo Simulation
        """
        rand = np.random.normal(0, 1, [1, self.iterations])

        # Equation for the S(t) stock price
        stock_price = self.position * np.exp(self.n * (self.mu - 0.5 * self.sigma ** 2) + self.sigma * np.sqrt(self.n) * rand)

        # Sort the stock prices to determine the percentile
        stock_price = np.sort(stock_price)
        percentile = np.percentile(stock_price, (1 - self.confidence) * 100)

        return self.position - percentile

if __name__ == "__main__":

    stocks = ['NVDA']

    start_date = '2018-01-01'
    end_date = '2025-01-01'
    stock_data = download_data()
    stock_data['returns'] = np.log(stock_data / stock_data.shift(1))
    stock_data = stock_data[1:]

    # Position at stake
    position = 1e6
    # Confidence level at 95%
    confidence = 0.95
    # Number of paths in the Monte-Carlo simulation
    iterations = 100000
    # Days in future
    n = 5

    # Assuming daily returns are normally distributed
    mu = np.mean(stock_data['returns'])
    sigma = np.std(stock_data['returns'])

    var_impl = ValueAtRiskImplementation(position, mu, sigma, confidence, n, iterations)

    print('Value at risk for NVDA at 95 percent confidence: %0.2f' % var_impl.calculate_var_ndays(position, confidence, mu, sigma, n))
    print('Value at risk for NVDA with Monte-Carlo simulation: %0.2f' % var_impl.montecarlo_simulation_var(position, confidence, mu, sigma, n, iterations))
