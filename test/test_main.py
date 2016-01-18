# -*- coding: utf-8 -*-
import unittest

from run import chat
import json

class TestReddit(unittest.TestCase):
    user_name = "Valentin"
    def test_chat(self):
        """ Test Global """
        data = {"text": ["! bonjour"], "user_name": [self.user_name]}
        result = json.loads(chat(data))
        self.assertEqual(result["text"], "Bonjour {0}".format(self.user_name))

if __name__ == '__main__':
    unittest.main()
