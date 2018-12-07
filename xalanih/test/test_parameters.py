import unittest
from io import StringIO
from unittest.mock import patch
from xalanih.utils.parameters import *



class TestParameters(unittest.TestCase):

    def test_minimalArguments(self):
        args=["create", "db"]
        params = Parameters(args)
        self.assertEquals(params.get_action(), Constants.ACTION_CREATE)

        args = ["update", "db"]
        params = Parameters(args)
        connection_info = params.get_connection_info()
        self.assertEquals(params.get_action(), Constants.ACTION_UPDATE)
        self.assertEquals(params.get_directory(), ".")
        self.assertEquals(params.get_database_type(), Constants.DB_MYSQL)
        self.assertEquals(connection_info.get_database(), "db")
        self.assertEquals(connection_info.get_password(), None)
        self.assertEquals(connection_info.get_user(), "root")
        self.assertEquals(connection_info.get_port(), 3306)
        self.assertEquals(connection_info.get_host(), "localhost")
        self.assertEquals(params.get_socket(), None)
        self.assertEquals(params.get_log_file(), None)
        self.assertEquals(params.get_verbosity(), 3)
        self.assertEquals(params.get_last_update(), None)
        self.assertEquals(params.get_no_update(), False)

    def test_arguments(self):
        args = ["-d", "dir", "-t", Constants.DB_MYSQL, "-H", "host", "-p", "80",
                "-u", "user", "-pwd", "pwd", "-s", "socket", "-l", "logfile",
                "-v", "4", "-to", "update", "-nu", "create", "db"]
        params = Parameters(args)
        connection_info = params.get_connection_info()
        self.assertEquals(params.get_directory(), "dir")
        self.assertEquals(params.get_database_type(), Constants.DB_MYSQL)
        self.assertEquals(connection_info.get_password(), "pwd")
        self.assertEquals(connection_info.get_user(), "user")
        self.assertEquals(connection_info.get_port(), 80)
        self.assertEquals(connection_info.get_host(), "host")
        self.assertEquals(params.get_socket(), "socket")
        self.assertEquals(params.get_log_file(), "logfile")
        self.assertEquals(params.get_verbosity(), 4)
        self.assertEquals(params.get_last_update(), "update")
        self.assertEquals(params.get_no_update(), True)

    @patch('sys.stderr', new_callable=StringIO)
    def test_wrongArgument(self, mock_stderr):
        args = ["-p","aze","create", "db"]
        with self.assertRaises(AssertionError):
            Parameters(args)

        args = ["wrong", "db"]
        with self.assertRaises(SystemExit):
            Parameters(args)
        self.assertRegexpMatches(mock_stderr.getvalue(), r"invalid choice")

        args = ["-v", "10","create", "db"]
        with self.assertRaises(SystemExit):
            Parameters(args)
        self.assertRegexpMatches(mock_stderr.getvalue(), r"invalid choice")

        args = []
        with self.assertRaises(SystemExit):
            Parameters(args)

        args = ["create"]
        with self.assertRaises(SystemExit):
            Parameters(args)



