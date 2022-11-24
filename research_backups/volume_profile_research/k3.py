from scipy.stats import norm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys
import numpy as np


def bivariate_normal(X, Y, sigmax=1.0, sigmay=1.0,
                     mux=0.0, muy=0.0, sigmaxy=0.0):
    """
    Bivariate Gaussian distribution for equal shape *X*, *Y*.
    See `bivariate normal
    <http://mathworld.wolfram.com/BivariateNormalDistribution.html>`_
    at mathworld.
    """
    Xmu = X-mux
    Ymu = Y-muy

    rho = sigmaxy/(sigmax*sigmay)
    z = Xmu**2/sigmax**2 + Ymu**2/sigmay**2 - 2*rho*Xmu*Ymu/(sigmax*sigmay)
    denom = 2*np.pi*sigmax*sigmay*np.sqrt(1-rho**2)
    return np.exp(-z/(2*(1-rho**2))) / denom


# read data from a text file. One number per line
arch = sys.path[0]+"/exmpl_best.txt"
datos = []
for item in open(arch, 'r'):
    item = item.strip()
    if item != '':
        try:
            datos.append(float(item))
        except ValueError:
            pass

# best fit of data
(mu, sigma) = norm.fit(datos)

# the histogram of the data
n, bins, patches = plt.hist(datos, 60, facecolor='green', alpha=0.75)

# add a 'best fit' line
y = bivariate_normal(bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=2)

# plot
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title(f'mean: {mu} sigma : {sigma}')
plt.grid(True)

plt.show()
