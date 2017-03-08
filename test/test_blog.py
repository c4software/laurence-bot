# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *

class TestMlleMadame(unittest.TestCase):
    def test_cmd_mademoiselle(self):
        retour = commands["mlle"](None)
        self.assertTrue("![image](" in retour)

    def test_cmd_madame(self):
        retour = commands["madame"](None)
        self.assertTrue("![image](" in retour)


if __name__ == '__main__':
    unittest.main()
