import unittest

# Unit tests for strategy generator
import minerva.strategy_generator as strategy_generator
from configuration_strategy import MARKET
from configuration_backtest import STRATEGIES_FOLDER
from genetic_algorithm import get_list_filepath_strategies

class Test(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """
    list_of_files_1 = get_list_filepath_strategies(STRATEGIES_FOLDER)

    strategy_generator()  

    list_of_files_2 = get_list_filepath_strategies(STRATEGIES_FOLDER)

    def test_0_addition_with_filepath_count(self):
        unittest.assert_equal( len(self.list_of_files_2), len(self.list_of_files_1) + 1  )

    def test_1_creation_of_the_correct_parameters(self):
        pass

    def test_2_starting_fitness_equal_to_zero(self):
    
        self.assertIsNotNone()  # null user id will fail the test
        self.assertEqual('There is no such user', self.person.get_name())



if __name__ == '__main__':
    unittest.main()