import unittest
import os
import sys
PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('tests/',''))

from minerva.configuration_backtest import *
from minerva.genetic_algorithm import mutate_float, mutate_int, mutate_strategy
class TestFileManeagement(unittest.TestCase):
    """
    create 1 generation
    cross over
    selection
    mutate 1 generation
    """

    variable_a = 1
    function_b = function()
    
    @classmethod
    def setUp(self):
        self.calculation = function(8, 2)

    def test_0_get_object(self):
        self.assertIsNotNone(self.variable) 


class TestGetAreaRectangle(unittest.TestCase):
    def runTest(self):
        rectangle = function(2, 3)
        self.assertEqual(rectangle.get_area(), 6, "incorrect area")

    def test_sum(self):  
        self.assertEqual(sum([2, 3, 5]), 10, "It should be 10")  