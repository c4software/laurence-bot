# -*- coding: utf-8 -*-
import unittest

from tools.extended_BaseHTTPServer import *

class TestExtended_BaseHTTPServer(unittest.TestCase):
    pseudo = "test_valentin"
    def test_redirect(self):
        data = redirect("test_lien")
        self.assertTrue(data["Location"] == "test_lien")

    def add_route(self):
        @route(path="/get", method=["GET"])
        def stub():
            pass

        @route(path="/post", method=["POST"])
        def stub():
            pass

        self.assertTrue("/get" in register_route["GET"])
        self.assertTrue("/post" in register_route["POST"])

if __name__ == '__main__':
    unittest.main()
