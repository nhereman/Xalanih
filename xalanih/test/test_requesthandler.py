import unittest
from xalanih.core.requesthandler import RequestHandler


class TestRequestHandler(unittest.TestCase):

    def test_non_implemented(self):
        handler = RequestHandler()

        with self.assertRaises(Exception):
            handler.request_xalanih_table()
        with self.assertRaises(Exception):
            handler.request_xalanih_table_creation()
        with self.assertRaises(Exception):
            handler.request_update_recording()
        with self.assertRaises(Exception):
            handler.request_update()
        with self.assertRaises(Exception):
            handler.request_last_update()
