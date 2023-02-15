import random

def crossover(parent1, parent2):
    child = {}

    for key in parent1:
        if key == 'fitness':
            continue
        if random.random() < 0.5:
            child[key] = parent1[key]
        else:
            child[key] = parent2[key]    
    return child

def genetic_algorithm(population, fitness_function):
    # Seleziona i genitori
    parents = selection(population, fitness_function)
    
    # Esegue il cross over
    children = []
    for i in range(0, len(parents), 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        child = crossover(parent1, parent2)
        children.append(child)
    
    return children

# Funzione di selezione fittness
def selection(population, fitness_function):
    sorted_population = sorted(population, key=fitness_function, reverse=True)
    return sorted_population[:len(population) // 2]

# Funzione di fitness
def fitness_function(individual):
    return individual['fitness']

def read_files(file_list):
    population = []
    for file in file_list:
        with open(file, 'r') as f:
            data = f.readlines()
            # assume che i valori di 'param1', 'param2', e 'fitness' siano sulla stessa riga del file separati da virgole
            # e convertili in un dizionario
            # individual = {'param1': float(data[0].split(',')[0]), 
            #               'param2': float(data[0].split(',')[1]),
            #               'fitness': float(data[0].split(',')[2])}
            population.append(individual)
    return population



initial_population = read_files()
new_population = genetic_algorithm(initial_population, fitness_function)
