# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *
from commands.giphy import get_gyphy

class TestReddit(unittest.TestCase):
    pseudo = "valentin_test"
    def test_cmd_gif(self):
        data = make_attrs(self.pseudo, "yolo", args=["yolo"])
        self.assertIsInstance(commands["random"](data), str)
        self.assertIsInstance(commands["nsfw"](data), str)
        self.assertIsInstance(commands["image"](data), str)
        self.assertIsInstance(commands["cute"](data), str)
        self.assertIsInstance(commands["top10"](data), str)

if __name__ == '__main__':
    unittest.main()
