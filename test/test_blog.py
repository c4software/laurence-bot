# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *

class TestBlog(unittest.TestCase):
    def test_cmd_mademoiselle(self):
        self.assertIsNot(commands["mlle"](None), None)

    def test_cmd_madame(self):
        self.assertIsNot(commands["madame"](None), None)

    def test_cmd_commitstrip(self):
        data = make_attrs("valentin", "", args=[""])
        self.assertTrue("http" in commands["commitstrip"](data))

    def test_cmd_commitstrip_random(self):
        data = make_attrs("valentin", "random", args=["random"])
        self.assertTrue("http" in commands["commitstrip"](data))

    def test_cmd_chuck(self):
        self.assertIsNot(commands["chuck"](None), None)

    def test_cmd_fml(self):
        self.assertIsNot(commands["fml"](None), None)

    def test_cmd_code(self):
        self.assertIsNot(commands["code"](None), None)

    def test_cmd_sysadmin(self):
        self.assertIsNot(commands["sysadmin"](None), None)


if __name__ == '__main__':
    unittest.main()
