import unittest
from xalanih.core.requesthandlerfactory import RequestHandlerFactory
from xalanih.core.xalanihexception import XalanihException
from xalanih.core.mysql.mysqlrequesthandler import MysqlRequestHandler
from xalanih.test.mocks.parameters import Parameters


class TestRequestHandlerFactory(unittest.TestCase):

    def setUp(self):
        self.params = Parameters()
    
    def tearDown(self):
        self.params = None

    def test_get_request_handlerWrongDbType(self):
        self.params.set_type_of_database("NON_SUPPORTED")
        with self.assertRaises(XalanihException) as cm:
            RequestHandlerFactory.get_request_handler(self.params)
        self.assertEqual(XalanihException.DB_TYPE_NOT_SUPPORTED,
                         cm.exception.get_error_code(),
                         "Wrong error code.")

    def test_get_request_handlerMysql(self):
        self.params.set_type_of_database("mysql")
        request_handler = RequestHandlerFactory.get_request_handler(self.params)
        self.assertIsInstance(request_handler, MysqlRequestHandler)
