# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *
from commands.giphy import get_gyphy

class TestGif(unittest.TestCase):
    def test_cmd_gif(self):
        data = make_attrs("valentin_test", "yolo", args=["yolo"])
        self.assertTrue("![image](" in commands["gif"](data))

    def test_cmd_fail(self):
        data = make_attrs("valentin_test", "", args=[""])
        self.assertTrue("![image](" in commands["fail"](data))

    def test_get_gyphy(self):
        self.assertIsInstance(get_gyphy("yolo", False), str)


if __name__ == '__main__':
    unittest.main()
