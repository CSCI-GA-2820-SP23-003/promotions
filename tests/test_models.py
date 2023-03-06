"""
Test cases for Promotion Model

"""
import os
import logging
import unittest
from service.models import Promotion, DataValidationError, db


######################################################################
#  Promotion   M O D E L   T E S T   C A S E S
######################################################################
class TestPromotion(unittest.TestCase):
    """ Test Cases for Promotion Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """

    def setUp(self):
        """ This runs before each test """

    def tearDown(self):
        """ This runs after each test """

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_example_replace_this(self):
        """ It should always be true """
        self.assertTrue(True)
