import unittest
import os
from core.dbcreator import DBCreator
from core.constants import Constants
from core.xalanihexception import XalanihException
from core.mysql.mysqlrequesthandler import MysqlRequestHandler
from test.mocks.connection import Connection
from test.mocks.logger import Logger

class TestDBCreatorMySQL(unittest.TestCase):

    def setUp(self):
        self.connection = Connection()
        self.logger = Logger()
        self.dir = os.path.dirname(__file__) + "/data/"
        self.req_handler = MysqlRequestHandler()
        self.dbcreator = DBCreator(self.dir, self.connection, self.req_handler,
                                    self.logger)

    def tearDown(self):
        self.connection.reinit()
        self.dbcreator = None

    def test__createTableAlreadyExists(self):
        self.connection.setResultList([((Constants.XALANIH_TABLE,),)])
        with self.assertRaises(XalanihException) as cm:
            self.dbcreator.createDatabase()
        self.assertEqual(cm.exception.getErrorCode(),
                            XalanihException.TABLE_EXISTS,
                            "Wrong error code.")

    def test_getConnectionNoScript(self):
        self.connection.setResultList([()])
        with self.assertRaises(XalanihException) as cm:
            self.dbcreator.createDatabase()
        self.assertEqual(cm.exception.getErrorCode(),
                            XalanihException.NO_CREATION_SCRIPT,
                            "Wrong error code.")

    def test_getConnectionSuccess(self):
        self.connection.setResultList([()])
        self.dir = self.dir + "/creation_test/"
        self.dbcreator = DBCreator(self.dir, self.connection, self.req_handler,
                                    self.logger)
        self.dbcreator.createDatabase()

        queries = self.connection.getQueries()
        self.assertEqual(len(queries), 7, "Wrong number of queries.")

        incFile = open(self.dir + "creation/included_updates")
        lines = incFile.readlines()
        incFile.close()
        for line in lines:
            if line != "":
                self.assertTrue(self.isUpdateIncluded(line.strip()),
                                    "Script {0} not included."
                                        .format(line.strip()))

        self.assertTrue(self.isXalanihTableRequested(), 
                            "Creation of Xalanih table not requested.")

    def isUpdateIncluded(self, update):
        for q in self.connection.getQueries():
            if q.find(update) != -1:
                return True
        return False

    def isXalanihTableRequested(self):
        for q in self.connection.getQueries():
            if q == self.req_handler.requestXalanihTable():
                return True
        return False
