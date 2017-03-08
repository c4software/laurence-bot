# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *

class TestBlog(unittest.TestCase):
    def test_cmd_mademoiselle(self):
        self.assertTrue("![image](" in commands["mlle"](None))

    def test_cmd_madame(self):
        self.assertTrue("![image](" in commands["madame"](None))

    def test_cmd_commitstrip(self):
        data = make_attrs("valentin", "", args=[""])
        self.assertTrue("http" in commands["commitstrip"](data))

    def test_cmd_chuck(self):
        self.assertIsNot(commands["chuck"](None), None)

    def test_cmd_fml(self):
        self.assertIsNot(commands["fml"](None), None)

    def test_cmd_code(self):
        self.assertTrue(isinstance(commands["code"](None), str))

    def test_cmd_sysadmin(self):
        self.assertTrue(isinstance(commands["sysadmin"](None), str))


if __name__ == '__main__':
    unittest.main()
