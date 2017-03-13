# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *
from commands.quizz import *

class TestQuizz(unittest.TestCase):
    pseudo = "valentin_test"
    def test_get_question(self):
        self.assertIsInstance(get_question(), str)

    def test_stop(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertTrue("Arret du quizz" in commands["stop"](data))

    def test_get_score(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertIsInstance(commands["score"](data), str)

    def test_indice(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertIsInstance(commands["indice"](data), str)

if __name__ == '__main__':
    unittest.main()
