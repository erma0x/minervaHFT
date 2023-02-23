
import unittest

from minerva.configuration_backtest import *
from minerva.database_utils import dropzeros, give_nice_data

class TestCreateRemoveFolders(unittest.TestCase):

    A=3000
    B=2340
    C=1.0023
    ALL = [A,B,C]
    ASK =[[2000,0.1 ] ,[2001,0.2] ,[2003,0.3]]
    FORMATTED_DATA = [dropzeros(i[0]) for i in give_nice_data(ask_or_bid=ASK)]

    def test_0_orderbook(self):
        for i in self.ALL:
            self.assertIsNotNone(give_nice_data(ask_or_bid=self.ASK))  
            self.assertEqual(type(give_nice_data(ask_or_bid=self.ASK)), list)  

            self.assertIsNotNone(dropzeros(i))  
            self.assertIn(type(dropzeros(i)), (float,int))  
        
        self.assertEqual(type(self.FORMATTED_DATA), list)  
        self.assertIsNotNone(self.FORMATTED_DATA)  



if __name__ == "__main__":
    unittest.main()
