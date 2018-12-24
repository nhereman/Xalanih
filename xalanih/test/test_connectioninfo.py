import unittest
from xalanih.core.connectioninfo import *


class TestConnectionInfo(unittest.TestCase):

    def setUp(self):
        self.connectionInfo = ConnectionInfo("localhost",1500,"db","user","pwd")

    def test_set_host(self):
        self.connectionInfo.set_host("new_host")
        self.assertEquals("new_host", self.connectionInfo.get_host())
        self.connectionInfo.set_host(None)
        self.assertEquals(None, self.connectionInfo.get_host())
        with self.assertRaises(AssertionError):
            self.connectionInfo.set_host(25)

    def test_set_port(self):
        self.connectionInfo.set_port(80)
        self.assertEquals(80, self.connectionInfo.get_port())
        self.connectionInfo.set_port(None)
        self.assertEquals(None, self.connectionInfo.get_port())
        with self.assertRaises(AssertionError):
            self.connectionInfo.set_port("port")

    def test_set_db(self):
        self.connectionInfo.set_database("db_name")
        self.assertEquals("db_name", self.connectionInfo.get_database())
        self.connectionInfo.set_database(None)
        self.assertEquals(None, self.connectionInfo.get_database())
        with self.assertRaises(AssertionError):
            self.connectionInfo.set_database(80)

    def test_set_user(self):
        self.connectionInfo.set_user("new_user")
        self.assertEquals("new_user", self.connectionInfo.get_user())
        self.connectionInfo.set_user(None)
        self.assertEquals(None, self.connectionInfo.get_user())
        with self.assertRaises(AssertionError):
            self.connectionInfo.set_user(80)

    def test_set_pwd(self):
        self.connectionInfo.set_password("new_pwd")
        self.assertEquals("new_pwd", self.connectionInfo.get_password())
        self.connectionInfo.set_password(None)
        self.assertEquals(None, self.connectionInfo.get_password())
        with self.assertRaises(AssertionError):
            self.connectionInfo.set_password(80)
