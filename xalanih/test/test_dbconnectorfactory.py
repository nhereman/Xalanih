import unittest
import sys
sys.modules['xalanih.core.mysql.mysqlconnector'] = __import__('xalanih.test.mocks.mysqlconnector', fromlist="MysqlConnector")
from xalanih.core.dbconnectorfactory import DBConnectorFactory
from xalanih.core.xalanihexception import XalanihException
from xalanih.test.mocks.parameters import Parameters
from xalanih.test.mocks.logger import Logger


class TestDBConnectorFactory(unittest.TestCase):

    def setUp(self):
        self.params = Parameters()
        self.logger = Logger()

    def tearDown(self):
        self.params = None
        self.logger = None
    
    def test_get_connectionNonSupported(self):
        self.params.setTypeOfDatabase("INVALID")
        with self.assertRaises(XalanihException) as cm:
            DBConnectorFactory.get_connection(self.params, self.logger)
        self.assertEqual(cm.exception.getErrorCode(), 
                            XalanihException.DB_TYPE_NOT_SUPPORTED,
                            "Wrong error code.")

    def test_get_connection_mysql(self):
        self.params.setTypeOfDatabase("mysql")
        connection = DBConnectorFactory.get_connection(self.params, self.logger)
        self.assertEquals(connection, "connect")
