import unittest
import random 

import os
import sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('tests/',''))
from copy import deepcopy 
#from configuration_backtest import *
from minerva.configuration_backtest import *
from research.genetic_algorithm.test_genetic_algorithm import get_filepaths_list, remove_folder, create_folder
from research.genetic_algorithm.test_genetic_algorithm import get_population, save_population
from research.genetic_algorithm.test_genetic_algorithm import mutate_float, mutate_int, mutate_strategy
from research.genetic_algorithm.test_genetic_algorithm import crossover, selection, fitness_function
from minerva.strategy_generator import strategy_generator
from research.genetic_algorithm.test_genetic_algorithm import get_best_initial_population, get_best


class TestFileManeagement(unittest.TestCase):
    """
    remove_folder()
    create_folder()
    get_list_filepath_strategies()
    strategy_generator()
    """
    create_folder(STRATEGIES_FOLDER)

    pop_size = 10
    generation_number = 5
    NEW_GENERATION_FOLDER = str(STRATEGIES_FOLDER).replace(f'generation_{generation_number}',f'generation_{generation_number+1}')


    # CREATE STRATEGY
    for i in range(pop_size): 
        strategy_generator(strategies_folder = STRATEGIES_FOLDER)

    list_of_files = get_filepaths_list(STRATEGIES_FOLDER)
    population = deepcopy(get_population(STRATEGIES_FOLDER))
    generation_number = 0
    # TEST get_filepaths_list(strategies_folder)
    def test_0_get_filepaths_list(self):
        self.assertIsNotNone(self.list_of_files)
        self.assertEqual(type(self.list_of_files),list)
        self.assertEqual(len(self.list_of_files), self.pop_size)

    def test_1_population(self):
        self.assertEqual(type(self.population),list)
        self.assertGreater(len(self.population),1)
        self.assertEqual(len(self.population),self.pop_size)

    def test_2_mutation(self):
        self.assertIsNotNone(mutate_float(value=5.1,min=5,max=5.2))

        self.assertEqual(type(mutate_float(value=5.1,min=5,max=5.2)),float)
        self.assertGreater(mutate_float(value=5.1,min=5,max=5.2),4.999)

        self.assertLess(mutate_float(value=5.1,min=5,max=5.2),5.201)
        self.assertAlmostEqual(round(mutate_float(value=5.001,min=5.0,max=5.01),1),5.0)
        

        self.assertIsNotNone(mutate_int(value=5,min=1,max=10))
        self.assertEqual(type(mutate_int(value=5,min=5,max=10)),int)

        self.assertGreaterEqual(mutate_int(value=5,min=1,max=10),1)
        self.assertLess(mutate_int(value=5,min=1,max=10),11)

        self.assertGreater(mutate_int(value=5,min=1,max=10),2)
        self.assertLess(mutate_int(value=5,min=1,max=10),8)
        self.assertNotIn(mutate_int(value=5,min=1,max=10),(1,2,8,9,10))

    def test_3_mutation_strategies(self):
        children = get_population(STRATEGIES_FOLDER)
        new_children = mutate_strategy(children)

        self.assertEqual(type(new_children),list)
        self.assertEqual(type(new_children[0]),dict)

        for i,j in zip(children, new_children):             
            self.assertEqual(type(i),dict)
            self.assertEqual(len(i), 15) # strategy parameters + fitness
            self.assertEqual(type(j),dict)
            self.assertEqual(len(j), 15) # strategy parameters + fitness
        self.assertNotEqual(children, new_children)

    def test_4_genetic_algorithm(self):

        children = get_population(STRATEGIES_FOLDER)
        self.assertIsNotNone(children)
        self.assertEqual(type(children),list)
        self.assertEqual(type(children[0]),dict)
        self.assertEqual(len(children),self.pop_size)

        for generation in range(self.generation_number): 

            children = selection(children, fitness_function)
            self.assertIsNotNone(children)
            self.assertEqual(type(children),list)
            self.assertGreater(len(children),1)

            for i in children:             
                self.assertEqual(len(i), 15) # strategy parameters + fitness

            if self.pop_size > len(children):
                while self.pop_size > len(children):
                    parent1 = random.choice(children)
                    parent2 = random.choice(children) 
                    child = crossover(parent1, parent2)
                    
                    child['fitness'] = mutate_float(1,0,10)

                    if child not in children:
                        children.append(child)

            self.assertIsNotNone(children)

            for i in children:             
                self.assertEqual(len(i), 15) # strategy parameters + fitness

            self.assertEqual(type(children),list)
            self.assertEqual(len(children),self.pop_size)

            self.generation_number = self.generation_number + 1

            self.assertIsNotNone(self.NEW_GENERATION_FOLDER)
            self.assertEqual(type(self.NEW_GENERATION_FOLDER),str)

            create_folder(self.NEW_GENERATION_FOLDER)

            save_population(population = children, dir_name = self.NEW_GENERATION_FOLDER )

            mutate_strategy(self.NEW_GENERATION_FOLDER)

            children = get_population(self.NEW_GENERATION_FOLDER)
            
            self.assertIsNotNone(children)
            self.assertEqual(type(children),list)
            self.assertEqual(len(children),self.pop_size)
            self.assertNotEqual(children,self.population)
        
if __name__ == "__main__":
    unittest.main()