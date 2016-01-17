# -*- coding: utf-8 -*-
import unittest

from commands.reddit import get_reddit_random, cmd_random

class TestReddit(unittest.TestCase):
    def test_get_reddit_random(self):
        """ Test l'accès à Reddit """
        self.assertTrue(isinstance(get_reddit_random(), dict))

if __name__ == '__main__':
    unittest.main()
