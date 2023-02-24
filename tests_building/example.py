import unittest
from unittest.mock import patch

import os
import sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('tests/',''))

from minerva.configuration_backtest import *

class TestFileManeagement(unittest.TestCase):
    """
    remove_folder()
    create_folder()
    get_list_filepath_strategies()
    strategy_generator()
    """

    variable_a = 1
    function_b = function()
    
    @classmethod
    def setUpClass(cls):
        print('setUpClass')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')

    @classmethod
    def setUp(self):
        print('setUp')
        self.calculation = function(8, 2)

    @classmethod
    def tearDown(self):
        print('tearDown')
        self.calculation = function(8, 2)

    def test_0_get_object(self):
        self.assertIsNotNone(self.variable) 
        self.assertRaises('TypeError',function())

class TestGetAreaRectangle(unittest.TestCase):
    def runTest(self):
        rectangle = function(2, 3)
        self.assertEqual(rectangle.get_area(), 6, "incorrect area")

    def test_sum(self):  
        self.assertEqual(sum([2, 3, 5]), 10, "It should be 10")  

if __name__ == '__main__':
    unittest.main()

"""
        assertEqual(a, b)	        a == b
        assertNotEqual(a, b)	    a != b
        assertTrue(x)	            bool(x) is True
        assertFalse(x)	            bool(x) is False
        assertIs(a, b)          	a is b
        assertIsNot(a, b)	        a is not b
        assertIsNone(x)         	x is None
        assertIsNotNone(x)      	x is not None
        assertIn(a, b)          	a in b
        assertNotIn(a, b)	        a not in b
        assertIsInstance(a, b)	    isinstance(a, b)
        assertNotIsInstance(a, b)	not isinstance(a, b)
"""