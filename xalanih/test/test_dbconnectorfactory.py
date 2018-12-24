import unittest
import sys
sys.modules['xalanih.core.mysql.mysqlconnector'] = \
    __import__('xalanih.test.mocks.mysqlconnector', fromlist=["MysqlConnector"])
sys.modules['xalanih.core.postgresql.postgresqlconnector'] = \
    __import__('xalanih.test.mocks.postgresqlconnector', fromlist=["PostgreSQLConnector"])
# noinspection PyPep8
from xalanih.core.dbconnectorfactory import DBConnectorFactory
# noinspection PyPep8
from xalanih.core.xalanihexception import XalanihException
# noinspection PyPep8
from xalanih.test.mocks.parameters import Parameters
# noinspection PyPep8
from xalanih.test.mocks.logger import Logger


class TestDBConnectorFactory(unittest.TestCase):

    def setUp(self):
        self.params = Parameters()
        self.logger = Logger()

    def tearDown(self):
        self.params = None
        self.logger = None
    
    def test_get_connectionNonSupported(self):
        self.params.set_type_of_database("INVALID")
        with self.assertRaises(XalanihException) as cm:
            DBConnectorFactory.get_connection(self.params, self.logger)
        self.assertEqual(XalanihException.DB_TYPE_NOT_SUPPORTED,
                         cm.exception.get_error_code(),
                         "Wrong error code.")

    def test_get_connection_mysql(self):
        self.params.set_type_of_database("mysql")
        connection = DBConnectorFactory.get_connection(self.params, self.logger)
        self.assertEquals("connect", connection)

    def test_get_connection_postgresql(self):
        self.params.set_type_of_database("postgresql")
        connection = DBConnectorFactory.get_connection(self.params, self.logger)
        self.assertEquals("connect_post", connection)
