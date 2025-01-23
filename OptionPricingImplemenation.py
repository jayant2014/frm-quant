import numpy as np
from scipy import stats
from numpy import log, exp, sqrt
 
class OptionPricing:
	"""
		Black-Scholes and Monte-Carlo Model implementation for option pricing
	"""
    
	def __init__(self, S0, E, T, rf, sigma, iterations):
		self.S0 = S0
		self.E = E
		self.T = T
		self.rf = rf
		self.sigma = sigma     
		self.iterations = iterations 
 
	def call_option_price(self):
    	# First we have to calculate d1 and d2 parameters
		d1 = (log(self.S0 / self.E) + (self.rf + self.sigma * self.sigma / 2.0) * self.T) / (self.sigma * sqrt(self.T))
		d2 = d1 - self.sigma * sqrt(self.T)
		print("The d1 and d2 parameters: %s, %s" % (d1, d2))
    	# Use the N(x) to calculate the price of the option
		return self.S0*stats.norm.cdf(d1) - self.E*exp(-self.rf*self.T)*stats.norm.cdf(d2)


	def put_option_price(self):
    	# First we have to calculate d1 and d2 parameters
		d1 = (log(self.S0 / self.E) + (self.rf + self.sigma * self.sigma / 2.0) * self.T) / (self.sigma * sqrt(self.T))
		d2 = d1 - self.sigma * sqrt(self.T)
		print("The d1 and d2 parameters: %s, %s" % (d1, d2))
    	# Use the N(x) to calculate the price of the option
		return -self.S0*stats.norm.cdf(-d1) + self.E*exp(-self.rf*self.T)*stats.norm.cdf(-d2)

	def call_option_simulation(self):
		
		# We have 2 columns - first with 0s and the second with the payoff
		# First column of 0s: payoff function is max(0,S-E) for call option
		option_data = np.zeros([self.iterations, 2])
		rand = np.random.normal(0, 1, [1, self.iterations])
		
		# Equation for the S(t) stock price
		stock_price = self.S0*np.exp(self.T*(self.rf - 0.5*self.sigma**2)+self.sigma*np.sqrt(self.T)*rand)

		option_data[:,1] = stock_price - self.E   
        
		# np.amax() returns the max(0,S-E) according to the formula
		average = np.sum(np.amax(option_data, axis=1))/float(self.iterations)
 
		return np.exp(-1.0*self.rf*self.T)*average
		
	def put_option_simulation(self):
	
		# We have 2 columns - first with 0s and the second with the payoff
		# First column of 0s: payoff function is max(0,E-S) for put option
		option_data = np.zeros([self.iterations, 2])
		rand = np.random.normal(0, 1, [1, self.iterations])
		
		# Equation for the S(t) stock price
		stock_price = self.S0*np.exp(self.T*(self.rf - 0.5*self.sigma**2)+self.sigma*np.sqrt(self.T)*rand)
 
		option_data[:,1] = self.E - stock_price  

		# np.amax() returns the max(0,E-S) according to the formula
		average = np.sum(np.amax(option_data, axis=1))/float(self.iterations)
 
		# Use the exp(-rT) discount factor
		return np.exp(-1.0*self.rf*self.T)*average

if __name__ == "__main__":
	
	# Underlying stock price at t=0
	S0=100	
	# Strike price				
	E=100
	# Expiry, 1 year
	T = 1
	# Risk free return
	rf = 0.07
	# Volatility of underlying stocks
	sigma=0.2
	# Number of iterations in the Monte-Carlo simulation	
	iterations = 1000000
	
	model = OptionPricing(S0, E , T, rf, sigma, iterations)

	print("Call option price according to Black-Scholes model: ", model.call_option_price())
	print("Put option price according to Black-Scholes model: ", model.put_option_price())
	
	print("Call option price with Monte-Carlo approach: ", model.call_option_simulation()) 
	print("Put option price with Monte-Carlo approach: ", model.put_option_simulation())
