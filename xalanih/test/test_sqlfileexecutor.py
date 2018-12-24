import unittest
import os
from xalanih.core.sqlfileexecutor import SqlFileExecutor
from xalanih.test.mocks.logger import Logger
from xalanih.test.mocks.connection import Connection


class TestSqlFileExecutor(unittest.TestCase):

    def setUp(self):
        self.connection = Connection()
        self.logger = Logger()
        self.dir = os.path.dirname(__file__) + "/data/executor_test/"

    def tearDown(self):
        self.connection.reinit()

    def test_executeSuccess(self):
        sql_file = open(self.dir + "success.sql")
        SqlFileExecutor.execute(self.connection, sql_file, self.logger)
        sql_file.close()
        self.assertEqual(3, len(self.connection.get_queries()),
                         "Wrong number of request executed.")

    def test_executeEmpty(self):
        sql_file = open(self.dir + "empty.sql")
        SqlFileExecutor.execute(self.connection, sql_file, self.logger)
        sql_file.close()
        self.assertEqual(0, len(self.connection.get_queries()),
                         "Wrong number of request executed.")
