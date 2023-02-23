
import unittest

from minerva.configuration_backtest import *
from minerva.database_utils import dropzeros, give_nice_data

class TestCreateRemoveFolders(unittest.TestCase):
    """
    remove_folder()
    create_folder()
    get_list_filepath_strategies()
    strategy_generator
    """
    A=3000
    B=2340
    C=1.0023
    ALL = [A,B,C]
    ASK =[[2000,0.1 ] ,[2001,0.2] ,[2003,0.3]]
    FORMATTED_DATA = [dropzeros(i[0]) for i in give_nice_data(ask_or_bid=ASK)]

    def test_0_get_object(self):
        for i in self.ALL:
            self.assertIsNotNone(dropzeros(i))  

    def test_1_type(self):
        for i in self.ALL:
            self.assertIn(type(dropzeros(i)), (float,int))  

    def test_2_get_object(self):
        for i in self.ALL:
            self.assertIsNotNone(give_nice_data(ask_or_bid=self.ASK))  

    def test_3_type_format_data(self):
        for i in self.ALL:
            self.assertEqual(type(give_nice_data(ask_or_bid=self.ASK)), list)  

    def test_4_get_object(self):
        self.assertIsNotNone(self.FORMATTED_DATA)  

    def test_5_get_object(self):
        self.assertEqual(type(self.FORMATTED_DATA), list)  


if __name__ == "__main__":
    unittest.main()
