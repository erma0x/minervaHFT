from genetic_algorithm import get_population
def get_best(population, fitness_function):
    sorted_population = sorted(population, key=fitness_function, reverse=True)
    return sorted_population[0]

def save_best(population, fitness_function,generation_number):
    best = get_best(population, fitness_function)
    with open(f'best_{generation_number}.py', 'w') as f:
        for key, value in best.items():
            if type(value) == str:
                f.write(f"{key} = '{value}'\n")
            else:
                f.write(f"{key} = {value}\n")

def fitness_function(individual):
    return individual['fitness']

if __name__ == '__main__':
    POP = get_population('./strategies/')
    
    generation_number = 2
    best = get_best(population=POP,fitness_function=fitness_function)
    save_best(population=POP,fitness_function=fitness_function,generation_number=generation_number)
    print(best)