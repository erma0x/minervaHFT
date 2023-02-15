from genetic_algorithm import get_population
from configuration_backtest import *

# Funzione di fitness
def fitness_function(individual):
    return individual['fitness']

def get_best(population, fitness_function):
    sorted_population = sorted(population, key=fitness_function, reverse=True)
    return sorted_population[0]

population = get_population(STRATEGY_FOLDER)

print(get_best(population=population,fitness_function = fitness_function))