import math

def selection(population, fitness_function):
    sorted_population = sorted(population, key=fitness_function, reverse=True)
    return sorted_population[:int(math.floor(len(population) // 2)) ]

def fitness_function(individual):
    return individual['fitness']

POP = [{'MARKET' : "BTCUSDT",
'LIMIT_ORDER_BOOK' : 398,
'RELATIVE_THRESHOLD_DIV' : 61,
'THRESHOLD_SHORT' : 0.63,
'fitness' : 0
},{'MARKET' : "BTCUSDT",
'LIMIT_ORDER_BOOK' : 123,
'RELATIVE_THRESHOLD_DIV' : 89,
'THRESHOLD_SHORT' : 0.12,
'fitness' : 1
}]

children = selection(population=POP,fitness_function=fitness_function)
print(children)