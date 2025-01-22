from math import exp

def future_discrete_value(x, r, n):
    return x*(1+r)**n

def future_continuous_value(x, r, t):
    return x*exp(r*t)

def present_discrete_value(x, r, n):
    return x*(1+r)**-n

def present_continuous_value(x, r, t):
    return x*exp(-r*t)

def time_value_of_money(investment, rate, period):
    """
        Args:
            investment: Initial investment
            rate: Rate of return
            period: Duration of investment in years
    """
    print("Investment value: %s, Future value (discrete model): %s" % (investment, future_discrete_value(investment, rate, period)))
    print("Investment value: %s, Future value (continuous model): %s" % (investment, future_continuous_value(investment, rate, period)))
    print("Investment value: %s, Present value (discrete model): %s" % (investment, present_discrete_value(investment, rate, period)))
    print("Investment value: %s, Present values (continuous model): %s" % (investment, present_continuous_value(investment, rate, period)))

if __name__ == '__main__':
    # Getting time value of money
    time_value_of_money(100, 0.07, 10)









