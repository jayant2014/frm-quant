import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

RISK_FREE_RATE = 0.07
MONTHS_IN_YEAR = 12

class CAPM:

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

    def initialize(self):
        stock_data = self.download_data()
        # Monthly returns instead of daily returns
        stock_data = stock_data.resample('ME').last()

        self.data = pd.DataFrame({'s_adjclose': stock_data[self.stocks[0]],
                                  'm_adjclose': stock_data[self.stocks[1]]})

        # Logarithmic monthly returns
        self.data[['s_returns', 'm_returns']] = np.log(self.data[['s_adjclose', 'm_adjclose']] /
                                            self.data[['s_adjclose', 'm_adjclose']].shift(1))

        # Remove the NaN values
        self.data = self.data[1:]

    def calculate_beta(self):
        # Covariance matrix - the diagonal items are the variances off diagonals are the covariances
        covariance_matrix = np.cov(self.data["s_returns"], self.data["m_returns"])
        # Calculating beta according to the formula
        beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
        print("Beta from formula: ", beta)

    def regression(self):
        beta, alpha = np.polyfit(self.data['m_returns'], self.data['s_returns'], deg=1)
        print("Beta from regression: ", beta)
        # Expected return as per the CAPM formula
        expected_return = RISK_FREE_RATE + beta * (self.data['m_returns'].mean()*MONTHS_IN_YEAR - RISK_FREE_RATE)
        print("Expected return: ", expected_return)
        self.plot_regression(alpha, beta)

    def plot_regression(self, alpha, beta):
        fig, axis = plt.subplots(1, figsize=(20, 10))
        axis.scatter(self.data["m_returns"], self.data['s_returns'], label="Data Points")
        axis.plot(self.data["m_returns"], beta * self.data["m_returns"] + alpha, color='red', label="CAPM Line")
        plt.title('Capital Asset Pricing Model, finding alpha and beta')
        plt.xlabel('Market return $R_m$', fontsize=18)
        plt.ylabel('Stock return $R_a$')
        plt.text(0.08, 0.05, r'$R_a = \beta * R_m + \alpha$', fontsize=18)
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == '__main__':

    # Top stocks as per market cap
    stocks = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOG', 'GOOGL', 'META', 'TSLA', 'AVGO', 'NFLX']

    # historical data - define START and END dates
    start_date = '2018-01-01'
    end_date = '2025-01-01'

    capm = CAPM(stocks, start_date, end_date)
    capm.initialize()
    capm.calculate_beta()
    capm.regression()
