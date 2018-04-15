# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *


class TestBlog(unittest.TestCase):
    def test_cmd_commitstrip(self):
        data = make_attrs("valentin", "", args=[""])
        self.assertTrue("http" in commands["commitstrip"](data))

    def test_cmd_commitstrip_random(self):
        data = make_attrs("valentin", "random", args=["random"])
        self.assertTrue("http" in commands["commitstrip"](data))


if __name__ == '__main__':
    unittest.main()
