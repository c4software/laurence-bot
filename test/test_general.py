# -*- coding: utf-8 -*-
import unittest

from commands.general import get_command_list

class TestGeneral(unittest.TestCase):
    def test_aide(self):
        self.assertTrue(isinstance(get_command_list(), str))

if __name__ == '__main__':
    unittest.main()
