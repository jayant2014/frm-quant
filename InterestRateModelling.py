import matplotlib.pyplot as plt
import numpy as np
from numpy.random import normal

class InterestRateModelling:

    def __init__(self, x0, r0, kappa, theta, sigma):
        self.x0 = x0
        self.r0 = r0
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma

    def generate_process(self, dt=0.1, theta=1.2, mu=0.9, sigma=0.9, n=10000):
        # x(t=0)=0 and initialize x(t) with zeros
        x = np.zeros(n)

        for t in range(1, n):
            x[t] = x[t-1] + theta*(mu-x[t-1])*dt + sigma * normal(0, np.sqrt(dt))

        return x

    def plot_process(self, x):
        plt.plot(x)
        plt.xlabel('t')
        plt.ylabel('x(t)')
        plt.title('Ornstein-Uhlenbeck Process')
        plt.show()

    def vasicek_model(self, r0, kappa, theta, sigma, T=1., N=1000):

        dt = T/float(N)
        t = np.linspace(0, T, N+1)
        rates = [r0]

        for _ in range(N):
            dr = kappa*(theta-rates[-1])*dt + sigma*np.sqrt(dt)*np.random.normal()
            rates.append(rates[-1]+dr)

        return t, rates

    def plot_model(self, t, r):
        plt.plot(t, r)
        plt.xlabel('Time (t)')
        plt.ylabel('Interest rate r(t)')
        plt.title('Vasicek Model')
        plt.show()


if __name__ == '__main__':

    # Position
    x = 10000
    # Initial IR
    r0 = 4.4
    kappa = 0.9
    theta = 4.5
    sigma = 0.03
    ir_model = InterestRateModelling(x, r0, kappa, theta, sigma)

    #data = ir_model.generate_process()
    #ir_model.plot_process(data)

    # Try out the params to see the variation
    time, data = ir_model.vasicek_model(r0, kappa, theta, sigma)
    ir_model.plot_model(time, data)
