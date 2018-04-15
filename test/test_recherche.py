# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *


class TestRecherche(unittest.TestCase):
    def test_google(self):
        data = make_attrs("valentin", "Test", args=["Test"])
        self.assertTrue(commands["google"](data) is not "Recherche impossible.")

    def test_google_no_keywords(self):
        data = make_attrs("valentin", "", args=[""])
        self.assertTrue("Oui ?" in commands["google"](data))

    def test_wikipedia(self):
        data = make_attrs("valentin", "Test", args=["Test"])
        self.assertTrue(isinstance(commands["def"](data), str))

    def test_wikipedia_no_keywords(self):
        data = make_attrs("valentin", "", args=[""])
        self.assertTrue("Sur" in commands["def"](data))

    def test_proche(self):
        data = make_attrs("valentin", "48.802,2.025", args=["48.802,2.025"])
        self.assertTrue("Désolé" not in commands["proche"](data))


if __name__ == '__main__':
    unittest.main()
