import numpy.random as npr
import numpy as np
import matplotlib.pyplot as plt

n = 1000

class RandomBehaviorImplementation:
    def __init__(self, mu, sigma, dt, x0):
        self.mu = mu
        self.sigma = sigma
        self.dt = dt
        self.x0 = x0

    def wiener_process(self):
        """
            Wiener Process implementation
        """
        # W(t=0)=0, initialize W(t) with zeros
        W = np.zeros(n+1)
        # N+1 timestamps
        t = np.linspace(x0, n, n+1)

        W[1:n+1] = np.cumsum(np.random.normal(0, np.sqrt(dt), n))

        return t, W

    def plot_process(self, t, W):
        plt.plot(t, W)
        plt.xlabel('Time(t)')
        plt.ylabel('Wiener-Process W(t)')
        plt.title('Wiener-Process')
        plt.show()

    def simulate_geometric_random_walk(self, S0, T=2):
        """
            Geomtric Brownian Motion Implementation
        """
        dt = T/n
        t = np.linspace(x0, T, n)
        W = np.random.standard_normal(size=n)
        # N(0,dt) = sqrt(dt) * N(0,1)
        W = np.cumsum(W) * np.sqrt(dt)
        X = (self.mu - 0.5 * self.sigma ** 2) * t + self.sigma * W
        S = S0 * np.exp(X)

        return t, S

    def plot_gbm(self, t, S):
        plt.plot(t, S)
        plt.xlabel('Time (t)')
        plt.ylabel('Stock Price S(t)')
        plt.title('Geometric Brownian Motion')
        plt.show()

if __name__ == '__main__':

    mu=0.1
    sigma=0.05
    x0 = 0
    dt = 0.1
    rbf_impl = RandomBehaviorImplementation(mu, sigma, dt, x0)
    time, data = rbf_impl.wiener_process()
    rbf_impl.plot_process(time, data)

    time, data = rbf_impl.simulate_geometric_random_walk(1)
    rbf_impl.plot_gbm(time, data)
