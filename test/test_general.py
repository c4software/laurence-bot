# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *
from commands.libs.history import save_last_tags, add_history
from commands.libs.context import get_awaiting_response
from commands.general import cmd_start
from settings import DEBUG_USER


class TestGeneral(unittest.TestCase):
    pseudo = "valentin_test"

    def test_start(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertIs(cmd_start(data), False)

    def test_echo(self):
        data = make_attrs(self.pseudo, "Bonjour", args=["Bonjour"])
        self.assertEqual(commands["echo"](data), "Bonjour")

    def test_bonjour(self):
        data = make_attrs(self.pseudo, "Bonjour", args=["Bonjour"])
        self.assertTrue(self.pseudo in commands["bonjour"](data))

    def test_bisous(self):
        data = make_attrs(self.pseudo, "bisous", args=["bisous"])
        self.assertEqual(commands["bisous"](data), ":kiss:")

    def test_aide(self):
        self.assertTrue(isinstance(general.get_command_list(), str))

    def test_hue(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertIs(commands["hue"](data), None)

    def test_context(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertIsInstance(commands["plus"](data), str)
        add_history(self.pseudo, "test")
        self.assertIsInstance(commands["plus"](data), str)
        self.assertTrue(get_awaiting_response(self.pseudo) is None)

    def test_learn(self):
        data = make_attrs(self.pseudo, "Bonjour", args=["Bonjour"])
        self.assertTrue("Vous devez avoir" in commands["learn"](data))

        save_last_tags(self.pseudo, [("echo"), ("test")])
        data = make_attrs(self.pseudo, "test_test", args=["test_test"])
        self.assertTrue("Désolé" in commands["learn"](data))

        save_last_tags(self.pseudo, [("echo"), ("test")])
        DEBUG_USER.append(self.pseudo)
        data = make_attrs(self.pseudo, "test_test", args=["test_test"], telegram=True)
        self.assertTrue("Correspondance" in commands["learn"](data))


if __name__ == '__main__':
    unittest.main()
