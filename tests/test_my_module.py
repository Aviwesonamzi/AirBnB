#!/usr/bin/python3
"""
test_my_module.py
Unit tests for my_module.py.
"""

import unittest
from my_module import my_function


class TestMyFunction(unittest.TestCase):

    def test_basic_case(self):
        """Test basic functionality."""
        self.assertEqual(my_function(1, 2), 3)


if __name__ == '__main__':
    unittest.main()
