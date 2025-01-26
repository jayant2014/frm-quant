import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm

class StockReturnsCalculation:

    def __init__(self, stocks, start_date, end_date):
        self.data = None
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date
    
    def download_data(self):
        stock_data = {}

        for stock in stocks:
            ticker = yf.Ticker(stock)
            stock_data[stock] = ticker.history(start=start_date, end=end_date)['Close']

        return pd.DataFrame(stock_data)

    def show_data(self, stock_data):
        stock_data.plot(figsize=(10, 5))
        plt.show()

    def calculate_returns(self, stock_data):
        log_return = np.log(stock_data / stock_data.shift(1))
        #return log_return[1:]
        #stock_data['Close'] = np.log(stock_data['Close'] / stock_data['Close'].shift(1))
        return log_return

    def show_plot(self, stock_data):
        plt.hist(stock_data, bins=300)
        stock_variance = stock_data.var()
        stock_mean = stock_data.mean()
        sigma = np.sqrt(stock_variance)
        x = np.linspace(stock_mean - 3 * sigma, stock_mean + 3 * sigma, 100)
        plt.plot(x, norm.pdf(x, stock_mean, sigma))
        plt.show()


if __name__ == '__main__':

    # Top stocks as per market cap
    # stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOG', 'GOOGL', 'META', 'TSLA', 'AVGO', 'NFLX']
    stocks = ['NVDA']

    # historical data - define START and END dates
    start_date = '2018-01-01'
    end_date = '2025-01-01'

    stock_return = StockReturnsCalculation(stocks, start_date, end_date)
    stock = stock_return.download_data()
    stock_return.show_data(stock)
    log_daily_returns = stock_return.calculate_returns(stock)
    stock_return.show_plot(log_daily_returns)

