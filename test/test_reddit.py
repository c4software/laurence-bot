# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *
from commands.reddit import get_reddit_random

class TestReddit(unittest.TestCase):
    pseudo = "valentin_test"
    def test_cmd_gif(self):
        data = make_attrs(self.pseudo, "yolo", args=["yolo"])
        self.assertIsInstance(commands["random"](data), str)
        self.assertTrue(get_reddit_random() is not None)
        self.assertIsInstance(commands["nsfw"](data), str)
        self.assertIsInstance(commands["image"](data), str)
        self.assertIsInstance(commands["cute"](data), str)
        self.assertIsInstance(commands["top10"](data), str)

if __name__ == '__main__':
    unittest.main()
