# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *
from commands.quizz import *
import itertools


class TestQuizz(unittest.TestCase):
    pseudo = "valentin_test"

    def test_get_question(self):
        self.assertIsInstance(get_question(), str)

    def test_question(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertIsInstance(commands["question"](data), str)

    def test_stop(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertTrue("Arret du quizz" in commands["stop"](data))

    def test_get_score(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertIsInstance(commands["score"](data), str)

    def test_r(self):
        get_question()

        # 30 tentatives
        for _ in itertools.repeat(None, 40):
            data = make_attrs(self.pseudo, "test", args=["test"])
            self.assertIsInstance(commands["r"](data), str)

        data = make_attrs(self.pseudo, quizz.quizz_reponse, args=[quizz.quizz_reponse])
        self.assertIsInstance(commands["r"](data), str)
        self.assertTrue(self.pseudo in commands["score"](data))

        quizz.quizz_reponse = "test t"
        data = make_attrs(self.pseudo, "test", args=["test"])
        self.assertTrue("pas loin" in commands["r"](data))

        # Deux bonnes réponses
        get_question()
        data = make_attrs(self.pseudo, quizz.quizz_reponse, args=[quizz.quizz_reponse])
        self.assertIsInstance(commands["r"](data), str)
        self.assertTrue(self.pseudo in commands["score"](data))

    def test_indice(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertIsInstance(commands["indice"](data), str)

        commands["stop"](data)
        self.assertIsInstance(commands["indice"](data), str)

        get_question()
        quizz.quizz_reponse = None
        self.assertIsInstance(commands["indice"](data), str)


if __name__ == '__main__':
    unittest.main()
