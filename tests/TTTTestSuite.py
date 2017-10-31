#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 12:06:38 2017

@author: david
"""

import unittest
import sys
sys.path.append('..')
#user defined
from TTTBoardTest import TestTTTBoard
from TTTServerTest import TestTTTConnection

test_board = unittest.TestLoader().loadTestsFromTestCase(TestTTTBoard)
test_server_client = unittest.TestLoader().loadTestsFromTestCase(TestTTTConnection)

test_suite = unittest.TestSuite([test_board, test_server_client])
runner_result = unittest.TextTestRunner(verbosity=2).run(test_suite).wasSuccessful()
#.run(testsuite)
#ret = not runner.run(test_suite).wasSuccessful()
sys.exit(not runner_result)