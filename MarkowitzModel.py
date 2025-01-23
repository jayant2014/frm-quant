import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization

# Markowitz Model - Investor can decide the risk or expected return
#   1. Max return with given risk volatilty 
#   2. Min risk with given fixed return
# No short positions, only long positions with 100% wealth to be divided among available assets
# Sum of the weights = 1
# Sharpe ratio S(x) = ( Avg. rate of return on investment - Rate of risk-free return ) / standard deviation
# S(x) > 1 is considerably good
# On an average there are 252 trading days in a year
NUM_TRADING_DAYS = 252
# Generate random w (different portfolios)
NUM_PORTFOLIOS = 10000

# Top stocks as per market cap
stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOG', 'GOOGL', 'META', 'TSLA', 'AVGO', 'NFLX']

# historical data - define START and END dates
start_date = '2018-01-01'
end_date = '2025-01-01'

class Markowitz:

    def __init__(self, stocks, start_date, end_date):
        self.data = None
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date

    def download_data(self):
        stock_data = {}

        for stock in self.stocks:
            ticker = yf.Ticker(stock)
            stock_data[stock] = ticker.history(start=self.start_date, end=self.end_date)['Close']

        return pd.DataFrame(stock_data)

    def show_data(self, data):
        data.plot(figsize=(10, 5))
        plt.show()

    def calculate_return(self, data):
        # NORMALIZATION - to measure all variables in comparable metric
        # s(t) / s(t-1)
        log_return = np.log(data / data.shift(1))
        return log_return[1:]

    def show_statistics(self, returns):
        # Annual metrics - mean of annual return
        print(returns.mean() * NUM_TRADING_DAYS)
        print(returns.cov() * NUM_TRADING_DAYS)

    def show_mean_variance(self, returns, weights):
        # we are after the annual return
        portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS
        # Co-variance matrix contains relationship between all the assets (sigma)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights)))
        print("Expected portfolio mean (return): ", portfolio_return)
        print("Expected portfolio volatility (standard deviation): ", portfolio_volatility)

    def show_portfolios(self, returns, volatilities):
        plt.figure(figsize=(10, 6))
        plt.scatter(volatilities, returns, c=returns / volatilities, marker='o')
        plt.grid(True)
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Return')
        plt.colorbar(label='Sharpe Ratio')
        plt.show()

    def generate_portfolios(self, returns):
        """
            Generating portfolio with risk adjustment
        """
        portfolio_means = []
        portfolio_risks = []
        portfolio_weights = []

        for _ in range(NUM_PORTFOLIOS):
            w = np.random.random(len(stocks))
            w /= np.sum(w)
            portfolio_weights.append(w)
            portfolio_means.append(np.sum(returns.mean() * w) * NUM_TRADING_DAYS)
            portfolio_risks.append(np.sqrt(np.dot(w.T, np.dot(returns.cov()
                                                          * NUM_TRADING_DAYS, w))))

        return np.array(portfolio_weights), np.array(portfolio_means), np.array(portfolio_risks)

    def statistics(self, weights, returns):
        """
            Show statistics
        """
        portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov()
                                                            * NUM_TRADING_DAYS, weights)))
        return np.array([portfolio_return, portfolio_volatility,
                     portfolio_return / portfolio_volatility])

    def min_function_sharpe(self, weights, returns):
        """
            scipy optimize module can find the minimum of a given function
            The maximum of a f(x) is the minimum of -f(x)
        """
        return -self.statistics(weights, returns)[2]

    # what are the constraints? The sum of weights = 1 !!!
    # f(x)=0 this is the function to minimize
    def optimize_portfolio(self, weights, returns):
        # Sum of weights is 1
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        # Weights would be in the range of 1, 1 means 100% invested in a single stock
        bounds = tuple((0, 1) for _ in range(len(stocks)))
        return optimization.minimize(fun=self.min_function_sharpe, x0=weights[0], args=returns
                                 , method='SLSQP', bounds=bounds, constraints=constraints)

    def print_optimal_portfolio(self, optimum, returns):
        print("Optimal portfolio: ", optimum['x'].round(3))
        print("Expected return, volatility and Sharpe ratio: ",
              self.statistics(optimum['x'].round(3), returns))

    def show_optimal_portfolio(self, opt, rets, portfolio_rets, portfolio_vols):
        plt.figure(figsize=(10, 6))
        plt.scatter(portfolio_vols, portfolio_rets, c=portfolio_rets / portfolio_vols, marker='o')
        plt.grid(True)
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Return')
        plt.colorbar(label='Sharpe Ratio')
        plt.plot(self.statistics(opt['x'], rets)[1], self.statistics(opt['x'], rets)[0], 'g*', markersize=20.0)
        plt.show()


if __name__ == '__main__':
    markowitz = Markowitz(stocks, start_date, end_date)
    dataset = markowitz.download_data()
    markowitz.show_data(dataset)
    log_daily_returns = markowitz.calculate_return(dataset)
    markowitz.show_statistics(log_daily_returns)

    pweights, means, risks = markowitz.generate_portfolios(log_daily_returns)
    markowitz.show_portfolios(means, risks)
    optimum = markowitz.optimize_portfolio(pweights, log_daily_returns)
    markowitz.print_optimal_portfolio(optimum, log_daily_returns)
    markowitz.show_optimal_portfolio(optimum, log_daily_returns, means, risks)
