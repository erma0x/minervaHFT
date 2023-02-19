import unittest

from ..minerva.configuration_backtest import *

from minerva.configuration_backtest import *

from minerva.configuration_backtest import TEST_STRATEGY_FOLDER
from minerva.genetic_algorithm import get_list_filepath_strategies, remove_folder, create_folder
from minerva.strategy_generator import strategy_generator


class TestCreateRemoveFolders(unittest.TestCase):
    """
    remove_folder()
    create_folder()
    get_list_filepath_strategies()
    strategy_generator
    """
    remove_folder(TEST_STRATEGY_FOLDER)

    create_folder(TEST_STRATEGY_FOLDER)

    for i in range(10):
        strategy_generator(strategies_folder = TEST_STRATEGY_FOLDER)

    list_of_files = get_list_filepath_strategies(TEST_STRATEGY_FOLDER)

    def test_0_get_object(self):
        self.assertIsNotNone(self.list_of_files)  

    def test_1_length(self):
        self.assertEqual(len(self.list_of_files), 10)

    def test_2_type(self):
        self.assertEqual(type(self.list_of_files), list)

    def test_3_try_to_get_error_filenotfound(self):
        remove_folder(TEST_STRATEGY_FOLDER)
        try:
            self.list_of_files = get_list_filepath_strategies(TEST_STRATEGY_FOLDER)
        
        except FileNotFoundError:
            self.assertIsNotNone(self.list_of_files) # still full 

    def test_4_get_file(self):
        create_folder(TEST_STRATEGY_FOLDER)
        self.assertIsNotNone(get_list_filepath_strategies(TEST_STRATEGY_FOLDER)) 

    def test_5_remove(self):
        remove_folder(TEST_STRATEGY_FOLDER)
        self.assertIsNotNone(get_list_filepath_strategies(TEST_STRATEGY_FOLDER)) 

if __name__ == "__main__":
    unittest.main()