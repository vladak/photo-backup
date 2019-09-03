import unittest
import os


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def load_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(SCRIPT_DIR, pattern='test_*.py')
    print(test_suite)
    return test_suite
