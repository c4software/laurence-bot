# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *

class TestGeneral(unittest.TestCase):
    def test_echo(self):
        data = make_attrs("valentin", "Bonjour", args=["Bonjour"])
        self.assertEqual(commands["echo"](data), "Bonjour")

    def test_bonjour(self):
        data = make_attrs("valentin", "Bonjour", args=["Bonjour"])
        self.assertTrue("valentin" in commands["bonjour"](data))


    def test_aide(self):
        self.assertTrue(isinstance(general.get_command_list(), str))


if __name__ == '__main__':
    unittest.main()
