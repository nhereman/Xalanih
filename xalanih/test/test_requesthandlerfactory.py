import unittest
from core.requesthandlerfactory import RequestHandlerFactory
from core.xalanihexception import XalanihException
from core.mysql.mysqlrequesthandler import MysqlRequestHandler
from test.mocks.parameters import Parameters
from test.mocks.logger import Logger

class TestRequestHandlerFactory(unittest.TestCase):

    def setUp(self):
        self.params = Parameters()
    
    def tearDown(self):
        self.params = None

    def test_getRequestHandlerWrongDbType(self):
        self.params.setTypeOfDatabase("NON_SUPPORTED")
        with self.assertRaises(XalanihException) as cm:
            RequestHandlerFactory.getRequestHandler(self.params)
        self.assertEqual(cm.exception.getErrorCode(),
                            XalanihException.DB_TYPE_NOT_SUPPORTED,
                            "Wrong error code.")

    def test_getRequestHandlerMysql(self):
        self.params.setTypeOfDatabase("mysql")
        request_handler = RequestHandlerFactory.getRequestHandler(self.params)
        self.assertIsInstance(request_handler,MysqlRequestHandler)