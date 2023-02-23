import unittest
import os
import sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('tests/',''))

from minerva.configuration_backtest import *
from minerva.database_utils import create_database, orderbook_storage

class TestDatabaseManeagement(unittest.TestCase):

    create_database()
    orderbook_storage()

    def test_0_get_object(self):
        for i in self.ALL:
            self.assertIsNotNone()  

    def test_1_type(self):
        for i in self.ALL:
            self.assertIn(type(), (float,int))  

    def test_3_type_format_data(self):
        for i in self.ALL:
            self.assertEqual(type(), list)  

    def test_4_get_object(self):
        self.assertIs(self.FORMATTED_DATA)  



if __name__ == "__main__":
    unittest.main()
