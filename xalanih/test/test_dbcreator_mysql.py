import unittest
import os
from xalanih.core.dbcreator import DBCreator
from xalanih.core.xalanihexception import XalanihException
from xalanih.core.mysql.mysqlrequesthandler import MysqlRequestHandler
from xalanih.test.mocks.connection import Connection
from xalanih.test.mocks.logger import Logger
from xalanih.test.mocks.dbchecker import DBChecker


class TestDBCreatorMySQL(unittest.TestCase):

    def setUp(self):
        self.connection = Connection()
        self.logger = Logger()
        self.dir = os.path.dirname(__file__) + "/data/"
        self.req_handler = MysqlRequestHandler()
        self.dbcreator = DBCreator(self.dir, self.connection, self.req_handler, self.logger)

    def tearDown(self):
        self.connection.reinit()
        self.dbcreator = None

    def test__createDbAlreadyExists(self):
        checker = DBChecker(exists=True)

        self.connection.set_result_list([])
        with self.assertRaises(XalanihException) as cm:
            self.dbcreator.create_database(checker)
        self.assertEqual(XalanihException.TABLE_EXISTS,
                         cm.exception.get_error_code(),
                         "Wrong error code.")

    def test_createDbNoScript(self):
        checker = DBChecker(exists=False)

        self.connection.set_result_list([()])
        with self.assertRaises(XalanihException) as cm:
            self.dbcreator.create_database(checker)
        self.assertEqual(XalanihException.NO_CREATION_SCRIPT,
                         cm.exception.get_error_code(),
                         "Wrong error code.")

    def test_createDbSuccess(self):
        checker = DBChecker(exists=False)

        self.connection.set_result_list([()])
        self.dir = self.dir + "/creation_test/"
        self.dbcreator = DBCreator(self.dir, self.connection, self.req_handler, self.logger)
        self.dbcreator.create_database(checker)

        queries = self.connection.get_queries()
        self.assertEqual(7, len(queries), "Wrong number of queries.")

        inc_files = open(self.dir + "creation/included_updates")
        lines = inc_files.readlines()
        inc_files.close()
        for line in lines:
            if line != "":
                self.assertTrue(self.isUpdateIncluded(line.strip()),
                                "Script {0} not included."
                                .format(line.strip()))

        self.assertTrue(self.isXalanihTableRequested(), 
                        "Creation of Xalanih table not requested.")

    def isUpdateIncluded(self, update):
        for q in self.connection.get_queries():
            if q.find(update) != -1:
                return True
        return False

    def isXalanihTableRequested(self):
        for q in self.connection.get_queries():
            if q == self.req_handler.request_xalanih_table_creation():
                return True
        return False
