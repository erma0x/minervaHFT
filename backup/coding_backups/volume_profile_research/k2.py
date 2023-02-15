import numpy
import scipy.interpolate
import random
import matplotlib.pyplot as pyplot

# create some normally distributed values and make a histogram
a = numpy.random.normal(size=10000)
counts, bins = numpy.histogram(a, bins=100, density=True)
cum_counts = numpy.cumsum(counts)
bin_widths = (bins[1:] - bins[:-1])

# generate more values with same distribution
x = cum_counts*bin_widths
y = bins[1:]
inverse_density_function = scipy.interpolate.interp1d(x, y)
b = numpy.zeros(10000)
for i in range(len(b)):
    u = random.uniform(x[0], x[-1])
    b[i] = inverse_density_function(u)

# plot both
pyplot.hist(a, 100)
pyplot.hist(b, 100)
pyplot.show()
