import unittest
from io import StringIO
from unittest.mock import patch
from xalanih.core.parameters import *


class TestParameters(unittest.TestCase):

    def test_minimalArguments(self):
        args = ["create", "db"]
        params = Parameters(args)
        self.assertEquals(Constants.ACTION_CREATE, params.get_action())

        args = ["check_update", "db"]
        params = Parameters(args)
        self.assertEquals(Constants.ACTION_CHECK_UPDATE, params.get_action())

        args = ["check_db", "db"]
        params = Parameters(args)
        self.assertEquals(Constants.ACTION_CHECK_DB, params.get_action())

        args = ["update", "db"]
        params = Parameters(args)
        connection_info = params.get_connection_info()
        self.assertEquals(Constants.ACTION_UPDATE, params.get_action())
        self.assertEquals(".", params.get_directory())
        self.assertEquals(Constants.DB_MYSQL, params.get_database_type())
        self.assertEquals("db", connection_info.get_database())
        self.assertEquals(None, connection_info.get_password())
        self.assertEquals("root", connection_info.get_user())
        self.assertEquals(3306, connection_info.get_port())
        self.assertEquals("localhost", connection_info.get_host())
        self.assertEquals(None, params.get_socket())
        self.assertEquals(None, params.get_log_file())
        self.assertEquals(3, params.get_verbosity())
        self.assertEquals(None, params.get_last_update())
        self.assertEquals(False, params.get_no_update())

    def test_arguments(self):
        args = ["-d", "dir", "-t", Constants.DB_MYSQL, "-H", "host", "-p", "80",
                "-u", "user", "-pwd", "pwd", "-s", "socket", "-l", "logfile",
                "-v", "4", "-to", "update", "-nu", "create", "db"]
        params = Parameters(args)
        connection_info = params.get_connection_info()
        self.assertEquals("dir", params.get_directory())
        self.assertEquals(Constants.DB_MYSQL, params.get_database_type())
        self.assertEquals("pwd", connection_info.get_password())
        self.assertEquals("user", connection_info.get_user())
        self.assertEquals(80, connection_info.get_port())
        self.assertEquals("host", connection_info.get_host())
        self.assertEquals("socket", params.get_socket())
        self.assertEquals("logfile", params.get_log_file())
        self.assertEquals(4, params.get_verbosity())
        self.assertEquals("update", params.get_last_update())
        self.assertEquals(True, params.get_no_update())

    # noinspection PyTypeChecker
    @patch('sys.stderr', new_callable=StringIO)
    def test_wrongArgument(self, mock_stderr):
        args = ["-p", "aze", "create", "db"]
        with self.assertRaises(AssertionError):
            Parameters(args)

        args = ["wrong", "db"]
        with self.assertRaises(SystemExit):
            Parameters(args)
        self.assertRegexpMatches(mock_stderr.getvalue(), r"invalid choice")

        args = ["-v", "10", "create", "db"]
        with self.assertRaises(SystemExit):
            Parameters(args)
        self.assertRegexpMatches(mock_stderr.getvalue(), r"invalid choice")

        args = []
        with self.assertRaises(SystemExit):
            Parameters(args)

        args = ["create"]
        with self.assertRaises(SystemExit):
            Parameters(args)



