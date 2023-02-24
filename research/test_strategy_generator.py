import unittest

# Unit tests for strategy generator
from minerva.strategy_generator import strategy_generator
from minerva.configuration_strategy import MARKET
from minerva.configuration_backtest import STRATEGIES_FOLDER
from minerva.genetic_algorithm import get_filepaths_list

class Test(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """
    REAL_FOLDER = STRATEGIES_FOLDER.replace('tests','minerva')
    list_of_files_1 = get_filepaths_list(REAL_FOLDER)

    strategy_generator(REAL_FOLDER)  

    list_of_files_2 = get_filepaths_list(REAL_FOLDER)

    def test_0_addition_with_filepath_count(self):
        self.assertEqual( len(self.list_of_files_2), len(self.list_of_files_1) + 1 ,' MUST BE EQUAL' )

    def test_0_addition_with_filepath_count(self):
        self.assertEqual( len(self.list_of_files_2), len(self.list_of_files_1) + 1 ,' MUST BE EQUAL' )


if __name__ == '__main__':
    unittest.main()