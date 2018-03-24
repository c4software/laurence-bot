# -*- coding: utf-8 -*-
import unittest

from tools.libs import *
from commands import *
from commands.planification import extract_hours_minutes
from commands.libs.history import add_history

class TestPlanification(unittest.TestCase):
    pseudo = "test_valentin"
    def test_extract_hours_minutes(self):
        hours, minutes = extract_hours_minutes("08:00")
        self.assertEqual(hours, "08")
        self.assertEqual(minutes, "00")

    def test_get_planning(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertIsInstance(commands["planning"](data), str)

    def test_planifier_no_heure_no_prev_messages(self):
        data = make_attrs(self.pseudo, "", args=[""])
        self.assertTrue("Désolé" in commands["planifier"](data))

if __name__ == '__main__':
    unittest.main()
