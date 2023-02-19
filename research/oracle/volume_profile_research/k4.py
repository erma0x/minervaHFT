import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt

# generate the data and plot it for an ideal normal curve

# x-axis for the plot
x_data = np.arange(-5, 5, 0.001)

# y-axis as the gaussian
y_data = stats.norm.pdf(x_data, 0, 1)

# plot data
plt.plot(x_data, y_data)
plt.show()
