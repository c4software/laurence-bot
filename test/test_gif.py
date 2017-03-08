# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *

class TestGif(unittest.TestCase):
    def test_cmd_gif(self):
        data = make_attrs("valentin", "yolo", args=["yolo"])
        self.assertTrue("![image](" in commands["gif"](data))

if __name__ == '__main__':
    unittest.main()
