import os
from commands import *
import unittest

from settings import MAP_TRADUCTION
from tools.libs import *
from tools.libs import make_attrs


class TestMeeting(unittest.TestCase):
    pseudo = "@valentin"

    def test_cmd_meeting(self):
        data = make_attrs(self.pseudo, "meeting", args={})
        self.assertEqual(commands["meeting"](data), MAP_TRADUCTION["yesterday"])
        data = make_attrs(self.pseudo, "meeting", args="TEST 1")
        self.assertEqual(commands["meeting"](data), MAP_TRADUCTION["today"])
        data = make_attrs(self.pseudo, "meeting", args="TEST 2")
        self.assertEqual(commands["meeting"](data), "Merci !")


if __name__ == '__main__':
    unittest.main()

