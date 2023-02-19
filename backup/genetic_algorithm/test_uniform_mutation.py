import random 
import numpy as np
import os, time
import math

MAX_PERCENTAGE_PER_TRADE = 0.1

def mutate_int(value,min,max):
    increment = min
    value = value + random.randint(-increment,increment)
    
    if value >= max:
        value = value - int(math.floor(max / random.uniform(2.0,4.0)))

    if value <= min:
        value = value + int(math.floor(max / random.uniform(2.0,4.0)))

    return value

def mutate_float(value,min,max):
    sigma = max/10
    mu = value
    value = np.random.normal(mu, sigma, 1)
    if value >= max:
        value = value - max / random.uniform(2.0,4.0)

    if value <= min:
        value = value + max / random.uniform(2.0,4.0)

    return value

print( mutate_float(value = 0.049, min = 0.01,max = 0.05) )
print( mutate_int(value = 56, min = 10,max = 500 ) )
