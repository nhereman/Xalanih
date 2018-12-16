import unittest
from xalanih.core.dbconnector import DBConnector


class TestDbConnector(unittest.TestCase):

    def test_non_implemented(self):
        connector = DBConnector()

        with self.assertRaises(Exception):
            connector.connect()
        with self.assertRaises(Exception):
                connector.get_connection()