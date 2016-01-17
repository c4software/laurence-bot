# -*- coding: utf-8 -*-
import unittest

from commands.reddit import get_reddit_random

class TestReddit(unittest.TestCase):
    def setUp(self):
        print ("====================")
        print ("Début du test Reddit")
        print ("====================")

    def test_get_reddit_random(self):
        """ Test l'accès à Reddit """
        self.assertTrue(isinstance(get_reddit_random(), dict))

if __name__ == '__main__':
    unittest.main()
