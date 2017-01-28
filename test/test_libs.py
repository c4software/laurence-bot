# -*- coding: utf-8 -*-
import unittest

from tools.libs import make_message

class TestReddit(unittest.TestCase):
    def test_make_message(self):
        """ Test de la création de message """
        self.assertTrue(isinstance(make_message(username="Test", icon_url="Test", fallback="Test", pretext="Test", title="Test", title_link="Test", text="Test", color="#7CD197"), dict))

if __name__ == '__main__':
    unittest.main()
