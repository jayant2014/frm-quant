from math import exp

class EquityMarket:

    def __init__(self, investment, rate, period):
        # Investment amount
        self.investment = investment
        # Rate of return
        self.rate = rate / 100
        # Duration of investment
        self.period = period

    def future_discrete_value(self, x, r, n):
        return x*(1+r)**n

    def future_continuous_value(self, x, r, t):
        return x*exp(r*t)

    def present_discrete_value(self, x, r, n):
        return x*(1+r)**-n

    def present_continuous_value(self, x, r, t):
        return x*exp(-r*t)

    def time_value_of_money(self):
        """
            Args:
                investment: Initial investment
                rate: Rate of return
                period: Duration of investment in years
        """
        print("Investment value: %s, Future value (discrete model): %s" % (self.investment, self.future_discrete_value(self.investment, self.rate, self.period)))
        print("Investment value: %s, Future value (continuous model): %s" % (self.investment, self.future_continuous_value(self.investment, self.rate, self.period)))
        print("Investment value: %s, Present value (discrete model): %s" % (self.investment, self.present_discrete_value(self.investment, self.rate, self.period)))
        print("Investment value: %s, Present values (continuous model): %s" % (self.investment, self.present_continuous_value(self.investment, self.rate, self.period)))

if __name__ == '__main__':
    # Getting time value of money
    equity = EquityMarket(100, 7, 10)
    equity.time_value_of_money()









