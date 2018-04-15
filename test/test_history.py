# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *
from commands.libs.history import *


class TestHistory(unittest.TestCase):
    pseudo = "valentin_test"

    def test_a(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertTrue(commands["historique"](data) is not None)

    def test_get_last_message(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertTrue(get_last_message(data) is not None)

    def test_get(self):
        self.assertTrue(get_history(self.pseudo) is not None)

    def test_insert(self):
        add_history(self.pseudo, "Test")
        self.assertTrue(get_history(self.pseudo) is not None)
        remove_last_history(self.pseudo)

    def test_get_last_tags(self):
        save_last_tags(self.pseudo, "test")
        self.assertTrue(get_last_tags(self.pseudo) == "test")


if __name__ == '__main__':
    unittest.main()
