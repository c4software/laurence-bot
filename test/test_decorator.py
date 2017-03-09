# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands.decorators import register_as_command, commands

class testDecorator(unittest.TestCase):
    def test_decorator(self):
        @register_as_command("test_decorator")
        def test():
            pass

        self.assertTrue("test_decorator" in commands)

    def test_decorator(self):
        @register_as_command("test_decorator", keywords=["test_decorator_alias"])
        def test():
            pass
        self.assertTrue("test_decorator_alias" in commands)

if __name__ == '__main__':
    unittest.main()
